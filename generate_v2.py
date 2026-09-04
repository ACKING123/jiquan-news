import pandas as pd
import json
import re
import os
import html as html_module

OUTPUT_DIR = '/Users/edy/Desktop/WORD/新闻/argos-news'
EXCEL_PATH = '/Users/edy/.trae-cn/attachments/6a94d9da5e035e7c75bd4438/a308d65d-998a-4e8a-b28d-fa40cdade289_e06fa2cd-e1bd-4bf6-9140-3d5edfd8c10e_全球机器狗相关新闻汇总_0903.xlsx'

# ============================================================
# 1. READ EXISTING CSS/JS TEMPLATE FROM index.html
# ============================================================
with open(os.path.join(OUTPUT_DIR, 'index.html'), 'r') as f:
    index_html = f.read()

css_match = re.search(r'<style>(.*?)</style>', index_html, re.DOTALL)
CSS_TEMPLATE = css_match.group(1) if css_match else ''

# Extract JS (everything between first <script> after </footer> and </script> before </body>)
js_match = re.search(r'</footer>\s*<script[^>]*>(.*?)(?:</script>\s*<script[^>]*>(.*?))*</script>\s*</body>', index_html, re.DOTALL)
JS_HEADER = '<script src="./_shared/js/echarts.min.js"></script>'

# ============================================================
# 2. READ & PROCESS NEWS DATA
# ============================================================
df = pd.read_excel(EXCEL_PATH, header=1)
df.columns = ['id', 'date', 'brand', 'title', 'url', 'ai_score', 'overview', 'summary']
df = df.dropna(subset=['title'])

