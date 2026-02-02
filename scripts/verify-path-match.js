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
        
        // Click on the component
        const componentEl = await page.$(`[data-component-id="${componentId}"]`);
        if (componentEl) {
            await componentEl.click();
            await new Promise(r => setTimeout(r, 1000));
        }
        
        const matchInfo = await page.evaluate((compId) => {
            const smartBorderEl = document.querySelector(`[data-component-id="${compId}"]`);
            const outerWrapper = smartBorderEl?.closest('.group.touch-none.relative');
            
            if (!outerWrapper || !smartBorderEl) {
                return { error: 'Elements not found' };
            }
            
            // Get the SVG path's bounding box
            const svgPath = smartBorderEl.querySelector('svg path');
            const pathBBox = svgPath?.getBBox?.();
            
            // Get the ResizeHandlesWrapper dimensions
            const resizeWrapper = outerWrapper.querySelector('[style*="position: absolute"][style*="pointer-events: none"]:not([style*="z-index"])');
            const resizeStyle = resizeWrapper?.getAttribute('style');
            const widthMatch = resizeStyle?.match(/width:\s*([\d.]+)px/);
            const heightMatch = resizeStyle?.match(/height:\s*([\d.]+)px/);
            
            const resizeWidth = widthMatch ? parseFloat(widthMatch[1]) : null;
            const resizeHeight = heightMatch ? parseFloat(heightMatch[1]) : null;
            
            // Compare
            const widthDiff = pathBBox && resizeWidth ? Math.abs(pathBBox.width - resizeWidth) : null;
            const heightDiff = pathBBox && resizeHeight ? Math.abs(pathBBox.height - resizeHeight) : null;
            
            return {
                pathBBox: pathBBox ? {
                    x: Math.round(pathBBox.x),
                    y: Math.round(pathBBox.y),
                    width: Math.round(pathBBox.width),
                    height: Math.round(pathBBox.height),
                } : null,
                resizeWrapper: {
                    width: resizeWidth ? Math.round(resizeWidth) : null,
                    height: resizeHeight ? Math.round(resizeHeight) : null,
                },
                match: {
                    widthDiff: widthDiff ? Math.round(widthDiff) : null,
                    heightDiff: heightDiff ? Math.round(heightDiff) : null,
                    widthMatches: widthDiff !== null && widthDiff < 5,
                    heightMatches: heightDiff !== null && heightDiff < 5,
                }
            };
        }, componentId);
        
        console.log('\n=== Path vs ResizeWrapper Match ===');
        console.log(JSON.stringify(matchInfo, null, 2));
        
        if (matchInfo.match) {
            if (matchInfo.match.widthMatches && matchInfo.match.heightMatches) {
                console.log('\n✅ SUCCESS: Resize handles now match SVG path bounds!');
            } else {
                console.log('\n⚠️ Dimensions still differ:');
                console.log(`   Width diff: ${matchInfo.match.widthDiff}px`);
                console.log(`   Height diff: ${matchInfo.match.heightDiff}px`);
            }
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error);
