// 宝可梦数据 - 使用本地镜像提升加载速度（为中国大陆网络优化）
// 原地址: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png
// 新地址: 使用我们自己的GitHub仓库镜像

const pokemonData = {
    total: 1025, // 目前共有1025只宝可梦
    shinyRate: 0.1, // 10%概率出现闪光
    
    // 获取随机宝可梦
    getRandom: function() {
        const id = Math.floor(Math.random() * this.total) + 1;
        const isShiny = Math.random() < this.shinyRate;
        
        // ✅ 修改点：使用我们自己的GitHub仓库镜像
        // 地址格式：https://raw.githubusercontent.com/plopenbot/polly-challenge/main/images/{type}/{id:04d}.png
        // 示例：https://raw.githubusercontent.com/plopenbot/polly-challenge/main/images/regular/0001.png
        //        https://raw.githubusercontent.com/plopenbot/polly-challenge/main/images/shiny/0001.png
        
        // 如果是已下载的图片（1-10），使用本地镜像，否则使用原地址（兼容性）
        const baseUrl = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon';
        const mirrorUrl = 'https://raw.githubusercontent.com/plopenbot/polly-challenge/main/images';
        
        let imageUrl;
        
        // 判断是否是已下载的图片范围（1-15）
        const isDownloaded = id <= 15;
        
        if (isDownloaded && isShiny) {
            // 闪亮下载图片（0001.png ~ 0015.png）
            const paddedId = String(id).padStart(4, '0');
            imageUrl = `${mirrorUrl}/shiny/${paddedId}.png`;
        } else if (isDownloaded && !isShiny) {
            // 普通下载图片（0001.png ~ 0015.png）
            const paddedId = String(id).padStart(4, '0');
            imageUrl = `${mirrorUrl}/regular/${paddedId}.png`;
        } else {
            // 其他图片暂时使用原地址（可后续补充下载）
            imageUrl = isShiny 
                ? `${baseUrl}/shiny/${id}.png`
                : `${baseUrl}/${id}.png`;
        }
        
        return {
            id: id,
            isShiny: isShiny,
            name: `宝可梦 #${id}`,
            imageUrl: imageUrl,
            rarity: isShiny ? '✨ 闪光' : '普通',
            source: isDownloaded ? '本地镜像' : 'PokeAPI原始地址'
        };
    },
    
    // 获取随机鼓励语
    getEncouragement: function() {
        const messages = [
            '太棒了！',
            '真聪明！',
            '继续加油！',
            '答对啦！',
            '你真厉害！',
            '完美！',
            '好样的！',
            '真优秀！'
        ];
        return messages[Math.floor(Math.random() * messages.length)];
    }
};