# Manually added news
extra_news = pd.DataFrame([
    {
        'id': 0, 'date': '2026-09-01', 'brand': '宇树科技',
        'title': '宇树消防机器人亮相，能背水炮、不怕火烧',
        'url': 'https://www.ithome.com/0/996/772.htm',
        'ai_score': 8,
        'overview': '宇树科技晒出四足机器人消防应急解决方案视频，展示A2-W背负、B2智能水炮、A2-W/B2侦测、As2云台侦查、B2卫星侦查、A2-W建模等多款消防机器狗，核心亮点为不怕火烧的B2耐高温机器狗，消防员还可通过机器狗与被困人员进行双向语音对讲。',
        'summary': '宇树以A2-W和B2两款平台衍生出8种消防角色，标志着四足机器人正从"单机作业"走向"集群编队"模式。一台机器狗解决一个问题、多台协同覆盖全流程——这种"平台化+模块化"思路意味着四足机器人的商业化重心已从"造出能走的机器"转向"造出能干活的系统"，消防只是第一个验证场景。',
    },
    {
        'id': 0, 'date': '2026-08-31', 'brand': '地平线机器人',
        'title': '地平线机器人2026年上半年归母净利润37.84亿元，同比扭亏为盈',
        'url': 'https://www.ithome.com/0/996/579.htm',
        'ai_score': 9,
        'overview': '地平线机器人发布2026财年半年报：营业总收入20.55亿元（同比+32.9%），毛利率66%，归母净利润37.84亿元同比扭亏为盈。自主品牌ADAS份额首破50%稳居行业第一，智驾计算平台总份额行业第一。',
        'summary': '地平线扭亏的核心驱动力是高毛利的授权及服务业务（+52.7%），占比升至55%——这意味着"卖IP"比"卖芯片"更赚钱。当智驾芯片厂商靠技术授权实现规模效应后，其积累的感知、决策、控制算法栈可向机器人领域溢出，地平线已成立地瓜机器人公司切入消费级机器人赛道，车载AI向具身智能的技术迁移正在发生。',
    },
    {
        'id': 0, 'date': '2026-08-31', 'brand': '商务部',
        'title': '商务部等7部门：加快人工智能手机和电脑、智能穿戴设备、智能机器人、智能家居等产品推广应用',
        'url': 'https://www.ithome.com/0/996/562.htm',
        'ai_score': 8,
        'overview': '商务部等7部门联合发布推动商品消费扩容升级实施意见，明确加快智能机器人等AI产品推广应用，建设消费领域国家AI应用中试基地和"人工智能+消费"集聚区，目标2030年社会消费品零售总额达60万亿元。',
        'summary': '这是国家级政策首次将"智能机器人"与手机、家电并列为消费扩容主力品类，信号意义大于执行细节。政策同时点名外骨骼机器人进老年人家庭，意味着养老场景被视为机器人消费化的突破口。对行业而言，政策红利可降低C端市场教育成本，但真正决定爆发的仍是产品力与价格——60万亿目标不会自动转化为机器人订单。',
    },
    {
        'id': 0, 'date': '2026-09-02', 'brand': '宇树科技',
        'title': 'A股"人形机器人第一股"宇树科技股价腰斩',
        'url': 'https://www.ithome.com/0/997/256.htm',
        'ai_score': 9,
        'overview': '宇树科技股价跌超4%，每股已跌至550元以下，相比首日开盘最高1100元/股已腰斩。公司8月19日上市发行价150.80元，开盘大涨629.44%后持续回调，2026上半年营收11.52亿元（+48.54%），扣非归母净利润2.44亿元（-19.34%）。',
        'summary': '上市14天股价腰斩，反映市场对人形机器人概念的狂热追捧正在退潮。营收增近五成但扣非利润反降19%，说明规模扩张尚未跑通盈利模型——"出货量全球第一"的标签撑不起4500亿市值预期。当炒作溢价被挤完后，估值将回归基本面，这也给整个四足/人形机器人行业敲响警钟：资本可以催熟上市，但无法替代商业模式的自我造血。',
    },
    {
        'id': 0, 'date': '2026-09-01', 'brand': '行业整体',
        'title': '我国牵头制定家用机器人国际标准，涵盖11项核心测试',
        'url': 'https://www.ithome.com/0/997/094.htm',
        'ai_score': 7,
        'overview': '我国牵头制定国际标准《家用和类似用途机器人性能评估方法》，涵盖避障、坡度运行、能耗等11项核心测试项目，为全球家用机器人行业提供统一性能评估框架，包括移动能力、障碍穿越、梅花阵型测试区域等。',
        'summary': '中国从"制造机器人"走向"定义机器人标准"，拿下国际标准制定权意味着在产业话语权上抢占了制高点。11项核心测试框架将加速行业优胜劣汰——有工程能力的企业获益，靠营销包装的玩家将被迫退场。标准统一后，消费者横向对比有了依据，有望加速家用机器人从"尝鲜"走向"标配"的渗透拐点。',
    },
    {
        'id': 0, 'date': '2026-09-02', 'brand': '宇树科技',
        'title': '宇树机器狗隐秘灰产链曝光，改电池标签"偷渡"上飞机',
        'url': 'https://www.ithome.com/0/997/497.htm',
        'ai_score': 8,
        'overview': '蓝鲸新闻曝光宇树机器狗灰产链：闲鱼租赁商通过篡改电池标签将421.2Wh高容量电池伪装成97.92Wh"合规电池"带上飞机。民航规定超160Wh电池禁止携带，宇树除Go1标准版外均不合规。宇树离职员工称2023年公司内部曾为客户粘贴低容量标签。',
        'summary': '灰产链暴露的不是个别商家道德问题，而是四足机器人跨区域运输的刚需与航空安全规则之间的结构性矛盾。机器狗电池普遍超160Wh，民航限制使其无法正常空运，租赁商被迫铤而走险。解决路径有二：一是电池模块化设计实现快速拆运，二是推动民航修订大型锂电池运输规则——谁先解决这个物流瓶颈，谁就能在租赁市场占据先发优势。',
    },
])
df = pd.concat([df, extra_news], ignore_index=True)
df = df.drop_duplicates(subset=['title'])
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
df['ai_score'] = pd.to_numeric(df['ai_score'], errors='coerce').fillna(0).astype(int)

# Clean brand names
df['brand'] = df['brand'].astype(str).str.replace(r'行业整体（.*?）', '行业整体', regex=True)

# Sort by date descending
df = df.sort_values('date', ascending=False).reset_index(drop=True)

