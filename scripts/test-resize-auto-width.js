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
        await new Promise(r => setTimeout(r, 2000));
        console.log('At form builder');
        
        // Click on target component
        const component = await page.$('[data-component-id="text-1768184324292-685"]');
        if (!component) {
            console.log('Component not found');
            return;
        }
        
        await component.click();
        console.log('Component selected');
        await new Promise(r => setTimeout(r, 1000));
        
        // Get component state BEFORE resize
        const beforeState = await page.evaluate(() => {
            const store = JSON.parse(localStorage.getItem('builder-store') || '{}');
            const formDef = store.formDefinition || {};
            const pages = formDef.desktopPages || formDef.pages || [];
            const activePageId = store.activePageId;
            const activePage = pages.find(p => p.id === activePageId);
            const comp = activePage?.components?.find(c => c.id === 'text-1768184324292-685');
            
            if (!comp) return null;
            
            const el = document.querySelector('[data-component-id="text-1768184324292-685"]');
            const outerEl = el?.querySelector('[style*="position: relative"]');
            const smartBorderEl = el?.querySelector('[data-smart-border]');
            const svgPath = smartBorderEl?.querySelector('svg path');
            
            return {
                component: {
                    id: comp.id,
                    type: comp.type,
                    position: comp.position,
                    width: comp.props.width,
                    componentScale: comp.props.componentScale,
                    objectLayout: comp.props.objectLayout,
                    inputWidthOverride: comp.props.inputWidthOverride,
                    labelWidthOverride: comp.props.labelWidthOverride,
                    helpWidthOverride: comp.props.helpWidthOverride,
                },
                dom: {
                    outerWidth: outerEl?.offsetWidth,
                    outerHeight: outerEl?.offsetHeight,
                    outerRect: outerEl ? {
                        x: outerEl.getBoundingClientRect().x,
                        y: outerEl.getBoundingClientRect().y,
                        width: outerEl.getBoundingClientRect().width,
                        height: outerEl.getBoundingClientRect().height,
                    } : null,
                    smartBorderPath: svgPath ? {
                        bbox: svgPath.getBBox(),
                    } : null,
                },
            };
        });
        
        console.log('\n=== BEFORE RESIZE ===');
        console.log('Component Props:', JSON.stringify(beforeState?.component, null, 2));
        console.log('DOM Measurements:', JSON.stringify(beforeState?.dom, null, 2));
        
        // Find the right resize handle (E handle)
        const eHandle = await page.evaluateHandle(() => {
            const handles = document.querySelectorAll('[style*="cursor: ew-resize"]');
            // Find the rightmost handle (E handle)
            let rightmost = null;
            let maxX = -Infinity;
            handles.forEach(h => {
                const rect = h.getBoundingClientRect();
                if (rect.x > maxX) {
                    maxX = rect.x;
                    rightmost = h;
                }
            });
            return rightmost;
        });
        
        if (!eHandle || eHandle.asElement() === null) {
            console.log('E resize handle not found');
            return;
        }
        
        const handleBox = await eHandle.asElement().boundingBox();
        console.log('\n=== RESIZE HANDLE POSITION ===');
        console.log('Handle position:', handleBox);
        
        // Get handle center
        const handleCenterX = handleBox.x + handleBox.width / 2;
        const handleCenterY = handleBox.y + handleBox.height / 2;
        
        // Move mouse to handle and start drag
        console.log('\n=== STARTING RESIZE ===');
        await page.mouse.move(handleCenterX, handleCenterY);
        await new Promise(r => setTimeout(r, 200));
        await page.mouse.down();
        await new Promise(r => setTimeout(r, 100));
        
        // Drag right by 50px
        console.log('Dragging right by 50px...');
        await page.mouse.move(handleCenterX + 50, handleCenterY, { steps: 10 });
        await new Promise(r => setTimeout(r, 500));
        
        // Get state DURING resize (preview)
        const duringState = await page.evaluate(() => {
            const store = JSON.parse(localStorage.getItem('builder-store') || '{}');
            const formDef = store.formDefinition || {};
            const pages = formDef.desktopPages || formDef.pages || [];
            const activePageId = store.activePageId;
            const activePage = pages.find(p => p.id === activePageId);
            const comp = activePage?.components?.find(c => c.id === 'text-1768184324292-685');
            
            const el = document.querySelector('[data-component-id="text-1768184324292-685"]');
            const outerEl = el?.querySelector('[style*="position: relative"]');
            
            return {
                component: comp ? {
                    width: comp.props.width,
                    position: comp.position,
                } : null,
                dom: outerEl ? {
                    width: outerEl.offsetWidth,
                    rect: outerEl.getBoundingClientRect(),
                } : null,
            };
        });
        
        console.log('\n=== DURING RESIZE (PREVIEW) ===');
        console.log('Component Props:', JSON.stringify(duringState?.component, null, 2));
        console.log('DOM Measurements:', JSON.stringify(duringState?.dom, null, 2));
        
        // Release mouse (commit resize)
        console.log('\n=== COMMITTING RESIZE ===');
        await page.mouse.up();
        await new Promise(r => setTimeout(r, 1000));
        
        // Get state AFTER resize
        const afterState = await page.evaluate(() => {
            const store = JSON.parse(localStorage.getItem('builder-store') || '{}');
            const formDef = store.formDefinition || {};
            const pages = formDef.desktopPages || formDef.pages || [];
            const activePageId = store.activePageId;
            const activePage = pages.find(p => p.id === activePageId);
            const comp = activePage?.components?.find(c => c.id === 'text-1768184324292-685');
            
            const el = document.querySelector('[data-component-id="text-1768184324292-685"]');
            const outerEl = el?.querySelector('[style*="position: relative"]');
            const smartBorderEl = el?.querySelector('[data-smart-border]');
            const svgPath = smartBorderEl?.querySelector('svg path');
            
            return {
                component: comp ? {
                    id: comp.id,
                    width: comp.props.width,
                    position: comp.position,
                    componentScale: comp.props.componentScale,
                    inputWidthOverride: comp.props.inputWidthOverride,
                    labelWidthOverride: comp.props.labelWidthOverride,
                    helpWidthOverride: comp.props.helpWidthOverride,
                } : null,
                dom: outerEl ? {
                    width: outerEl.offsetWidth,
                    height: outerEl.offsetHeight,
                    rect: outerEl.getBoundingClientRect(),
                } : null,
                smartBorderPath: svgPath ? {
                    bbox: svgPath.getBBox(),
                } : null,
            };
        });
        
        console.log('\n=== AFTER RESIZE (COMMITTED) ===');
        console.log('Component Props:', JSON.stringify(afterState?.component, null, 2));
        console.log('DOM Measurements:', JSON.stringify(afterState?.dom, null, 2));
        console.log('SmartBorder Path:', JSON.stringify(afterState?.smartBorderPath, null, 2));
        
        // Calculate changes
        console.log('\n=== CHANGES SUMMARY ===');
        if (beforeState && afterState) {
            const widthChange = {
                props: {
                    before: beforeState.component.width,
                    after: afterState.component.width,
                },
                dom: {
                    before: beforeState.dom.outerWidth,
                    after: afterState.dom.outerWidth,
                    delta: afterState.dom.outerWidth - beforeState.dom.outerWidth,
                },
            };
            const positionChange = {
                x: {
                    before: beforeState.component.position.x,
                    after: afterState.component.position.x,
                    delta: afterState.component.position.x - beforeState.component.position.x,
                },
                y: {
                    before: beforeState.component.position.y,
                    after: afterState.component.position.y,
                    delta: afterState.component.position.y - beforeState.component.position.y,
                },
            };
            
            console.log('Width Changes:', JSON.stringify(widthChange, null, 2));
            console.log('Position Changes:', JSON.stringify(positionChange, null, 2));
        }
        
        console.log('\nTest complete!');
    } catch (error) {
        console.error('Error:', error.message);
        console.error(error.stack);
    }
})();
