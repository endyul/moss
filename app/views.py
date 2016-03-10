from flask import Blueprint, render_template, jsonify, request
from datetime import datetime
import time
import random
from app.models import Moss, Notification, Settings

moss_page = Blueprint('moss_page', __name__,
        template_folder='app/templates')

@moss_page.route('/')
@moss_page.route('/index')
@moss_page.route('/monitor')
def index():
	return render_template('monitor.html')

@moss_page.route('/camera')
def camera():
    return render_template('camera.html')

@moss_page.route('/settings')
def settings():
    users = Notification.get_all_recievers()
    fire_value = Settings.get_fire_value()
    alert = Settings.get_alert_switch_value()
    return render_template('settings.html', users=users, fire_value=fire_value, alert=alert)

@moss_page.route('/settings/fire-value', methods=['GET', 'POST'])
def fire_value():
    if request.method == 'GET':
        fire_value = Settings.get_fire_value()
        return jsonify({'status':'ok', 'fire_value': fire_value})
    elif request.method == 'POST':
        fire_value = request.form.get('fire_value')
        if fire_value:
            fire_value = float(fire_value)
            Settings.set_fire_value(fire_value)
        return jsonify({'status': 'ok', 'fire_value': fire_value})

@moss_page.route('/settings/alert-switch', methods=['GET', 'POST'])
def alert_switch():
    if request.method == 'GET':
        alert_switch_value = Settings.get_alert_switch_value()
        return jsonify({'status':'ok', 'alert_switch_value': alert_switch_value})
    elif request.method == 'POST':
        alert_switch_value = request.form.get('alert_switch_value')
        alert_switch_value = (alert_switch_value == 'true')
        if not (alert_switch_value is None):
            Settings.set_alert_switch_value(alert_switch_value)
        return jsonify({'status': 'ok', 'alert_switch_value': alert_switch_value})



@moss_page.route('/data')
def fetch_data():
    cur_temp = Moss.get_newest_record()
    data = {#'point': [time.time() * 1000, random.randint(20, 30),],
            'point': cur_temp,
            }
    return jsonify(data)

@moss_page.route('/receivers/add', methods=['POST'])
def add_receiver():
    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'invalid email address'})
    try:
        user = Notification.subscribe(email)
        data = {'status':'ok', 'user': {'id': user.id, 'email': user.email}}
    except Exception, e:
        data = {'status': 'error', 'msg': e}
    return jsonify(data)


@moss_page.route('/receivers/delete', methods=['POST'])
def delete_receiver():
    uid = request.form.get('uid')
    if not uid:
        return jsonify({'status': 'error', 'msg': 'invalid email address'})
    try:
        Notification.unsubscribe(uid)
        return jsonify({'status': 'ok'})
    except Exception, e:
        return jsonify({'status': 'error', 'msg': 'server error'})

@moss_page.route('/data/recent')
def fetch_recent_data():
    points = Moss.get_recent_records()
    data = {'points': points}
    return jsonify(data)

@moss_page.route('/data/day')
def get_day_data():
    points = Moss.get_day_data()
    data = {'points': points}
    return jsonify(data)

@moss_page.route('/data/week')
def get_week_data():
    points = Moss.get_week_data()
    data = {'points': points}
    return jsonify(data)

@moss_page.route('/data/month')
def get_month_data():
    points = Moss.get_month_data()
    data = {'points': points}
    return jsonify(data)

@moss_page.route('/data/year')
def get_year_data():
    points = Moss.get_year_data()
    data = {'points': points}
    return jsonify(data)
