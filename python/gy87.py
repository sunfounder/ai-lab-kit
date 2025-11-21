#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from smbus2 import SMBus
import time
import math

I2C_BUS = 1

def scan_i2c(bus_id=I2C_BUS):
    found = []
    with SMBus(bus_id) as b:
        for addr in range(0x03, 0x78):
            try:
                b.read_byte(addr)
                found.append(addr)
            except Exception:
                pass
    return found

# ------------------------ Tool Function ------------------------
def tilt_comp_heading(mx, my, mz, ax, ay, az, decl_deg=0.0):
    """
    Tilt-compensated heading angle: Roll/pitch is increased using acceleration, then the magnetometer is compensated.

    Return value: 0..360 degrees (magnetic north to true north can be corrected using decl_deg)
    """
    roll  = math.atan2(ay, az)
    pitch = math.atan2(-ax, max(1e-6, math.sqrt(ay*ay + az*az)))
    mx2 = mx * math.cos(pitch) + mz * math.sin(pitch)
    my2 = mx * math.sin(roll) * math.sin(pitch) + my * math.cos(roll) - mz * math.sin(roll) * math.cos(pitch)
    hdg = math.degrees(math.atan2(my2, mx2)) + decl_deg
    if hdg < 0: hdg += 360.0
    if hdg >= 360.0: hdg -= 360.0
    return hdg

# ------------------------ MPU6050 ------------------------
class MPU6050:
    REG_WHO_AM_I     = 0x75
    REG_PWR_MGMT_1   = 0x6B
    REG_PWR_MGMT_2   = 0x6C
    REG_SMPLRT_DIV   = 0x19
    REG_CONFIG       = 0x1A
    REG_GYRO_CONFIG  = 0x1B
    REG_ACCEL_CONFIG = 0x1C
    REG_ACCEL_XOUT_H = 0x3B
    REG_TEMP_OUT_H   = 0x41
    REG_GYRO_XOUT_H  = 0x43
    REG_INT_PIN_CFG  = 0x37
    REG_USER_CTRL    = 0x6A

    def __init__(self, bus: SMBus, addr=None):
        self.bus = bus
        cand = [0x68, 0x69] if addr is None else [addr]
        detected = None
        who_val = None
        for a in cand:
            try:
                who = self.bus.read_byte_data(a, self.REG_WHO_AM_I)
                if who in (0x68, 0x69):
                    detected, who_val = a, who
                    break
            except Exception:
                pass
        if detected is None:
            raise RuntimeError("未检测到 MPU6050（尝试 0x68/0x69 失败）。")

        self.ADDR = detected
        # 复位 → PLL 时钟 → 唤醒
        self.bus.write_byte_data(self.ADDR, self.REG_PWR_MGMT_1, 0x80)
        time.sleep(0.1)
        self.bus.write_byte_data(self.ADDR, self.REG_PWR_MGMT_1, 0x01)  # CLKSEL=1
        self.bus.write_byte_data(self.ADDR, self.REG_PWR_MGMT_2, 0x00)  # 启用各轴
        time.sleep(0.05)
        # 配置
        self.bus.write_byte_data(self.ADDR, self.REG_SMPLRT_DIV,   0x07) # 125Hz
        self.bus.write_byte_data(self.ADDR, self.REG_CONFIG,       0x03) # DLPF=3
        self.bus.write_byte_data(self.ADDR, self.REG_GYRO_CONFIG,  0x00) # ±250dps
        self.bus.write_byte_data(self.ADDR, self.REG_ACCEL_CONFIG, 0x00) # ±2g
        time.sleep(0.02)

        self.accel_sensitivity = 16384.0
        self.gyro_sensitivity  = 131.0

        p1 = self.bus.read_byte_data(self.ADDR, self.REG_PWR_MGMT_1)
        p2 = self.bus.read_byte_data(self.ADDR, self.REG_PWR_MGMT_2)
        print(f"MPU6050 @0x{self.ADDR:02X}: WHO_AM_I=0x{who_val:02X}, "
              f"PWR_MGMT_1=0x{p1:02X}, PWR_MGMT_2=0x{p2:02X}")

    def enable_bypass(self):
        # 关闭 I2C 主控
        self.bus.write_byte_data(self.ADDR, self.REG_USER_CTRL, 0x00)
        time.sleep(0.002)
        # 开旁路
        self.bus.write_byte_data(self.ADDR, self.REG_INT_PIN_CFG, 0x02)
        time.sleep(0.002)
        uc = self.bus.read_byte_data(self.ADDR, self.REG_USER_CTRL)
        ic = self.bus.read_byte_data(self.ADDR, self.REG_INT_PIN_CFG)
        print(f"Bypass enabled: USER_CTRL=0x{uc:02X}, INT_PIN_CFG=0x{ic:02X}")

    def _read_word(self, reg_h):
        high = self.bus.read_byte_data(self.ADDR, reg_h)
        low  = self.bus.read_byte_data(self.ADDR, reg_h + 1)
        val = (high << 8) | low
        if val >= 0x8000:
            val = -((65535 - val) + 1)
        return val

    def read_accel(self):
        ax = self._read_word(self.REG_ACCEL_XOUT_H)       / self.accel_sensitivity
        ay = self._read_word(self.REG_ACCEL_XOUT_H + 2)   / self.accel_sensitivity
        az = self._read_word(self.REG_ACCEL_XOUT_H + 4)   / self.accel_sensitivity
        return ax, ay, az

    def read_gyro(self):
        gx = self._read_word(self.REG_GYRO_XOUT_H)        / self.gyro_sensitivity
        gy = self._read_word(self.REG_GYRO_XOUT_H + 2)    / self.gyro_sensitivity
        gz = self._read_word(self.REG_GYRO_XOUT_H + 4)    / self.gyro_sensitivity
        return gx, gy, gz

    def read_temp_c(self):
        raw = self._read_word(self.REG_TEMP_OUT_H)
        return (raw / 340.0) + 36.53

