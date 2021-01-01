from flask import Flask


def create_app(config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)

    with app.app_context():
        from .routes import hello

        app.register_blueprint(hello.hello)
        return app
