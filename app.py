"""
中医舌诊识别系统 - 应用入口
Flask 工厂模式 + 蓝图注册
"""
import os
from flask import Flask, render_template, send_from_directory, jsonify
from config import config


def create_app(config_name=None):
    """Flask 应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['default']))

    # 确保必要的目录存在
    from config import Config
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.THUMBNAIL_FOLDER, exist_ok=True)
    os.makedirs(Config.INSTANCE_DIR, exist_ok=True)

    # ---- 注册蓝图 ----
    from routes.auth import auth_bp
    from routes.analyze import analyze_bp
    from routes.history import history_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(history_bp)

    # ---- Web 前端路由（保留兼容）----
    @app.route('/')
    def index():
        return render_template('index.html')

    # 向后兼容：/analyze 重定向到 /api/analyze（旧版 Web 前端使用）
    @app.route('/analyze', methods=['POST'])
    def analyze_compat():
        from routes.analyze import analyze_tongue
        return analyze_tongue()

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    @app.route('/uploads/thumbnails/<filename>')
    def uploaded_thumbnail(filename):
        return send_from_directory(Config.THUMBNAIL_FOLDER, filename)

    # ---- 健康检查 ----
    @app.route('/api/health')
    def health_check():
        return {"status": "ok", "service": "tongue-diagnosis-ai"}

    # ---- 全局错误处理：确保所有错误都返回 JSON ----
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({"error": "请求参数错误"}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "接口不存在"}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "请求方法不允许"}), 405

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"error": "上传文件过大"}), 413

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "服务器内部错误，请稍后重试"}), 500

    return app


# ---- 直接运行入口 ----
if __name__ == '__main__':
    application = create_app()
    port = int(os.environ.get('PORT', 5000))
    print("=" * 55)
    print("  TCM Tongue Diagnosis System v2.0")
    print("  AI Engine + CV + NLG")
    print("=" * 55)
    print(f"  URL:  http://0.0.0.0:{port}")
    print(f"  API:  http://0.0.0.0:{port}/api/health")
    print("=" * 55)
    application.run(debug=False, host='0.0.0.0', port=port)
else:
    # WSGI 入口（gunicorn等）
    application = create_app()
