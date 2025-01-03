from flask import Blueprint, jsonify, request # type: ignore
from app.models import db, Event
from app.schemas.event_schemas import EventRequest

events_bp = Blueprint('events', __name__)

@events_bp.route('/', methods=['POST'])
def create_event():
    data = request.json
    event_data = EventRequest(**data)
    event = Event(
        event_id=event_data.event_id,
        title=event_data.title,
        description=event_data.description,
        station_id=event_data.station_id,
        start_time=event_data.start_time,
        duration=event_data.duration,
        public=event_data.public,
        signups_open=event_data.signups_open
    )
    db.session.add(event)
    db.session.commit()
    return jsonify(event.to_dict()), 200

@events_bp.route('/<event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict()), 200

@events_bp.route('/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted"}), 200
