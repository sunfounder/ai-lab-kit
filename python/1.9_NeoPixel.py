
import time               # Used for delays
import board              # Provides board-specific pin definitions
import neopixel_spi as neopixel   # NeoPixel SPI driver

# Create an SPI object using the default SPI bus of the board
spi = board.SPI()

LED_COUNT = 12  # Number of LED pixels in the strip
PIXEL_ORDER = neopixel.GRB  # Color order used by the LEDs (Green, Red, Blue)

# Create a NeoPixel strip object over SPI
# auto_write=False means we must call strip.show() to update the LEDs
strip = neopixel.NeoPixel_SPI(spi, LED_COUNT, pixel_order=PIXEL_ORDER, auto_write=False)

time.sleep(0.01)   # Short delay to ensure the strip is ready

strip.fill(0)      # Turn all pixels off (color value 0 = off)
strip.show()       # Send the data to the LED strip

try:
    while True:
        print("RGB test")

        # Display red on all LEDs
        print("Red")
        strip.fill((255, 0, 0))  # Full red, no green, no blue
        strip.show()
        time.sleep(1)

        # Display green on all LEDs
        print("Green")
        strip.fill((0, 255, 0))  # Full green
        strip.show()
        time.sleep(1)

        # Display blue on all LEDs
        print("Blue")
        strip.fill((0, 0, 255))  # Full blue
        strip.show()
        time.sleep(1)
    
        # Turn all LEDs off
        # print("Off for 10 seconds")
        strip.fill((0, 0, 0))    # All channels 0 = off
        strip.show()
        time.sleep(1)

# Gracefully handle script termination (e.g., via KeyboardInterrupt)
except KeyboardInterrupt: 
    pass
