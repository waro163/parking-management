import os
import consts
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', consts.SECRECT_KEY)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', consts.MAIL_SERVER)
    MAIL_PORT = int(os.environ.get('MAIL_PORT', consts.MAIL_PORT))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', consts.MAIL_USE_TLS)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME',consts.MAIL_USERNAME)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD',consts.MAIL_PASSWORD)
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = os.environ.get('MAIL_USERNAME',consts.MAIL_USERNAME)
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN',consts.ADMIN)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    APPID = os.getenv('APPID')
    APPSECRET = os.getenv('APPSECRET')
    TOKEN = os.getenv('TOKEN',consts.WechatToken)
    AES_KEY = os.getenv('AES_KEY',consts.AES_Key)
    EMAIL_PATTERN = os.getenv('EMAIL_PATTERN',consts.EMAIL_PATTERN)
    UPLOAD_ROOT_FOLDER = os.path.join(basedir, os.getenv('UPLOAD_ROOT_FOLDER', consts.UPLOAD_ROOT_FOLDER))
    PHOTO_SUB_FOLDER = os.getenv('PHOTO_SUB_FOLDER',consts.PHOTO_SUB_FOLDER)
    ALLOWED_PHOTO_EXTENSIONS  = os.getenv('ALLOWED_PHOTO_EXTENSIONS',consts.ALLOWED_PHOTO_EXTENSIONS)

    @classmethod
    def check_portrait_folder(cls):
        if not os.path.isdir(cls.PORTRAIT_FOLDER):
            os.mkdir(cls.PORTRAIT_FOLDER)

    @staticmethod
    def init_app(app):
        _photo_folder = os.path.join(Config.UPLOAD_ROOT_FOLDER,Config.PHOTO_SUB_FOLDER)
        if not os.path.isdir(_photo_folder):
            os.mkdir(_photo_folder)
        # pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
