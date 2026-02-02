const puppeteer = require('puppeteer');

async function main() {
    try {
        const browser = await puppeteer.connect({
            browserURL: 'http://127.0.0.1:9222',
            defaultViewport: null
        });
        
        console.log('Connected to Chrome!');
        
        const pages = await browser.pages();
        let page = pages.find(p => p.url().includes('localhost:3000'));
        
        if (!page) {
            console.log('No page found');
            return;
        }
        
        // Click on the component to select it
        const componentId = 'text-1768184324292-685';
        const componentEl = await page.$(`[data-component-id="${componentId}"]`);
        if (componentEl) {
            await componentEl.click();
            console.log('Component selected');
            await new Promise(r => setTimeout(r, 1500));
        }
        
        // Explore the Properties Panel
        const panelInfo = await page.evaluate(() => {
            const result = {
                panels: [],
                labels: [],
                selects: [],
                buttons: [],
            };
            
            // Find all labels
            const labels = Array.from(document.querySelectorAll('label, span'));
            result.labels = labels
                .map(l => l.textContent?.trim())
                .filter(t => t && t.length < 50)
                .slice(0, 50);
            
            // Find all select elements
            const selects = Array.from(document.querySelectorAll('select'));
            result.selects = selects.map(s => ({
                name: s.name,
                id: s.id,
                value: s.value,
                options: Array.from(s.options).map(o => o.value).slice(0, 10),
            }));
            
            // Find all collapsible section buttons
            const buttons = Array.from(document.querySelectorAll('button'));
            result.buttons = buttons
                .map(b => b.textContent?.trim())
                .filter(t => t && t.length < 100)
                .slice(0, 30);
            
            // Find the Properties Panel by looking for a specific structure
            // Usually on the right side of the screen
            const rightPanels = Array.from(document.querySelectorAll('div'))
                .filter(d => {
                    const style = window.getComputedStyle(d);
                    const rect = d.getBoundingClientRect();
                    return rect.right > window.innerWidth - 400 && rect.width > 200 && rect.height > 200;
                })
                .slice(0, 3);
            
            result.panels = rightPanels.map(p => ({
                className: p.className?.substring(0, 100),
                childLabels: Array.from(p.querySelectorAll('label, span'))
                    .map(l => l.textContent?.trim())
                    .filter(t => t && t.length < 50)
                    .slice(0, 20),
            }));
            
            return result;
        });
        
        console.log('\n=== Properties Panel Exploration ===');
        console.log('\n--- Labels found (first 50) ---');
        console.log(panelInfo.labels.join(', '));
        
        console.log('\n--- Select elements ---');
        console.log(JSON.stringify(panelInfo.selects, null, 2));
        
        console.log('\n--- Buttons (first 30) ---');
        console.log(panelInfo.buttons.join(', '));
        
        console.log('\n--- Right side panels ---');
        panelInfo.panels.forEach((p, i) => {
            console.log(`\nPanel ${i + 1}: ${p.className}`);
            console.log('Labels:', p.childLabels.join(', '));
        });
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
