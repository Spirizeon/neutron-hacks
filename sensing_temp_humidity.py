import Adafruit_DHT

# Sensor type and GPIO pin configuration
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Replace with the GPIO pin number you're using

def read_temperature_and_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print(f"Temperature: {temperature:.1f}°C")
        print(f"Humidity: {humidity:.1f}%")
    else:
        print("Failed to retrieve data from the sensor")

if __name__ == "__main__":
    read_temperature_and_humidity()

