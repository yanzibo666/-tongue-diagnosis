"""
中医舌诊知识库
舌色、苔色、苔质 → 证型映射规则
"""

# ============================================================
# 舌体颜色诊断
# ============================================================
TONGUE_COLOR_DIAGNOSIS = {
    "pale_white": {
        "name": "淡白舌",
        "indication": "气血两虚或阳虚寒证",
        "detail": "舌色淡白少华，主虚证、寒证。多见于贫血、营养不良、慢性消耗性疾病。",
        "advice": [
            "宜补气养血：当归、黄芪、党参、红枣",
            "推荐食疗：红枣桂圆粥、当归生姜羊肉汤",
            "注意保暖，避免过度劳累",
            "建议就诊：中医内科，做血常规检查"
        ]
    },
    "light_red": {
        "name": "淡红舌",
        "indication": "正常舌象或表证初起",
        "detail": "舌色淡红润泽，为正常健康舌色。若伴有其他症状，可能为外感表证初期。",
        "advice": [
            "舌象基本正常，保持良好生活习惯",
            "饮食均衡，适度运动",
            "若伴有不适症状，请结合其他体征综合判断"
        ]
    },
    "red": {
        "name": "红舌",
        "indication": "热证（实热或阴虚内热）",
        "detail": "舌色鲜红，主热证。实热多见舌红苔黄，阴虚多见舌红少苔。",
        "advice": [
            "实热证：宜清热泻火：金银花、菊花、莲子心",
            "阴虚证：宜滋阴降火：麦冬、沙参、石斛、生地",
            "推荐食疗：绿豆汤（实热）、银耳雪梨羹（阴虚）",
            "避免辛辣、油炸、烧烤食物",
            "若持续不退，建议中医科就诊"
        ]
    },
    "deep_red": {
        "name": "绛红舌",
        "indication": "热入营血，阴虚火旺",
        "detail": "舌色深红，为热邪深入营血之征。多见于高热、严重感染、败血症等危重病症。",
        "advice": [
            "此为较重舌象，建议立即就医",
            "宜清热凉血：水牛角、生地、丹皮、赤芍",
            "多饮水，物理降温",
            "建议尽快就诊：急诊科或中医科"
        ]
    },
    "purple": {
        "name": "青紫舌",
        "indication": "血瘀证或寒凝血瘀",
        "detail": "舌色青紫或有瘀斑，主气血运行不畅。多见于心血管疾病、肝病、妇科疾病。",
        "advice": [
            "宜活血化瘀：丹参、川芎、桃仁、红花",
            "推荐食疗：山楂红糖水、三七炖鸡",
            "适当运动促进血液循环",
            "建议就诊：心血管内科或中医科"
        ]
    }
}

# ============================================================
# 舌苔颜色诊断
# ============================================================
COATING_COLOR_DIAGNOSIS = {
    "white": {
        "name": "白苔",
        "indication": "表证、寒证、湿证",
        "detail": "薄白苔为正常苔象；厚白苔主寒湿内停。",
        "advice": [
            "薄白苔属正常，无需处理",
            "厚白苔：宜温中化湿：苍术、厚朴、陈皮",
            "避免生冷食物，注意腹部保暖"
        ]
    },
    "yellow": {
        "name": "黄苔",
        "indication": "热证、里热证",
        "detail": "苔色黄，主热邪。淡黄为热轻，深黄为热重，焦黄为热结。",
        "advice": [
            "宜清热化湿：黄连、黄芩、栀子",
            "推荐食疗：苦瓜、冬瓜、薏米",
            "避免辛辣、油腻食物",
            "多饮水，保持大便通畅"
        ]
    },
    "gray_black": {
        "name": "灰黑苔",
        "indication": "热极或寒极（危重证）",
        "detail": "苔色灰黑，可为热极伤阴或寒极所致。干燥者为热，润滑者为寒。",
        "advice": [
            "灰黑苔多提示病情较重，建议尽快就医",
            "若苔干燥：热极伤阴，急需养阴清热",
            "若苔润滑：寒极，急需温阳救逆",
            "建议立即就诊：中医科或急诊科"
        ]
    }
}

# ============================================================
# 舌苔厚薄诊断
# ============================================================
COATING_THICKNESS_DIAGNOSIS = {
    "thin": {
        "name": "薄苔",
        "indication": "正常或病邪在表",
        "detail": "透过舌苔能隐约看到舌体，为正常或病邪尚浅。",
        "advice": ["苔薄属正常或病轻，保持良好作息"]
    },
    "thick": {
        "name": "厚苔",
        "indication": "病邪入里，或内有积滞",
        "detail": "舌苔厚而不能见底，主里证、痰湿、食积。",
        "advice": [
            "宜消食导滞、化痰祛湿",
            "推荐：山楂、神曲、茯苓、陈皮",
            "饮食清淡，减少油腻摄入",
            "若长期厚苔不化，建议中医调理"
        ]
    },
    "peeled": {
        "name": "剥苔",
        "indication": "胃气阴两伤",
        "detail": "舌苔部分剥落，舌面光滑，主胃阴不足或气阴两虚。",
        "advice": [
            "宜养阴益胃：沙参、麦冬、玉竹、石斛",
            "推荐食疗：山药粥、蜂蜜水",
            "避免辛辣刺激性食物",
            "建议中医科调理脾胃"
        ]
    }
}

