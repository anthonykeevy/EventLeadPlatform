/**
 * SmartBorder Diagnostic Script
 * 
 * Run this in the browser console on the builder page to inspect
 * the dropdown component's SmartBorder and content dimensions.
 * 
 * Usage:
 * 1. Open browser console (F12)
 * 2. Paste this entire script
 * 3. Press Enter
 * 4. Look for the diagnostic output
 */

(function() {
    console.log('🔍 SmartBorder Diagnostic Tool');
    console.log('============================\n');
    
    // Find all dropdown components on the canvas
    const dropdownComponents = [];
    
    // Method 1: Find by component type attribute
    const allComponents = document.querySelectorAll('[data-component-id]');
    allComponents.forEach(comp => {
        // Check if it contains a dropdown (look for select element or dropdown-specific classes)
        const hasDropdown = comp.querySelector('select') || 
                           comp.textContent.includes('Dropdown') ||
                           comp.querySelector('[data-smart-content]');
        
        if (hasDropdown) {
            dropdownComponents.push(comp);
        }
    });
    
    if (dropdownComponents.length === 0) {
        console.warn('⚠️ No dropdown components found. Make sure you have a dropdown on the canvas.');
        console.log('Trying alternative search...');
        
        // Method 2: Find by SmartBorder structure
        const smartBorders = document.querySelectorAll('[data-smart-content]');
        smartBorders.forEach(sb => {
            const parent = sb.closest('[data-component-id]');
            if (parent) {
                dropdownComponents.push(parent);
            }
        });
    }
    
    console.log(`Found ${dropdownComponents.length} component(s) to inspect\n`);
    
    dropdownComponents.forEach((component, idx) => {
        console.log(`\n📦 Component ${idx + 1}:`);
        console.log('─'.repeat(50));
        
        // Get component ID
        const componentId = component.getAttribute('data-component-id') || 'unknown';
        console.log(`Component ID: ${componentId}`);
        
        // Find SmartBorder container
        const smartBorderContainer = component.closest('.group') || component;
        const contentWrapper = smartBorderContainer.querySelector('[data-smart-content]');
        const svgPath = smartBorderContainer.querySelector('svg path');
        
        if (!contentWrapper) {
            console.error('❌ Content wrapper not found!');
            return;
        }
        
        // Get container bounds
        const containerRect = smartBorderContainer.getBoundingClientRect();
        const wrapperRect = contentWrapper.getBoundingClientRect();
        const wrapperStyle = window.getComputedStyle(contentWrapper);
        
        // Get padding from computed style
        const paddingTop = parseFloat(wrapperStyle.paddingTop) || 0;
        const paddingRight = parseFloat(wrapperStyle.paddingRight) || 0;
        const paddingBottom = parseFloat(wrapperStyle.paddingBottom) || 0;
        const paddingLeft = parseFloat(wrapperStyle.paddingLeft) || 0;
        
        console.log('\n📐 Container Dimensions:');
        console.log(`  Position: (${containerRect.left.toFixed(1)}, ${containerRect.top.toFixed(1)})`);
        console.log(`  Size: ${containerRect.width.toFixed(1)} × ${containerRect.height.toFixed(1)}px`);
        
        console.log('\n📦 Content Wrapper:');
        console.log(`  Position: (${wrapperRect.left.toFixed(1)}, ${wrapperRect.top.toFixed(1)})`);
        console.log(`  Size: ${wrapperRect.width.toFixed(1)} × ${wrapperRect.height.toFixed(1)}px`);
        console.log(`  Padding: ${paddingTop}px top, ${paddingRight}px right, ${paddingBottom}px bottom, ${paddingLeft}px left`);
        
        // Calculate offset from container
        const offsetX = wrapperRect.left - containerRect.left;
        const offsetY = wrapperRect.top - containerRect.top;
        console.log(`  Offset from container: (${offsetX.toFixed(1)}, ${offsetY.toFixed(1)})px`);
        
        // Check if padding matches offset
        const paddingMatches = Math.abs(offsetX - paddingLeft) < 1 && Math.abs(offsetY - paddingTop) < 1;
        console.log(`  ✅ Padding matches offset: ${paddingMatches ? 'YES' : 'NO'}`);
        
        // Get child elements (label, input, validation)
        const children = Array.from(contentWrapper.children);
        console.log(`\n👶 Child Elements (${children.length}):`);
        
        children.forEach((child, childIdx) => {
            const childRect = child.getBoundingClientRect();
            const childStyle = window.getComputedStyle(child);
            const childOffsetTop = child.offsetTop;
            const childOffsetLeft = child.offsetLeft;
            
            // Try to identify the child type
            let childType = 'Unknown';
            if (child.tagName === 'LABEL' || child.textContent.includes('Dropdown')) {
                childType = 'Label';
            } else if (child.tagName === 'SELECT' || child.querySelector('select')) {
                childType = 'Input/Dropdown';
            } else if (child.textContent.includes('Validation') || child.textContent.includes('error')) {
                childType = 'Validation';
            }
            
            console.log(`\n  ${childIdx + 1}. ${childType}:`);
            console.log(`     Position: (${childRect.left.toFixed(1)}, ${childRect.top.toFixed(1)})`);
            console.log(`     Size: ${childRect.width.toFixed(1)} × ${childRect.height.toFixed(1)}px`);
            console.log(`     offsetTop: ${childOffsetTop}px`);
            console.log(`     offsetLeft: ${childOffsetLeft}px`);
            
            // Calculate position relative to content wrapper
            const relativeX = childRect.left - wrapperRect.left;
            const relativeY = childRect.top - wrapperRect.top;
            console.log(`     Relative to wrapper: (${relativeX.toFixed(1)}, ${relativeY.toFixed(1)})px`);
            
            // Check if child respects padding
            const respectsPaddingX = Math.abs(relativeX - paddingLeft) < 1;
            const respectsPaddingY = Math.abs(relativeY - paddingTop) < 1;
            console.log(`     ✅ Respects padding: X=${respectsPaddingX ? 'YES' : 'NO'}, Y=${respectsPaddingY ? 'YES' : 'NO'}`);
        });
        
        // Get SVG path information
        if (svgPath) {
            console.log('\n🎨 SmartBorder SVG Path:');
            const pathD = svgPath.getAttribute('d') || '';
            const pathLength = svgPath.getTotalLength();
            const pathBBox = svgPath.getBBox();
            
            console.log(`  Path data: ${pathD.substring(0, 100)}...`);
            console.log(`  Path length: ${pathLength.toFixed(1)}px`);
            console.log(`  Bounding box: x=${pathBBox.x.toFixed(1)}, y=${pathBBox.y.toFixed(1)}, width=${pathBBox.width.toFixed(1)}, height=${pathBBox.height.toFixed(1)}`);
            
            // Get SVG element
            const svg = svgPath.closest('svg');
            if (svg) {
                const svgRect = svg.getBoundingClientRect();
                console.log(`  SVG position: (${svgRect.left.toFixed(1)}, ${svgRect.top.toFixed(1)})`);
                console.log(`  SVG size: ${svgRect.width.toFixed(1)} × ${svgRect.height.toFixed(1)}px`);
                
                // Compare SVG position with content wrapper
                const svgOffsetX = svgRect.left - containerRect.left;
                const svgOffsetY = svgRect.top - containerRect.top;
                console.log(`  SVG offset from container: (${svgOffsetX.toFixed(1)}, ${svgOffsetY.toFixed(1)})px`);
                
                // Path should start at -padding relative to content wrapper
                const expectedPathStartX = -paddingLeft;
                const expectedPathStartY = -paddingTop;
                console.log(`  Expected path start: (${expectedPathStartX}, ${expectedPathStartY})px`);
                console.log(`  Actual path bbox start: (${pathBBox.x.toFixed(1)}, ${pathBBox.y.toFixed(1)})px`);
                
                const pathMatches = Math.abs(pathBBox.x - expectedPathStartX) < 1 && Math.abs(pathBBox.y - expectedPathStartY) < 1;
                console.log(`  ✅ Path matches expected: ${pathMatches ? 'YES' : 'NO'}`);
            }
        } else {
            console.warn('\n⚠️ SVG path not found! SmartBorder may not be rendered.');
        }
        
        // Summary
        console.log('\n📊 Summary:');
        const allChildrenRespectPadding = children.every((child, idx) => {
            const childRect = child.getBoundingClientRect();
            const relativeX = childRect.left - wrapperRect.left;
            const relativeY = childRect.top - wrapperRect.top;
            return Math.abs(relativeX - paddingLeft) < 1 && Math.abs(relativeY - paddingTop) < 1;
        });
        
        console.log(`  Content wrapper has padding: ${paddingTop > 0 ? 'YES' : 'NO'} (${paddingTop}px)`);
        console.log(`  All children respect padding: ${allChildrenRespectPadding ? 'YES' : 'NO'}`);
        console.log(`  SVG path exists: ${svgPath ? 'YES' : 'NO'}`);
        
        if (!allChildrenRespectPadding) {
            console.warn('\n⚠️ ISSUE DETECTED: Children are not respecting the content wrapper padding!');
            console.warn('   This means the SmartBorder will overlap the content.');
        }
    });
    
    console.log('\n✅ Diagnostic complete!');
})();




