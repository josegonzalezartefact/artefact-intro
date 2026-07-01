import { createRequire } from "node:module";
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/jose/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");

const url = "file:///Users/jose/Documents/we-are-artefact-website/artefact-latam-website.html";
const outDir = resolve("tmp/qa");
mkdirSync(outDir, { recursive: true });

const qa = { consoleErrors: [], pageErrors: [], checks: {} };
const browser = await chromium.launch({
  headless: true,
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
});

const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
page.on("console", (msg) => {
  if (["error", "warning"].includes(msg.type())) qa.consoleErrors.push({ type: msg.type(), text: msg.text() });
});
page.on("pageerror", (err) => qa.pageErrors.push(err.message));
await page.goto(url, { waitUntil: "load" });
await page.waitForTimeout(1800);
qa.checks.title = await page.title();
qa.checks.desktopBodyWidth = await page.evaluate(() => `${document.documentElement.scrollWidth} / ${window.innerWidth}`);
qa.checks.wordmark = await page.locator('img[alt="Artefact"]').count();
qa.checks.iconDataUri = await page.locator('link[rel="icon"]').getAttribute("href").then((href) => href?.startsWith("data:image/png"));
qa.checks.railLinks = await page.locator(".rail a").count();
qa.checks.sections = await page.locator("main section").count();
qa.checks.logoCells = await page.locator(".logo-cell img").count();
qa.checks.mailtos = await page.locator('a[href^="mailto:"]').count();
qa.checks.heroEyebrowRemoved = await page.locator('#hero').locator("text=Artefact LATAM").count();
qa.checks.personVideoEmbedded = await page.locator("[data-person-video]").getAttribute("src").then((src) => src?.startsWith("data:video/mp4"));
qa.checks.typeCaretAfterTyping = await page.locator(".type-caret").count();
await page.screenshot({ path: `${outDir}/desktop-hero.png`, fullPage: false });
await page.locator('[data-case-trigger="heineken"]').scrollIntoViewIfNeeded();
await page.locator('[data-case-trigger="heineken"]').click();
await page.waitForTimeout(300);
qa.checks.dialogAfterOpen = await page.locator("dialog[open]").count();
qa.checks.activeElementAfterOpen = await page.evaluate(() => document.activeElement?.matches("[data-modal-close]"));
await page.keyboard.press("Escape");
await page.waitForTimeout(300);
qa.checks.dialogAfterEscape = await page.locator("dialog[open]").count();
await page.screenshot({ path: `${outDir}/desktop-presence.png`, fullPage: false });

const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true });
mobile.on("console", (msg) => {
  if (["error", "warning"].includes(msg.type())) qa.consoleErrors.push({ type: `mobile-${msg.type()}`, text: msg.text() });
});
mobile.on("pageerror", (err) => qa.pageErrors.push(`mobile: ${err.message}`));
await mobile.goto(url, { waitUntil: "load" });
await mobile.waitForTimeout(1800);
qa.checks.mobileBodyWidth = await mobile.evaluate(() => `${document.documentElement.scrollWidth} / ${window.innerWidth}`);
qa.checks.mobileRailDisplay = await mobile.locator(".rail").evaluate((el) => getComputedStyle(el).display);
await mobile.screenshot({ path: `${outDir}/mobile.png`, fullPage: false });

await browser.close();
writeFileSync(`${outDir}/qa.json`, JSON.stringify(qa, null, 2));
console.log(JSON.stringify(qa, null, 2));
