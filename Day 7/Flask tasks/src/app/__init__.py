from flask import Flask
from flask import g
from flask import request

import time
import uuid

from .routes import api_bp
from .logging_config import logger


def create_app():

    app = Flask(__name__)

    app.register_blueprint(
        api_bp,
        url_prefix="/api/v1"
    )

    @app.before_request
    def before_request():

        g.start_time = time.time()

        g.correlation_id = str(
            uuid.uuid4()
        )

    @app.after_request
    def after_request(response):

        duration = (
            time.time()
            - g.start_time
        ) * 1000

        logger.info(
            "request",
            correlation_id=g.correlation_id,
            method=request.method,
            path=request.path,
            status=response.status_code,
            duration_ms=round(duration, 2)
        )

        return response

    @app.errorhandler(404)
    def not_found(e):

        return {
            "error": "Not found"
        }, 404

    @app.errorhandler(422)
    def validation_error(e):

        return {
            "error": "Validation failed"
        }, 422

    @app.errorhandler(500)
    def internal_error(e):

        return {
            "error": "Internal server error"
        }, 500

    return app