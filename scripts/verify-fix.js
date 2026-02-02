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
        
        // Force a complete refresh with cache bypass
        console.log('Force refreshing with cache bypass...');
        await page.evaluate(() => {
            window.location.reload(true);
        });
        
        // Wait for page to reload
        await page.waitForNavigation({ waitUntil: 'networkidle2' });
        await new Promise(r => setTimeout(r, 3000));
        
        console.log('Page reloaded');
        
        // Click on the component
        const componentId = 'text-1768184324292-685';
        const componentEl = await page.$(`[data-component-id="${componentId}"]`);
        if (componentEl) {
            await componentEl.click();
            console.log('Clicked on component');
            await new Promise(r => setTimeout(r, 1000));
        }
        
        // Check the current state
        const result = await page.evaluate((compId) => {
            // From localStorage
            const formDefJson = localStorage.getItem('builder-formDefinition-44');
            let storedWidth = 'N/A';
            if (formDefJson) {
                const formDef = JSON.parse(formDefJson);
                const pages = formDef.pages || formDef.desktopPages || [];
                for (const page of pages) {
                    const comp = page.components?.find(c => c.id === compId);
                    if (comp) {
                        storedWidth = comp.props.width === undefined ? 'UNDEFINED (Auto)' : comp.props.width;
                        break;
                    }
                }
            }
            
            // From DOM
            const el = document.querySelector(`[data-component-id="${compId}"]`);
            const outer = el?.closest('.group.touch-none.relative');
            const outerStyle = outer?.getAttribute('style');
            
            // Check SmartBorder class
            const smartBorderEl = el?.querySelector('.relative.inline-block, .relative.block');
            const smartBorderClass = el?.className;
            
            // Check if SmartBorder is using shrink mode (inline-block)
            const hasShrinkClass = smartBorderClass?.includes('inline-block');
            const hasFillClass = smartBorderClass?.includes('w-full');
            
            // Get resize wrapper position
            const resizeWrapper = outer?.querySelector('[style*="pointer-events: none"][style*="position: absolute"]');
            
            return {
                storedWidth,
                outerStyle: outerStyle?.substring(0, 200),
                smartBorderClass,
                hasShrinkClass,
                hasFillClass,
                resizeWrapperFound: !!resizeWrapper,
                resizeWrapperStyle: resizeWrapper?.style?.cssText?.substring(0, 200),
            };
        }, componentId);
        
        console.log('\n=== VERIFICATION RESULT ===');
        console.log(JSON.stringify(result, null, 2));
        
        if (result.storedWidth === 'UNDEFINED (Auto)' && !result.hasFillClass) {
            console.log('\n✅ FIX APPLIED SUCCESSFULLY!');
            console.log('Width is now Auto and SmartBorder is not using fill mode.');
        } else if (result.storedWidth === 'UNDEFINED (Auto)' && result.hasFillClass) {
            console.log('\n⚠️ Width is Auto but SmartBorder still shows fill mode.');
            console.log('The React code may need another update.');
        } else {
            console.log('\n❌ Width is still set:', result.storedWidth);
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
