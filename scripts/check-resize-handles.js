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
        
        // Get resize handles info
        const info = await page.evaluate((compId) => {
            // Find the outer wrapper
            const smartBorderEl = document.querySelector(`[data-component-id="${compId}"]`);
            const outerWrapper = smartBorderEl?.closest('.group.touch-none.relative');
            const outerRect = outerWrapper?.getBoundingClientRect();
            
            if (!outerWrapper || !outerRect) {
                return { error: 'Outer wrapper not found' };
            }
            
            // Find ALL absolutely positioned children that look like resize handles
            const allAbsolute = Array.from(outerWrapper.querySelectorAll('[style*="position: absolute"]'));
            
            const handles = allAbsolute.map((el, i) => {
                const rect = el.getBoundingClientRect();
                const style = el.getAttribute('style');
                const isHandle = style?.includes('cursor') && (
                    style.includes('nwse-resize') || 
                    style.includes('nesw-resize') || 
                    style.includes('ew-resize') || 
                    style.includes('ns-resize') || 
                    style.includes('pointer')
                );
                return {
                    index: i,
                    isHandle,
                    tagName: el.tagName,
                    className: el.className?.substring?.(0, 50) || el.className,
                    rect: {
                        top: Math.round(rect.top - outerRect.top),
                        left: Math.round(rect.left - outerRect.left),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        right: Math.round(rect.right - outerRect.left),
                        bottom: Math.round(rect.bottom - outerRect.top),
                    },
                    styleSnippet: style?.substring(0, 100),
                };
            });
            
            // Get the SmartBorder SVG path bounding box
            const svg = outerWrapper.querySelector('svg');
            const svgRect = svg?.getBoundingClientRect();
            const path = svg?.querySelector('path');
            const pathBox = path?.getBBox?.();
            
            return {
                outerWrapper: {
                    width: Math.round(outerRect.width),
                    height: Math.round(outerRect.height),
                },
                svgPosition: svgRect ? {
                    left: Math.round(svgRect.left - outerRect.left),
                    top: Math.round(svgRect.top - outerRect.top),
                    width: Math.round(svgRect.width),
                    height: Math.round(svgRect.height),
                } : null,
                pathBBox: pathBox ? {
                    x: Math.round(pathBox.x),
                    y: Math.round(pathBox.y),
                    width: Math.round(pathBox.width),
                    height: Math.round(pathBox.height),
                } : null,
                allAbsoluteElements: handles.filter(h => h.isHandle || h.tagName === 'DIV'),
            };
        }, componentId);
        
        console.log('\n=== Resize Handles Check ===');
        console.log(JSON.stringify(info, null, 2));
        
        if (info.allAbsoluteElements) {
            console.log('\n--- Element Analysis ---');
            info.allAbsoluteElements.forEach(el => {
                if (el.isHandle) {
                    console.log(`Handle at (${el.rect.left}, ${el.rect.top}) - ${el.rect.width}x${el.rect.height}px`);
                }
            });
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