# ============================================================
# 3. CATEGORIZATION
# ============================================================
def categorize(row):
    text = f"{row['title']} {row['overview']} {row['summary']}"
    scores = {'capital': 0, 'industry': 0, 'consumer': 0}
    for k in ['融资', '上市', 'IPO', '估值', '投资', '资本', '募资', '股份购买', '战投', '领投', '跟投', '券商', '科创板', '赴港', '募集', '入股', '股价', '市值', '腰斩', '净利润', '半年报', '财报', '股东', '溢利', '营收', '亏损']:
        if k in text: scores['capital'] += 2
    for k in ['巡检', '电力', '矿山', '消防', '安防', '警务', '应急', '工厂', '工业', '制造', '石油', '化工', '建筑', '施工', '农业', '林业', '水下', '管廊', '变电', '风电', '光伏', '钢厂', '冶炼', '仓储', '物流', '港口', '码头', '机场', '地铁', '铁路', '道路', '桥梁', '隧道', '水利', '大坝', '核电站', '燃气', '管道', '车辆', '装备', '雷达', '通信', '机场', '安保', '巡逻', '探测', '侦查', '救援', '排爆', '防暴', '军用', '国防', '武器', '弹药', '车辆', '机器狗', '机器人', '自动化', '智能化', '产线', '车间', '质量', '检测', '维护', '保养', '修理', '维修']:
        if k in text: scores['industry'] += 1
    for k in ['家庭', '导盲', '陪伴', '养老', '儿童', '宠物', '教育', '学校', '开学', '校园', '科普', '展会', '展览', '博览', '嘉年华', '表演', '娱乐', '文旅', '景区', '乐园', '博物馆', '图书馆', '商场', '商圈', '夜经济', '消费', '零售', '餐饮', '酒店', '迎新', '迎宾', '互动', '体验', '赛事', '比赛', '竞赛', '社区', '街道', '公园', '广场']:
        if k in text: scores['consumer'] += 1
    for k in ['消费', '零售', '家庭', '民生', '生活', '养老', '导盲', '陪伴']:
        if k in text: scores['consumer'] += 2
    for k in ['标准', '政策', '法规', '认证', '推广', '消费扩容', '人工智能+消费']:
        if k in text: scores['consumer'] += 2
    max_cat = max(scores, key=scores.get)
    if scores[max_cat] == 0:
        return 'industry'
    return max_cat

df['category'] = df.apply(categorize, axis=1)

# Stats
total_news = len(df)
avg_score = round(df['ai_score'].mean(), 1)
date_range = (pd.to_datetime(df['date']).max() - pd.to_datetime(df['date']).min()).days + 1
unique_brands = df['brand'].nunique()

cat_counts = df['category'].value_counts().to_dict()
cat_items = {
    'capital': df[df['category'] == 'capital'].sort_values('date', ascending=False),
    'industry': df[df['category'] == 'industry'].sort_values('date', ascending=False),
    'consumer': df[df['category'] == 'consumer'].sort_values('date', ascending=False),
}

print(f"News items: {total_news}")
for cat, items in cat_items.items():
    print(f"  {cat}: {len(items)} items")

# ============================================================
# 4. HTML GENERATION HELPERS
# ============================================================
def esc(text):
    """Escape HTML special characters"""
    if pd.isna(text):
        return ''
    return html_module.escape(str(text))

def score_class(score):
    if score >= 9: return 'score-hot'
    if score >= 8: return 'score-high'
    if score >= 6: return 'score-mid'
    return 'score-low'

def gen_card(row, rank):
    """Generate a news card HTML"""
    url = str(row['url']) if pd.notna(row['url']) else '#'
    return f'''            <article class="news-card" onclick="window.open('{url}', '_blank')" style="cursor:pointer;">
                <div class="card-rank">{rank}</div>
                <div class="card-content">
                    <div class="card-meta">
                        <span class="card-score {score_class(row['ai_score'])}">
                            <span class="score-label">AI热度</span>
                            <span class="score-value">{row['ai_score']}</span>
                        </span>
                        <span class="card-brand">{esc(row['brand'])}</span>
                        <span class="card-date">{row['date']}</span>
                    </div>
                    <h3 class="card-title">{esc(row['title'])}</h3>
                    <p class="card-overview">{esc(row['overview'])}</p>
                    <div class="card-summary">
                        <span class="summary-tag">启发</span>
                        <span class="summary-text">{esc(row['summary'])}</span>
                    </div>
                </div>
                <div class="card-glow"></div>
            </article>'''

