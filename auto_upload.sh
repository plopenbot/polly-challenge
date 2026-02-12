#!/bin/bash
# 一键上传脚本：宝可梦项目到GitHub
# 用户：pispeng | 仓库：polly-challenge

echo "🚀 宝可梦项目GitHub一键上传"
echo "=================================="

# 配置信息
GITHUB_USER="pispeng"
GITHUB_REPO="polly-challenge"
GITHUB_URL="https://github.com/$GITHUB_USER/$GITHUB_REPO.git"

echo "📋 配置:"
echo "  用户: $GITHUB_USER"
echo "  仓库: $GITHUB_REPO"
echo "  地址: $GITHUB_URL"
echo ""

# 步骤1：检查git状态
if [ ! -d ".git" ]; then
    echo "🔧 初始化Git仓库..."
    git init
    if [ $? -ne 0 ]; then
        echo "❌ Git初始化失败"
        exit 1
    fi
else
    echo "✅ Git仓库已存在"
fi

# 步骤2：添加文件
echo "📦 添加文件..."
git add .
if [ $? -ne 0 ]; then
    echo "⚠️  部分文件添加失败，继续..."
fi

# 步骤3：提交
echo "💾 提交更改..."
git commit -m "迁移宝可梦项目到 $GITHUB_USER 的GitHub

原项目: https://github.com/plopenbot/polly-challenge
迁移时间: $(date '+%Y-%m-%d %H:%M:%S')
"
if [ $? -ne 0 ]; then
    echo "⚠️  提交失败，可能没有新的更改"
fi

# 步骤4：获取当前分支
CURRENT_BRANCH=$(git branch --show-current)
if [ -z "$CURRENT_BRANCH" ]; then
    CURRENT_BRANCH="main"
    git branch -M main
fi

echo "🌿 当前分支: $CURRENT_BRANCH"

# 步骤5：添加远程仓库
echo "🔗 设置远程仓库..."
git remote add origin $GITHUB_URL 2>/dev/null || {
    echo "🔄 更新远程仓库地址..."
    git remote set-url origin $GITHUB_URL
}

# 检查连接（可选）
echo "📡 测试远程连接..."
git ls-remote origin >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "⚠️  无法连接到远程仓库，请检查:"
    echo "  1. 仓库是否存在: $GITHUB_URL"
    echo "  2. 网络连接"
    echo "  3. GitHub认证"
    echo ""
    echo "🧠 使用GitHub Token的方法:"
    echo "git remote set-url origin https://<YOUR_TOKEN>@github.com/$GITHUB_USER/$GITHUB_REPO.git"
    echo ""
    read -p "是否继续尝试推送? (y/N): " -n 1 CONTINUE
    if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ 远程仓库连接正常"
fi

# 步骤6：推送
echo "📤 推送到GitHub..."
git push -u origin $CURRENT_BRANCH

PUSH_RESULT=$?
if [ $PUSH_RESULT -eq 0 ]; then
    echo ""
    echo "🎉 恭喜！项目已成功推送到你的GitHub"
    echo "🌐 访问: https://github.com/$GITHUB_USER/$GITHUB_REPO"
    echo ""
    echo "📋 下一步操作:"
    echo "  1. 上传宝可梦图片到 images/ 目录"
    echo "  2. 使用 pokemon-zh-data-pispeng.js 替换原数据文件"
    echo "  3. 测试游戏图片加载"
else
    echo ""
    echo "❌ 推送失败，常见原因:"
    echo "  1. 仓库不存在: 请访问 https://github.com/new 创建 '$GITHUB_REPO'"
    echo "  2. 认证失败: 使用GitHub Token（见下面）"
    echo "  3. 分支不匹配: 尝试 git push -u origin main 或 master"
    echo ""
    echo "🔧 手动推送命令:"
    echo "# 尝试main分支"
    echo "git push -u origin main"
    echo "# 或master分支"
    echo "git push -u origin master"
    echo ""
    echo "🔐 使用GitHub Token推送:"
    echo "git remote set-url origin https://<YOUR_GITHUB_TOKEN>@github.com/$GITHUB_USER/$GITHUB_REPO.git"
    echo "git push -u origin main"
    echo ""
    echo "📖 详细指南见: README_MIGRATION.md"
fi

echo ""
echo "=================================="
echo "✅ 一键上传流程完成"
echo ""
echo "💡 快速部署GitHub Pages:"
echo "  1. 访问: https://github.com/$GITHUB_USER/$GITHUB_REPO/settings/pages"
echo "  2. 分支: $CURRENT_BRANCH"
echo "  3. 文件夹: / (根目录)"
echo "  4. 访问: https://$GITHUB_USER.github.io/$GITHUB_REPO/"