# ------------------------ HMC5883L ------------------------
class HMC5883L:
    DEF_ADDR = 0x1E
    REG_CONFIG_A = 0x00
    REG_CONFIG_B = 0x01
    REG_MODE     = 0x02
    REG_OUT_X_H  = 0x03

    def __init__(self, bus: SMBus, addr: int = DEF_ADDR):
        self.bus = bus
        self.ADDR = addr
        self.bus.write_byte_data(self.ADDR, self.REG_CONFIG_A, 0b01110000) # 8样本,15Hz
        self.bus.write_byte_data(self.ADDR, self.REG_CONFIG_B, 0x20)       # ±1.3G
        self.bus.write_byte_data(self.ADDR, self.REG_MODE, 0x00)           # 连续
        time.sleep(0.006)
        self.scale = 1090.0

    def _read_word(self, reg_h):
        high = self.bus.read_byte_data(self.ADDR, reg_h)
        low  = self.bus.read_byte_data(self.ADDR, reg_h + 1)
        val = (high << 8) | low
        if val >= 0x8000:
            val = -((65535 - val) + 1)
        return val

    def read_magnet(self):
        x = self._read_word(self.REG_OUT_X_H)
        z = self._read_word(self.REG_OUT_X_H + 4)  # X Z Y
        y = self._read_word(self.REG_OUT_X_H + 2)
        return (x / self.scale, y / self.scale, z / self.scale)

