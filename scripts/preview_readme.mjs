#!/usr/bin/env node
import fs from 'node:fs/promises';
import http from 'node:http';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const help = `Render README Markdown locally and capture desktop/mobile, light/dark views.
Usage: node preview_readme.mjs --repo PROJECT --out OUTPUT [--module-root NODE_MODULES] [--browser CHROMIUM] FILE...
Requires marked, sanitize-html, and playwright. Module roots may be repeated.
Remote resources are blocked. Screenshots approximate GitHub, not its live renderer.`;

function options(argv) {
  const result = { repo: process.cwd(), roots: [], files: [] };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') return null;
    if (['--repo', '--out', '--browser', '--module-root'].includes(arg)) {
      const value = argv[++i];
      if (!value || value.startsWith('--')) throw new Error(`Missing value for ${arg}`);
      if (arg === '--module-root') result.roots.push(path.resolve(value));
      else result[arg.slice(2)] = path.resolve(value);
    } else if (arg.startsWith('-')) throw new Error(`Unknown option: ${arg}`);
    else result.files.push(arg);
  }
  if (!result.out || !result.files.length) throw new Error(help);
  return result;
}

function inside(root, candidate) {
  const relative = path.relative(root, candidate);
  return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
}

const escape = value => String(value).replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char]);

async function dependency(name, roots) {
  const loaders = [createRequire(import.meta.url), ...roots.map(root => createRequire(path.join(root, '_yoho_loader.cjs')))];
  for (const loader of loaders) {
    let resolved;
    try { resolved = loader.resolve(name); } catch (error) {
      if (error.code === 'MODULE_NOT_FOUND') continue;
      throw error;
    }
    return import(pathToFileURL(resolved).href);
  }
  throw new Error(`Missing ${name}. Supply an existing --module-root or use an environment-native renderer. See references/validation.md.`);
}

function typography(theme) {
  const dark = theme === 'dark';
  return `:root{color-scheme:${theme}}*{box-sizing:border-box}body{margin:0;background:${dark ? '#0d1117' : '#ffffff'};color:${dark ? '#e6edf3' : '#1f2328'};font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",sans-serif;letter-spacing:0}article{max-width:964px;margin:auto;padding:28px 32px;overflow-wrap:break-word}h1,h2,h3,h4,h5,h6{line-height:1.25;margin:24px 0 16px;font-weight:600}h1{font-size:32px}h2{font-size:24px}h1,h2{padding-bottom:8px;border-bottom:1px solid ${dark ? '#30363d' : '#d1d9e0'}}p,ul,ol,pre,table,blockquote{margin:0 0 16px}li+li{margin-top:4px}a{color:${dark ? '#58a6ff' : '#0969da'};text-decoration:none}img{max-width:100%;height:auto;vertical-align:middle}pre{padding:16px;background:${dark ? '#161b22' : '#f6f8fa'};border-radius:6px;overflow-x:auto;max-width:100%;font-size:13px;line-height:1.5;overflow-wrap:normal}code{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:85%;background:${dark ? '#30363d' : '#eff1f3'};padding:2px 5px;border-radius:4px}pre code{padding:0;background:transparent;font-size:100%}table{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse}td,th{padding:6px 13px;border:1px solid ${dark ? '#30363d' : '#d1d9e0'}}blockquote{padding:0 16px;border-left:4px solid ${dark ? '#30363d' : '#d1d9e0'};color:${dark ? '#9198a1' : '#59636e'}}summary{cursor:pointer}hr{border:0;border-top:1px solid ${dark ? '#30363d' : '#d1d9e0'};margin:24px 0}@media(max-width:480px){article{padding:16px}h1{font-size:28px}h2{font-size:22px}}`;
}

