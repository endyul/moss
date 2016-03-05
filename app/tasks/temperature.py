from app.models import Moss, Notification
from app import app
import time
import threading

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Temperature(threading.Thread):
    __metaclass__ = Singleton

    def __init__(self):
        super(Temperature, self).__init__()
        self.fire_value = None
        self.firing = False
        self.should_alarm = False

        self.current_value = 0

        #self.read_value()

    def get_temp(self):
        import random
        random_value = random.random() * 10 + 20
        return random_value

    def read_value(self):
        val = self.get_temp()
        if val:
            self.current_value = val
            ts = time.time()
            self.add_history(ts, self.current_value)
            app.logger.info('%s: %s C' % (str(ts),str(val)))
            self.check_fire()

    def add_history(self, timestamp, value):
        Moss.add_record(timestamp, value)

    def set_target(self, target_temp):
        app.logger.info('setting target to ' + str(target_temp))
        self.fire_value = target_temp
        self.firing = False

    def clear_target(self):
        self.fire_value = None
        self.firing = False

    def fire_reached(self):
        msg = ''
        app.logger.info(msg)
        if self.should_alarm and not self.firing:
            Notification.send_notification(msg)
        self.firing = True

    def fire_gone(self):
        msg = ''
        app.logger.info(msg)
        if self.should_alarm and self.firing:
            self.firing = False

    def check_fire(self):
        if self.fire_value and not self.firing:
            if self.current_value >= self.fire_value:
                self.fire_reached()
        elif self.fire_value and self.firing:
            if self.current_value <= self.fire_value:
                self.fire_gone()

    def run(self):
        app.logger.info('thread starting')
        while True:
            self.read_value()
            time.sleep(1)
