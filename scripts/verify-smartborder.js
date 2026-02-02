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
        
        // Get detailed info about SmartBorder and resize handles
        const info = await page.evaluate((compId) => {
            // Find the SmartBorder wrapper (has data-component-id)
            const smartBorderEl = document.querySelector(`[data-component-id="${compId}"]`);
            const smartBorderRect = smartBorderEl?.getBoundingClientRect();
            
            // Find the outer wrapper (.group.touch-none.relative)
            const outerWrapper = smartBorderEl?.closest('.group.touch-none.relative');
            const outerRect = outerWrapper?.getBoundingClientRect();
            const outerStyle = outerWrapper?.getAttribute('style');
            
            // Find the SVG (SmartBorder path)
            const svg = smartBorderEl?.querySelector('svg');
            const svgRect = svg?.getBoundingClientRect();
            const pathD = smartBorderEl?.querySelector('path')?.getAttribute('d');
            
            // Find the content area
            const smartContent = smartBorderEl?.querySelector('[data-smart-content]');
            const contentRect = smartContent?.getBoundingClientRect();
            
            // Find resize handles
            const resizeHandles = outerWrapper?.querySelectorAll('[class*="resize"], [style*="cursor"][style*="resize"]');
            const handleRects = Array.from(resizeHandles || []).map(h => ({
                style: h.getAttribute('style')?.substring(0, 100),
                rect: h.getBoundingClientRect(),
            }));
            
            // Check for ResizeHandlesWrapper
            const resizeWrapper = outerWrapper?.querySelector('[style*="pointer-events: none"][style*="position: absolute"]');
            const resizeWrapperRect = resizeWrapper?.getBoundingClientRect();
            
            return {
                smartBorderClass: smartBorderEl?.className,
                smartBorderDimensions: smartBorderRect ? {
                    width: smartBorderRect.width,
                    height: smartBorderRect.height,
                } : null,
                outerWrapperDimensions: outerRect ? {
                    width: outerRect.width,
                    height: outerRect.height,
                } : null,
                outerStyle,
                svgDimensions: svgRect ? {
                    width: svgRect.width,
                    height: svgRect.height,
                } : null,
                pathD: pathD?.substring(0, 100) + '...',
                contentDimensions: contentRect ? {
                    width: contentRect.width,
                    height: contentRect.height,
                } : null,
                resizeWrapperDimensions: resizeWrapperRect ? {
                    width: resizeWrapperRect.width,
                    height: resizeWrapperRect.height,
                } : null,
                resizeHandlesCount: handleRects.length,
                widthComparison: {
                    outerWidth: Math.round(outerRect?.width || 0),
                    contentWidth: Math.round(contentRect?.width || 0),
                    match: Math.abs((outerRect?.width || 0) - (contentRect?.width || 0)) < 20,
                },
            };
        }, componentId);
        
        console.log('\n=== SmartBorder Verification ===');
        console.log(JSON.stringify(info, null, 2));
        
        if (info.widthComparison.match) {
            console.log('\n✅ SUCCESS: Outer wrapper width matches content width!');
            console.log(`   Outer: ${info.widthComparison.outerWidth}px, Content: ${info.widthComparison.contentWidth}px`);
        } else {
            console.log('\n⚠️ WARNING: Width mismatch detected');
            console.log(`   Outer: ${info.widthComparison.outerWidth}px, Content: ${info.widthComparison.contentWidth}px`);
            console.log('   This may cause resize handle misalignment');
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
