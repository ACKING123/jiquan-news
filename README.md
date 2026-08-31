# 机犬智讯 JIQUAN NEWS - 部署到 GitHub Pages 指南

## 网站结构

```
argos-news/
├── index.html          # 首页（特色轮播 + 分类导航 + 最新资讯 + 数据看板）
├── capital.html        # 资本动态（融资、上市、投资）
├── tech.html           # 技术突破（算法、模型、硬件）
├── security.html       # 安防巡检（警务、消防、应急）
├── industry.html       # 工业应用（电力、矿山、制造）
├── overseas.html       # 海外市场（出海、国际合作）
├── consumer.html       # 消费民生（家庭、导盲、文旅）
├── expo.html           # 行业盛会（博览会、大会）
├── products.html       # WRC展品库（129款产品展示）
├── assets/
│   └── news_data.json  # 新闻原始数据
└── _shared/
    ├── js/
    │   └── echarts.min.js  # 图表库
    └── fonts/              # 字体文件
        ├── InstrumentSans-Regular.ttf
        ├── InstrumentSans-Bold.ttf
        ├── BigShoulders-Bold.ttf
        └── JetBrainsMono-Regular.ttf
```

---

## 方法一：网页界面上传（最简单）

### 步骤 1：创建 GitHub 仓库
1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** → **New repository**
3. 仓库名称：`jiquan-news`（或你喜欢的名字）
4. 选择 **Public**
5. 点击 **Create repository**

### 步骤 2：上传文件
1. 在仓库页面点击 **Add file** → **Upload files**
2. 将 `argos-news` 文件夹**内部**的所有文件和子文件夹拖入上传区：
   - 9 个 `.html` 文件
   - `assets/` 文件夹
   - `_shared/` 文件夹（含 `js/` 和 `fonts/`）
3. 点击 **Commit changes**

> ⚠️ 确保 `index.html` 在仓库根目录，不要嵌套在子文件夹中。

### 步骤 3：开启 GitHub Pages
1. 点击仓库顶部 **Settings**
2. 左侧菜单找到 **Pages**（在 "Code and automation" 下）
3. **Source** 选 **Deploy from a branch**
4. **Branch** 选 `main`，文件夹选 `/ (root)`
5. 点击 **Save**
6. 等待 1-2 分钟，页面顶部显示：
   ```
   Your site is live at https://你的用户名.github.io/jiquan-news/
   ```

---

## 方法二：Git 命令行（推荐，方便后续更新）

### 初始化并上传
```bash
# 进入网站目录
cd /Users/edy/Desktop/WORD/新闻/argos-news

# 初始化 Git
git init
git add .
git commit -m "机犬智讯 JIQUAN NEWS 多页面网站"

# 关联远程仓库（替换用户名和仓库名）
git branch -M main
git remote add origin https://github.com/你的用户名/jiquan-news.git
git push -u origin main
```

### 后续更新
```bash
cd /Users/edy/Desktop/WORD/新闻/argos-news
git add .
git commit -m "更新资讯数据"
git push
```
推送后 GitHub Pages 自动重新部署，约 30 秒生效。

### 开启 Pages
同方法一步骤 3。

---

## 自定义域名（可选）

1. 仓库 **Settings** → **Pages** → **Custom domain** 填入你的域名
2. 到域名服务商添加 DNS 记录：
   ```
   类型：A     主机：@     值：185.199.108.153
   类型：A     主机：@     值：185.199.109.153
   类型：A     主机：@     值：185.199.110.153
   类型：A     主机：@     值：185.199.111.153
   类型：CNAME  主机：www   值：你的用户名.github.io
   ```
3. 回 GitHub 点 **Save**，勾选 **Enforce HTTPS**

---

## 常见问题

**Q: 页面打开后样式不对/404？**
A: 检查所有文件是否都在仓库根目录（不是嵌套在 `argos-news/` 文件夹内）。GitHub Pages 路径区分大小写。

**Q: 图表不显示？**
A: 确认 `_shared/js/echarts.min.js` 已上传。按 F12 查看控制台是否有 404。

**Q: 字体不生效？**
A: 确认 `_shared/fonts/` 下的 4 个 TTF 文件已上传。

**Q: 导航链接跳转 404？**
A: 确保所有 9 个 HTML 文件都已上传：`index.html`、`capital.html`、`tech.html`、`security.html`、`industry.html`、`overseas.html`、`consumer.html`、`expo.html`、`products.html`。

**Q: 如何添加新的资讯分类页面？**
A: 复制任意分类页面（如 `tech.html`），修改页面标题和内容，在所有页面的导航栏 `<nav class="main-nav">` 中添加对应的链接即可。
