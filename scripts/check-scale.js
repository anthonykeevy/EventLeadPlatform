const puppeteer = require('puppeteer');

async function main() {
    try {
        const browser = await puppeteer.connect({
            browserURL: 'http://127.0.0.1:9222',
            defaultViewport: null
        });
        
        const pages = await browser.pages();
        let page = pages.find(p => p.url().includes('localhost:3000'));
        
        // Click on the component to select it
        const componentId = 'text-1768184324292-685';
        const componentEl = await page.$(`[data-component-id="${componentId}"]`);
        if (componentEl) {
            await componentEl.click();
            await new Promise(r => setTimeout(r, 1000));
        }
        
        // Check for scale transforms
        const scaleInfo = await page.evaluate((compId) => {
            const smartBorderEl = document.querySelector(`[data-component-id="${compId}"]`);
            const outerWrapper = smartBorderEl?.closest('.group.touch-none.relative');
            
            const transforms = [];
            let el = outerWrapper;
            while (el && el !== document.body) {
                const cs = window.getComputedStyle(el);
                if (cs.transform && cs.transform !== 'none') {
                    const rect = el.getBoundingClientRect();
                    transforms.push({
                        tag: el.tagName,
                        className: el.className?.substring?.(0, 50),
                        transform: cs.transform,
                        transformOrigin: cs.transformOrigin,
                        rectWidth: rect.width,
                        rectHeight: rect.height,
                    });
                }
                el = el.parentElement;
            }
            
            // Also check for zoom
            const canvas = document.querySelector('.relative.bg-white.shadow-, [style*="transform: scale"]');
            const canvasStyle = canvas ? window.getComputedStyle(canvas) : null;
            
            // Find the actual canvas/stage element
            const stageEl = document.querySelector('[style*="transform: scale"]');
            const stageTransform = stageEl?.getAttribute('style');
            
            return {
                transforms,
                canvasTransform: canvasStyle?.transform,
                stageStyle: stageTransform?.substring(0, 200),
                // Get the zoom level from the builder store if available
                zoomInfo: window.useBuilderStore?.getState?.()?.zoom || 'unknown',
            };
        }, componentId);
        
        console.log('\n=== Scale Transform Analysis ===');
        console.log(JSON.stringify(scaleInfo, null, 2));
        
        // Calculate the scale from the transform matrix
        if (scaleInfo.transforms.length > 0) {
            scaleInfo.transforms.forEach(t => {
                if (t.transform.startsWith('matrix(')) {
                    // matrix(a, b, c, d, tx, ty) - scale is sqrt(a^2 + b^2) or just a for uniform scale
                    const values = t.transform.match(/matrix\(([^)]+)\)/)?.[1].split(',').map(v => parseFloat(v.trim()));
                    if (values) {
                        const scaleX = Math.sqrt(values[0]**2 + values[1]**2);
                        console.log(`\nScale for ${t.className}: ${scaleX.toFixed(4)} (${(scaleX * 100).toFixed(1)}%)`);
                    }
                }
            });
        }
        
    } catch (error) {
        console.error('Error:', error.message);
        console.error('Stack:', error.stack);
    }
}

main().catch(console.error);
