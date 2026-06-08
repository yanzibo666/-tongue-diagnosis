"""
历史记录路由 - 分析记录查询与趋势
"""
import sqlite3
from flask import Blueprint, request, jsonify, g
from config import Config
from services.user_service import verify_token
from models.user import User
from models.analysis import Analysis

history_bp = Blueprint('history', __name__, url_prefix='/api')


def get_db():
    if 'db' not in g:
        import os as _os
        db_path = Config.DATABASE_PATH
        _os.makedirs(_os.path.dirname(db_path), exist_ok=True)
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def require_user():
    """验证并返回user_id，未登录返回None"""
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.replace('Bearer ', '')
    if not token:
        return None

    payload = verify_token(token)
    if not payload:
        return None

    db = get_db()
    user = User.get_by_openid(db, payload.get('openid', ''))
    return user['id'] if user else None


@history_bp.route('/history', methods=['GET'])
def get_history():
    """获取历史分析记录列表"""
    user_id = require_user()
    if not user_id:
        return jsonify({"error": "请先登录"}), 401

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    db = get_db()
    records = Analysis.get_by_user(db, user_id, page=page, per_page=per_page)
    total = Analysis.count_by_user(db, user_id)

    # 简化列表返回（不返回完整diagnosis_json）
    simplified = []
    for r in records:
        diag = r.get('diagnosis_json', {})
        feats = r.get('features_json', {})
        simplified.append({
            "id": r['id'],
            "health_score": r.get('health_score', 0),
            "risk_level": r.get('risk_level', 'low'),
            "headline": diag.get('headline', ''),
            "primary_syndrome": diag.get('syndrome_analysis', [{}])[0].get('tcm_term', '') if diag.get('syndrome_analysis') else '',
            "tongue_color": feats.get('tongue_color', ''),
            "coating_color": feats.get('coating_color', ''),
            "coating_thickness": feats.get('coating_thickness', ''),
            "image_url": r.get('thumbnail_path') or r.get('image_path', ''),
            "created_at": r.get('created_at', ''),
        })

    return jsonify({
        "success": True,
        "records": simplified,
        "total": total,
        "page": page,
        "per_page": per_page,
        "has_more": page * per_page < total,
    })


@history_bp.route('/history/<int:analysis_id>', methods=['GET'])
def get_detail(analysis_id: int):
    """获取单次分析详情"""
    user_id = require_user()
    if not user_id:
        return jsonify({"error": "请先登录"}), 401

    db = get_db()
    record = Analysis.get_by_id(db, analysis_id)

    if not record:
        return jsonify({"error": "记录不存在"}), 404

    if record.get('user_id') != user_id:
        return jsonify({"error": "无权访问此记录"}), 403

    return jsonify({
        "success": True,
        "record": {
            "id": record['id'],
            "features": record.get('features_json', {}),
            "diagnosis": record.get('diagnosis_json', {}),
            "health_score": record.get('health_score', 0),
            "risk_level": record.get('risk_level', 'low'),
            "image_url": f"/uploads/{record['image_path'].split('/')[-1]}" if record.get('image_path') else '',
            "processing_time_ms": record.get('processing_time_ms', 0),
            "created_at": record.get('created_at', ''),
        }
    })


@history_bp.route('/health-trend', methods=['GET'])
def get_health_trend():
    """获取健康趋势数据"""
    user_id = require_user()
    if not user_id:
        return jsonify({"error": "请先登录"}), 401

    days = request.args.get('days', 30, type=int)

    db = get_db()
    trend = Analysis.get_trend(db, user_id, days=days)

    trend_data = []
    for t in trend:
        feats = t.get('features_json', {})
        trend_data.append({
            "date": t.get('created_at', '')[:10],
            "health_score": t.get('health_score', 0),
            "risk_level": t.get('risk_level', 'low'),
            "tongue_color": feats.get('tongue_color', ''),
        })

    return jsonify({
        "success": True,
        "trend": trend_data,
        "days": days,
    })


@history_bp.route('/profile', methods=['GET'])
def get_profile():
    """获取用户概览"""
    user_id = require_user()
    if not user_id:
        return jsonify({"error": "请先登录"}), 401

    db = get_db()
    stats = Analysis.get_user_stats(db, user_id)
    user = User.get_by_id(db, user_id)

    return jsonify({
        "success": True,
        "user": {
            "nickname": user.get('nickname', '舌诊用户') if user else '舌诊用户',
            "avatar_url": user.get('avatar_url', '') if user else '',
            "created_at": user.get('created_at', '') if user else '',
        },
        "stats": {
            "total_analyses": stats.get('total_analyses', 0),
            "avg_health_score": stats.get('avg_health_score', 0),
            "risk_distribution": stats.get('risk_distribution', {}),
        },
    })


@history_bp.teardown_app_request
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
