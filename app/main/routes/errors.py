import logging

from flask import Blueprint, jsonify

error_blueprint = Blueprint("errors", __name__)


@error_blueprint.app_errorhandler(400)
def bad_request(e):
    logging.error(e)
    return make_error(400, "The request you are sending is invalid")


@error_blueprint.app_errorhandler(404)
def not_found(e):
    logging.error(e)
    return make_error(404, "No data found for what you are looking for")


@error_blueprint.app_errorhandler(500)
def server_error(e):
    logging.error(e)
    return make_error(500, "Sorry, something went wrong :(")


@error_blueprint.app_errorhandler(Exception)
def server_error(e):
    logging.error(e)
    return make_error(500, "Sorry, something went wrong :(")


def make_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'message': message,
    })
    response.status_code = status_code
    return response
