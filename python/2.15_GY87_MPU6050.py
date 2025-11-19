# Import the MPU6050 IMU module (accelerometer + gyroscope + temperature)
from fusion_hat.modules import MPU6050
# Import sleep for timing delays
from time import sleep

# Create an MPU6050 sensor object with default settings
mpu = MPU6050()

# Optional: Set accelerometer and gyroscope range
# mpu.set_accel_range(MPU6050.ACCEL_RANGE_2G)
# mpu.set_gyro_range(MPU6050.GYRO_RANGE_250DEG)

# Loop forever
while True:
    # Read temperature in Celsius
    temp = mpu.get_temp()

    # Read accelerometer data (X, Y, Z axes), in units of g
    acc_x, acc_y, acc_z = mpu.get_accel_data()

    # Read gyroscope data (X, Y, Z axes), in degrees per second
    gyro_x, gyro_y, gyro_z = mpu.get_gyro_data()

    # Print temperature, acceleration, and gyroscope readings
    print(
        f"Temp: {temp:0.2f} 'C",
        f"  |  ACC: {acc_x:8.5f}g {acc_y:8.5f}g {acc_z:8.5f}g",
        f"  |  GYRO: {gyro_x:8.5f}deg/s {gyro_y:8.5f}deg/s {gyro_z:8.5f}deg/s"
    )

    # Wait 0.2 seconds before next read
    sleep(0.2)
