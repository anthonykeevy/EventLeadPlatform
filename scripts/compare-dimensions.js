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
        
        // Compare SmartBorder vs outer wrapper dimensions
        const dimensions = await page.evaluate((compId) => {
            // Find the SmartBorder wrapper (has data-component-id inside the outer)
            const smartBorderEls = document.querySelectorAll(`[data-component-id="${compId}"]`);
            
            // There might be two elements with this ID - outer wrapper and SmartBorder
            const elements = Array.from(smartBorderEls).map(el => {
                const rect = el.getBoundingClientRect();
                const isSmartBorder = el.querySelector('svg path') !== null;
                const hasDataSmartContent = el.querySelector('[data-smart-content]') !== null;
                return {
                    tagName: el.tagName,
                    className: el.className?.substring?.(0, 60),
                    isSmartBorder,
                    hasDataSmartContent,
                    rect: {
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        top: Math.round(rect.top),
                        left: Math.round(rect.left),
                    }
                };
            });
            
            // Get outer wrapper
            const outerWrapper = document.querySelector(`[data-component-id="${compId}"]`)?.closest('.group.touch-none.relative');
            const outerRect = outerWrapper?.getBoundingClientRect();
            
            // Get SmartBorder specifically (has the SVG path)
            const smartBorder = outerWrapper?.querySelector('.relative.inline-block.group, .relative.block.w-full.group');
            const smartBorderRect = smartBorder?.getBoundingClientRect();
            
            // Get the ResizeHandlesWrapper
            const resizeWrapper = outerWrapper?.querySelector('[style*="position: absolute"][style*="pointer-events: none"][style*="width:"]');
            const resizeStyle = resizeWrapper?.getAttribute('style');
            const resizeRect = resizeWrapper?.getBoundingClientRect();
            
            // Parse width from style
            const widthMatch = resizeStyle?.match(/width:\s*([\d.]+)px/);
            const heightMatch = resizeStyle?.match(/height:\s*([\d.]+)px/);
            
            return {
                elements,
                outerWrapper: outerRect ? {
                    width: Math.round(outerRect.width),
                    height: Math.round(outerRect.height),
                } : null,
                smartBorder: smartBorderRect ? {
                    width: Math.round(smartBorderRect.width),
                    height: Math.round(smartBorderRect.height),
                    className: smartBorder.className,
                } : null,
                resizeWrapper: {
                    styleWidth: widthMatch ? parseFloat(widthMatch[1]) : null,
                    styleHeight: heightMatch ? parseFloat(heightMatch[1]) : null,
                    renderedWidth: resizeRect ? Math.round(resizeRect.width) : null,
                    renderedHeight: resizeRect ? Math.round(resizeRect.height) : null,
                    fullStyle: resizeStyle?.substring(0, 200),
                },
                comparison: {
                    outerWidth: outerRect ? Math.round(outerRect.width) : null,
                    smartBorderWidth: smartBorderRect ? Math.round(smartBorderRect.width) : null,
                    match: outerRect && smartBorderRect ? 
                        Math.abs(outerRect.width - smartBorderRect.width) < 5 : null,
                }
            };
        }, componentId);
        
        console.log('\n=== Dimension Comparison ===');
        console.log(JSON.stringify(dimensions, null, 2));
        
        if (dimensions.comparison) {
            console.log('\n--- Comparison Result ---');
            console.log(`Outer wrapper: ${dimensions.comparison.outerWidth}px`);
            console.log(`SmartBorder: ${dimensions.comparison.smartBorderWidth}px`);
            console.log(`Match: ${dimensions.comparison.match ? '✅ Yes' : '❌ No'}`);
            
            if (dimensions.resizeWrapper.styleWidth) {
                console.log(`\nResizeWrapper style width: ${dimensions.resizeWrapper.styleWidth}px`);
                console.log(`ResizeWrapper rendered width: ${dimensions.resizeWrapper.renderedWidth}px`);
            }
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error);
