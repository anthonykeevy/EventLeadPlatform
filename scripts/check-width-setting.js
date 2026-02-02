const puppeteer = require('puppeteer');

async function main() {
    try {
        const browser = await puppeteer.connect({
            browserURL: 'http://127.0.0.1:9222',
            defaultViewport: null
        });
        
        const pages = await browser.pages();
        let page = pages.find(p => p.url().includes('localhost:3000'));
        
        const componentId = 'text-1768184324292-685';
        
        // Get current width from localStorage
        const widthInfo = await page.evaluate((compId) => {
            const formDefJson = localStorage.getItem('builder-formDefinition-44');
            if (!formDefJson) return { error: 'Form not found' };
            
            const formDef = JSON.parse(formDefJson);
            const pages = formDef.pages || formDef.desktopPages || [];
            
            for (const page of pages) {
                const comp = page.components?.find(c => c.id === compId);
                if (comp) {
                    return {
                        width: comp.props.width,
                        widthType: typeof comp.props.width,
                        hasWidth: 'width' in comp.props,
                        inputWidthOverride: comp.props.inputWidthOverride,
                    };
                }
            }
            return { error: 'Component not found' };
        }, componentId);
        
        console.log('\n=== Current Width Setting ===');
        console.log(JSON.stringify(widthInfo, null, 2));
        
        if (widthInfo.hasWidth && widthInfo.width) {
            console.log(`\n⚠️ Component has explicit width: "${widthInfo.width}"`);
            console.log('This causes SmartBorder to use "fill" mode and stretch the wrapper.');
        } else if (!widthInfo.width) {
            console.log(`\n✅ Component has no explicit width (Auto mode)`);
        }
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main().catch(console.error);
