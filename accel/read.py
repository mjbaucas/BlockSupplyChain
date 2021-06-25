import time
import board
import adafruit_adxl34x

i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

while True:
    data = accelerometer.acceleration
    print("X: " + data[0])
    print("Y: " + data[1])
    print("Z: " + data[2])
    time.sleep(5)
    
    