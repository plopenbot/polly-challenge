const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generatePDFWithWaiting() {
    console.log('🚀 启动浏览器生成高质量PDF...');
    
    // 启动浏览器
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
        defaultViewport: { width: 1200, height: 800 }
    });
    
    try {
        console.log('✅ 浏览器已启动');
        
        // 创建新页面
        const page = await browser.newPage();
        
        // 设置更长的超时时间
        page.setDefaultNavigationTimeout(120000); // 120秒
        
        // 加载HTML文件
        const htmlPath = 'file://' + path.join(process.cwd(), 'pokemon_pdf_generation.html');
        console.log(`📖 加载页面: ${htmlPath}`);
        
        await page.goto(htmlPath, {
            waitUntil: 'networkidle2', // 等待网络空闲
            timeout: 60000
        });
        
        console.log('✅ 页面加载完成，等待所有图片加载...');
        
        // 等待所有图片加载的专用逻辑
        await page.evaluate(async () => {
            console.log('🖼️ 开始等待图片加载');
            
            // 等待加载状态显示"完成"
            return new Promise((resolve, reject) => {
                let checkCount = 0;
                const maxChecks = 60; // 最多等待60秒
                
                const checkLoading = () => {
                    checkCount++;
                    
                    // 检查加载状态
                    const statusElement = document.querySelector('.loading-status');
                    const loadingText = statusElement ? statusElement.textContent : '';
                    
                    if (loadingText.includes('✅ 所有图片已加载完成')) {
                        console.log('🎉 检测到所有图片加载完成');
                        resolve();
                        return;
                    }
                    
                    if (checkCount >= maxChecks) {
                        console.log('⚠️ 超时，但继续生成PDF');
                        resolve(); // 即使没全部加载也继续
                        return;
                    }
                    
                    setTimeout(checkLoading, 1000); // 每秒检查一次
                };
                
                checkLoading();
            });
        });
        
        console.log('✅ 所有图片加载等待完成');
        
        // 额外等待2秒确保渲染稳定
        await page.waitForTimeout(2000);
        
        // 生成PDF
        const pdfPath = path.join(process.cwd(), 'pokemon_verification_final.pdf');
        console.log('🖨️ 正在生成PDF...');
        
        await page.pdf({
            path: pdfPath,
            format: 'A4',
            landscape: false,
            printBackground: true,
            margin: { top: '20px', right: '20px', bottom: '20px', left: '20px' },
            scale: 0.85
        });
        
        console.log(`✅ PDF生成成功: ${pdfPath}`);
        
        // 检查文件大小
        const stats = fs.statSync(pdfPath);
        console.log(`📊 PDF文件大小: ${(stats.size / 1024 / 1024).toFixed(2)} MB`);
        
        // 截图预览
        const screenshotPath = path.join(process.cwd(), 'pdf_preview.png');
        await page.screenshot({ path: screenshotPath, fullPage: false });
        console.log(`📸 预览截图已保存: ${screenshotPath}`);
        
        return pdfPath;
        
    } catch (error) {
        console.error('❌ 生成PDF失败:', error);
        throw error;
    } finally {
        await browser.close();
        console.log('🔚 浏览器已关闭');
    }
}

// 运行
generatePDFWithWaiting()
    .then(pdfPath => {
        console.log(`🎉 完成！PDF已保存至: ${pdfPath}`);
        console.log('📄 现在可以将这个PDF发送给用户检查。');
    })
    .catch(error => {
        console.error('💥 出错:', error);
        process.exit(1);
    });

