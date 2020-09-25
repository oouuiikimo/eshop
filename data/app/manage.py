from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from application.share.models import db
from application.models.user import User

app = Flask(__name__)
app.config.from_object('config.Config')

#db = SQLAlchemy(app)
db.init_app(app) 
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
"""
if __name__ == '__main__':
    manager.run()