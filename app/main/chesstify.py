import os

from app.main import config
from app.main import create_app

config = config.ProdConfig if "prod" == os.getenv("FLASK_ENV") else config.DevConfig

app = create_app(config)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