# ------------------------ QMC5883L ------------------------
class QMC5883L:
    DEF_ADDR = 0x0D
    REG_CONTROL   = 0x09
    REG_SET_RESET = 0x0B
    REG_OUT_X_L   = 0x00

    def __init__(self, bus: SMBus, addr: int = DEF_ADDR):
        self.bus = bus
        self.ADDR = addr
        try:
            self.bus.write_byte_data(self.ADDR, self.REG_SET_RESET, 0x01)
        except OSError:
            pass
        # OSR=512, RNG=8G, ODR=50Hz, CONT
        self.bus.write_byte_data(self.ADDR, self.REG_CONTROL, 0b11110101)
        time.sleep(0.01)
        self.scale = 12000.0  # 近似值

    def _read_word_le(self, reg_l):
        low  = self.bus.read_byte_data(self.ADDR, reg_l)
        high = self.bus.read_byte_data(self.ADDR, reg_l + 1)
        val = (high << 8) | low
        if val >= 0x8000:
            val = -((65535 - val) + 1)
        return val

    def read_magnet(self):
        x = self._read_word_le(self.REG_OUT_X_L + 0)
        y = self._read_word_le(self.REG_OUT_X_L + 2)
        z = self._read_word_le(self.REG_OUT_X_L + 4)
        return (x / self.scale, y / self.scale, z / self.scale)

# ------------------------ QMC5883P ------------------------
class QMC5883P:
    DEF_ADDR = 0x2C
    # 寄存器（按你 Arduino 代码）
    REG_X_LSB   = 0x01  # X_L, X_H, Y_L, Y_H, Z_L, Z_H
    REG_STATUS  = 0x09
    REG_MODE    = 0x0A  # 模式/ODR 在这
    REG_CONFIG  = 0x0B  # Set/Reset & 量程

    def __init__(self, bus: SMBus, addr: int = DEF_ADDR):
        self.bus = bus
        self.ADDR = addr
        # 与 Arduino 一致的初始化：MODE=0xCF，CONFIG=0x08
        # 说明：0xCF = 连续模式 + ODR=200Hz（厂商文档/克隆批次常用），0x08 = 开启 set/reset，±8G
        try:
            self.bus.write_byte_data(self.ADDR, self.REG_MODE,   0xCF)
            time.sleep(0.003)
            self.bus.write_byte_data(self.ADDR, self.REG_CONFIG, 0x08)
            time.sleep(0.003)
        except Exception:
            # 不抛异常，允许上层继续尝试读取
            pass
        # 经验尺度，后续可做 min/max 校准微调
        self.scale = 12000.0

    @staticmethod
    def _to_i16(lsb, msb):
        v = (msb << 8) | lsb
        if v >= 0x8000:
            v -= 0x10000
        return v

    def read_magnet(self):
        """
        从 0x01 连续读 6 字节，小端有符号。
        出错时返回 0，不让主循环中断。
        """
        try:
            raw = self.bus.read_i2c_block_data(self.ADDR, self.REG_X_LSB, 6)
            # X_LSB,X_MSB,Y_LSB,Y_MSB,Z_LSB,Z_MSB
            x = self._to_i16(raw[0], raw[1])
            y = self._to_i16(raw[2], raw[3])
            z = self._to_i16(raw[4], raw[5])
            return (x / self.scale, y / self.scale, z / self.scale)
        except Exception:
            return (0.0, 0.0, 0.0)

