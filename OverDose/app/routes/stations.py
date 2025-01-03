from flask import Blueprint, jsonify, request
from app.models import db, Station, Deployment
from app.schemas.station_schemas import StationRequest, StationResponse

stations_bp = Blueprint('stations', __name__)

# Fetch all stations with deployments
@stations_bp.route('/', methods=['GET'])
def list_stations():
    stations = Station.query.all()
    # Convert stations to the StationResponse schema format
    return jsonify([StationResponse.from_orm(station).dict() for station in stations]), 200


# Create a new station
@stations_bp.route('/', methods=['POST'])
def create_station():
    data = request.json
    station_data = StationRequest(**data)

    # Create a new Station object
    station = Station(
        station_id=station_data.station_id,
        station_name=station_data.station_name,
        created=station_data.created or datetime.utcnow(),  # Set created to current time if not provided
        config=station_data.config
    )

    # Save the station
    db.session.add(station)
    db.session.commit()

    return jsonify(StationResponse.from_orm(station).dict()), 200


# Fetch a specific station
@stations_bp.route('/<station_id>', methods=['GET'])
def get_station(station_id):
    station = Station.query.get(station_id)
    if not station:
        return jsonify({"error": "Station not found"}), 404
    return jsonify(StationResponse.from_orm(station).dict()), 200


# Delete a station
@stations_bp.route('/<station_id>', methods=['DELETE'])
def delete_station(station_id):
    station = Station.query.get(station_id)
    if not station:
        return jsonify({"error": "Station not found"}), 404
    db.session.delete(station)
    db.session.commit()
    return jsonify({"message": "Station deleted"}), 200
