from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config = True)
app.config.from_envvar('APP_CONFIG_FILE')

db = SQLALchemy(app)

mail = Mail(app)