# ============================================================
# 齿痕诊断
# ============================================================
TOOTH_MARK_DIAGNOSIS = {
    "none": {
        "name": "无齿痕",
        "indication": "正常",
        "detail": "舌边缘光滑，无牙齿压痕。",
        "advice": ["正常"]
    },
    "mild": {
        "name": "轻度齿痕",
        "indication": "脾气虚",
        "detail": "舌边缘有轻微牙齿压痕，主脾气虚弱。",
        "advice": [
            "宜健脾益气：党参、白术、茯苓、山药",
            "推荐食疗：山药薏米粥、四君子汤",
            "饮食规律，避免暴饮暴食",
            "适度运动，增强体质"
        ]
    },
    "severe": {
        "name": "明显齿痕（胖大舌）",
        "indication": "脾虚湿盛",
        "detail": "舌体胖大，边缘有明显齿痕，主脾虚不能运化水湿。",
        "advice": [
            "宜健脾祛湿：茯苓、薏苡仁、白术、泽泻",
            "推荐食疗：薏米红豆粥、冬瓜汤",
            "减少盐分摄入，避免生冷食物",
            "建议中医科系统调理脾胃"
        ]
    }
}

# ============================================================
# 裂纹诊断
# ============================================================
CRACK_DIAGNOSIS = {
    "none": {
        "name": "无裂纹",
        "indication": "正常",
        "advice": ["正常"]
    },
    "few": {
        "name": "少量裂纹",
        "indication": "阴液不足",
        "detail": "舌面有少量浅裂纹，主阴液亏虚。",
        "advice": [
            "宜滋阴润燥：麦冬、沙参、玉竹、天花粉",
            "推荐食疗：银耳百合羹、梨汁",
            "多饮水，室内保持湿度"
        ]
    },
    "many": {
        "name": "明显裂纹",
        "indication": "热盛伤阴或血虚不润",
        "detail": "舌面有较深、较多裂纹，主热盛伤津或血虚失于濡养。",
        "advice": [
            "宜清热养阴、补血润燥",
            "推荐：当归、生地、麦冬、玄参",
            "注意补充水分和电解质",
            "若伴有发热、消瘦，建议尽早就医"
        ]
    }
}


def get_color_diagnosis(color_type):
    """根据舌色类型返回诊断"""
    return TONGUE_COLOR_DIAGNOSIS.get(color_type)


def get_coating_color_diagnosis(coating_color):
    """根据苔色返回诊断"""
    return COATING_COLOR_DIAGNOSIS.get(coating_color)


def get_coating_thickness_diagnosis(thickness):
    """根据苔厚薄返回诊断"""
    return COATING_THICKNESS_DIAGNOSIS.get(thickness)


def get_tooth_mark_diagnosis(level):
    """根据齿痕程度返回诊断"""
    return TOOTH_MARK_DIAGNOSIS.get(level)


def get_crack_diagnosis(level):
    """根据裂纹程度返回诊断"""
    return CRACK_DIAGNOSIS.get(level)


def comprehensive_diagnosis(tongue_color, coating_color, coating_thickness,
                           tooth_mark_level, crack_level):
    """综合诊断：结合所有舌象特征给出综合判断"""
    results = []

    color_dx = get_color_diagnosis(tongue_color)
    if color_dx:
        results.append({
            "category": "舌色",
            "finding": color_dx["name"],
            "diagnosis": color_dx["indication"],
            "detail": color_dx.get("detail", ""),
            "advice": color_dx.get("advice", [])
        })

    coat_color_dx = get_coating_color_diagnosis(coating_color)
    if coat_color_dx:
        results.append({
            "category": "苔色",
            "finding": coat_color_dx["name"],
            "diagnosis": coat_color_dx["indication"],
            "detail": coat_color_dx.get("detail", ""),
            "advice": coat_color_dx.get("advice", [])
        })

    coat_thick_dx = get_coating_thickness_diagnosis(coating_thickness)
    if coat_thick_dx:
        results.append({
            "category": "苔质",
            "finding": coat_thick_dx["name"],
            "diagnosis": coat_thick_dx["indication"],
            "detail": coat_thick_dx.get("detail", ""),
            "advice": coat_thick_dx.get("advice", [])
        })

    tooth_dx = get_tooth_mark_diagnosis(tooth_mark_level)
    if tooth_dx:
        results.append({
            "category": "齿痕",
            "finding": tooth_dx["name"],
            "diagnosis": tooth_dx["indication"],
            "detail": tooth_dx.get("detail", ""),
            "advice": tooth_dx.get("advice", [])
        })

    crack_dx = get_crack_diagnosis(crack_level)
    if crack_dx:
        results.append({
            "category": "裂纹",
            "finding": crack_dx["name"],
            "diagnosis": crack_dx["indication"],
            "detail": crack_dx.get("detail", ""),
            "advice": crack_dx.get("advice", [])
        })

    # Consolidate all advice
    all_advice = []
    for r in results:
        all_advice.extend(r.get("advice", []))

    # Remove duplicates while preserving order
    seen = set()
    unique_advice = []
    for a in all_advice:
        if a not in seen:
            seen.add(a)
            unique_advice.append(a)

    return {
        "findings": results,
        "summary": generate_summary(results),
        "all_advice": unique_advice
    }


def generate_summary(results):
    """生成综合摘要"""
    if not results:
        return "未能完成分析，请重新拍照。确保光线充足，舌头自然伸出。"

    indications = [r["diagnosis"] for r in results if r["diagnosis"] != "正常" and r["diagnosis"] != "正常舌象或表证初起"]
    normal_count = sum(1 for r in results if r["diagnosis"] in ("正常", "正常舌象或表证初起"))

    if normal_count == len(results):
        return "舌象基本正常，体质平和。继续保持良好的生活习惯！"
    elif len(indications) <= 1:
        return f"舌象提示：{indications[0]}。建议结合其他症状综合判断。"
    else:
        return f"舌象综合分析提示：{'；'.join(indications[:3])}。建议面诊中医师进行全面辨证论治。"
