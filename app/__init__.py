from flask import Flask
app = Flask(__name__, instance_relative_config = True)
app.config.from_envvar('APP_CONFIG_FILE')

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_mail import Mail
mail = Mail(app)

from flask.ext.bootstrap import Bootstrap
Bootstrap(app)

from app.views import moss_page
app.register_blueprint(moss_page)

