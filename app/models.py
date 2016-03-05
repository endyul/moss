from app import db, mail
from flask_mail import Message
import datetime

class Moss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
    cache = []

    @classmethod
    def add_record(cls, ts, temp):
        if int(ts) % 60 == 0:
            dt = datetime.datetime.fromtimestamp(ts)
            record = cls(temperature=temp, timestamp=dt)
            db.session.add(record)
            db.session.commit()
        cls.cache.insert(0, [ts, temp])
        if len(cls.cache) > 60:
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


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    @classmethod
    def get_all_recievers(self):
        users = cls.query.all()
        return users

    @classmethod
    def subscribe(cls, user_email):
        user = cls(email=user_email)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def unsubscribe(cls, uid):
        user = cls.query.get(uid)
        if user:
            db.session.delete(user)
            db.session.commit()

    @classmethod
    def send_notification(self, msg):
        users = [user.email for user in cls.query.all()]
        msg = Message(msg,
                recipients=users)
        mail.send(msg)
