from flask import Blueprint, render_template, jsonify
from datetime import datetime
import time
import random
from app.models import Moss

moss_page = Blueprint('moss_page', __name__,
        template_folder='app/templates')

@moss_page.route('/')
def index():
	return render_template('index.html')

@moss_page.route('/data')
def fetch_data():
    cur_temp = Moss.get_newest_record()
    data = {#'point': [time.time() * 1000, random.randint(20, 30),],
            'point': cur_temp,
            'fire_value': 35,
            }
    return jsonify(data)

@moss_page.route('/history-data')
def fetch_history_data():
    points = Moss.get_recent_records()
    data = {
            #'points': [[time.time() * 1000, 36],],
            'points': points,
            'fire_value': 35,
            }
    return jsonify(data)
