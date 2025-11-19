# Import the DHT11 temperature & humidity sensor module
from fusion_hat.modules import DHT11
# Import sleep function for delays
from time import sleep

# Create a DHT11 sensor object on GPIO pin 17
dht11 = DHT11(pin=17)

# Loop forever
while True:
    # Read data from the DHT11 sensor
    result = dht11.read()

    # If data was successfully read, unpack humidity and temperature
    if result:
        humidity, temperature = result

        # Print the humidity and temperature values
        print("humidity: %s %%,  Temperature: %s C" % (humidity, temperature))
    else:
        # Print timeout message if reading failed
        print("time out")

    # Wait 1 second before the next reading
    sleep(1)
