import serial
import sys


class DHT11(object):
    def __init__(self, port='/dev/cu.usbserial-AH01A8MP', baundrate=9600):
        self.port = port
        self.baundrate = baundrate
        self.ser = serial.Serial(self.port, self.baundrate)

    def read(self):
        return float(self.ser.readline().strip())
