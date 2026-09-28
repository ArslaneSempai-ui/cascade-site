// The sample report's first page as an image, and the whole report as a PDF, rendered by Chrome from the HTML
// that rapport.py wrote. usage: node capturer-rapport.mjs <report.html> <out.pdf> <out-page1.webp>
import { createRequire } from "node:module";
import { homedir } from "node:os";
const puppeteer = createRequire(homedir() + "/.claude/skills/design-arslane/scripts/capturer-vue.mjs")("puppeteer-core");
const [html, pdf, png] = process.argv.slice(2);
const nav = await puppeteer.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: "new" });
const p = await nav.newPage();
await p.emulateMediaType("print");
await p.setViewport({ width: 816, height: 1056, deviceScaleFactor: 1.5 });
await p.goto("file://" + html, { waitUntil: "networkidle2" }); await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: pdf, format: "Letter", printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
await p.screenshot({ path: png, type: "webp", quality: 86, clip: { x: 0, y: 0, width: 816, height: 1056 } });
await nav.close();
console.log("pdf and page 1 written");
