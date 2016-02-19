from app.models import Moss, Notification
from app import app


class Temperature:
    def __init__(self):
        self.counter = 0
        self.should_stop = False

        self.fire_value = None
        self.firing = False
        self.should_alarm = False

        self.current_value = 0

        self.read_value()

    def get_temp(self):
        return 22.1

    def read_value(self):
        val = get_temp()
        if val:
            self.current_value = val
            self.add_history(time.time(), self.current_value)
            self.check_fire()

    def add_history(self, timestamp, value):
        if self.counter  == 60:
            self.counter = 0
            Moss.add(value, timestamp)
        else:
            self.counter += 1

    def set_target(self, target_temp):
        app.logger.warning('setting target to ' + str(target_temp))
        self.fire_value = target_temp
        self.firing = False

    def clear_target(self):
        self.fire_value = None
        self.firing = False

    def fire_reached(self):
        msg = ''
        app.logger.warning(msg)
        #TODO notification
        if self.should_alarm and not self.firing:
            Notification.send_notification(msg)
        self.firing = True

    def fire_gone(self):
        msg = ''
        app.logger.warning(msg)
        if self.should_alarm and self.firing:
            self.firing = False

    def check_fire(self):
        if self.fire_value and not self.firing:
            if self.current_value >= self.fire_value:
                self.fire_reached()
        elif self.fire_value and self.firing:
            if self.current_value <= self.fire_value:
                self.fire_gone()

    def loop(self):
        while self.should_stop is False:
            self.read_value()
            time.sleep(5)
        app.logger.debug('Loop exited')

    def start(self):
        self.should_stop = False
        app.logger.debug('Starting thread')
        t = Thread(target=self.loop)
        t.start()

    def stop(self):
        app.logger.debug('Stopping thread')
        self.should_stop = True
