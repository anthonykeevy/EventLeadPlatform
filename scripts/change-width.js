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
        
        // Click on Appearance section to expand it
        console.log('Looking for Appearance button...');
        const clicked = await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const appearanceBtn = buttons.find(b => b.textContent?.includes('Appearance'));
            if (appearanceBtn) {
                appearanceBtn.click();
                return { found: true, text: appearanceBtn.textContent?.trim() };
            }
            return { found: false };
        });
        console.log('Appearance button:', clicked);
        await new Promise(r => setTimeout(r, 500));
        
        // Now look for Width dropdown within the expanded section
        console.log('Looking for Width dropdown...');
        const allSelectsInfo = await page.evaluate(() => {
            // Get all selects after expansion
            const selects = Array.from(document.querySelectorAll('select'));
            return selects.map((s, i) => {
                const parent = s.closest('div.space-y-1, div.flex');
                const label = parent?.querySelector('label')?.textContent?.trim() || 
                             parent?.previousElementSibling?.textContent?.trim() ||
                             `Unknown-${i}`;
                return {
                    index: i,
                    label,
                    value: s.value,
                    options: Array.from(s.options).map(o => o.value),
                };
            });
        });
        
        console.log('All selects after expansion:');
        console.log(JSON.stringify(allSelectsInfo, null, 2));
        
        // Find the Width select - look for one with 'auto' option
        const widthSelect = allSelectsInfo.find(s => s.options.includes('auto') && s.options.includes('custom'));
        if (widthSelect) {
            console.log('\nFound Width select at index', widthSelect.index);
            console.log('Current value:', widthSelect.value);
            
            // Change to auto
            const result = await page.evaluate((idx) => {
                const selects = Array.from(document.querySelectorAll('select'));
                const select = selects[idx];
                if (select) {
                    const oldValue = select.value;
                    select.value = 'auto';
                    select.dispatchEvent(new Event('change', { bubbles: true }));
                    return { success: true, oldValue, newValue: 'auto' };
                }
                return { success: false };
            }, widthSelect.index);
            
            console.log('Change result:', result);
            await new Promise(r => setTimeout(r, 1000));
            
            // Verify the change in DOM
            const verification = await page.evaluate((compId) => {
                const el = document.querySelector(`[data-component-id="${compId}"]`);
                const outer = el?.closest('.group.touch-none.relative');
                return {
                    outerStyle: outer?.getAttribute('style')?.substring(0, 150),
                    hasWidth960: outer?.getAttribute('style')?.includes('960px'),
                };
            }, componentId);
            
            console.log('\nDOM verification:', verification);
            
            if (!verification.hasWidth960) {
                console.log('\n✅ Width changed successfully!');
            } else {
                console.log('\n⚠️ Width still shows 960px in DOM');
            }
        } else {
            console.log('\n❌ Could not find Width select with auto/custom options');
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
