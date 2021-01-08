from flask import Flask


def create_app(config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config)

    with app.app_context():
        from .routes import hello, games, errors

        app.register_blueprint(hello.hello)
        app.register_blueprint(games.games_blueprint)
        app.register_blueprint(errors.error_blueprint)
        return app
