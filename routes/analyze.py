"""
分析路由 - 舌象上传与分析
"""
import os
import uuid
import sqlite3
from flask import Blueprint, request, jsonify, g
from werkzeug.utils import secure_filename
from config import Config
from services.diagnosis_service import analyze_image
from services.user_service import verify_token

analyze_bp = Blueprint('analyze', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db():
    """获取数据库连接（放在请求上下文中）"""
    if 'db' not in g:
        import os as _os
        db_path = Config.DATABASE_PATH
        _os.makedirs(_os.path.dirname(db_path), exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
        # 初始化表
        from models.user import User
        from models.analysis import Analysis
        User.init_table(g.db)
        Analysis.init_table(g.db)
    return g.db


def get_user_id():
    """从请求头获取用户ID"""
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.replace('Bearer ', '')
    if token:
        payload = verify_token(token)
        if payload:
            # 查找用户
            db = get_db()
            from models.user import User
            user = User.get_by_openid(db, payload.get('openid', ''))
            if user:
                return user['id']
    return None


@analyze_bp.route('/analyze', methods=['POST'])
def analyze_tongue():
    """上传图片并分析舌象（支持游客模式）"""
    if 'image' not in request.files:
        return jsonify({"error": "未上传图片"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "不支持的图片格式，请使用 JPG/PNG/BMP"}), 400

    # 保存图片
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = Config.UPLOAD_FOLDER
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    try:
        # 获取用户ID（可选）
        user_id = get_user_id()
        db = get_db() if user_id else None

        # 分析
        result = analyze_image(filepath, user_id=user_id, db_conn=db)

        # 添加用户信息到返回
        if user_id:
            result["user_id"] = user_id

        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"分析失败: {str(e)}"}), 500


@analyze_bp.teardown_app_request
def close_db(exception=None):
    """请求结束时关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()