async function main() {
  const args = options(process.argv.slice(2));
  if (!args) { process.stdout.write(`${help}\n`); return; }
  const repo = await fs.realpath(args.repo);
  const { marked } = await dependency('marked', args.roots);
  const sanitizerModule = await dependency('sanitize-html', args.roots);
  const sanitize = sanitizerModule.default;
  const playwrightModule = await dependency('playwright', args.roots);
  const chromium = playwrightModule.chromium ?? playwrightModule.default?.chromium;
  if (!chromium) throw new Error('Playwright Chromium API is unavailable');
  const candidates = [];
  for (const [index, input] of args.files.entries()) {
    const file = await fs.realpath(path.resolve(repo, input));
    if (!inside(repo, file)) throw new Error(`Input leaves repository: ${input}`);
    if (path.extname(file).toLowerCase() !== '.md') throw new Error(`Expected Markdown: ${file}`);
    const source = await fs.readFile(file, 'utf8');
    const slug = `${String(index + 1).padStart(2, '0')}-${path.basename(path.dirname(file))}-${path.basename(file, '.md')}`.replace(/[^a-z0-9_-]+/gi, '-');
    const documentPath = `/repo/${path.relative(repo, file).split(path.sep).map(encodeURIComponent).join('/')}`;
    const remote = new Set();
    const localSource = value => {
      if (!value) return '';
      if (/^(?:https?:)?\/\//i.test(value)) { remote.add(value); return ''; }
      if (/^[a-z][a-z0-9+.-]*:/i.test(value)) { remote.add(value); return ''; }
      return value.startsWith('/') ? `/repo${value}` : new URL(value, `http://localhost${documentPath}`).pathname;
    };
    const rendered = marked.parse(source, { gfm: true });
    const html = sanitize(rendered, {
      allowedTags: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'span', 'br', 'hr', 'a', 'img', 'picture', 'source', 'ul', 'ol', 'li', 'pre', 'code', 'em', 'strong', 'del', 's', 'blockquote', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'details', 'summary', 'kbd', 'sup', 'sub', 'dl', 'dt', 'dd'],
      allowedAttributes: { a: ['href', 'title'], img: ['src', 'alt', 'width', 'height', 'title'], source: ['srcset', 'media', 'type'], p: ['align'], div: ['align'], code: ['class'], ol: ['start'], td: ['align', 'colspan', 'rowspan'], th: ['align', 'colspan', 'rowspan'], details: ['open'] },
      allowedClasses: { code: [/^language-[a-z0-9_-]+$/] },
      allowedSchemes: ['http', 'https', 'mailto', 'tel'],
      allowProtocolRelative: false,
      transformTags: {
        img: (tagName, attrs) => {
          const src = localSource(attrs.src);
          return src ? { tagName, attribs: { ...attrs, src } } : { tagName: 'span', attribs: {}, text: `[Unverified image: ${attrs.alt || attrs.src || 'missing source'}]` };
        },
        source: (tagName, attrs) => {
          const entries = (attrs.srcset || '').split(',').map(item => {
            const [url, ...descriptor] = item.trim().split(/\s+/);
            const src = localSource(url);
            return src ? [src, ...descriptor].join(' ') : '';
          }).filter(Boolean);
          return { tagName, attribs: { ...attrs, srcset: entries.join(', ') } };
        },
      },
    });
    candidates.push({ slug, file, html, remote_resources_not_checked: [...remote], mermaid_not_rendered: /(?:^|\s)class="language-mermaid"/.test(html), views: [] });
  }
  await fs.mkdir(args.out, { recursive: true });
  const mime = { '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif', '.avif': 'image/avif' };
  const server = http.createServer(async (request, response) => {
    try {
      const url = new URL(request.url, 'http://localhost');
      const match = url.pathname.match(/^\/__preview__\/(\d+)$/);
      if (match && candidates[Number(match[1])]) {
        const candidate = candidates[Number(match[1])];
        const theme = url.searchParams.get('theme') === 'dark' ? 'dark' : 'light';
        response.setHeader('Content-Type', 'text/html; charset=utf-8');
        response.setHeader('Content-Security-Policy', "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; script-src 'none'; object-src 'none'; base-uri 'none'");
        response.end(`<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(candidate.slug)}</title><style>${typography(theme)}</style><article>${candidate.html}</article></html>`);
        return;
      }
      if (!url.pathname.startsWith('/repo/')) { response.writeHead(404).end(); return; }
      const file = await fs.realpath(path.resolve(repo, `.${decodeURIComponent(url.pathname.slice(5))}`));
      if (!inside(repo, file) || !mime[path.extname(file).toLowerCase()]) { response.writeHead(403).end(); return; }
      const data = await fs.readFile(file);
      response.setHeader('Content-Type', mime[path.extname(file).toLowerCase()]);
      response.setHeader('X-Content-Type-Options', 'nosniff');
      response.end(data);
    } catch { response.writeHead(404).end(); }
  });
  let browser;
  try {
    await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
    const origin = `http://127.0.0.1:${server.address().port}`;
    browser = await chromium.launch({ headless: true, ...(args.browser ? { executablePath: args.browser } : {}) });
    for (const [index, candidate] of candidates.entries()) {
      for (const viewport of [{ name: 'desktop', width: 900, height: 1000 }, { name: 'mobile', width: 360, height: 840 }]) {
        for (const theme of ['light', 'dark']) {
          const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, colorScheme: theme, reducedMotion: 'reduce', deviceScaleFactor: 1, javaScriptEnabled: false });
          try {
            await context.route('**/*', route => new URL(route.request().url()).origin === origin ? route.continue() : route.abort());
            const page = await context.newPage();
            await page.goto(`${origin}/__preview__/${index}?theme=${theme}`, { waitUntil: 'networkidle', timeout: 20000 });
            const inspection = await page.evaluate(() => ({
              page_overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
              broken_images: [...document.images].filter(img => !img.complete || img.naturalWidth === 0).map(img => img.getAttribute('src')),
              visible_text_length: document.querySelector('article').innerText.trim().length,
            }));
            const filename = `${candidate.slug}-${viewport.name}-${theme}.png`;
            await page.screenshot({ path: path.join(args.out, filename), fullPage: false });
            candidate.views.push({ viewport: viewport.name, width: viewport.width, height: viewport.height, theme, screenshot: filename, ...inspection });
          } finally { await context.close(); }
        }
      }
    }
  } finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
  const report = {
    renderer: 'Local sanitized GFM approximation; not a check on GitHub itself',
    checks_not_performed: ['semantic accuracy', 'bilingual equivalence', 'human visual review', 'external images and URLs', 'Mermaid rendering', 'content below captured first screen'],
    candidates: candidates.map(({ html, ...candidate }) => candidate),
  };
  const hasIssues = candidates.some(candidate => candidate.views.some(view => view.page_overflow || view.broken_images.length || view.visible_text_length === 0));
  report.status = hasIssues ? 'issues-found' : 'ready-for-human-review';
  const sections = candidates.map(candidate => `<section><h2>${escape(candidate.slug)}</h2><p>Source: ${escape(path.relative(repo, candidate.file))}</p>${candidate.remote_resources_not_checked.length ? '<p>Remote images were replaced with unverified-image labels.</p>' : ''}${candidate.mermaid_not_rendered ? '<p>Mermaid remains an unrendered code block.</p>' : ''}<div class="views">${candidate.views.map(view => `<figure><a href="${escape(view.screenshot)}"><img src="${escape(view.screenshot)}" alt="${escape(`${candidate.slug}, ${view.viewport}, ${view.theme}`)}"></a><figcaption>${escape(`${view.width}px / ${view.theme}`)}${view.page_overflow || view.broken_images.length ? ' / inspect errors in report.json' : ''}</figcaption></figure>`).join('')}</div></section>`).join('');
  await fs.writeFile(path.join(args.out, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  await fs.writeFile(path.join(args.out, 'index.html'), `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>README visual review</title><style>body{margin:24px auto;padding:0 20px;max-width:1200px;font:15px/1.5 system-ui;background:#f5f6f8;color:#222}h1{font-size:26px}h2{font-size:20px}section{border-top:1px solid #ccd1d7;margin-top:28px}.views{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}figure{margin:0}img{display:block;width:100%;height:auto;border:1px solid #ccd1d7}figcaption{padding:8px 0}@media(max-width:600px){.views{grid-template-columns:1fr}}</style><h1>README visual review</h1><p>Local GFM approximation. Review each image at full size. See report.json for capture checks and limitations.</p>${sections}</html>\n`);
  process.stdout.write(JSON.stringify({ status: report.status, candidates: candidates.length, screenshots: candidates.length * 4, output: args.out }, null, 2) + '\n');
  if (hasIssues) process.exitCode = 1;
}

main().catch(error => { process.stderr.write(`Preview failed: ${error.message}\n`); process.exitCode = 2; });
