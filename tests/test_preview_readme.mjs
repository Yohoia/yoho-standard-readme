import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

const script = fileURLToPath(new URL('../scripts/preview_readme.mjs', import.meta.url));
const moduleRoots = (process.env.YOHO_PREVIEW_MODULE_ROOTS || '').split(path.delimiter).filter(Boolean);
const browser = process.env.YOHO_PREVIEW_BROWSER;
const browserSkip = moduleRoots.length ? false : 'Set YOHO_PREVIEW_MODULE_ROOTS to existing marked, sanitize-html, and playwright module roots to run Chromium integration tests.';
const limitations = ['semantic accuracy', 'bilingual equivalence', 'human visual review', 'external images and URLs', 'Mermaid rendering'];
const firstScreenLimitation = 'content below captured first screen';

function run(...args) {
  const result = spawnSync(process.execPath, [script, ...args], { encoding: 'utf8', timeout: 90000 });
  assert.equal(result.error, undefined, result.error?.message);
  assert.equal(result.signal, null, result.stderr);
  return result;
}

function browserArgs(repo, out) {
  return ['--repo', repo, '--out', out, ...moduleRoots.flatMap(root => ['--module-root', root]), ...(browser ? ['--browser', browser] : [])];
}

async function fixture(t, markdown) {
  const root = await fs.realpath(await fs.mkdtemp(path.join(os.tmpdir(), 'yoho-preview-test-')));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  const repo = path.join(root, 'target-project');
  await fs.mkdir(path.join(repo, 'assets'), { recursive: true });
  await fs.writeFile(path.join(repo, 'README.md'), markdown);
  await fs.writeFile(path.join(repo, 'assets', 'local.svg'), '<svg xmlns="http://www.w3.org/2000/svg" width="80" height="30"><rect width="80" height="30" fill="#225588"/></svg>');
  return { root, repo };
}

async function readCapture(out) {
  return {
    report: JSON.parse(await fs.readFile(path.join(out, 'report.json'), 'utf8')),
    index: await fs.readFile(path.join(out, 'index.html'), 'utf8'),
  };
}

async function pngDimensions(filename) {
  const data = await fs.readFile(filename);
  assert.deepEqual(data.subarray(0, 8), Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]));
  assert.equal(data.toString('ascii', 12, 16), 'IHDR');
  return { width: data.readUInt32BE(16), height: data.readUInt32BE(20) };
}

test('help describes capture modes without loading renderer dependencies', () => {
  const result = run('--help');
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /--full-page/);
  assert.match(result.stdout, /first[- ]screen/i);
  assert.equal(result.stderr, '');
});

test('unknown options fail before renderer dependencies are loaded', () => {
  const result = run('--unknown-option');
  assert.equal(result.status, 2);
  assert.match(result.stderr, /Unknown option: --unknown-option/);
  assert.equal(result.stdout, '');
});

test('first-screen and full-page capture the same README in four real Chromium views', { skip: browserSkip, timeout: 180000 }, async t => {
  const paragraphs = Array.from({ length: 90 }, (_, index) => `## Section ${index + 1}\n\nTarget project paragraph ${index + 1}. This local README content makes the complete document taller than every viewport.\n`).join('\n');
  const source = '# Target project\n\n![Local image](assets/local.svg)\n\n![Remote example](https://example.invalid/remote.png)\n\n```mermaid\ngraph LR\n  A --> B\n```\n\n' + paragraphs;
  const { root, repo } = await fixture(t, source);
  for (const mode of ['first-screen', 'full-page']) {
    const out = path.join(root, mode);
    const result = run(...browserArgs(repo, out), ...(mode === 'full-page' ? ['--full-page'] : []), 'README.md');
    assert.equal(result.status, 0, result.stderr || result.stdout);
    const summary = JSON.parse(result.stdout);
    assert.equal(summary.capture_mode, mode);
    assert.equal(summary.candidates, 1);
    assert.equal(summary.screenshots, 4);
    assert.equal(summary.status, 'ready-for-human-review');
    const { report, index } = await readCapture(out);
    assert.equal(report.capture_mode, mode);
    assert.equal(report.status, 'ready-for-human-review');
    assert.equal(report.candidates.length, 1);
    assert.match(index, mode === 'full-page' ? /full[- ]page|full document/i : /first[- ]screen/i);
    for (const limitation of limitations) assert.ok(report.checks_not_performed.includes(limitation), limitation);
    assert.equal(report.checks_not_performed.includes(firstScreenLimitation), mode === 'first-screen');
    const candidate = report.candidates[0];
    assert.equal(candidate.file, path.join(repo, 'README.md'));
    assert.deepEqual(candidate.remote_resources_not_checked, ['https://example.invalid/remote.png']);
    assert.equal(candidate.mermaid_not_rendered, true);
    assert.match(index, /unverified-image|unverified image/i);
    assert.match(index, /Mermaid remains an unrendered code block/);
    assert.equal(candidate.views.length, 4);
    assert.deepEqual(candidate.views.map(view => `${view.viewport}/${view.theme}`).sort(), ['desktop/dark', 'desktop/light', 'mobile/dark', 'mobile/light']);
    for (const view of candidate.views) {
      const viewport = view.viewport === 'desktop' ? { width: 900, height: 1000 } : { width: 360, height: 840 };
      assert.equal(view.width, viewport.width);
      assert.equal(view.height, viewport.height);
      assert.equal(view.page_overflow, false);
      assert.deepEqual(view.broken_images, []);
      assert.ok(view.visible_text_length > 0);
      assert.match(view.screenshot, new RegExp(`-${view.viewport}-${view.theme}\\.png$`));
      assert.ok(index.includes(`<a href="${view.screenshot}">`), `Original screenshot link: ${view.screenshot}`);
      const image = await pngDimensions(path.join(out, view.screenshot));
      assert.equal(image.width, viewport.width);
      if (mode === 'first-screen') assert.equal(image.height, viewport.height);
      else assert.ok(image.height > viewport.height, `Full-page image height ${image.height} must exceed ${viewport.height}`);
    }
  }
});

