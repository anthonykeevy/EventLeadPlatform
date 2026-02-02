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
            await new Promise(r => setTimeout(r, 1000));
        }
        
        // Check parent chain of ResizeHandlesWrapper
        const info = await page.evaluate((compId) => {
            // Find the outer wrapper
            const smartBorderEl = document.querySelector(`[data-component-id="${compId}"]`);
            const outerWrapper = smartBorderEl?.closest('.group.touch-none.relative');
            
            if (!outerWrapper) {
                return { error: 'Outer wrapper not found' };
            }
            
            // Find the ResizeHandlesWrapper - it should have pointer-events: none and position: absolute
            // with width matching the SmartBorder
            const absoluteChildren = Array.from(outerWrapper.querySelectorAll(':scope > [style*="position: absolute"]'));
            
            const resizeWrapper = absoluteChildren.find(el => {
                const style = el.getAttribute('style');
                return style?.includes('pointer-events: none') && 
                       style?.includes('width:') && 
                       !style?.includes('z-index: 0'); // exclude overlays
            });
            
            if (!resizeWrapper) {
                return { 
                    error: 'ResizeHandlesWrapper not found',
                    absoluteChildren: absoluteChildren.map(el => ({
                        tag: el.tagName,
                        style: el.getAttribute('style')?.substring(0, 100),
                        rect: el.getBoundingClientRect(),
                    })),
                };
            }
            
            const resizeRect = resizeWrapper.getBoundingClientRect();
            const outerRect = outerWrapper.getBoundingClientRect();
            const resizeStyle = resizeWrapper.getAttribute('style');
            const computedStyle = window.getComputedStyle(resizeWrapper);
            
            // Check if there's any clipping
            let parent = resizeWrapper.parentElement;
            const parentChain = [];
            while (parent && parent !== document.body) {
                const ps = window.getComputedStyle(parent);
                parentChain.push({
                    tag: parent.tagName,
                    className: parent.className?.substring?.(0, 50),
                    overflow: ps.overflow,
                    overflowX: ps.overflowX,
                    width: parent.getBoundingClientRect().width,
                    position: ps.position,
                    display: ps.display,
                });
                parent = parent.parentElement;
            }
            
            return {
                resizeWrapper: {
                    inlineStyle: resizeStyle,
                    computedWidth: computedStyle.width,
                    computedHeight: computedStyle.height,
                    rectWidth: resizeRect.width,
                    rectHeight: resizeRect.height,
                },
                outerWrapper: {
                    rectWidth: outerRect.width,
                    rectHeight: outerRect.height,
                },
                parentChain: parentChain.slice(0, 5), // First 5 parents
            };
        }, componentId);
        
        console.log('\n=== Parent Chain Analysis ===');
        console.log(JSON.stringify(info, null, 2));
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
