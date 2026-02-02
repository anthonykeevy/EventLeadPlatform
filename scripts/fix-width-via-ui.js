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
        
        console.log('Current URL:', page.url());
        
        // Navigate if needed
        if (!page.url().includes('/forms/44/builder')) {
            await page.goto('http://localhost:3000/forms/44/builder', { waitUntil: 'networkidle2' });
        }
        
        await new Promise(r => setTimeout(r, 2000));
        
        // Click on the component to select it
        const componentId = 'text-1768184324292-685';
        console.log('Selecting component:', componentId);
        
        const componentEl = await page.$(`[data-component-id="${componentId}"]`);
        if (componentEl) {
            await componentEl.click();
            console.log('Component selected');
            await new Promise(r => setTimeout(r, 1000));
        } else {
            console.log('Component not found!');
            return;
        }
        
        // Look for the Properties Panel
        // Find the Dimensions section or Appearance section with Width dropdown
        console.log('Looking for Width dropdown in Properties Panel...');
        
        // First, try to expand the Dimensions section if it's collapsed
        await page.evaluate(() => {
            const buttons = Array.from(document.querySelectorAll('button'));
            const dimensionsBtn = buttons.find(b => b.textContent?.includes('Dimensions'));
            if (dimensionsBtn) {
                dimensionsBtn.click();
            }
        });
        await new Promise(r => setTimeout(r, 500));
        console.log('Attempted to expand Dimensions section');
        
        // Find the width dropdown by looking for the label "Width"
        const widthDropdown = await page.evaluate(() => {
            // Look for a select or dropdown near a "Width" label
            const labels = Array.from(document.querySelectorAll('label, span'));
            for (const label of labels) {
                if (label.textContent?.trim() === 'Width') {
                    // Find the closest select or dropdown
                    const parent = label.closest('.space-y-1, .flex, div');
                    if (parent) {
                        const select = parent.querySelector('select, [role="combobox"], button');
                        if (select) {
                            return {
                                found: true,
                                type: select.tagName,
                                currentValue: select.value || select.textContent?.trim(),
                            };
                        }
                    }
                }
            }
            return { found: false };
        });
        
        console.log('Width dropdown info:', widthDropdown);
        
        // Try to find and change the width to Auto using the Properties Panel
        const result = await page.evaluate(() => {
            // Find all selects in the Properties Panel (right side)
            const rightPanel = document.querySelector('.properties-panel, [class*="properties"], div[style*="width: 320px"]');
            
            // Look for the Width select/dropdown
            const allLabels = Array.from(document.querySelectorAll('label, span'));
            const widthLabel = allLabels.find(l => l.textContent?.trim() === 'Width');
            
            if (!widthLabel) {
                return { error: 'Width label not found' };
            }
            
            // Find the parent container
            let container = widthLabel.parentElement;
            for (let i = 0; i < 5 && container; i++) {
                const select = container.querySelector('select');
                if (select) {
                    // Get current value
                    const currentValue = select.value;
                    
                    // Find the "auto" option
                    const autoOption = Array.from(select.options).find(o => o.value === 'auto');
                    
                    if (autoOption) {
                        // Change to auto
                        select.value = 'auto';
                        // Dispatch change event
                        select.dispatchEvent(new Event('change', { bubbles: true }));
                        
                        return {
                            success: true,
                            previousValue: currentValue,
                            newValue: 'auto',
                        };
                    } else {
                        return {
                            error: 'Auto option not found',
                            options: Array.from(select.options).map(o => o.value),
                        };
                    }
                }
                container = container.parentElement;
            }
            
            return { error: 'Select element not found near Width label' };
        });
        
        console.log('\n=== Change Result ===');
        console.log(JSON.stringify(result, null, 2));
        
        if (result.success) {
            console.log('\n✅ Width changed to Auto via UI!');
            
            // Wait for the change to propagate
            await new Promise(r => setTimeout(r, 1000));
            
            // Verify the DOM changed
            const verification = await page.evaluate((compId) => {
                const el = document.querySelector(`[data-component-id="${compId}"]`);
                const outer = el?.closest('.group.touch-none.relative');
                return {
                    outerStyle: outer?.getAttribute('style'),
                    smartBorderClass: el?.className,
                };
            }, componentId);
            
            console.log('\n=== DOM After Change ===');
            console.log(JSON.stringify(verification, null, 2));
        }
        
        console.log('\nBrowser kept open for inspection.');
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
