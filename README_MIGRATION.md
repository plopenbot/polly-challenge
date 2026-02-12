# 🚀 宝可梦项目GitHub迁移指南

## 📋 问题背景
原项目图片地址：`https://raw.githubusercontent.com/plopenbot/polly-challenge/main/`
中国大陆访问不稳定，你希望迁移到你的GitHub仓库。

## ✅ 已完成的工作

### 1. 下载了测试图片
已成功下载：
- `images/regular/0001.png ~ 0010.png`（前10个普通图片）
- `images/shiny/0001.png ~ 0005.png`（前5个闪亮图片）

### 2. 生成了替换版数据文件
创建了 **`pokemon-zh-data-pispeng.js`**，所有图片地址已改为：
`https://raw.githubusercontent.com/pispeng/polly-challenge/main/`

### 3. 文件结构已准备好
```
polly-challenge/
├── index.html              # 游戏主页面
├── game.js                 # 游戏逻辑
├── pokemon-data.js        # 原始数据（英文）
├── pokemon-zh-data.js     # 原始中文数据（指向plopenbot）
├── pokemon-zh-data-pispeng.js # ✅ 你的版本，已修改地址
├── images/                 # 宝可梦图片目录
├── auto_upload.sh         # 一键上传脚本
└── README_MIGRATION.md    # 本指南
```

## 🚀 完整迁移步骤

### 第一步：创建GitHub仓库
1. 访问 https://github.com/new
2. 仓库名：`polly-challenge`
3. 描述：`Polly Challenge - 宝可梦答题游戏`
4. **重要**：不要初始化README等文件（保持空仓库）

### 第二步：推送到你的GitHub
使用以下脚本**一键推送**：

```bash
# 进入项目目录
cd /root/.openclaw/workspace/polly-challenge

# 一键上传（已为你写好）
bash auto_upload.sh
```

<details>
<summary>如果一键脚本失败，手动执行：</summary>

```bash
# 初始化git（如果还没有）
git init
git add .
git commit -m "迁移宝可梦项目到我的GitHub"

# 添加你的远程仓库
git remote add origin https://github.com/pispeng/polly-challenge.git

# 推送
git push -u origin main
# 如果失败，尝试：
git push -u origin master
```
</details>

### 第三步：批量下载所有图片
你需要下载全部1025只宝可梦的图片（约2050张）：

**方法A**：使用我的脚本逐步下载（推荐）
```bash
# 执行批量下载
python3 download_pokemon_images.py --all
# 或者
bash download_all_images.sh
```

**方法B**：如果你只需要测试，先推现有部分，后续慢慢补充：
图片会从你的GitHub加载，缺失的会显示占位符。

### 第四步：更新游戏文件
用你的数据文件替换原文件：

```bash
# 备份原文件
cp pokemon-zh-data.js pokemon-zh-data-original.js

# 使用你的版本（已修改地址）
cp pokemon-zh-data-pispeng.js pokemon-zh-data.js
```

### 第五步：测试游戏
1. 上传到GitHub Pages（可选）
2. 访问：`https://github.com/pispeng/polly-challenge`
3. 图片应该从你的仓库加载

## 🔧 可选优化方案

### 方案1：图片后台上传
先推代码，图片后续上传：
```bash
# 先推送代码
git add --all :!images/
git commit -m "先推送代码，图片稍后"
git push
```

### 方案2：使用CDN镜像（高级）
如果GitHub仍然慢，可以使用：
- jsDelivr: `https://cdn.jsdelivr.net/gh/pispeng/polly-challenge@main/`
- 或者国内镜像服务

### 方案3：懒加载优化
在`game.js`中添加图片加载失败的回退：
```javascript
// 在你的game.js中搜索图片加载代码
// 可以添加：
img.onerror = function() {
  this.src = 'images/placeholder.png'; // 本地备用图片
};
```

## 📁 重要文件说明

1. **`pokemon-zh-data-pispeng.js`** - ✅ **已完成替换**
   - 所有`plopenbot`地址已改为`pispeng`
   - 可以直接替换原文件使用

2. **`auto_upload.sh`** - 一键推送脚本
   - 包含错误处理和回退机制

3. **`download_pokemon_images.py`** - 批量下载工具
   - 支持断点续传、批量下载

## 📞 常见问题

**Q：上传2050张图片会不会太慢？**
A：可以先上传代码，图片分批上传。游戏有容错机制，缺失图片会显示占位符。

**Q：Git推送遇到认证问题？**
A：使用GitHub Token替代密码：
```bash
git remote set-url origin https://<YOUR_TOKEN>@github.com/pispeng/polly-challenge.git
```

**Q：如何测试是否生效？**
A：部署后打开浏览器控制台，查看图片加载来源是否为你的GitHub仓库。

## 🎯 下一步建议

1. **立即执行**：`bash auto_upload.sh` 推送代码
2. **后台运行**：批量下载图片脚本
3. **快速测试**：替换数据文件，看游戏效果

---

**你的GitHub仓库图片地址：**
`https://raw.githubusercontent.com/pispeng/polly-challenge/main/images/regular/0001.png`
`https://raw.githubusercontent.com/pispeng/polly-challenge/main/images/shiny/0001.png`

现在图片将从你的仓库稳定加载！