test('a missing local image in the README body reports a capture issue', { skip: browserSkip, timeout: 90000 }, async t => {
  const { root, repo } = await fixture(t, '# Target project\n\n![Missing body image](assets/missing.png)\n');
  const out = path.join(root, 'broken-body-image');
  const result = run(...browserArgs(repo, out), '--full-page', 'README.md');
  assert.equal(result.status, 1, result.stderr || result.stdout);
  const summary = JSON.parse(result.stdout);
  const { report } = await readCapture(out);
  assert.equal(summary.status, 'issues-found');
  assert.equal(report.status, 'issues-found');
  assert.equal(report.capture_mode, 'full-page');
  assert.equal(report.candidates[0].views.length, 4);
  for (const view of report.candidates[0].views) assert.deepEqual(view.broken_images, ['/repo/assets/missing.png']);
});

test('delayed local images and system-font text are ready in all Chromium views', { skip: browserSkip || (process.platform === 'win32' ? 'Named-pipe fixture requires mkfifo.' : false), timeout: 90000 }, async t => {
  const { root, repo } = await fixture(t, '# 图片与字体就绪 / Image readiness\n\n![Delayed local image](assets/delayed.svg)\n\n中英文正文使用预览器的系统字体。 Local system-font text remains readable.\n');
  const fifo = path.join(repo, 'assets', 'delayed.svg');
  const made = spawnSync('mkfifo', [fifo], { encoding: 'utf8' });
  assert.equal(made.error, undefined, made.error?.message);
  assert.equal(made.status, 0, made.stderr);
  const delivered = path.join(root, 'delivered.json');
  const writer = spawn(process.execPath, ['--input-type=module', '-e', `
    import fs from 'node:fs/promises';
    const [fifo, delivered] = process.argv.slice(1);
    const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="120"><rect width="320" height="120" fill="#1769aa"/></svg>';
    for (let index = 0; index < 4; index++) {
      const file = await fs.open(fifo, 'w');
      await new Promise(resolve => setTimeout(resolve, 350));
      await file.writeFile(svg);
      await file.close();
    }
    await fs.writeFile(delivered, JSON.stringify({ requests: 4, delay_ms: 350 }));
  `, fifo, delivered], { stdio: ['ignore', 'ignore', 'pipe'] });
  let writerStderr = '';
  writer.stderr.on('data', chunk => { writerStderr += chunk; });
  const writerDone = new Promise((resolve, reject) => {
    writer.once('error', reject);
    writer.once('exit', (code, signal) => resolve({ code, signal }));
  });
  t.after(async () => { if (writer.exitCode === null) writer.kill('SIGKILL'); await writerDone; });
  const out = path.join(root, 'delayed-image');
  const result = run(...browserArgs(repo, out), '--full-page', 'README.md');
  if (result.status !== 0) writer.kill('SIGKILL');
  const writerResult = await writerDone;
  assert.equal(result.status, 0, result.stderr || result.stdout);
  assert.deepEqual(writerResult, { code: 0, signal: null }, writerStderr);
  assert.deepEqual(JSON.parse(await fs.readFile(delivered, 'utf8')), { requests: 4, delay_ms: 350 });
  const { report } = await readCapture(out);
  assert.equal(report.status, 'ready-for-human-review');
  assert.equal(report.candidates[0].views.length, 4);
  for (const view of report.candidates[0].views) {
    assert.deepEqual(view.broken_images, []);
    assert.equal(view.page_overflow, false);
    assert.ok(view.visible_text_length > 60);
    assert.equal((await pngDimensions(path.join(out, view.screenshot))).width, view.width);
  }
});

test('browser launch failure closes the local preview server and exits', { skip: browserSkip, timeout: 90000 }, async t => {
  const { root, repo } = await fixture(t, '# Target project\n\nLocal content.\n');
  const out = path.join(root, 'failed-launch');
  const result = run(...browserArgs(repo, out), '--browser', path.join(root, 'missing-browser'), 'README.md');
  assert.equal(result.status, 2);
  assert.match(result.stderr, /Preview failed:.*[Ll]aunch/);
  assert.equal(result.stdout, '');
  await assert.rejects(fs.access(path.join(out, 'report.json')), { code: 'ENOENT' });
});
