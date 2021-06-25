import time
import board
import adafruit_adxl34x

i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

while True:
    data = accelerometer.acceleration
    print("X: " + str(data[0]))
    print("Y: " + str(data[1]))
    print("Z: " + str(data[2]))
    time.sleep(5)
    
    