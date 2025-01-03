from flask import Blueprint, jsonify, request # type: ignore
from app.models import db, Deployment
from app.schemas.deployment_schemas import DeploymentRequest

deployments_bp = Blueprint('deployments', __name__)

@deployments_bp.route('/', methods=['POST'])
def create_deployment():
    data = request.json
    deployment_data = DeploymentRequest(**data)
    deployment = Deployment(
        deployment_id=deployment_data.deployment_id,
        deployment_name=deployment_data.deployment_name,
        station_id=deployment_data.station_id,
        ip=deployment_data.ip,
        version=deployment_data.version
    )
    db.session.add(deployment)
    db.session.commit()
    return jsonify(deployment.to_dict()), 200

@deployments_bp.route('/<deployment_id>', methods=['GET'])
def get_deployment(deployment_id):
    deployment = Deployment.query.get(deployment_id)
    if not deployment:
        return jsonify({"error": "Deployment not found"}), 404
    return jsonify(deployment.to_dict()), 200

@deployments_bp.route('/<deployment_id>', methods=['DELETE'])
def delete_deployment(deployment_id):
    deployment = Deployment.query.get(deployment_id)
    if not deployment:
        return jsonify({"error": "Deployment not found"}), 404
    db.session.delete(deployment)
    db.session.commit()
    return jsonify({"message": "Deployment deleted"}), 200
