# coding: utf-8
from app import db, mail
from flask_mail import Message
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule
import time


interval = 2

class Moss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
    cache = []

    @classmethod
    def add_record(cls, ts, temp):
        global interval
        if int(ts) % 60 < interval:
            dt = datetime.fromtimestamp(ts)
            record = cls(temperature=temp, timestamp=dt)
            db.session.add(record)
            db.session.commit()
        cls.cache.insert(0, [ts, temp])
        if len(cls.cache) > (60/interval):
            cls.cache.pop()

    @classmethod
    def get_newest_record(cls):
        if len(cls.cache) > 0:
            record = cls.cache[0]
        else:
            record = cls.query.order_by(cls.timestamp).first()
        return record

    @classmethod
    def get_recent_records(cls):
        return cls.cache[::-1]

    @classmethod
    def span_avgtemps(cls, v):
        r = []
        for b, e in zip(v[:-1], v[1:]):
            records = cls.query.filter(cls.timestamp.between(b, e)).all()
            avg = (sum(map(lambda x: x.temperature, records)) / len(records)) if len(records) else 0
            avg = round(avg, 2)
            r.append([time.mktime(b.timetuple()), avg])
        return r


    @classmethod
    def get_day_data(cls):
        now = datetime.now()
        end_time = datetime(now.year, now.month, now.day, now.hour) + relativedelta(hours=1)
        start_time = end_time - relativedelta(hours=24)
        hours = list(rrule.rrule(rrule.HOURLY, dtstart=start_time, until=end_time))
        r = cls.span_avgtemps(hours)
        return r

    @classmethod
    def get_week_data(cls):
        today = date.today()
        end_day = today + relativedelta(days=1)
        start_day = end_day - relativedelta(days=7)
        days = list(rrule.rrule(rrule.DAILY, dtstart=start_day, until=end_day))
        r = cls.span_avgtemps(days)
        return r

    @classmethod
    def get_month_data(cls):
        today = date.today()
        end_day = today + relativedelta(days=1)
        start_day = end_day - relativedelta(months=1)
        days = list(rrule.rrule(rrule.DAILY, dtstart=start_day, until=end_day))
        r = cls.span_avgtemps(days)
        return r

    @classmethod
    def get_year_data(cls):
        today = date.today()
        end_month = date(today.year, today.month, 1) + relativedelta(months=1)
        start_month = end_month - relativedelta(months=12)
        months = list(rrule.rrule(rrule.MONTHLY, dtstart=start_month, until=end_month))
        r = cls.span_avgtemps(months)
        return r


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_type = db.Column(db.Integer, unique=True)
    setting_value = db.Column(db.Float)
    TYPE_FIRE_VALUE = 1
    TYPE_ALERT_SWITCH_VALUE = 2

    EVENT_ON_CHANGE = 1

    listeners = {EVENT_ON_CHANGE: []}

    @classmethod
    def on_change(cls, func):
        cls.listeners[EVENT_ON_CHANGE].append(func)

    @classmethod
    def notify(cls, event):
        for func in cls.listeners[event]:
            func()

    @classmethod
    def get_fire_value(cls):
        v = cls.get_setting_value(cls.TYPE_FIRE_VALUE)
        if v:
            return int(v)
        return None

    @classmethod
    def set_fire_value(cls, v):
        cls.set_setting_value(cls.TYPE_FIRE_VALUE, v)

    @classmethod
    def get_alert_switch_value(cls):
        v = cls.get_setting_value(cls.TYPE_ALERT_SWITCH_VALUE)
        return bool(v)

    @classmethod
    def set_alert_switch_value(cls, v):
        v = float(bool(v))
        cls.set_setting_value(cls.TYPE_ALERT_SWITCH_VALUE, v)

    @classmethod
    def get_setting_value(cls, typeid):
        setting = cls.query.filter_by(setting_type=typeid).first()
        if setting:
            return setting.setting_value
        return None

    @classmethod
    def set_setting_value(cls, typeid, v):
        setting = cls.query.filter_by(setting_type=typeid).first()
        if setting is None:
            setting = cls(setting_type=typeid, setting_value=v)
            db.session.add(setting)
            db.session.commit()
        else:
            setting.setting_value = v
            db.session.commit()
        cls.notify(EVENT_ON_CHANGE)
        return setting


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    @classmethod
    def get_all_recievers(cls):
        users = cls.query.all()
        return users

    @classmethod
    def subscribe(cls, user_email):
        user = cls(email=user_email)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def unsubscribe(cls, uid):
        user = cls.query.get(uid)
        if user:
            db.session.delete(user)
            db.session.commit()

    @classmethod
    def send_async_email(cls, msg):
        from app import app
        with app.app_context():
            app.logger.info('start sending mail...')
            mail.send(msg)
            app.logger.info('finish sending mail')

    @classmethod
    def send_notification(cls, head, body):
        from app import app
        from threading import Thread
        with app.app_context():
            users = [user.email for user in cls.query.all()]
            msg = Message(head,
                    recipients=users)
            msg.body = body
            thread = Thread(target=cls.send_async_email, args=[msg])
            thread.start()

