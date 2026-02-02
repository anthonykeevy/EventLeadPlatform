const puppeteer = require('puppeteer');

async function main() {
    try {
        const browser = await puppeteer.connect({
            browserURL: 'http://127.0.0.1:9222',
            defaultViewport: null
        });
        
        const pages = await browser.pages();
        let page = pages.find(p => p.url().includes('localhost:3000'));
        
        const componentId = 'text-1768184324292-685';
        
        const scaleInfo = await page.evaluate((compId) => {
            // Find the canvas with scale transform
            const stageEl = document.querySelector('[style*="transform: scale"]');
            const stageStyle = stageEl?.getAttribute('style');
            
            // Extract scale value
            const scaleMatch = stageStyle?.match(/scale\(([\d.]+)\)/);
            const scale = scaleMatch ? parseFloat(scaleMatch[1]) : 1;
            
            // Get outer wrapper dimensions
            const smartBorderEl = document.querySelector(`[data-component-id="${compId}"]`);
            const outerWrapper = smartBorderEl?.closest('.group.touch-none.relative');
            const outerRect = outerWrapper?.getBoundingClientRect();
            const outerStyle = outerWrapper?.getAttribute('style');
            
            // Get ResizeHandlesWrapper
            const resizeWrapper = outerWrapper?.querySelector('[style*="position: absolute"][style*="pointer-events: none"]:not([style*="z-index"])');
            const resizeRect = resizeWrapper?.getBoundingClientRect();
            const resizeStyle = resizeWrapper?.getAttribute('style');
            
            // Calculate expected width after scale
            const resizeWidthMatch = resizeStyle?.match(/width:\s*([\d.]+)px/);
            const styledWidth = resizeWidthMatch ? parseFloat(resizeWidthMatch[1]) : null;
            const expectedRenderedWidth = styledWidth ? styledWidth * scale : null;
            
            return {
                scale,
                outerWrapper: {
                    styleWidth: outerStyle?.match(/width:\s*([\d.]+)px/)?.[1] || 'not set',
                    renderedWidth: outerRect ? Math.round(outerRect.width) : null,
                },
                resizeWrapper: {
                    styledWidth,
                    renderedWidth: resizeRect ? Math.round(resizeRect.width) : null,
                    expectedRenderedWidth: expectedRenderedWidth ? Math.round(expectedRenderedWidth) : null,
                },
                calculation: {
                    actualToExpectedRatio: (resizeRect?.width && expectedRenderedWidth) 
                        ? (resizeRect.width / expectedRenderedWidth).toFixed(3) 
                        : null,
                    renderedToStyleRatio: (resizeRect?.width && styledWidth)
                        ? (resizeRect.width / styledWidth).toFixed(3)
                        : null,
                }
            };
        }, componentId);
        
        console.log('\n=== Scale Verification ===');
        console.log(JSON.stringify(scaleInfo, null, 2));
        
        if (scaleInfo.calculation.renderedToStyleRatio) {
            const ratio = parseFloat(scaleInfo.calculation.renderedToStyleRatio);
            if (Math.abs(ratio - scaleInfo.scale) < 0.05) {
                console.log(`\n✅ Rendered/Style ratio (${ratio}) matches canvas scale (${scaleInfo.scale})`);
            } else {
                console.log(`\n⚠️ Rendered/Style ratio (${ratio}) does NOT match canvas scale (${scaleInfo.scale})`);
            }
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error);
