#!/bin/bash
# 机犬智讯 GitHub 部署脚本
# 用法：在终端中运行 bash deploy.sh

set -e

echo "=========================================="
echo "  机犬智讯 JIQUAN NEWS - GitHub 部署脚本"
echo "=========================================="
echo ""

# 测试 SSH 连接
echo "[1/4] 测试 SSH 连接..."
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "  ✓ SSH 连接成功"
else
    echo "  ✗ SSH 连接失败！请先添加 SSH 密钥到 GitHub"
    echo ""
    echo "  公钥内容（复制到 GitHub Settings → SSH keys）："
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "  添加地址：https://github.com/settings/keys"
    echo "  添加后重新运行此脚本"
    exit 1
fi

# 推送代码
echo ""
echo "[2/4] 推送代码到 GitHub..."
cd /Users/edy/Desktop/WORD/新闻/argos-news
git push -u origin main
echo "  ✓ 代码推送成功"

# 完成提示
echo ""
echo "[3/4] 部署完成！"
echo ""
echo "  GitHub 仓库地址：https://github.com/acking123/jiquan-news"
echo ""
echo "[4/4] 开启 GitHub Pages："
echo "  1. 打开 https://github.com/acking123/jiquan-news/settings/pages"
echo "  2. Source 选择 'Deploy from a branch'"
echo "  3. Branch 选择 'main' + '/ (root)'"
echo "  4. 点击 Save"
echo "  5. 等待 1-2 分钟，网站地址将显示为："
echo "     https://acking123.github.io/jiquan-news/"
echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
