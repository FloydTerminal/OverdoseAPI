from flask_sqlalchemy import SQLAlchemy # type: ignore
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String, nullable=False)
    discord_id = db.Column(db.String, nullable=True)
    platform = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "discord_id": self.discord_id,
            "platform": self.platform,
            "created": self.created.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None
        }

class Station(db.Model):
    __tablename__ = 'station'
    
    station_id = db.Column(db.String, primary_key=True)
    station_name = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    config = db.Column(db.JSON, nullable=True)

    # Relationship to deployments (One-to-Many)
    deployments = db.relationship('Deployment', backref='station', lazy=True)

    def to_dict(self):
        return {
            "station_id": self.station_id,
            "station_name": self.station_name,
            "created": self.created.isoformat(),
            "deployments": [deployment.to_dict() for deployment in self.deployments],
            "config": self.config
        }


class Deployment(db.Model):
    __tablename__ = 'deployment'

    deployment_id = db.Column(db.String, primary_key=True)
    station_id = db.Column(db.String, db.ForeignKey('station.station_id'), nullable=False)
    deployment_name = db.Column(db.String, nullable=True)
    region = db.Column(db.String, nullable=True)
    ip = db.Column(db.String, nullable=True)
    version = db.Column(db.String, nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    online = db.Column(db.Boolean, default=False)
    last_event = db.Column(db.DateTime, nullable=True)
    player_count = db.Column(db.Integer, default=0)
    config = db.Column(db.JSON, nullable=True)

    def to_dict(self):
        return {
            "deployment_id": self.deployment_id,
            "station_id": self.station_id,
            "deployment_name": self.deployment_name,
            "region": self.region,
            "ip": self.ip,
            "version": self.version,
            "created": self.created.isoformat(),
            "online": self.online,
            "last_event": self.last_event.isoformat() if self.last_event else None,
            "player_count": self.player_count,
            "config": self.config
        }

class Event(db.Model):
    event_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    station_id = db.Column(db.String, db.ForeignKey('station.station_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    public = db.Column(db.Boolean, default=True)
    signups_open = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "station_id": self.station_id,
            "start_time": self.start_time.isoformat(),
            "duration": self.duration,
            "public": self.public,
            "signups_open": self.signups_open,
        }
