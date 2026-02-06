#!/usr/bin/env python3
from fusion_hat.pin import Pin, Mode
import time

# Initialize Buzzer and LED to GPIO pins
BeepPin = Pin(22, mode=Mode.OUT)
ALedPin = Pin(17, mode=Mode.OUT)

# Morse code representation for characters
MORSECODE = {
    'A': '01', 'B': '1000', 'C': '1010', 'D': '100', 'E': '0', 'F': '0010', 'G': '110',
    'H': '0000', 'I': '00', 'J': '0111', 'K': '101', 'L': '0100', 'M': '11', 'N': '10',
    'O': '111', 'P': '0110', 'Q': '1101', 'R': '010', 'S': '000', 'T': '1',
    'U': '001', 'V': '0001', 'W': '011', 'X': '1001', 'Y': '1011', 'Z': '1100',
    '1': '01111', '2': '00111', '3': '00011', '4': '00001', '5': '00000',
    '6': '10000', '7': '11000', '8': '11100', '9': '11110', '0': '11111',
    '?': '001100', '/': '10010', ',': '110011', '.': '010101', ';': '101010',
    '!': '101011', '@': '011010', ':': '111000',
}

# Timing (seconds)
UNIT = 0.25                 # base unit
DOT = UNIT / 2              # dot length
DASH = UNIT                 # dash length
INTRA_SYMBOL_GAP = UNIT / 2 # gap between dot/dash in one letter
LETTER_GAP = UNIT           # gap between letters
WORD_GAP = UNIT * 2         # gap between words (space)

def on():
    """Turn on the buzzer and LED."""
    BeepPin.on()
    ALedPin.on()

def off():
    """Turn off the buzzer and LED."""
    BeepPin.off()
    ALedPin.off()

def beep(duration):
    """Beep (and flash LED) for 'duration' seconds."""
    on()
    time.sleep(duration)
    off()

def play_symbol(symbol):
    """Play one morse symbol: '0' (dot) or '1' (dash)."""
    if symbol == '0':
        beep(DOT)
    elif symbol == '1':
        beep(DASH)
    time.sleep(INTRA_SYMBOL_GAP)

def morsecode(text):
    """
    Convert text to Morse code and output via buzzer+LED.
    Supports spaces between words and ignores unsupported characters.
    """
    for ch in text:
        if ch == ' ':
            # Space means word gap
            time.sleep(WORD_GAP)
            continue

        # Skip unsupported characters instead of crashing
        if ch not in MORSECODE:
            continue

        pattern = MORSECODE[ch]
        for sym in pattern:
            play_symbol(sym)

        # Pause between letters
        time.sleep(LETTER_GAP)

def destroy():
    """Ensure buzzer and LED are turned off."""
    BeepPin.off()
    ALedPin.off()
    print("")

try:
    while True:
        code = input("Please input the messenger:").upper()
        print(code)
        morsecode(code)
except KeyboardInterrupt:
    destroy()