# ------------------------ BMP180 ------------------------
class BMP180:
    ADDR = 0x77
    REG_CAL  = 0xAA
    REG_CTRL = 0xF4
    REG_DATA = 0xF6
    CMD_TEMP = 0x2E
    CMD_PRES_BASE = 0x34

    def __init__(self, bus: SMBus, oversampling=3):
        self.bus = bus
        self.oss = max(0, min(3, oversampling))
        self._read_calibration()

    def _readS16(self, reg):
        high = self.bus.read_byte_data(self.ADDR, reg)
        low  = self.bus.read_byte_data(self.ADDR, reg+1)
        val = (high << 8) | low
        if val & 0x8000:
            val = -((~val & 0xFFFF) + 1)
        return val

    def _readU16(self, reg):
        high = self.bus.read_byte_data(self.ADDR, reg)
        low  = self.bus.read_byte_data(self.ADDR, reg+1)
        return (high << 8) | low

    def _read_calibration(self):
        self.AC1 = self._readS16(self.REG_CAL + 0)
        self.AC2 = self._readS16(self.REG_CAL + 2)
        self.AC3 = self._readS16(self.REG_CAL + 4)
        self.AC4 = self._readU16(self.REG_CAL + 6)
        self.AC5 = self._readU16(self.REG_CAL + 8)
        self.AC6 = self._readU16(self.REG_CAL +10)
        self.B1  = self._readS16(self.REG_CAL +12)
        self.B2  = self._readS16(self.REG_CAL +14)
        self.MB  = self._readS16(self.REG_CAL +16)
        self.MC  = self._readS16(self.REG_CAL +18)
        self.MD  = self._readS16(self.REG_CAL +20)

    def _read_raw_temp(self):
        self.bus.write_byte_data(self.ADDR, self.REG_CTRL, self.CMD_TEMP)
        time.sleep(0.005)
        msb = self.bus.read_byte_data(self.ADDR, self.REG_DATA)
        lsb = self.bus.read_byte_data(self.ADDR, self.REG_DATA+1)
        return (msb << 8) | lsb

    def _read_raw_pressure(self):
        self.bus.write_byte_data(self.ADDR, self.REG_CTRL, self.CMD_PRES_BASE + (self.oss << 6))
        time.sleep({0:0.005, 1:0.008, 2:0.014, 3:0.026}[self.oss])
        msb = self.bus.read_byte_data(self.ADDR, self.REG_DATA)
        lsb = self.bus.read_byte_data(self.ADDR, self.REG_DATA+1)
        xlsb= self.bus.read_byte_data(self.ADDR, self.REG_DATA+2)
        raw = ((msb << 16) + (lsb << 8) + xlsb) >> (8 - self.oss)
        return raw

    def read(self):
        UT = self._read_raw_temp()
        UP = self._read_raw_pressure()

        X1 = (UT - self.AC6) * self.AC5 / 32768.0
        X2 = (self.MC * 2048.0) / (X1 + self.MD)
        B5 = X1 + X2
        temp = (B5 + 8.0) / 16.0 / 10.0

        B6 = B5 - 4000.0
        X1 = (self.B2 * (B6 * B6 / 4096.0)) / 2048.0
        X2 = (self.AC2 * B6) / 2048.0
        X3 = X1 + X2
        B3 = (((self.AC1*4.0 + X3) * (1<<self.oss)) + 2.0) / 4.0
        X1 = (self.AC3 * B6) / 8192.0
        X2 = (self.B1 * (B6 * B6 / 4096.0)) / 65536.0
        X3 = ((X1 + X2) + 2.0) / 4.0
        B4 = self.AC4 * (X3 + 32768.0) / 32768.0

        # 避免对浮点做位移
        B7 = (UP - B3) * (50000.0 / (2 ** self.oss))

        if B7 < 0x80000000:
            p = (B7 * 2.0) / B4
        else:
            p = (B7 / B4) * 2.0

        X1 = (p / 256.0) ** 2
        X1 = (X1 * 3038.0) / 65536.0
        X2 = (-7357.0 * p) / 65536.0
        p = p + (X1 + X2 + 3791.0) / 16.0

        altitude = 44330.0 * (1.0 - (p / 101325.0) ** (1/5.255))
        return float(temp), float(p), float(altitude)