def gen_slide(row, index):
    """Generate a slider slide HTML"""
    url = str(row['url']) if pd.notna(row['url']) else '#'
    img_num = (index % 5) + 1
    active = 'active' if index == 0 else ''
    return f'''            <div class="slide {active}" data-index="{index}" data-url="{url}" style="cursor:pointer;">
                <div class="slide-bg" style="background-image: url('assets/images/slide{img_num}.jpg?v=20260904');"></div>
                <div class="slide-content">
                    <div class="card-meta" style="margin-bottom:16px;">
                        <span class="card-score {score_class(row['ai_score'])}">
                            <span class="score-label">AI热度</span>
                            <span class="score-value">{row['ai_score']}</span>
                        </span>
                        <span class="card-brand">{esc(row['brand'])}</span>
                        <span class="card-date">{row['date']}</span>
                    </div>
                    <h2 class="slide-title">{esc(row['title'])}</h2>
                    <p class="slide-overview">{esc(row['overview'])}</p>
                </div>
            </div>'''

def gen_nav(active_page):
    items = [
        ('index.html', '首页', 'nav-home', ''),
        ('capital.html', '资本动态', '', ''),
        ('industry.html', '工业领域', '', ''),
        ('consumer.html', '消费领域', '', ''),
        ('products.html', '相关产品', 'nav-products', ''),
    ]
    links = []
    for href, name, extra_class, _ in items:
        cls = 'nav-item'
        if href == active_page:
            cls += ' active'
        if extra_class:
            cls += ' ' + extra_class
        links.append(f'<a href="{href}" class="{cls}">{name}</a>')
    return '\n'.join(links)

def gen_footer():
    return '''    <footer class="site-footer">
        <div class="container">
            <div class="footer-inner">
                <div class="footer-brand">
                    <a href="index.html" class="logo">
                        <span class="logo-main">机犬智讯</span>
                        <span class="logo-sub">JIQUAN NEWS</span>
                    </a>
                    <p class="footer-desc">
                        聚焦全球四足机器人与机器狗产业动态，实时追踪技术突破、资本动向、产业落地与市场格局，为行业从业者提供高价值情报。
                    </p>
                </div>
                <div class="footer-links">
                    <div class="footer-col">
                        <h4>资讯分类</h4>
                        <ul>
                            <li><a href="capital.html">资本动态</a></li>
                            <li><a href="industry.html">工业领域</a></li>
                            <li><a href="consumer.html">消费领域</a></li>
                        </ul>
                    </div>
                    <div class="footer-col">
                        <h4>更多</h4>
                        <ul>
                            <li><a href="products.html">相关产品</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <span class="footer-copyright">© 2026 JIQUAN NEWS 机犬智讯. All rights reserved.</span>
                <span class="footer-tech">
                    <span class="tech-dot"></span>
                    Powered by AI Intelligence
                </span>
            </div>
        </div>
    </footer>'''

def gen_header(active_page, page_title):
    return f'''    <header class="site-header">
        <div class="container">
            <div class="header-inner">
                <a href="index.html" class="logo">
                    <span class="logo-main">机犬智讯</span>
                    <span class="logo-sub">JIQUAN NEWS</span>
                </a>
                <nav class="main-nav">
                    {gen_nav(active_page)}
                </nav>
                <div class="header-right">
                    <button class="theme-toggle" id="themeToggle" aria-label="切换日/夜模式" title="切换日/夜模式">🌙</button>
                </div>
            </div>
        </div>
    </header>'''

def gen_theme_script():
    return '''    <script>
        (function() {
            var stored = localStorage.getItem('jiquan-theme');
            var prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
            if (stored === 'light' || (!stored && prefersLight)) {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        })();
    </script>'''

def gen_head(page_title):
    return f'''<!-- Generated by Trae Work -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <title>{page_title}</title>
    <meta name="description" content="聚焦全球机器狗与四足机器人行业动态，实时追踪技术突破、资本动向、产业落地与海外市场">
    {gen_theme_script()}
    <style>
{CSS_TEMPLATE}
    </style>
</head>
<body>'''

# Chart data generation
def gen_score_chart_data(df):
    scores = df['ai_score'].value_counts().sort_index(ascending=False)
    labels = []
    values = []
    for s in [10, 9, 8, 7, 6, 5]:
        labels.append(str(s))
        values.append(int(scores.get(s, 0)))
    return json.dumps(labels), json.dumps(values)

