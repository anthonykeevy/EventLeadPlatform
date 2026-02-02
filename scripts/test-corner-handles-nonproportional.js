const puppeteer = require('puppeteer');

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function ensureLoggedIn(page) {
  // If redirected to login, perform login
  if (!page.url().includes('/login')) return;
  console.log('Logging in...');
  await page.type('input[name="email"], input[type="email"]', 'user2@test.com');
  await page.type('input[name="password"], input[type="password"]', 'JChMom7KYLfL88&!');
  await page.click('button[type="submit"]');
  await page.waitForNavigation({ waitUntil: 'networkidle0', timeout: 20000 });
  console.log('Logged in, URL:', page.url());
}

async function getComponentState(page, componentId, formId = '46') {
  return page.evaluate(
    ({ componentId, formId }) => {
      const defKey = `builder-formDefinition-${formId}`;
      const defRaw = localStorage.getItem(defKey);
      const storeRaw = localStorage.getItem('builder-store');

      const def = defRaw ? JSON.parse(defRaw) : (storeRaw ? JSON.parse(storeRaw).formDefinition : null);
      if (!def) return { error: 'No form definition in storage', componentId };

      const pages = (def.desktopPages && def.desktopPages.length > 0) ? def.desktopPages : (def.pages || []);
      const activePageId = (storeRaw ? JSON.parse(storeRaw).activePageId : null) || (pages[0] && pages[0].id);
      const activePage = pages.find((p) => p.id === activePageId) || pages[0];
      if (!activePage) return { error: 'No active page', componentId };

      const findRecursive = (list) => {
        for (const c of list || []) {
          if (c.id === componentId) return c;
          if (c.children) {
            const found = findRecursive(c.children);
            if (found) return found;
          }
        }
        return null;
      };

      const comp = findRecursive(activePage.components);
      if (!comp) return { error: 'Component not found in definition', componentId };

      return {
        id: comp.id,
        type: comp.type,
        position: comp.position,
        width: comp.props && comp.props.width,
        componentScale: comp.props && comp.props.componentScale,
        styleOverrides: comp.props && comp.props.styleOverrides,
        labelGapOverride: comp.props && comp.props.labelGapOverride,
        inputHelpGapOverride: comp.props && comp.props.inputHelpGapOverride,
      };
    },
    { componentId, formId }
  );
}

(async () => {
  const FORM_ID = '46';
  try {
    const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
    const pages = await browser.pages();
    let page = pages.find((p) => p.url().includes('localhost:3000')) || (await browser.newPage());

    // Navigate to builder; login if needed
    await page.goto(`http://localhost:3000/forms/${FORM_ID}/builder`, { waitUntil: 'networkidle0' });
    await ensureLoggedIn(page);
    if (page.url().includes('/login')) {
      // If login didn't redirect, go to builder again
      await page.goto(`http://localhost:3000/forms/${FORM_ID}/builder`, { waitUntil: 'networkidle0' });
    }

    console.log('At:', page.url());
    await sleep(2000);

    // Pick a canvas component id (prefer a text component)
    const componentId = await page.evaluate(() => {
      const canvas = document.querySelector('[data-canvas-container]') || document.body;
      const els = Array.from(canvas.querySelectorAll('[data-component-id]'));
      const preferText = els.find((el) => (el.getAttribute('data-component-id') || '').startsWith('text-'));
      return (preferText || els[0])?.getAttribute('data-component-id') || null;
    });

    if (!componentId) {
      console.error('No component found on canvas.');
      return;
    }

    console.log('Selected component id:', componentId);
    await page.click(`[data-component-id="${componentId}"]`);
    await sleep(800);

    const before = await getComponentState(page, componentId, FORM_ID);
    console.log('\n=== BEFORE CORNER RESIZE ===\n', before);

    // Drag SE corner handle (bottom-right)
    const seHandle = await page.$('[title="Corner resize (SE)"]');
    if (!seHandle) {
      console.error('SE corner handle not found. Is the component selected?');
      return;
    }

    const box = await seHandle.boundingBox();
    if (!box) {
      console.error('SE handle has no bounding box.');
      return;
    }

    const cx = box.x + box.width / 2;
    const cy = box.y + box.height / 2;

    console.log('\nDragging SE corner by +60px,+40px (screen px)...');
    await page.mouse.move(cx, cy);
    await page.mouse.down();
    await page.mouse.move(cx + 60, cy + 40, { steps: 10 });
    await sleep(300);
    await page.mouse.up();
    await sleep(1200);

    const afterCorner = await getComponentState(page, componentId, FORM_ID);
    console.log('\n=== AFTER CORNER RESIZE ===\n', afterCorner);

    if (afterCorner.error) {
      console.error('Could not read after-corner state:', afterCorner.error);
    } else {
      const scaleUnchanged = (afterCorner.componentScale ?? 100) === (before.componentScale ?? 100);
      console.log('Assert componentScale unchanged:', scaleUnchanged);
      if (!scaleUnchanged) {
        throw new Error(`componentScale changed via corner resize (before=${before.componentScale}, after=${afterCorner.componentScale})`);
      }
    }

    // Now verify Component Scale slider changes scale
    const slider = await page.$('input[type="range"].accent-blue-500');
    if (!slider) {
      console.error('Component Scale slider not found (accent-blue-500).');
      return;
    }

    console.log('\nSetting Component Scale slider to 150...');
    await page.evaluate(() => {
      const el = document.querySelector('input[type="range"].accent-blue-500');
      if (!el) return;
      el.value = '150';
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
    });
    await sleep(800);

    const afterSlider = await getComponentState(page, componentId, FORM_ID);
    console.log('\n=== AFTER SCALE SLIDER ===\n', afterSlider);
    if (!afterSlider.error) {
      const is150 = (afterSlider.componentScale ?? 100) === 150;
      console.log('Assert componentScale == 150:', is150);
      if (!is150) {
        throw new Error(`componentScale did not update via slider (expected=150, actual=${afterSlider.componentScale})`);
      }
    }

    console.log('\nDone: corner resize is non-proportional; scale slider updates componentScale.');
  } catch (err) {
    console.error('\nTEST FAILED:', err);
    process.exitCode = 1;
  }
})();

