class Config:
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class ProdConfig(Config):
    # Production variables will go here
    pass
