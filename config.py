"""
中医舌诊系统 - 配置管理
"""
import os


class Config:
    """基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'tongue-diagnosis-secret-key-change-in-production')

    # 数据库
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
    DATABASE_PATH = os.environ.get('DATABASE_PATH', os.path.join(INSTANCE_DIR, 'tongue.db'))

    # 上传
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
    THUMBNAIL_FOLDER = os.environ.get('THUMBNAIL_FOLDER', os.path.join(BASE_DIR, 'uploads', 'thumbnails'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp'}

    # 微信小程序
    WECHAT_APPID = os.environ.get('WECHAT_APPID', 'wxb02cb659c85517d4')
    WECHAT_SECRET = os.environ.get('WECHAT_SECRET', '')

    # Token
    TOKEN_EXPIRE_HOURS = 72

    # AI 引擎
    AI_CONFIDENCE_THRESHOLD = 0.3  # 证型置信度最低阈值
    AI_MAX_SYNDROMES = 5           # 最多返回几个证型

    # CV 引擎
    CV_TONGUE_AREA_MIN_RATIO = 0.05  # 舌体最小面积比例
    CV_IMAGE_MAX_WIDTH = 800
    CV_IMAGE_MAX_HEIGHT = 600


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