def gen_category_chart_data():
    data = []
    colors = {'industry': '#22c55e', 'consumer': '#ec4899', 'capital': '#f59e0b'}
    names = {'industry': '工业领域', 'consumer': '消费领域', 'capital': '资本动态'}
    for cat in ['industry', 'consumer', 'capital']:
        count = len(cat_items[cat])
        if count > 0:
            data.append({"name": names[cat], "value": count, "itemStyle": {"color": colors[cat]}})
    return json.dumps(data, ensure_ascii=False)

def gen_charts_js(page_type='index', cat_key=None):
    score_labels, score_values = gen_score_chart_data(df)
    cat_data = gen_category_chart_data()
    cat_names = json.dumps(["工业领域", "消费领域", "资本动态"], ensure_ascii=False)
    cat_links = json.dumps(["industry", "consumer", "capital"])

    if page_type == 'index':
        chart_html = f'''<div id="scoreChart" class="chart-container"></div>'''
        cat_chart_html = f'''<div id="categoryChart" class="chart-container"></div>'''
    else:
        chart_html = ''
        cat_chart_html = f'''<div id="catDistChart" class="chart-container" style="min-height:260px;"></div>'''

    return f'''
(function() {{
    var style = getComputedStyle(document.documentElement);
    var accent = style.getPropertyValue('--accent').trim();
    var accent2 = style.getPropertyValue('--accent2').trim();
    var ink = style.getPropertyValue('--ink').trim();
    var muted = style.getPropertyValue('--muted').trim();
    var rule = style.getPropertyValue('--rule').trim();
    var bg2 = style.getPropertyValue('--bg2').trim();

    var scoreEl = document.getElementById('scoreChart');
    if (scoreEl) {{
        var scoreChart = echarts.init(scoreEl, null, {{ renderer: 'svg' }});
        scoreChart.setOption({{
            animation: false,
            tooltip: {{ trigger: 'axis', appendToBody: true, backgroundColor: bg2, borderColor: rule, textStyle: {{ color: ink }} }},
            grid: {{ top: 10, right: 10, bottom: 24, left: 30 }},
            xAxis: {{ type: 'category', data: {score_labels}, axisLine: {{ lineStyle: {{ color: rule }} }}, axisLabel: {{ color: muted, fontSize: 11 }}, axisTick: {{ show: false }} }},
            yAxis: {{ type: 'value', axisLine: {{ show: false }}, axisLabel: {{ color: muted, fontSize: 10 }}, splitLine: {{ lineStyle: {{ color: rule, type: 'dashed' }} }}, minInterval: 1 }},
            series: [{{ type: 'bar', data: {score_values}, itemStyle: {{ color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{{ offset: 0, color: accent }}, {{ offset: 1, color: accent2 }}]), borderRadius: [4, 4, 0, 0] }}, barWidth: '50%' }}]
        }});
        window.addEventListener('resize', function() {{ scoreChart.resize(); }});
    }}

    var catEl = document.getElementById('categoryChart') || document.getElementById('catDistChart');
    if (catEl) {{
        var catColors = ["#22c55e", "#ec4899", "#f59e0b"];
        var categoryChart = echarts.init(catEl, null, {{ renderer: 'svg' }});
        categoryChart.setOption({{
            animation: false,
            tooltip: {{ trigger: 'item', appendToBody: true, backgroundColor: bg2, borderColor: rule, textStyle: {{ color: ink }} }},
            series: [{{ type: 'pie', radius: ['45%', '70%'], center: ['50%', '50%'], avoidLabelOverlap: true, itemStyle: {{ borderRadius: 4, borderColor: bg2, borderWidth: 2 }}, label: {{ show: true, position: 'outside', color: muted, fontSize: 11, formatter: '{{b}}\\n{{d}}%' }}, labelLine: {{ lineStyle: {{ color: rule }} }}, data: {cat_data} }}]
        }});
        var catNames = {cat_names};
        var catLinks = {cat_links};
        categoryChart.on('click', function(p) {{
            var idx = catNames.indexOf(p.name);
            if (idx >= 0) window.location.href = catLinks[idx] + '.html';
        }});
        window.addEventListener('resize', function() {{ categoryChart.resize(); }});
    }}
}})();

(function() {{
    const header = document.querySelector('.site-header');
    if (header) {{
        window.addEventListener('scroll', () => {{
            if (window.scrollY > 20) header.classList.add('scrolled');
            else header.classList.remove('scrolled');
        }}, {{ passive: true }});
    }}
    const toggle = document.getElementById('themeToggle');
    if (toggle) {{
        const stored = localStorage.getItem('jiquan-theme');
        const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
        if (stored === 'light' || (!stored && prefersLight)) {{
            document.documentElement.setAttribute('data-theme', 'light');
            toggle.textContent = '☀';
        }}
        toggle.addEventListener('click', () => {{
            const isLight = document.documentElement.getAttribute('data-theme') === 'light';
            if (isLight) {{
                document.documentElement.removeAttribute('data-theme');
                toggle.textContent = '🌙';
                localStorage.setItem('jiquan-theme', 'dark');
            }} else {{
                document.documentElement.setAttribute('data-theme', 'light');
                toggle.textContent = '☀';
                localStorage.setItem('jiquan-theme', 'light');
            }}
            setTimeout(() => location.reload(), 150);
        }});
    }}
}})();'''

