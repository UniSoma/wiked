async page => {
  const check = (condition, message) => { if (!condition) throw new Error(message); };
  const requests = [];
  page.on('request', request => requests.push(request.url()));
  const entryURL = page.url();
  const host = page.locator('[data-wiked-diagram="process"]');
  try {
    await host.waitFor();
  } catch (error) {
    throw new Error('Diagram enhancement failed: ' + await page.evaluate(() => JSON.stringify({
      images: [...document.querySelectorAll('img')].map(el => ({ src: el.src, origin: el.getAttribute('data-origin'), error: el.getAttribute('data-wiked-error') })),
      content: document.querySelector('.markdown-section')?.innerHTML,
    })));
  }
  await page.locator('[data-wiked-diagram="other"]').waitFor();
  const nodes = host.locator('[role="link"]');
  check(await nodes.count() === 2, "Expected two process occurrences");
  await nodes.first().click();
  check(await page.evaluate(() => document.activeElement.id) === "step_receive", "Node did not focus its section");
  check(page.url() === entryURL, "Node click changed the entry route");
  await page.getByRole('link', { name: 'Back to step in diagram: Receive request - retry', exact: true }).click();
  check(await page.evaluate(() => {
    const shadow = document.querySelector('[data-wiked-diagram="process"]').shadowRoot;
    return shadow.activeElement?.getAttribute('class') === btoa('receive_again');
  }), "Return did not reach the specific repeated node");
  await nodes.first().focus();
  await page.keyboard.press('Enter');
  check(await page.evaluate(() => document.activeElement.id) === "step_receive", "Keyboard activation failed");
  await page.getByRole('link', { name: 'Back to step in diagram: Receive request - other flow', exact: true }).click();
  check(await page.evaluate(() => {
    const shadow = document.querySelector('[data-wiked-diagram="other"]').shadowRoot;
    return shadow.activeElement?.getAttribute('class') === btoa('receive');
  }), "Separate diagram reused the wrong node");
  check(await nodes.first().locator('rect').getAttribute('width') === '200', "Node geometry changed");
  check(await nodes.first().locator('text').textContent() === 'Receive request', "Node title changed");
  await page.getByRole('link', { name: 'Other entry', exact: true }).click();
  await page.getByRole('heading', { name: 'Other entry' }).waitFor();
  await page.goto(entryURL);
  await host.waitFor();
  await page.reload();
  await host.waitFor();
  check(await page.locator('[data-wiked-diagram="process"]').count() === 1, "Duplicate enhancement after reload");
  await page.route('**/process.svg', route => route.fulfill({
    contentType: 'image/svg+xml', body: '<svg xmlns="http://www.w3.org/2000/svg"><script>window.__unsafe=true</script></svg>'
  }));
  await page.reload();
  const failed = page.locator('img[data-wiked-error]');
  await failed.waitFor({ state: 'visible' });
  check(await page.locator('[data-wiked-diagram="process"]').count() === 0, "Unsafe SVG was enhanced");
  check(!await page.evaluate(() => window.__unsafe), "Unsafe SVG executed");
  await page.unroute('**/process.svg');
  await page.reload();
  await host.waitFor();
  // A renamed heading keeps the authored explicit target.
  await page.route('**/process.md', async route => {
    const response = await route.fetch();
    await route.fulfill({ response, body: (await response.text()).replace('## Receive request', '## Renamed request') });
  });
  await page.reload();
  await host.waitFor();
  await host.locator('[role="link"]').first().click();
  check(await page.evaluate(() => document.activeElement.id) === 'step_receive', "Heading rename broke identity");
  await page.unroute('**/process.md');
  // A delayed image/fetch from a previous entry cannot enhance the next one.
  let release;
  const gate = new Promise(resolve => { release = resolve; });
  const delayed = [];
  await page.route('**/process.svg', route => {
    const task = gate.then(() => route.continue()).catch(() => {});
    delayed.push(task);
    return task;
  });
  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.getByRole('link', { name: 'Other entry', exact: true }).click();
  await page.getByRole('heading', { name: 'Other entry' }).waitFor();
  release();
  await Promise.all(delayed);
  check(await page.locator('[data-wiked-diagram]').count() === 0, "Stale load modified another entry");
  await page.unroute('**/process.svg');
  // No adapter: normal images, headings and descriptions still render.
  await page.route('**/viewer/index.html', async route => {
    const response = await route.fetch();
    const body = (await response.text()).replace(
      /<script id="wiked-docsify-diagrams">[\s\S]*?<\/script>/, '');
    await route.fulfill({ response, body });
  });
  await page.goto(entryURL);
  await page.reload();
  await page.locator('img[data-origin="process.svg"]').waitFor({ state: 'visible' });
  await page.getByRole('heading', { name: 'Receive request', exact: true }).first().waitFor();
  check(await page.locator('[data-wiked-diagram]').count() === 0, "Uninstalled adapter still enhanced an image");
  check(requests.every(url => !url.includes('/.agents/') && !url.includes('/distr/') &&
    !url.includes('docsify-diagrams.js')), 'Viewer requested an installed-skill dependency');
  return 'WIKED_BROWSER_PASS';
}
