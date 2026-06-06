"""
舌象分析引擎
基于 OpenCV 对舌部图像进行分割和特征提取
"""
import cv2
import numpy as np
from collections import Counter


def analyze(image_path):
    """主入口：分析舌象照片，返回所有特征"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")

    img = cv2.resize(img, (600, 800) if img.shape[0] > img.shape[1] else (800, 600))

    # 1. 分割舌体区域
    tongue_mask, tongue_region = extract_tongue_region(img)
    if tongue_region is None:
        return _fallback_analysis(img)

    # 2. 舌色分析
    tongue_color = analyze_tongue_color(tongue_region, tongue_mask)

    # 3. 舌苔分析
    coating_color, coating_thickness = analyze_coating(tongue_region, tongue_mask)

    # 4. 齿痕检测
    tooth_mark_level = detect_tooth_marks(tongue_mask)

    # 5. 裂纹检测
    crack_level = detect_cracks(tongue_region)

    return {
        "tongue_color": tongue_color,
        "coating_color": coating_color,
        "coating_thickness": coating_thickness,
        "tooth_mark_level": tooth_mark_level,
        "crack_level": crack_level,
        "tongue_found": True
    }


def extract_tongue_region(img):
    """
    从图像中分割舌体区域
    使用 HSV 肤色范围 + GrabCut 精修
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blurred = cv2.GaussianBlur(hsv, (5, 5), 0)

    # 舌体/皮肤 HSV 范围（粉色-红色调）
    lower1 = np.array([0, 20, 40])
    upper1 = np.array([25, 255, 255])
    lower2 = np.array([160, 20, 40])
    upper2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(blurred, lower1, upper1)
    mask2 = cv2.inRange(blurred, lower2, upper2)
    mask = cv2.bitwise_or(mask1, mask2)

    # 形态学操作
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)

    # 找最大连通区域
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None

    largest = max(contours, key=cv2.contourArea)

    # 面积太小说明没检测到舌头
    img_area = img.shape[0] * img.shape[1]
    if cv2.contourArea(largest) < img_area * 0.05:
        return None, None

    # 创建精确 mask
    final_mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.drawContours(final_mask, [largest], -1, 255, -1)

    # GrabCut 精修
    try:
        rect = cv2.boundingRect(largest)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        grab_mask = np.zeros(img.shape[:2], np.uint8)
        grab_mask[final_mask == 255] = cv2.GC_PR_FGD
        grab_mask[final_mask == 0] = cv2.GC_PR_BGD
        cv2.grabCut(img, grab_mask, rect, bgd_model, fgd_model, 3,
                     cv2.GC_INIT_WITH_MASK)
        final_mask = np.where((grab_mask == cv2.GC_FGD) |
                              (grab_mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    except Exception:
        pass  # Fallback to basic mask

    tongue_region = cv2.bitwise_and(img, img, mask=final_mask)
    return final_mask, tongue_region


def analyze_tongue_color(region, mask):
    """
    分析舌体颜色
    使用 LAB 色彩空间对舌体像素进行聚类分析
    """
    lab = cv2.cvtColor(region, cv2.COLOR_BGR2LAB)
    pixels = lab[mask == 255]

    if len(pixels) < 100:
        return "light_red"  # default

    # 计算 L (亮度)、A (红-绿轴) 平均值
    L_mean = np.mean(pixels[:, 0])
    A_mean = np.mean(pixels[:, 1])

    # 基于 LAB 值的舌色分类规则
    if A_mean < 125 and L_mean > 160:
        return "pale_white"
    elif A_mean < 130 and L_mean > 100:
        return "light_red"
    elif A_mean < 145:
        return "red"
    elif A_mean < 155:
        return "deep_red"
    else:
        return "purple"


def analyze_coating(region, mask):
    """
    分析舌苔
    返回: (苔色, 苔质)
    """
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)

    pixels_gray = gray[mask == 255]
    pixels_h = hsv[:, :, 0][mask == 255]
    pixels_s = hsv[:, :, 1][mask == 255]

    if len(pixels_gray) < 100:
        return "white", "thin"

    # ---- 苔色分析 ----
    # 明亮像素（苔） vs 暗像素（舌体）
    bright_threshold = np.percentile(pixels_gray, 60)
    coating_pixels = pixels_gray[pixels_gray > bright_threshold]

    if len(coating_pixels) < 50:
        return "white", "thin"

    # 苔色：基于亮像素的 HSV 色调
    bright_mask = gray > bright_threshold
    coating_h = hsv[:, :, 0][mask == 255][gray[mask == 255] > bright_threshold]

    if len(coating_h) == 0:
        return "white", "thin"

    h_mean = np.mean(coating_h)

    if h_mean < 25 or h_mean > 170:
        return "white", _analyze_thickness(coating_pixels, pixels_gray)
    elif h_mean < 40:
        return "yellow", _analyze_thickness(coating_pixels, pixels_gray)
    else:
        return "gray_black", _analyze_thickness(coating_pixels, pixels_gray)


def _analyze_thickness(coating_pixels, all_pixels):
    """分析苔质厚薄"""
    coating_ratio = len(coating_pixels) / max(len(all_pixels), 1)

    if coating_ratio < 0.15:
        return "peeled"
    elif coating_ratio < 0.35:
        return "thin"
    else:
        return "thick"


def detect_tooth_marks(mask):
    """
    齿痕检测
    通过分析舌体边缘的曲率变化判断
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return "none"

    cnt = max(contours, key=cv2.contourArea)

    # 计算边缘曲率变化
    peri = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.002 * peri, True)

    # 分析轮廓的凹凸变化
    hull = cv2.convexHull(cnt)
    hull_area = cv2.contourArea(hull)
    contour_area = cv2.contourArea(cnt)

    if hull_area == 0:
        return "none"

    concavity_ratio = (hull_area - contour_area) / hull_area

    if concavity_ratio < 0.02:
        return "none"
    elif concavity_ratio < 0.06:
        return "mild"
    else:
        return "severe"


def detect_cracks(region):
    """
    裂纹检测
    使用 Canny 边缘检测 + 线条分析
    """
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    if np.count_nonzero(gray) < 500:
        return "none"

    # 增强对比度
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Canny 边缘检测
    edges = cv2.Canny(enhanced, 40, 120)

    # 霍夫线检测找长裂纹
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180,
                             threshold=50, minLineLength=30, maxLineGap=10)

    if lines is None:
        return "none"

    crack_count = len(lines)
    if crack_count < 5:
        return "none"
    elif crack_count < 20:
        return "few"
    else:
        return "many"


def _fallback_analysis(img):
    """后备方案：对整个图像进行简单分析"""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L = np.mean(lab[:, :, 0])
    A = np.mean(lab[:, :, 1])

    if A < 125 and L > 155:
        tc = "pale_white"
    elif A < 130 and L > 100:
        tc = "light_red"
    elif A < 145:
        tc = "red"
    elif A < 155:
        tc = "deep_red"
    else:
        tc = "purple"

    return {
        "tongue_color": tc,
        "coating_color": "white",
        "coating_thickness": "thin",
        "tooth_mark_level": "none",
        "crack_level": "none",
        "tongue_found": False
    }
