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
        
        // Find the ResizeHandlesWrapper (should have pointer-events: none but NO z-index)
        const wrapperInfo = await page.evaluate((compId) => {
            const outerWrapper = document.querySelector(`[data-component-id="${compId}"]`)?.closest('.group.touch-none.relative');
            
            if (!outerWrapper) {
                return { error: 'Outer wrapper not found' };
            }
            
            const outerRect = outerWrapper.getBoundingClientRect();
            
            // Find all direct children with position: absolute and pointer-events: none
            const absoluteChildren = Array.from(outerWrapper.querySelectorAll(':scope > [style*="position: absolute"]'));
            
            const wrappers = absoluteChildren.map((el, i) => {
                const style = el.getAttribute('style');
                const rect = el.getBoundingClientRect();
                const hasZIndex = style?.includes('z-index');
                const children = el.children.length;
                const hasResizeHandles = el.querySelectorAll('[style*="cursor"][style*="resize"]').length > 0;
                
                // Parse dimensions from style
                const widthMatch = style?.match(/width:\s*([\d.]+)px/);
                const heightMatch = style?.match(/height:\s*([\d.]+)px/);
                const leftMatch = style?.match(/left:\s*([\d.]+)px/);
                const topMatch = style?.match(/top:\s*([\d.]+)px/);
                
                return {
                    index: i,
                    hasZIndex,
                    hasResizeHandles,
                    childCount: children,
                    style: {
                        width: widthMatch ? parseFloat(widthMatch[1]) : null,
                        height: heightMatch ? parseFloat(heightMatch[1]) : null,
                        left: leftMatch ? parseFloat(leftMatch[1]) : null,
                        top: topMatch ? parseFloat(topMatch[1]) : null,
                    },
                    rect: {
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        relativeLeft: Math.round(rect.left - outerRect.left),
                        relativeTop: Math.round(rect.top - outerRect.top),
                    },
                    fullStyle: style?.substring(0, 150),
                };
            });
            
            // The ResizeHandlesWrapper should:
            // - Have pointer-events: none
            // - NOT have z-index
            // - Have resize handle children
            const resizeHandlesWrapper = wrappers.find(w => !w.hasZIndex && w.hasResizeHandles);
            const inputResizeWrapper = wrappers.find(w => w.hasZIndex && w.style.left > 50);
            
            return {
                outerDimensions: {
                    width: Math.round(outerRect.width),
                    height: Math.round(outerRect.height),
                },
                allWrappers: wrappers,
                resizeHandlesWrapper,
                inputResizeWrapper,
                analysis: resizeHandlesWrapper ? {
                    styleMatchesOuter: 
                        Math.abs(resizeHandlesWrapper.style.width - outerRect.width) < 5 &&
                        Math.abs(resizeHandlesWrapper.style.height - outerRect.height) < 5,
                    styleWidth: resizeHandlesWrapper.style.width,
                    outerWidth: Math.round(outerRect.width),
                } : null,
            };
        }, componentId);
        
        console.log('\n=== ResizeHandlesWrapper Analysis ===');
        console.log(JSON.stringify(wrapperInfo, null, 2));
        
        if (wrapperInfo.resizeHandlesWrapper) {
            const wrapper = wrapperInfo.resizeHandlesWrapper;
            const outer = wrapperInfo.outerDimensions;
            console.log('\n--- ResizeHandlesWrapper Found ---');
            console.log(`Style dimensions: ${wrapper.style.width}x${wrapper.style.height}`);
            console.log(`Outer dimensions: ${outer.width}x${outer.height}`);
            console.log(`Match: ${wrapperInfo.analysis?.styleMatchesOuter ? '✅ Yes' : '❌ No'}`);
        } else {
            console.log('\n❌ ResizeHandlesWrapper not found!');
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error);
