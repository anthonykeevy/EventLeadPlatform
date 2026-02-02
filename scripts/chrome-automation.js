const puppeteer = require('puppeteer');

async function main() {
    try {
        // Connect to existing Chrome instance
        const browser = await puppeteer.connect({
            browserURL: 'http://127.0.0.1:9222',
            defaultViewport: null
        });
        
        console.log('Connected to Chrome!');
        
        // Set up console listener early
        const consoleLogs = [];
        
        // Get all pages
        const pages = await browser.pages();
        console.log(`Found ${pages.length} pages`);
        
        // Find or create a page for our app
        let page = pages.find(p => p.url().includes('localhost:3000'));
        
        if (!page) {
            console.log('Creating new page...');
            page = await browser.newPage();
            await page.goto('http://localhost:3000/login', { waitUntil: 'networkidle2' });
        }
        
        console.log('Current URL:', page.url());
        
        // Check if we're on login page
        if (page.url().includes('/login')) {
            console.log('On login page, attempting login...');
            
            // Wait for form
            await page.waitForSelector('input[type="email"], input[name="email"], input[placeholder*="email" i]', { timeout: 5000 });
            
            // Find email input
            const emailInput = await page.$('input[type="email"], input[name="email"], input[placeholder*="email" i]');
            if (emailInput) {
                await emailInput.click({ clickCount: 3 });
                await emailInput.type('user2@test.com');
                console.log('Entered email');
            }
            
            // Find password input
            const passwordInput = await page.$('input[type="password"]');
            if (passwordInput) {
                await passwordInput.click({ clickCount: 3 });
                await passwordInput.type('JChMom7KYLfL88&!');
                console.log('Entered password');
            }
            
            // Find and click submit button
            const submitButton = await page.$('button[type="submit"]');
            if (submitButton) {
                await submitButton.click();
                console.log('Clicked login button');
                await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 10000 }).catch(() => {});
            } else {
                // Try finding button by text content
                await page.evaluate(() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const loginBtn = buttons.find(b => b.textContent?.toLowerCase().includes('login') || b.textContent?.toLowerCase().includes('sign in'));
                    if (loginBtn) loginBtn.click();
                });
                console.log('Clicked login button via text search');
                await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 10000 }).catch(() => {});
            }
        }
        
        console.log('After login URL:', page.url());
        
        // Navigate to form builder
        if (!page.url().includes('/forms/44/builder')) {
            console.log('Navigating to form builder...');
            await page.goto('http://localhost:3000/forms/44/builder', { waitUntil: 'networkidle2' });
        }
        
        console.log('Final URL:', page.url());
        
        // Wait for the canvas to load
        await page.waitForSelector('[data-component-id]', { timeout: 10000 }).catch(() => console.log('No components found yet'));
        
        // Set up console listener
        page.on('console', msg => {
            const text = msg.text();
            if (text.includes('component.width') || text.includes('hasExplicit') || text.includes('smartBorderLayout')) {
                consoleLogs.push(text);
                console.log('Console:', text);
            }
        });
        
        // Click on the component to select it and trigger debug logging
        const componentId = 'text-1768184324292-685';
        const componentEl = await page.$(`[data-component-id="${componentId}"]`);
        if (componentEl) {
            await componentEl.click();
            console.log('Clicked on component to select it');
            await new Promise(r => setTimeout(r, 1000)); // Wait for selection and re-render
        }
        
        // Get form definition from localStorage
        const formData = await page.evaluate((compId) => {
            const formDefJson = localStorage.getItem('builder-formDefinition-44');
            if (!formDefJson) return { error: 'Form definition not found in localStorage' };
            
            try {
                const formDef = JSON.parse(formDefJson);
                
                // Find the component
                const pages = formDef.pages || formDef.desktopPages || [];
                let comp = null;
                
                for (const page of pages) {
                    if (page.components) {
                        comp = page.components.find(c => c.id === compId);
                        if (comp) break;
                        
                        // Check children recursively
                        const findInChildren = (comps) => {
                            for (const c of comps) {
                                if (c.id === compId) return c;
                                if (c.children) {
                                    const found = findInChildren(c.children);
                                    if (found) return found;
                                }
                            }
                            return null;
                        };
                        comp = findInChildren(page.components);
                        if (comp) break;
                    }
                }
                
                if (!comp) {
                    return { 
                        error: 'Component not found in form definition',
                        pagesCount: pages.length,
                        componentIds: pages[0]?.components?.map(c => c.id).slice(0, 10)
                    };
                }
                
                return {
                    found: true,
                    componentId: comp.id,
                    type: comp.type,
                    props: {
                        width: comp.props.width,
                        widthType: typeof comp.props.width,
                        widthValue: JSON.stringify(comp.props.width),
                        inputWidthOverride: comp.props.inputWidthOverride,
                        labelWidthOverride: comp.props.labelWidthOverride,
                        helpWidthOverride: comp.props.helpWidthOverride,
                        inputWidthMode: comp.props.inputWidthMode,
                        objectLayout: comp.props.objectLayout,
                        label: comp.props.label,
                    }
                };
            } catch (e) {
                return { error: 'Failed to parse form definition: ' + e.message };
            }
        }, componentId);
        
        console.log('\n=== Form Definition Component ===');
        console.log(JSON.stringify(formData, null, 2));
        
        // If width is set, let's clear it to "Auto" (undefined)
        if (formData.found && formData.props.width) {
            console.log('\n=== Fixing Width to Auto ===');
            console.log('Current width:', formData.props.width);
            
            await page.evaluate((compId) => {
                const formDefJson = localStorage.getItem('builder-formDefinition-44');
                if (!formDefJson) return;
                
                const formDef = JSON.parse(formDefJson);
                const pages = formDef.pages || formDef.desktopPages || [];
                
                for (const page of pages) {
                    if (page.components) {
                        const comp = page.components.find(c => c.id === compId);
                        if (comp) {
                            console.log('Found component, clearing width');
                            delete comp.props.width; // Set to undefined (Auto)
                            localStorage.setItem('builder-formDefinition-44', JSON.stringify(formDef));
                            console.log('Width cleared - refresh the page to see changes');
                            return;
                        }
                    }
                }
            }, componentId);
            
            console.log('Width cleared in localStorage. Refreshing page...');
            
            // Refresh the page to apply changes
            await page.reload({ waitUntil: 'networkidle2' });
            await new Promise(r => setTimeout(r, 2000));
            
            // Click on the component again
            const compEl = await page.$(`[data-component-id="${compId}"]`);
            if (compEl) {
                await compEl.click();
                await new Promise(r => setTimeout(r, 500));
            }
            
            // Verify the fix
            const verifyData = await page.evaluate((cId) => {
                const formDefJson = localStorage.getItem('builder-formDefinition-44');
                if (!formDefJson) return { error: 'Form not found' };
                
                const formDef = JSON.parse(formDefJson);
                const pages = formDef.pages || formDef.desktopPages || [];
                
                for (const page of pages) {
                    const comp = page.components?.find(c => c.id === cId);
                    if (comp) {
                        return { 
                            width: comp.props.width,
                            hasWidth: 'width' in comp.props
                        };
                    }
                }
                return { error: 'Component not found' };
            }, compId);
            
            console.log('Verification after fix:', JSON.stringify(verifyData));
            
            // Get new DOM info
            const newDomInfo = await page.evaluate((cId) => {
                const el = document.querySelector(`[data-component-id="${cId}"]`);
                const outer = el?.closest('.group.touch-none.relative');
                return {
                    outerWrapperStyle: outer?.getAttribute('style'),
                    smartBorderClass: el?.className,
                };
            }, compId);
            
            console.log('New DOM state:', JSON.stringify(newDomInfo, null, 2));
        }
        
        // Find and get info about the target component
        const componentInfo = await page.evaluate(() => {
            const componentId = 'text-1768184324292-685';
            
            // Try multiple ways to access the Zustand store
            // Method 1: Direct window access
            let state = window.useBuilderStore?.getState?.();
            
            // Method 2: Check for React DevTools access
            if (!state) {
                // Try to find the store through React's internal fiber
                const rootEl = document.getElementById('root');
                if (rootEl && rootEl._reactRootContainer) {
                    // React 17 style
                    const fiber = rootEl._reactRootContainer?._internalRoot?.current;
                    console.log('React 17 fiber:', !!fiber);
                }
            }
            
            // Method 3: Check for __ZUSTAND__ on window
            if (!state && window.__ZUSTAND__) {
                state = window.__ZUSTAND__;
            }
            
            // Method 4: Try to find store in module cache
            if (!state) {
                // Check common patterns
                for (const key of Object.keys(window)) {
                    if (key.includes('store') || key.includes('Store') || key.includes('zustand')) {
                        console.log('Found store-like key:', key);
                    }
                }
            }
            
            const formDef = state?.formDefinition;
            
            // Debug store structure
            const storeDebug = {
                hasStore: !!state,
                hasFormDef: !!formDef,
                formDefKeys: formDef ? Object.keys(formDef) : [],
                pagesCount: formDef?.pages?.length,
                desktopPagesCount: formDef?.desktopPages?.length,
            };
            
            // Try multiple page sources
            const pageSources = [
                formDef?.pages,
                formDef?.desktopPages,
            ].filter(Boolean);
            
            let comp = null;
            let foundIn = null;
            
            for (const pages of pageSources) {
                for (const page of pages) {
                    // Search in components array
                    if (page.components) {
                        comp = page.components.find(c => c.id === componentId);
                        if (comp) {
                            foundIn = 'page.components';
                            break;
                        }
                        // Also search in children recursively
                        const findInChildren = (comps) => {
                            for (const c of comps) {
                                if (c.id === componentId) return c;
                                if (c.children) {
                                    const found = findInChildren(c.children);
                                    if (found) return found;
                                }
                            }
                            return null;
                        };
                        comp = findInChildren(page.components);
                        if (comp) {
                            foundIn = 'page.components.children';
                            break;
                        }
                    }
                }
                if (comp) break;
            }
            
            // Get DOM element info - check both outer wrapper and SmartBorder
            const outerWrapper = document.querySelector(`[data-component-id="${componentId}"]`)?.closest('.group.touch-none.relative');
            const smartBorderWrapper = document.querySelector(`[data-component-id="${componentId}"]`);
            const el = smartBorderWrapper;
            const rect = el?.getBoundingClientRect();
            
            // Get SmartBorder and content info
            const smartContent = el?.querySelector('[data-smart-content]');
            const smartContentRect = smartContent?.getBoundingClientRect();
            const wrapperClass = el?.className;
            
            // Check the layout group for width: 100%
            const layoutGroup = smartContent?.querySelector('[data-layout-group]');
            const layoutGroupStyle = layoutGroup?.getAttribute('style');
            
            // Check if SmartBorder is using fill or shrink mode
            const isFillMode = wrapperClass?.includes('w-full') || wrapperClass?.includes('block');
            const isShrinkMode = wrapperClass?.includes('inline-block');
            
            // Get outer wrapper style
            const outerWrapperStyle = outerWrapper?.getAttribute('style');
            const outerWrapperRect = outerWrapper?.getBoundingClientRect();
            
            // Look for resize handles wrapper
            const resizeWrapper = outerWrapper?.querySelector('[style*="pointer-events: none"]');
            const resizeWrapperStyle = resizeWrapper?.getAttribute('style');
            
            return {
                storeDebug,
                found: !!comp,
                foundIn,
                props: comp?.props ? {
                    width: comp.props.width,
                    inputWidthOverride: comp.props.inputWidthOverride,
                    labelWidthOverride: comp.props.labelWidthOverride,
                    helpWidthOverride: comp.props.helpWidthOverride,
                    inputWidthMode: comp.props.inputWidthMode,
                    objectLayout: comp.props.objectLayout,
                    label: comp.props.label,
                } : null,
                width: comp?.props?.width,
                widthType: typeof comp?.props?.width,
                inputWidthOverride: comp?.props?.inputWidthOverride,
                domInfo: {
                    outerWrapperRect: outerWrapperRect ? { width: outerWrapperRect.width, height: outerWrapperRect.height } : null,
                    outerWrapperStyle,
                    smartBorderRect: rect ? { width: rect.width, height: rect.height } : null,
                    smartBorderClass: wrapperClass,
                    isFillMode,
                    isShrinkMode,
                    smartContentRect: smartContentRect ? { width: smartContentRect.width, height: smartContentRect.height } : null,
                    layoutGroupStyle,
                    resizeWrapperStyle,
                }
            };
        });
        
        console.log('\n=== Component Info ===');
        console.log(JSON.stringify(componentInfo, null, 2));
        
        // Don't disconnect - keep browser open for user
        console.log('\nBrowser kept open for inspection.');
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
