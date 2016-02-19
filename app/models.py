from app import db, mail
from flask_mail import Message

class Moss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

    @classmethod
    def add(cls, temp, ts):
        record = cls(temperature=temp, timestamp=ts)
        db.session.add(record)
        db.session.commit()


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
    def unsubscribe(cls, id):
        user = cls.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()

    @classmethod
    def send_notification(self, msg):
        users = [user.email for user in cls.query.all()]
        msg = Message(msg,
                recipients=users)
        mail.send(msg)
