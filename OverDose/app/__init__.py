from flask import Flask
from app.models import db
from app.routes.users import users_bp
from app.routes.stations import stations_bp
from app.routes.deployments import deployments_bp
from app.routes.events import events_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backend.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    # Automatically create database tables
    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(stations_bp, url_prefix='/stations')
    app.register_blueprint(deployments_bp, url_prefix='/deployments')
    app.register_blueprint(events_bp, url_prefix='/events')

    return app
