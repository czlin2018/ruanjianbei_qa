#-*- coding: UTF-8 -*- 
from flask import Flask
from flask_migrate import Migrate
from simpledu.config import configs
from simpledu.models import db, User,Course, QA
from flask_login import LoginManager


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'



def register_blueprints(app):
    from .handlers import front, course, admin
    app.register_blueprint(front)
    app.register_blueprint(course)
    app.register_blueprint(admin)


def create_app(config):
    app = Flask(__name__)
    
    app.config.from_object(configs.get(config))
    
    register_extensions(app) 
    register_blueprints(app)
     
    return app

app = create_app('development')

if __name__=='__main__':
    app.run(host='0.0.0.0', port='80')

