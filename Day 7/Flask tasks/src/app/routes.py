from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from .models import PredictionRequest
from .service import PredictionService

api_bp = Blueprint("api", __name__)

svc = PredictionService()


@api_bp.route("/health", methods=["GET"])
def health():

    return jsonify(
        {"status": "healthy"}
    ), 200


@api_bp.route("/predictions", methods=["POST"])
def create_prediction():

    try:
        payload = PredictionRequest(
            **request.get_json()
        )

    except ValidationError as e:

        return jsonify(
            {"errors": e.errors()}
        ), 422

    result = svc.predict(payload)

    return jsonify(
        result.model_dump()
    ), 201


@api_bp.route(
    "/predictions/<string:pid>",
    methods=["GET"]
)
def get_prediction(pid):

    result = svc.get(pid)

    if not result:

        return jsonify(
            {"error": "Not found"}
        ), 404

    return jsonify(
        result.model_dump()
    ), 200