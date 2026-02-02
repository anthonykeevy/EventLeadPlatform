/**
 * Automated test script for all resize handles (N, S, W, E, NE, SE, NW, SW)
 * 
 * This script:
 * 1. Selects a component on the canvas
 * 2. Tests each resize handle by simulating PointerEvents
 * 3. Moves mouse in 5px increments to trigger capture events
 * 4. Waits for resize capture logs to be sent to backend
 * 
 * Usage: Run this via browser_evaluate after navigating to the form builder
 */

(async function testAllResizeHandles() {
    const handles = ['n', 's', 'w', 'e', 'ne', 'se', 'nw', 'sw'];
    const componentId = 'text-1768866112931-605'; // Update with actual component ID
    
    console.log('Starting resize handle tests...');
    
    // Helper to find and click a component
    function findAndClickComponent(componentId) {
        const component = document.querySelector(`[data-component-id="${componentId}"]`);
        if (!component) {
            console.error(`Component ${componentId} not found`);
            return false;
        }
        
        // Click to select
        const clickEvent = new MouseEvent('click', {
            bubbles: true,
            cancelable: true,
            view: window
        });
        component.dispatchEvent(clickEvent);
        
        // Wait for handles to appear
        setTimeout(() => {}, 500);
        return true;
    }
    
    // Helper to find a resize handle
    function findHandle(handle, componentId) {
        const selector = `[data-resize-handle="${handle}"][data-resize-component-id="${componentId}"]`;
        return document.querySelector(selector);
    }
    
    // Helper to simulate resize drag for a handle
    function simulateResizeDrag(handle, componentId, deltaX, deltaY, steps = 10) {
        const handleEl = findHandle(handle, componentId);
        if (!handleEl) {
            console.error(`Handle ${handle} not found for component ${componentId}`);
            return Promise.resolve();
        }
        
        const rect = handleEl.getBoundingClientRect();
        const startX = rect.left + rect.width / 2;
        const startY = rect.top + rect.height / 2;
        const endX = startX + deltaX;
        const endY = startY + deltaY;
        
        return new Promise((resolve) => {
            // Pointer down
            const pointerDown = new PointerEvent('pointerdown', {
                bubbles: true,
                cancelable: true,
                pointerId: 1,
                clientX: startX,
                clientY: startY,
                button: 0,
                buttons: 1
            });
            
            try {
                handleEl.dispatchEvent(pointerDown);
                if (typeof handleEl.setPointerCapture === 'function') {
                    try {
                        handleEl.setPointerCapture(1);
                    } catch (e) {
                        // Ignore capture failures
                    }
                }
            } catch (e) {
                console.warn('Pointer down failed:', e);
            }
            
            // Wait a bit
            setTimeout(() => {
                // Move in steps
                let stepIndex = 0;
                const stepX = deltaX / steps;
                const stepY = deltaY / steps;
                
                function moveStep() {
                    if (stepIndex >= steps) {
                        // Pointer up
                        const pointerUp = new PointerEvent('pointerup', {
                            bubbles: true,
                            cancelable: true,
                            pointerId: 1,
                            clientX: endX,
                            clientY: endY,
                            button: 0,
                            buttons: 0
                        });
                        
                        try {
                            handleEl.dispatchEvent(pointerUp);
                            if (typeof handleEl.releasePointerCapture === 'function') {
                                try {
                                    handleEl.releasePointerCapture(1);
                                } catch (e) {
                                    // Ignore
                                }
                            }
                        } catch (e) {
                            console.warn('Pointer up failed:', e);
                        }
                        
                        // Wait for logs to be sent
                        setTimeout(() => resolve(), 1000);
                        return;
                    }
                    
                    const currentX = startX + (stepIndex + 1) * stepX;
                    const currentY = startY + (stepIndex + 1) * stepY;
                    
                    const pointerMove = new PointerEvent('pointermove', {
                        bubbles: true,
                        cancelable: true,
                        pointerId: 1,
                        clientX: currentX,
                        clientY: currentY,
                        button: 0,
                        buttons: 1
                    });
                    
                    try {
                        handleEl.dispatchEvent(pointerMove);
                    } catch (e) {
                        console.warn('Pointer move failed:', e);
                    }
                    
                    stepIndex++;
                    setTimeout(moveStep, 50); // 50ms between steps = ~5px per step
                }
                
                moveStep();
            }, 100);
        });
    }
    
    // Test each handle
    if (!findAndClickComponent(componentId)) {
        return { error: 'Component not found', componentId };
    }
    
    const results = {};
    
    for (const handle of handles) {
        console.log(`Testing handle: ${handle}`);
        
        // Determine drag direction based on handle
        let deltaX = 0;
        let deltaY = 0;
        
        switch (handle) {
            case 'n': deltaY = -30; break;  // Up
            case 's': deltaY = 30; break;  // Down
            case 'w': deltaX = -30; break; // Left
            case 'e': deltaX = 30; break;  // Right
            case 'ne': deltaX = 30; deltaY = -30; break;  // Right + Up
            case 'se': deltaX = 30; deltaY = 30; break;  // Right + Down
            case 'nw': deltaX = -30; deltaY = -30; break; // Left + Up
            case 'sw': deltaX = -30; deltaY = 30; break;  // Left + Down
        }
        
        try {
            await simulateResizeDrag(handle, componentId, deltaX, deltaY, 6); // 6 steps = 30px total
            results[handle] = 'completed';
            console.log(`✓ Handle ${handle} test completed`);
            
            // Wait between handles
            await new Promise(r => setTimeout(r, 2000));
        } catch (error) {
            results[handle] = { error: error.message };
            console.error(`✗ Handle ${handle} test failed:`, error);
        }
    }
    
    return {
        success: true,
        componentId,
        results,
        message: 'All handle tests completed. Check resize capture logs in database.'
    };
})();
