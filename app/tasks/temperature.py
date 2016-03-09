# coding: utf-8
from app.models import Moss, Notification
from app import app
import time
import threading
from app.io import DHT11
from datetime import datetime

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Temperature(threading.Thread):
    __metaclass__ = Singleton

    def __init__(self, dev_port, fire_value = None, should_alarm = False):
        super(Temperature, self).__init__()
        #self.fire_value = Settings.get_fire_value()
        self.fire_value = fire_value
        self.firing = False
        #self.should_alarm = Settings.get_alert_switch_value()
        self.should_alarm = should_alarm
        self.dev_port = dev_port

        self.current_value = 0
        self.device = DHT11(port=self.dev_port)

        #self.read_value()

    def get_temp(self):
        '''
        import random
        random_value = random.random() * 10 + 20
        return random_value
        '''
        return self.device.read()


    def read_value(self):
        val = self.get_temp()
        if val:
            self.current_value = val
            ts = time.time()
            self.add_history(ts, self.current_value)
            app.logger.info('%s: %s °C, settings: [alert switch %s, fire value %s]' %
                    (str(datetime.fromtimestamp(ts)),str(val),self.should_alarm, self.fire_value))
            self.check_fire()

    def add_history(self, timestamp, value):
        Moss.add_record(timestamp, value)

    def set_target(self, target_temp):
        app.logger.info('setting target to ' + str(target_temp))
        self.fire_value = target_temp
        self.firing = False

    def set_alert_switch(self, v):
        app.logger.info('setting alert switch: ' + str(v))
        self.should_alarm = v
        self.firing = False

    def clear_target(self):
        self.fire_value = None
        self.firing = False

    def fire_reached(self):
        msg = '达到预警温度！当前机房温度%d°C\n查看实时温度 %s' % (self.fire_value, 'http://127.0.0.1:5000')
        app.logger.info(msg)
        if self.should_alarm and not self.firing:
            Notification.send_notification('机房温度警报', msg)
        self.firing = True

    def fire_gone(self):
        msg = '温度警报解除，当前机房温度%d°C\n查看实时温度 %s' % (self.fire_value, 'http://127.0.0.1:5000')
        app.logger.info(msg)
        if self.should_alarm and self.firing:
            Notification.send_notification('机房温度警报解除', msg)
        self.firing = False

    def check_fire(self):
        if self.fire_value and not self.firing:
            if self.current_value >= self.fire_value:
                self.fire_reached()
        elif self.fire_value and self.firing:
            if self.current_value < self.fire_value:
                self.fire_gone()

    def run(self):
        app.logger.info('thread starting')
        while True:
            self.read_value()
            time.sleep(2)