def gen_slider_js():
    return '''
    (function() {
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const dots = document.querySelectorAll('.slide-dot');
        const totalSlides = slides.length;
        if (totalSlides === 0) return;
        let autoTimer = null;
        function goToSlide(index) {
            slides[currentSlide].classList.remove('active');
            dots[currentSlide].classList.remove('active');
            currentSlide = (index + totalSlides) % totalSlides;
            slides[currentSlide].classList.add('active');
            dots[currentSlide].classList.add('active');
        }
        document.getElementById('prevSlide')?.addEventListener('click', () => goToSlide(currentSlide - 1));
        document.getElementById('nextSlide')?.addEventListener('click', () => goToSlide(currentSlide + 1));
        dots.forEach((dot, i) => dot.addEventListener('click', () => goToSlide(i)));
        autoTimer = setInterval(() => goToSlide(currentSlide + 1), 5000);

        const slider = document.querySelector('.featured-slider');
        if (slider) {
            let touchStartX = 0, touchStartY = 0, touchEndX = 0, touchEndY = 0, isSwiping = false;
            slider.addEventListener('touchstart', (e) => {
                touchStartX = e.changedTouches[0].screenX;
                touchStartY = e.changedTouches[0].screenY;
                isSwiping = false;
                clearInterval(autoTimer);
            }, { passive: true });
            slider.addEventListener('touchmove', (e) => {
                const moveX = e.changedTouches[0].screenX;
                const moveY = e.changedTouches[0].screenY;
                const diffX = Math.abs(touchStartX - moveX);
                const diffY = Math.abs(touchStartY - moveY);
                if (diffX > 10 && diffX > diffY) { isSwiping = true; e.preventDefault(); }
            }, { passive: false });
            slider.addEventListener('touchend', (e) => {
                touchEndX = e.changedTouches[0].screenX;
                touchEndY = e.changedTouches[0].screenY;
                const diff = touchStartX - touchEndX;
                if (Math.abs(diff) > 40) {
                    if (diff > 0) { goToSlide(currentSlide + 1); }
                    else { goToSlide(currentSlide - 1); }
                } else if (!isSwiping) {
                    const url = slides[currentSlide].dataset.url;
                    if (url) window.open(url, '_blank');
                }
                autoTimer = setInterval(() => goToSlide(currentSlide + 1), 5000);
            }, { passive: true });
            slider.addEventListener('click', (e) => {
                if (e.target.closest('.slider-btn') || e.target.closest('.slide-dot')) return;
                const url = slides[currentSlide].dataset.url;
                if (url) window.open(url, '_blank');
            });
        }
    })();'''

def gen_loadmore_js():
    return '''
    (function() {
        const cards = document.querySelectorAll('.news-card');
        const btn = document.getElementById('loadMoreBtn');
        if (!btn) return;
        let visible = 15;
        function updateVisibility() {
            cards.forEach((card, i) => { card.style.display = i < visible ? 'flex' : 'none'; });
            if (visible >= cards.length) btn.style.display = 'none';
        }
        btn.addEventListener('click', () => { visible += 10; updateVisibility(); });
        updateVisibility();
    })();'''

# ============================================================
# 5. GENERATE INDEX.HTML
# ============================================================
top5 = df.head(5)
index_cards = df.head(15)

