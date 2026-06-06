"""
舌诊识别 Web 应用
Flask 后端 + 舌象分析引擎
"""
import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from tongue_analyzer import analyze
from tcm_knowledge import comprehensive_diagnosis

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_tongue():
    """上传图片并分析舌象"""
    if 'image' not in request.files:
        return jsonify({"error": "未上传图片"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "未选择文件"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "不支持的图片格式，请使用 JPG/PNG/BMP"}), 400

    # 保存上传的图片
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # 分析舌象
        features = analyze(filepath)

        # 综合诊断
        diagnosis = comprehensive_diagnosis(
            tongue_color=features["tongue_color"],
            coating_color=features["coating_color"],
            coating_thickness=features["coating_thickness"],
            tooth_mark_level=features["tooth_mark_level"],
            crack_level=features["crack_level"]
        )

        return jsonify({
            "success": True,
            "features": features,
            "diagnosis": diagnosis,
            "image_url": f"/uploads/{filename}",
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({"error": f"分析失败: {str(e)}"}), 500


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("=" * 50)
    print("  中医舌诊识别系统")
    print("  Tongue Diagnosis System")
    print("=" * 50)
    print(f"  访问: http://0.0.0.0:{port}")
    app.run(debug=False, host='0.0.0.0', port=port)
