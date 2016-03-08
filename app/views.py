from flask import Blueprint, render_template, jsonify, request
from datetime import datetime
import time
import random
from app.models import Moss, Notification

moss_page = Blueprint('moss_page', __name__,
        template_folder='app/templates')

@moss_page.route('/')
@moss_page.route('/index')
@moss_page.route('/monitor')
def index():
	return render_template('monitor.html')

@moss_page.route('/settings')
def settings():
    users = Notification.get_all_recievers()
    return render_template('settings.html', users=users)

@moss_page.route('/data')
def fetch_data():
    cur_temp = Moss.get_newest_record()
    data = {#'point': [time.time() * 1000, random.randint(20, 30),],
            'point': cur_temp,
            'fire_value': 35,
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

@moss_page.route('/history-data')
def fetch_history_data():
    points = Moss.get_recent_records()
    data = {
            #'points': [[time.time() * 1000, 36],],
            'points': points,
            'fire_value': 35,
            }
    return jsonify(data)