slides_html = '\n'.join(gen_slide(row, i) for i, (_, row) in enumerate(top5.iterrows()))
dots_html = ''.join(f'<button class="slide-dot {"active" if i == 0 else ""}" data-index="{i}"></button>' for i in range(5))
cards_html = '\n'.join(gen_card(row, i+1) for i, (_, row) in enumerate(index_cards.iterrows()))

cat_counts_display = {
    'capital': len(cat_items['capital']),
    'industry': len(cat_items['industry']),
    'consumer': len(cat_items['consumer']),
}

index_html_out = f'''{gen_head('机犬智讯-全球机器狗实时热点')}
{gen_header('index.html', '首页')}

    <main class="container">
        <section class="hero-section">
        <div class="featured-slider">
            <div class="slides-container">
{slides_html}
            </div>
        </div>
        <div class="slider-nav">
            <button class="slider-btn prev" id="prevSlide">‹</button>
            <div class="slider-dots">{dots_html}</div>
            <button class="slider-btn next" id="nextSlide">›</button>
        </div>
        </section>

        <section id="catSection" style="padding: 0 0 24px;">
            <h2 class="section-title" style="margin-bottom: 20px;">资讯分类</h2>
            <div class="cat-grid"><a href="capital.html" class="cat-card" style="--cat-color: #f59e0b">
        <span class="cat-icon">💰</span>
        <span class="cat-name">资本动态</span>
        <span class="cat-desc">融资、上市、投资与资本运作</span>
        <span class="cat-count">{cat_counts_display['capital']}<span class="cat-count-unit"> 条资讯 →</span></span>
    </a>
    <a href="industry.html" class="cat-card" style="--cat-color: #22c55e">
        <span class="cat-icon">⚙️</span>
        <span class="cat-name">工业领域</span>
        <span class="cat-desc">安防巡检、电力矿山、仓储物流等工业应用</span>
        <span class="cat-count">{cat_counts_display['industry']}<span class="cat-count-unit"> 条资讯 →</span></span>
    </a>
    <a href="consumer.html" class="cat-card" style="--cat-color: #ec4899">
        <span class="cat-icon">🏠</span>
        <span class="cat-name">消费领域</span>
        <span class="cat-desc">家庭、导盲、文旅与生活场景应用</span>
        <span class="cat-count">{cat_counts_display['consumer']}<span class="cat-count-unit"> 条资讯 →</span></span>
    </a>
    <a href="products.html" class="cat-card" style="--cat-color: #eab308">
    <span class="cat-icon">🏆</span>
    <span class="cat-name">相关产品</span>
    <span class="cat-desc">机器人整机、配件与软件平台产品库</span>
    <span class="cat-count">145<span class="cat-count-unit"> 款产品 →</span></span>
</a>
</div>
        </section>

        <div class="main-layout">
            <div class="main-col">
                <div class="filter-bar">
                    <h2 class="section-title">最新资讯</h2>
                </div>
                <div class="news-list" id="newsList">
{cards_html}
                </div>
                <div class="load-more">
                    <button class="load-more-btn" id="loadMoreBtn">加载更多</button>
                </div>
                <div class="more-info-hint" onclick="document.getElementById('catSection').scrollIntoView({{behavior:'smooth'}})" style="cursor:pointer;">
                    <span class="more-info-icon">📂</span>
                    <span class="more-info-text">更多资讯请查阅分类板块</span>
                    <span class="more-info-arrow">↑</span>
                </div>
            </div>
            <aside class="sidebar">
                <div class="sidebar-widget">
                    <div class="widget-header">
                        <span class="widget-title"><span>📊</span> 数据概览</span>
                    </div>
                    <div class="stats-grid">
                        <div class="stat-item"><div class="stat-value">{total_news}</div><div class="stat-label">资讯总数</div></div>
                        <div class="stat-item"><div class="stat-value">{avg_score}</div><div class="stat-label">平均热度</div></div>
                        <div class="stat-item"><div class="stat-value">{date_range}</div><div class="stat-label">覆盖天数</div></div>
                        <div class="stat-item"><div class="stat-value">145</div><div class="stat-label">相关产品</div></div>
                    </div>
                </div>
                <div class="sidebar-widget">
                    <div class="widget-header">
                        <span class="widget-title"><span>📈</span> 热度分布</span>
                    </div>
                    <div class="chart-widget"><div id="scoreChart" class="chart-container"></div></div>
                </div>
                <div class="sidebar-widget">
                    <div class="widget-header">
                        <span class="widget-title"><span>🗂️</span> 分类占比</span>
                    </div>
                    <div class="chart-widget"><div id="categoryChart" class="chart-container"></div></div>
                </div>
            </aside>
        </div>
    </main>

{gen_footer()}
<script src="./_shared/js/echarts.min.js"></script>
<script>
{gen_slider_js()}
{gen_loadmore_js()}
{gen_charts_js('index')}
</script>
</body>
</html>'''