# ------------------------ GY-87  ------------------------
class GY87:
    def __init__(self, bus_id=I2C_BUS, decl_deg=0.0):
        self.bus = SMBus(bus_id)
        self.mpu = MPU6050(self.bus)
        self.bmp = BMP180(self.bus)
        self.decl_deg = float(decl_deg)

        # 开旁路
        self.mpu.enable_bypass()

        # ---- 磁力计探测：先 QMC-P@0x2C → 再 QMC@0x0D → 最后 HMC@0x1E ----
        self.mag = None
        # 先粗测总线是否能ACK 0x2C
        def i2c_ack(addr):
            try:
                self.bus.read_byte(addr); return True
            except Exception:
                return False

        if i2c_ack(0x2C):
            self.mag = QMC5883P(self.bus, addr=0x2C)
            print("Magnetometer: QMC5883P @0x2C")
        elif i2c_ack(0x0D):
            try:
                self.mag = QMC5883L(self.bus, addr=0x0D)
                print("Magnetometer: QMC5883L @0x0D")
            except Exception:
                pass
        elif i2c_ack(0x1E):
            try:
                self.mag = HMC5883L(self.bus, addr=0x1E)
                print("Magnetometer: HMC5883L @0x1E")
            except Exception:
                pass
        else:
            print("No magnetometer found on 0x2C/0x0D/0x1E; running without MAG.")

    def read_all(self):
        # 基础读：出现 I2C 错误时重试一次并自恢复
        def _safe(f, default):
            try:
                return f()
            except Exception:
                # 自修复：重启 MPU 并重新旁路
                try:
                    self.mpu = MPU6050(self.bus)
                    self.mpu.enable_bypass()
                except Exception:
                    pass
                try:
                    return f()
                except Exception:
                    return default

        ax, ay, az = _safe(self.mpu.read_accel, (0.0, 0.0, 0.0))
        gx, gy, gz = _safe(self.mpu.read_gyro,  (0.0, 0.0, 0.0))
        t_mpu      = _safe(self.mpu.read_temp_c, 0.0)
        try:
            t_bmp, p_pa, alt = self.bmp.read()
        except Exception:
            t_bmp, p_pa, alt = (0.0, 0.0, 0.0)

        result = {
            "accel_g": (ax, ay, az),
            "gyro_dps": (gx, gy, gz),
            "temp_mpu_c": t_mpu,
            "temp_bmp_c": t_bmp,
            "pressure_pa": p_pa,
            "altitude_m": alt
        }
        if self.mag is not None:
            try:
                mx, my, mz = self.mag.read_magnet()
            except Exception:
                mx = my = mz = 0.0
            # 倾斜补偿航向角
            heading = tilt_comp_heading(mx, my, mz, ax, ay, az, decl_deg=self.decl_deg if hasattr(self, "decl_deg") else 0.0)
            result.update({"mag_gauss": (mx, my, mz), "heading_deg": heading})
        return result


# ------------------------ Demo  ------------------------
def demo_loop():
    addrs = scan_i2c()
    print("I2C devices found:", ["0x%02X" % a for a in addrs])

    # decl_deg: angle of declination in degree, 0.0 if unknown , see https://www.magnetic-declination.com/
    dev = GY87(decl_deg=0.0)
    print("reading data...(press Ctrl+C to exit)")
    has_mag = dev.mag is not None

    while True:
        d = dev.read_all()
        if has_mag:
            print(
                # "ACC(g): x={:+.3f} y={:+.3f} z={:+.3f} | "
                # "GYR(dps): x={:+.1f} y={:+.1f} z={:+.1f} | "
                "MAG(G): x={:+.3f} y={:+.3f} z={:+.3f} | "
                # "HDG(tilt-comp): {:6.1f}° | "
                # "TMP(°C): MPU={:+.2f} BMP={:+.2f} | "
                # "P(Pa): {:,.0f} | ALT(m): {:+.2f}"
                .format(
                    # *d["accel_g"], *d["gyro_dps"],
                    *d.get("mag_gauss", (0.0,0.0,0.0))
                    #, 
                    #d.get("heading_deg", float("nan")),
                    # d["temp_mpu_c"], d["temp_bmp_c"],
                    # d["pressure_pa"], d["altitude_m"]
                )
            )
        else:
            print(
                "ACC(g): x={:+.3f} y={:+.3f} z={:+.3f} | "
                "GYR(dps): x={:+.1f} y={:+.1f} z={:+.1f} | "
                "TMP(°C): MPU={:+.2f} BMP={:+.2f} | "
                "P(Pa): {:,.0f} | ALT(m): {:+.2f}".format(
                    *d["accel_g"], *d["gyro_dps"],
                    d["temp_mpu_c"], d["temp_bmp_c"],
                    d["pressure_pa"], d["altitude_m"]
                )
            )
        time.sleep(0.2)

if __name__ == "__main__":
    try:
        demo_loop()
    except KeyboardInterrupt:
        print("\n exit。")
