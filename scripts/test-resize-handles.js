const puppeteer = require('puppeteer');

(async () => {
    try {
        const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
        const pages = await browser.pages();
        let page = pages.find(p => p.url().includes('localhost:3000'));
        
        if (!page) {
            page = await browser.newPage();
            await page.goto('http://localhost:3000/login');
        }
        
        console.log('Current URL:', page.url());
        
        // Login if needed
        if (page.url().includes('/login')) {
            console.log('Logging in...');
            await page.type('input[name="email"], input[type="email"]', 'user2@test.com');
            await page.type('input[name="password"], input[type="password"]', 'JChMom7KYLfL88&!');
            await page.click('button[type="submit"]');
            await page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 10000 });
            console.log('Logged in, URL:', page.url());
        }
        
        // Navigate to form builder
        console.log('Navigating to form builder...');
        await page.goto('http://localhost:3000/forms/44/builder', { waitUntil: 'networkidle0' });
        await new Promise(r => setTimeout(r, 2000));
        console.log('At form builder');
        
        // Click on target component
        const component = await page.$('[data-component-id="text-1768184324292-685"]');
        if (component) {
            await component.click();
            console.log('Component selected');
            await new Promise(r => setTimeout(r, 1000));
            
            // Check for resize handles with pointerEvents
            const handleInfo = await page.evaluate(() => {
                // Find elements that look like resize handles (small, colored boxes with cursor styles)
                const allDivs = document.querySelectorAll('div');
                const handles = [];
                
                allDivs.forEach(div => {
                    const style = div.style;
                    const computed = window.getComputedStyle(div);
                    
                    // Resize handles have specific cursor styles
                    if (computed.cursor && computed.cursor.includes('resize')) {
                        handles.push({
                            cursor: computed.cursor,
                            pointerEvents: style.pointerEvents || computed.pointerEvents,
                            width: computed.width,
                            height: computed.height,
                            backgroundColor: computed.backgroundColor
                        });
                    }
                });
                
                return handles;
            });
            
            console.log('Resize handles found:', handleInfo.length);
            if (handleInfo.length > 0) {
                console.log('Handle details:');
                handleInfo.forEach((h, i) => {
                    console.log(`  Handle ${i + 1}: cursor=${h.cursor}, pointerEvents=${h.pointerEvents}, size=${h.width}x${h.height}`);
                });
                
                // Check if any handle has pointerEvents: auto
                const hasAutoPointerEvents = handleInfo.some(h => h.pointerEvents === 'auto');
                console.log('\n✅ pointerEvents: auto applied:', hasAutoPointerEvents);
            }
        } else {
            console.log('Component not found');
        }
        
        console.log('\nTest complete!');
    } catch (error) {
        console.error('Error:', error.message);
    }
})();
