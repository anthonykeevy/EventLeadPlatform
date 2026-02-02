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
        
        console.log('Current URL:', page.url());
        
        // Login if needed
        if (page.url().includes('/login')) {
            console.log('Logging in...');
            await page.type('input[name="email"], input[type="email"]', 'user2@test.com');
            await page.type('input[name="password"], input[type="password"]', 'JChMom7KYLfL88&!');
            await page.click('button[type="submit"]');
            await page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 10000 });
            console.log('Logged in, URL:', page.url());
        }
        
        // Navigate to form builder
        console.log('Navigating to form builder...');
        await page.goto('http://localhost:3000/forms/44/builder', { waitUntil: 'networkidle0' });
        
        // Check for console errors
        page.on('console', msg => {
            if (msg.type() === 'error') {
                console.log('Console error:', msg.text());
            }
        });
        
        page.on('pageerror', error => {
            console.log('Page error:', error.message);
        });
        
        // Wait for React to hydrate - check for common React/component markers
        console.log('Waiting for page to load...');
        await new Promise(r => setTimeout(r, 5000)); // Longer wait for React hydration
        
        // Check if page loaded successfully
        const pageTitle = await page.title();
        console.log('Page title:', pageTitle);
        
        // Wait for component to appear in DOM
        console.log('Waiting for component to appear...');
        try {
            await page.waitForSelector('[data-component-id]', { timeout: 15000 });
            console.log('Component found in DOM');
        } catch (e) {
            console.log('Warning: No components found with data-component-id attribute');
            // Check what's actually on the page
            const bodyText = await page.evaluate(() => document.body.innerText);
            console.log('Body text preview:', bodyText.substring(0, 200));
        }
        
        console.log('At form builder, URL:', page.url());
        
        // List all components in DOM
        const allComponents = await page.evaluate(() => {
            const components = document.querySelectorAll('[data-component-id]');
            return Array.from(components).map(el => ({
                id: el.getAttribute('data-component-id'),
                tagName: el.tagName,
                className: el.className,
            }));
        });
        console.log(`Found ${allComponents.length} components in DOM:`, allComponents);
        
        // Click on target component to select it
        const component = await page.$('[data-component-id="text-1768184324292-685"]');
        if (component) {
            await component.click();
            await new Promise(r => setTimeout(r, 500));
            console.log('Component selected');
        } else {
            console.log('Target component not found. Available component IDs:', allComponents.map(c => c.id));
        }
        
        // Wait a bit for page to fully load
        await new Promise(r => setTimeout(r, 2000));
        
        // Try to expose Zustand store to window
        await page.evaluate(() => {
            // Try to find and expose the builder store
            if (window.__REACT_DEVTOOLS_GLOBAL_HOOK__) {
                const hook = window.__REACT_DEVTOOLS_GLOBAL_HOOK__;
                // This is a hack to access React internals - may not work in production
            }
        });
        
        // Get comprehensive component information
        const componentInfo = await page.evaluate(() => {
            const compId = 'text-1768184324292-685';
            
            // Try multiple ways to get the store
            let store = null;
            let storeSource = 'none';
            
            // Method 1: window.useBuilderStore (Zustand) - most reliable
            if (window.useBuilderStore) {
                try {
                    store = window.useBuilderStore.getState();
                    storeSource = 'window.useBuilderStore';
                } catch (e) {
                    console.log('Failed to get window.useBuilderStore:', e);
                }
            }
            
            // Method 2: localStorage (may not be used by Zustand)
            if (!store) {
                const storeStr = localStorage.getItem('builder-store');
                if (storeStr) {
                    try {
                        store = JSON.parse(storeStr);
                        storeSource = 'localStorage';
                    } catch (e) {
                        console.log('Failed to parse localStorage store:', e);
                    }
                }
            }
            
            // Method 3: window.__ZUSTAND_STORES__
            if (!store && window.__ZUSTAND_STORES__) {
                try {
                    const builderStore = window.__ZUSTAND_STORES__.builder;
                    if (builderStore) {
                        store = builderStore.getState();
                        storeSource = 'window.__ZUSTAND_STORES__';
                    }
                } catch (e) {
                    console.log('Failed to get __ZUSTAND_STORES__:', e);
                }
            }
            
            if (!store) {
                // Try to find component in DOM and extract from data attributes
                const el = document.querySelector(`[data-component-id="${compId}"]`);
                if (!el) return { 
                    error: 'Component not found in DOM and store not available',
                    storeSource: storeSource,
                    availableGlobals: {
                        useBuilderStore: !!window.useBuilderStore,
                        localStorage: !!localStorage.getItem('builder-store'),
                        __ZUSTAND_STORES__: !!window.__ZUSTAND_STORES__,
                    }
                };
                
                // Return DOM-only info
                return {
                    error: 'Store not available, using DOM only',
                    domOnly: true,
                    storeSource: storeSource,
                    componentElement: {
                        offsetWidth: el.offsetWidth,
                        offsetHeight: el.offsetHeight,
                        boundingRect: el.getBoundingClientRect(),
                    },
                };
            }
            
            const formDef = store.formDefinition || {};
            const pages = formDef.desktopPages || formDef.pages || [];
            const activePageId = store.activePageId || store.activePage?.id;
            const activePage = pages.find(p => p.id === activePageId) || pages[0];
            
            // Try to find component recursively (including children)
            const findComponent = (components, id) => {
                for (const c of components || []) {
                    if (c.id === id) return c;
                    if (c.children) {
                        const found = findComponent(c.children, id);
                        if (found) return found;
                    }
                }
                return null;
            };
            
            const comp = findComponent(activePage?.components, compId);
            
            if (!comp) return { error: 'Component not found in store', activePageId, pagesCount: pages.length };
            
            // Get DOM elements
            const el = document.querySelector(`[data-component-id="${compId}"]`);
            const outerEl = el?.querySelector('[style*="position: relative"]');
            const smartBorderEl = el?.querySelector('[data-smart-border]');
            const svgPath = smartBorderEl?.querySelector('svg path');
            
            // Get canvas settings
            const canvasWidth = formDef?.canvasSettings?.width || 1920;
            const canvasHeight = formDef?.canvasSettings?.height || 980;
            const scale = store.scale || 1;
            
            // Calculate expected width if percentage
            let expectedWidth = null;
            if (comp.props.width?.endsWith('%')) {
                const pct = parseFloat(comp.props.width);
                expectedWidth = Math.round((canvasWidth * pct) / 100);
            }
            
            return {
                storeSource: storeSource,
                componentProps: {
                    width: comp.props.width,
                    position: comp.position,
                    componentScale: comp.props.componentScale,
                    objectLayout: comp.props.objectLayout,
                    inputWidthOverride: comp.props.inputWidthOverride,
                    labelWidthOverride: comp.props.labelWidthOverride,
                    helpWidthOverride: comp.props.helpWidthOverride,
                },
                canvasSettings: {
                    width: canvasWidth,
                    height: canvasHeight,
                    scale: scale,
                },
                expectedWidth: expectedWidth,
                domMeasurements: {
                    outerElement: outerEl ? {
                        offsetWidth: outerEl.offsetWidth,
                        offsetHeight: outerEl.offsetHeight,
                        clientWidth: outerEl.clientWidth,
                        clientHeight: outerEl.clientHeight,
                        boundingRect: outerEl.getBoundingClientRect(),
                        computedStyle: {
                            width: window.getComputedStyle(outerEl).width,
                            height: window.getComputedStyle(outerEl).height,
                        },
                    } : null,
                    smartBorder: smartBorderEl ? {
                        offsetWidth: smartBorderEl.offsetWidth,
                        offsetHeight: smartBorderEl.offsetHeight,
                        boundingRect: smartBorderEl.getBoundingClientRect(),
                    } : null,
                    svgPath: svgPath ? {
                        bbox: svgPath.getBBox(),
                    } : null,
                    componentElement: el ? {
                        offsetWidth: el.offsetWidth,
                        offsetHeight: el.offsetHeight,
                        boundingRect: el.getBoundingClientRect(),
                    } : null,
                },
                resizeHandles: (() => {
                    const handles = document.querySelectorAll('.resize-handle');
                    return Array.from(handles).map((h, i) => ({
                        index: i,
                        position: h.getAttribute('data-position'),
                        boundingRect: h.getBoundingClientRect(),
                        computedStyle: {
                            cursor: window.getComputedStyle(h).cursor,
                            pointerEvents: window.getComputedStyle(h).pointerEvents,
                        },
                    }));
                })(),
            };
        });
        
        console.log('\n=== COMPONENT INSPECTION ===');
        console.log(JSON.stringify(componentInfo, null, 2));
        
        // Analysis
        if (componentInfo.componentProps?.width?.endsWith('%')) {
            console.log('\n=== ANALYSIS ===');
            console.log(`Component width prop: ${componentInfo.componentProps.width}`);
            console.log(`Canvas width: ${componentInfo.canvasSettings.width}px`);
            console.log(`Expected width (calculated): ${componentInfo.expectedWidth}px`);
            console.log(`Actual DOM offsetWidth: ${componentInfo.domMeasurements.outerElement?.offsetWidth}px`);
            console.log(`Actual DOM boundingRect width: ${componentInfo.domMeasurements.outerElement?.boundingRect?.width}px`);
            
            if (componentInfo.expectedWidth) {
                const diff = componentInfo.domMeasurements.outerElement?.offsetWidth - componentInfo.expectedWidth;
                console.log(`\nDifference: ${diff}px (DOM is ${diff > 0 ? 'larger' : 'smaller'} than expected)`);
                
                if (Math.abs(diff) > 50) {
                    console.log(`⚠️ WARNING: Large discrepancy detected!`);
                    console.log(`   This suggests the DOM measurement is incorrect or the component is expanded.`);
                }
            }
        }
        
        console.log('\n=== RESIZE HANDLES ===');
        if (componentInfo.resizeHandles && Array.isArray(componentInfo.resizeHandles)) {
            componentInfo.resizeHandles.forEach((h, i) => {
                console.log(`Handle ${i + 1} (${h.position}):`);
                console.log(`  Position: ${h.boundingRect.x}, ${h.boundingRect.y}`);
                console.log(`  Size: ${h.boundingRect.width}x${h.boundingRect.height}`);
                console.log(`  Cursor: ${h.computedStyle.cursor}`);
                console.log(`  Pointer Events: ${h.computedStyle.pointerEvents}`);
            });
        } else {
            console.log('No resize handles found or componentInfo.resizeHandles is not an array');
        }
        
        console.log('\nInspection complete!');
    } catch (error) {
        console.error('Error:', error.message);
        console.error(error.stack);
    }
})();
