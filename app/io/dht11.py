import serial
import sys

g_port = '/dev/cu.usbserial-AH01A8MP'
g_baundrate = 9600

class DHT11(object):
    def __init__(self):
        global g_port, g_baundrate
        self.port = g_port
        self.baundrate = g_baundrate
        self.ser = serial.Serial(self.port, self.baundrate)

    def read(self):
        return float(self.ser.readline().strip())