with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w') as f:
    f.write(index_html_out)
print('  ✓ index.html')

# ============================================================
# 6. GENERATE CATEGORY PAGES
# ============================================================
cat_config = {
    'capital': {'name': '资本动态', 'icon': '💰', 'desc': '融资、上市、投资与资本运作', 'color': '#f59e0b'},
    'industry': {'name': '工业领域', 'icon': '⚙️', 'desc': '安防巡检、电力矿山、仓储物流等工业应用', 'color': '#22c55e'},
    'consumer': {'name': '消费领域', 'icon': '🏠', 'desc': '家庭、导盲、文旅与生活场景应用', 'color': '#ec4899'},
}

for cat_key, config in cat_config.items():
    items = cat_items[cat_key]
    count = len(items)
    avg_cat = round(items['ai_score'].mean(), 1) if count > 0 else 0
    cat_date_range = (pd.to_datetime(items['date']).max() - pd.to_datetime(items['date']).min()).days + 1 if count > 0 else 0
    cat_brands = items['brand'].nunique()

    cat_cards = '\n'.join(gen_card(row, i+1) for i, (_, row) in enumerate(items.iterrows()))

    page_html = f'''{gen_head(f'{config["name"]} - 机犬智讯')}
{gen_header(f'{cat_key}.html', config['name'])}

    <main class="container">
        <div class="page-header">
            <h1 class="page-title">{config["icon"]} {config["name"]}</h1>
            <p class="page-subtitle">{config["desc"]} · 共 {count} 条资讯</p>
        </div>

        <div class="main-layout">
            <div class="main-col">
                <div class="filter-bar">
                    <h2 class="section-title">{config["name"]}资讯</h2>
                </div>
                <div class="news-list" id="newsList">
{cat_cards}
                </div>
                <div class="load-more">
                    <button class="load-more-btn" id="loadMoreBtn">加载更多</button>
                </div>
            </div>
            <aside class="sidebar">
                <div class="sidebar-widget">
                    <div class="widget-header">
                        <span class="widget-title"><span>📊</span> 分类总览</span>
                    </div>
                    <div class="stats-grid">
                        <div class="stat-item"><div class="stat-value">{count}</div><div class="stat-label">本类资讯</div></div>
                        <div class="stat-item"><div class="stat-value">{avg_cat}</div><div class="stat-label">平均热度</div></div>
                        <div class="stat-item"><div class="stat-value">{cat_date_range}</div><div class="stat-label">覆盖天数</div></div>
                        <div class="stat-item"><div class="stat-value">{cat_brands}</div><div class="stat-label">品牌机构</div></div>
                    </div>
                    <div class="chart-widget">
                        <p style="font-size:12px;color:var(--muted);margin-bottom:8px;text-align:center;">点击饼图扇区跳转至对应分类</p>
                        <div id="catDistChart" class="chart-container" style="min-height:260px;"></div>
                    </div>
                </div>
            </aside>
        </div>
    </main>

{gen_footer()}
<script src="./_shared/js/echarts.min.js"></script>
<script>
{gen_slider_js()}
{gen_loadmore_js()}
{gen_charts_js('category', cat_key)}
</script>
</body>
</html>'''

    with open(os.path.join(OUTPUT_DIR, f'{cat_key}.html'), 'w') as f:
        f.write(page_html)
    print(f'  ✓ {cat_key}.html')

print(f'\n✅ All pages generated!')
print(f'   News items: {total_news}')
print(f'   Products: 145')
print(f'   Categories: 3')
for cat_key, config in cat_config.items():
    print(f'     {config["name"]}: {len(cat_items[cat_key])} items')
