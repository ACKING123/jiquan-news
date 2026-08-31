# 天戎资讯 ARGOS NEWS - 部署到 GitHub Pages 指南

## 方法一：使用 GitHub 网页界面（最简单，无需命令行）

### 步骤 1：创建 GitHub 仓库
1. 登录 [GitHub](https://github.com)
2. 点击右上角 **+** → **New repository**
3. 仓库名称建议：`argos-news`（或你喜欢的名字）
4. 选择 **Public**（公开仓库才能免费使用 GitHub Pages）
5. 勾选 **Add a README file**（可选）
6. 点击 **Create repository**

### 步骤 2：上传网站文件
1. 在仓库页面，点击 **Add file** → **Upload files**
2. 将 `argos-news` 文件夹内的**所有文件和文件夹**拖拽到上传区域：
   - `index.html`（主页）
   - `argos-news.html`（备用）
   - `assets/` 文件夹
   - `_shared/` 文件夹（包含 js 和 fonts）
3. 滚动到底部，点击 **Commit changes**

> ⚠️ 注意：确保 `index.html` 在仓库根目录，而不是嵌套在子文件夹中。
> 如果你的文件都在 `argos-news/` 文件夹内，请上传文件夹**内部**的内容到仓库根目录。

### 步骤 3：启用 GitHub Pages
1. 在仓库页面，点击顶部的 **Settings**（设置）
2. 左侧菜单找到 **Pages**（在 "Code and automation" 分类下）
3. 在 **Build and deployment** 部分：
   - **Source** 选择 **Deploy from a branch**
   - **Branch** 选择 `main`（或 `master`），文件夹选择 `/ (root)`
   - 点击 **Save**
4. 等待 1-2 分钟，页面上方会显示你的网站地址：
   ```
   Your site is live at https://你的用户名.github.io/仓库名/
   ```

---

## 方法二：使用 Git 命令行（推荐，方便后续更新）

### 前置准备
- 安装 Git：https://git-scm.com/downloads
- 拥有 GitHub 账号

### 步骤 1：在 GitHub 创建仓库
同上方法一步骤 1

### 步骤 2：初始化本地仓库并上传
打开终端（Mac 的 Terminal 或 Windows 的 PowerShell），执行：

```bash
# 进入你的网站文件目录
cd /path/to/argos-news

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 天戎资讯网站"

# 关联远程仓库（替换为你的 GitHub 用户名和仓库名）
git branch -M main
git remote add origin https://github.com/你的用户名/argos-news.git

# 推送到 GitHub
git push -u origin main
```

### 步骤 3：启用 GitHub Pages
同上方法一步骤 3

---

## 后续更新网站内容

### 使用命令行（推荐）
```bash
cd /path/to/argos-news
git add .
git commit -m "更新新闻数据"
git push
```
推送后 GitHub Pages 会自动重新部署，通常 30 秒内生效。

### 使用网页界面
直接在仓库页面拖拽上传新文件覆盖即可。

---

## 自定义域名（可选）

如果你有自己的域名（比如 `argos.news`）：

1. 在仓库 **Settings** → **Pages** → **Custom domain** 中填入你的域名
2. 在域名服务商处添加 DNS 记录：
   - **CNAME** 记录：`www` → `你的用户名.github.io`
   - 或 **A** 记录：`@` → GitHub Pages IP（参考 GitHub 官方文档）
3. 勾选 **Enforce HTTPS** 启用 HTTPS

---

## 文件结构说明

```
argos-news/
├── index.html              # 主页（必须）
├── argos-news.html         # 备用页面
├── assets/
│   └── news_data.json      # 新闻数据（JSON格式）
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

## 常见问题

**Q: 网站打开后样式不对？**
A: 检查文件路径是否正确。GitHub Pages 区分大小写，确保文件名和 HTML 中的引用一致。

**Q: 图表不显示？**
A: 确认 `_shared/js/echarts.min.js` 文件已正确上传。打开浏览器控制台（F12）查看是否有 404 错误。

**Q: 字体不生效？**
A: 确认 `_shared/fonts/` 下的 TTF 文件已上传。GitHub Pages 支持 TTF 字体。

**Q: 可以有多个页面吗？**
A: 可以。在根目录创建更多 HTML 文件，通过链接互相跳转。比如 `about.html` 可以通过 `https://你的用户名.github.io/argos-news/about.html` 访问。

**Q: 网站是免费的吗？**
A: 公开仓库的 GitHub Pages 完全免费。私有仓库需要 GitHub Pro 订阅。
