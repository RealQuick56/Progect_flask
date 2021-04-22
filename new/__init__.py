from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES


app = Flask(__name__)
app.secret_key = 'top secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///templates/shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOADED_PHOTOS_DEST'] = 'new/static/img'
db = SQLAlchemy(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

manager = LoginManager(app)

from new import routes, models

db.create_all()