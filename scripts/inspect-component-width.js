const puppeteer = require('puppeteer');

(async () => {
    try {
        const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
        const pages = await browser.pages();
        let page = pages.find(p => p.url().includes('localhost:3000'));
        
        if (!page) {
            page = await browser.newPage();
            await page.goto('http://localhost:3000/login');
        }
        
        // Login if needed
        if (page.url().includes('/login')) {
            await page.type('input[name="email"], input[type="email"]', 'user2@test.com');
            await page.type('input[name="password"], input[type="password"]', 'JChMom7KYLfL88&!');
            await page.click('button[type="submit"]');
            await page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 10000 });
        }
        
        // Navigate to form builder
        await page.goto('http://localhost:3000/forms/44/builder', { waitUntil: 'networkidle0' });
        await new Promise(r => setTimeout(r, 2000));
        
        // Click on target component
        const component = await page.$('[data-component-id="text-1768184324292-685"]');
        if (!component) {
            console.log('Component not found');
            return;
        }
        
        await component.click();
        await new Promise(r => setTimeout(r, 1000));
        
        // Get comprehensive measurements
        const measurements = await page.evaluate(() => {
            const compId = 'text-1768184324292-685';
            const el = document.querySelector(`[data-component-id="${compId}"]`);
            if (!el) return null;
            
            // Find all relevant elements
            const outerEl = el.querySelector('[style*="position: relative"]');
            const smartBorderEl = el.querySelector('[data-smart-border]');
            const svgPath = smartBorderEl?.querySelector('svg path');
            
            // Check for canvas scale
            const canvasEl = el.closest('[style*="transform"]') || document.querySelector('[data-canvas]') || document.querySelector('main');
            const canvasStyle = canvasEl ? window.getComputedStyle(canvasEl) : null;
            const canvasTransform = canvasStyle?.transform;
            
            // Parse transform scale if present
            let canvasScale = 1;
            if (canvasTransform && canvasTransform !== 'none') {
                const match = canvasTransform.match(/scale\(([\d.]+)\)/);
                if (match) {
                    canvasScale = parseFloat(match[1]);
                }
            }
            
            // Get component from store
            const store = JSON.parse(localStorage.getItem('builder-store') || '{}');
            const formDef = store.formDefinition || {};
            const pages = formDef.desktopPages || formDef.pages || [];
            const activePageId = store.activePageId;
            const activePage = pages.find(p => p.id === activePageId);
            const comp = activePage?.components?.find(c => c.id === compId);
            
            // Get canvas settings
            const canvasWidth = formDef?.canvasSettings?.width || 1920;
            const canvasHeight = formDef?.canvasSettings?.height || 980;
            const scale = store.scale || 1;
            
            return {
                componentProps: comp ? {
                    width: comp.props.width,
                    position: comp.position,
                    componentScale: comp.props.componentScale,
                } : null,
                canvasSettings: {
                    width: canvasWidth,
                    height: canvasHeight,
                    scale: scale,
                    canvasScale: canvasScale,
                },
                domMeasurements: {
                    outerElement: outerEl ? {
                        offsetWidth: outerEl.offsetWidth,
                        offsetHeight: outerEl.offsetHeight,
                        clientWidth: outerEl.clientWidth,
                        clientHeight: outerEl.clientHeight,
                        scrollWidth: outerEl.scrollWidth,
                        scrollHeight: outerEl.scrollHeight,
                        boundingRect: outerEl.getBoundingClientRect(),
                        computedStyle: {
                            width: window.getComputedStyle(outerEl).width,
                            height: window.getComputedStyle(outerEl).height,
                            transform: window.getComputedStyle(outerEl).transform,
                        },
                    } : null,
                    smartBorder: smartBorderEl ? {
                        offsetWidth: smartBorderEl.offsetWidth,
                        offsetHeight: smartBorderEl.offsetHeight,
                        boundingRect: smartBorderEl.getBoundingClientRect(),
                    } : null,
                    svgPath: svgPath ? {
                        bbox: svgPath.getBBox(),
                        viewBox: svgPath.ownerSVGElement?.viewBox?.baseVal,
                    } : null,
                    componentElement: {
                        offsetWidth: el.offsetWidth,
                        offsetHeight: el.offsetHeight,
                        boundingRect: el.getBoundingClientRect(),
                    },
                },
                parentChain: (() => {
                    const chain = [];
                    let current = el.parentElement;
                    let depth = 0;
                    while (current && depth < 5) {
                        const rect = current.getBoundingClientRect();
                        const style = window.getComputedStyle(current);
                        chain.push({
                            tag: current.tagName,
                            id: current.id,
                            className: current.className,
                            width: {
                                offset: current.offsetWidth,
                                client: current.clientWidth,
                                scroll: current.scrollWidth,
                                computed: style.width,
                                rect: rect.width,
                            },
                            transform: style.transform,
                            scale: style.transform.match(/scale\(([\d.]+)\)/)?.[1],
                        });
                        current = current.parentElement;
                        depth++;
                    }
                    return chain;
                })(),
            };
        });
        
        console.log('\n=== COMPONENT WIDTH ANALYSIS ===');
        console.log(JSON.stringify(measurements, null, 2));
        
        // Calculate what the width should be if it's 50%
        if (measurements?.componentProps?.width === '50%') {
            const canvasWidth = measurements.canvasSettings.width;
            const expected50Percent = canvasWidth * 0.5;
            console.log(`\n=== EXPECTED VALUES ===`);
            console.log(`Canvas width: ${canvasWidth}px`);
            console.log(`50% of canvas: ${expected50Percent}px`);
            console.log(`Actual DOM offsetWidth: ${measurements.domMeasurements.outerElement?.offsetWidth}px`);
            console.log(`Actual DOM boundingRect width: ${measurements.domMeasurements.outerElement?.boundingRect?.width}px`);
            
            // Check if there's a scale factor
            const canvasScale = measurements.canvasSettings.canvasScale;
            if (canvasScale !== 1) {
                console.log(`\nCanvas scale detected: ${canvasScale}`);
                console.log(`If offsetWidth is scaled, actual width = ${measurements.domMeasurements.outerElement?.offsetWidth / canvasScale}px`);
            }
        }
        
        console.log('\nTest complete!');
    } catch (error) {
        console.error('Error:', error.message);
        console.error(error.stack);
    }
})();
