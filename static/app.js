// ============================================================
// 中医舌诊识别系统 - 前端交互逻辑
// ============================================================

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const placeholder = document.getElementById('placeholder');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const noResults = document.getElementById('noResults');
const resultsContent = document.getElementById('resultsContent');

let selectedFile = null;

// ---------- File Selection ----------
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#6366f1';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '#d1d5db';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#d1d5db';
    handleFile(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

function handleFile(file) {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
        alert('请选择图片文件 (JPG/PNG/BMP)');
        return;
    }

    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.src = e.target.result;
        preview.style.display = 'block';
        placeholder.style.display = 'none';
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

// ---------- Analyze ----------
analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    analyzeBtn.disabled = true;
    loading.style.display = 'block';
    resultsContent.style.display = 'none';
    noResults.style.display = 'none';

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert('分析失败: ' + data.error);
            return;
        }

        displayResults(data);
    } catch (err) {
        alert('网络错误: ' + err.message);
    } finally {
        loading.style.display = 'none';
        analyzeBtn.disabled = false;
    }
});

// ---------- Display Results ----------
function displayResults(data) {
    noResults.style.display = 'none';
    resultsContent.style.display = 'block';

    const dx = data.diagnosis;

    // Summary
    document.getElementById('resultSummary').innerHTML = `
        <div>🧬 综合评估：${dx.summary}</div>
    `;

    // Findings cards
    let findingsHTML = '';
    dx.findings.forEach((f, i) => {
        const isNormal = f.diagnosis.includes('正常');
        const isDanger = f.finding.includes('绛红') || f.finding.includes('青紫') ||
                         f.finding.includes('灰黑') || f.finding.includes('明显');
        let cardClass = 'finding-card';
        if (isNormal) cardClass += ' normal';
        else if (isDanger) cardClass += ' danger';
        else cardClass += ' warning';

        findingsHTML += `
            <div class="${cardClass}">
                <div class="finding-header">
                    <span class="finding-category">${f.category}</span>
                    <span class="finding-name">${f.finding}</span>
                </div>
                <div class="finding-diagnosis">📌 ${f.diagnosis}</div>
                ${f.detail ? `<div class="finding-detail">${f.detail}</div>` : ''}
            </div>
        `;
    });
    document.getElementById('findingsList').innerHTML = findingsHTML;

    // Features table
    const feat = data.features;
    const colorNames = {
        "pale_white": "淡白舌", "light_red": "淡红舌", "red": "红舌",
        "deep_red": "绛红舌", "purple": "青紫舌"
    };
    const coatingColorNames = {
        "white": "白苔", "yellow": "黄苔", "gray_black": "灰黑苔"
    };
    const thicknessNames = {
        "thin": "薄苔", "thick": "厚苔", "peeled": "剥苔"
    };
    const toothMarkNames = {
        "none": "无齿痕", "mild": "轻度齿痕", "severe": "明显齿痕（胖大舌）"
    };
    const crackNames = {
        "none": "无裂纹", "few": "少量裂纹", "many": "明显裂纹"
    };

    document.getElementById('featuresTable').innerHTML = `
        <table class="features-table">
            <tr><td>🔴 舌色</td><td>${colorNames[feat.tongue_color] || feat.tongue_color}</td></tr>
            <tr><td>🟡 苔色</td><td>${coatingColorNames[feat.coating_color] || feat.coating_color}</td></tr>
            <tr><td>📏 苔质</td><td>${thicknessNames[feat.coating_thickness] || feat.coating_thickness}</td></tr>
            <tr><td>🦷 齿痕</td><td>${toothMarkNames[feat.tooth_mark_level] || feat.tooth_mark_level}</td></tr>
            <tr><td>〰️ 裂纹</td><td>${crackNames[feat.crack_level] || feat.crack_level}</td></tr>
            <tr><td>✅ 舌体识别</td><td>${feat.tongue_found ? '已定位舌体' : '未精确识别（使用整体分析）'}</td></tr>
        </table>
    `;

    // Advice
    let advHTML = '';
    dx.all_advice.forEach(a => { advHTML += `<li>${a}</li>`; });
    document.getElementById('adviceList').innerHTML = advHTML;

    // Image
    document.getElementById('resultImage').src = data.image_url;

    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}
