from flask import Blueprint

hello = Blueprint("hello", __name__)


@hello.route('/hello')
def get_profile():
    return "Hello World!"
