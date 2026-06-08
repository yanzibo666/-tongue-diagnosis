"""
认证路由 - 微信登录
"""
from flask import Blueprint, request, jsonify
from services.user_service import wechat_login, verify_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """微信小程序登录"""
    data = request.get_json(silent=True) or {}
    code = data.get('code', '')

    if not code:
        return jsonify({"error": "缺少登录code参数"}), 400

    nickname = data.get('nickname')
    avatar_url = data.get('avatar_url')

    try:
        result = wechat_login(code, nickname, avatar_url)
        return jsonify({
            "success": True,
            "token": result["token"],
            "user_id": result["user_id"],
            "nickname": result["nickname"],
            "is_new_user": result["is_new_user"],
        })
    except Exception as e:
        return jsonify({"error": f"登录失败: {str(e)}"}), 500


@auth_bp.route('/verify', methods=['POST'])
def verify():
    """验证Token是否有效"""
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.replace('Bearer ', '')

    if not token:
        return jsonify({"valid": False, "error": "缺少Token"}), 401

    payload = verify_token(token)
    if payload:
        return jsonify({"valid": True, "openid": payload.get("openid")})
    else:
        return jsonify({"valid": False, "error": "Token无效或已过期"}), 401
