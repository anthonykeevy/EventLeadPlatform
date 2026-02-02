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
        
        // Get the SmartBorder path bounding box and resize handle positions
        const alignment = await page.evaluate((compId) => {
            const smartBorderEl = document.querySelector(`[data-component-id="${compId}"]`);
            const outerWrapper = smartBorderEl?.closest('.group.touch-none.relative');
            
            if (!smartBorderEl || !outerWrapper) {
                return { error: 'Elements not found' };
            }
            
            const outerRect = outerWrapper.getBoundingClientRect();
            
            // Get SmartBorder content area (the actual component content)
            const smartContent = smartBorderEl.querySelector('[data-smart-content]');
            const contentRect = smartContent?.getBoundingClientRect();
            
            // Get the SVG path's visual bounds
            const svgPath = smartBorderEl.querySelector('svg path');
            const pathBBox = svgPath?.getBBox?.();
            const svgRect = smartBorderEl.querySelector('svg')?.getBoundingClientRect();
            
            // Find all corner handles (8px x 8px elements with cursor styles)
            const handles = Array.from(outerWrapper.querySelectorAll('[style*="cursor"]'))
                .filter(el => el.getAttribute('style')?.includes('resize') || el.getAttribute('style')?.includes('cursor: pointer'))
                .map(el => {
                    const rect = el.getBoundingClientRect();
                    return {
                        position: el.getAttribute('style')?.match(/top:|bottom:|left:|right:/g)?.join(' '),
                        relativeToOuter: {
                            top: Math.round(rect.top - outerRect.top),
                            left: Math.round(rect.left - outerRect.left),
                            right: Math.round(rect.right - outerRect.left),
                            bottom: Math.round(rect.bottom - outerRect.top),
                        },
                    };
                });
            
            // Calculate where handles SHOULD be based on content
            const contentRelative = contentRect ? {
                top: Math.round(contentRect.top - outerRect.top),
                left: Math.round(contentRect.left - outerRect.left),
                right: Math.round(contentRect.right - outerRect.left),
                bottom: Math.round(contentRect.bottom - outerRect.top),
                width: Math.round(contentRect.width),
                height: Math.round(contentRect.height),
            } : null;
            
            return {
                outerDimensions: {
                    width: Math.round(outerRect.width),
                    height: Math.round(outerRect.height),
                },
                contentBounds: contentRelative,
                handlePositions: handles.slice(0, 12), // First 12 handles
                pathBBox: pathBBox ? {
                    x: Math.round(pathBBox.x),
                    y: Math.round(pathBBox.y),
                    width: Math.round(pathBBox.width),
                    height: Math.round(pathBBox.height),
                } : null,
                // Check alignment
                alignmentCheck: contentRelative ? {
                    topLeftHandleShouldBeAt: { x: 0, y: 0 },
                    topRightHandleShouldBeAt: { x: contentRelative.width, y: 0 },
                    bottomRightHandleShouldBeAt: { x: contentRelative.width, y: contentRelative.height },
                    bottomLeftHandleShouldBeAt: { x: 0, y: contentRelative.height },
                } : null,
            };
        }, componentId);
        
        console.log('\n=== Resize Handle Alignment Verification ===');
        console.log(JSON.stringify(alignment, null, 2));
        
        if (alignment.contentBounds && alignment.handlePositions) {
            console.log('\n--- Alignment Summary ---');
            const content = alignment.contentBounds;
            console.log(`Content: ${content.width}x${content.height} at (${content.left}, ${content.top})`);
            console.log(`Outer wrapper: ${alignment.outerDimensions.width}x${alignment.outerDimensions.height}`);
            
            if (content.width === alignment.outerDimensions.width) {
                console.log('\n✅ Content width matches outer wrapper width');
            } else {
                console.log(`\n⚠️ Width mismatch: Content=${content.width}px, Outer=${alignment.outerDimensions.width}px`);
            }
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error);
