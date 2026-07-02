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
qa.checks.topMenuLinks = await page.locator(".top-menu a").count();
qa.checks.heroMenuVisible = await page.locator(".top-menu").evaluate((el) => Number(getComputedStyle(el).opacity) > 0.9);
qa.checks.sections = await page.locator("main section").count();
qa.checks.logoCells = await page.locator(".logo-cell img").count();
qa.checks.mailtos = await page.locator('a[href^="mailto:"]').count();
qa.checks.heroEyebrowRemoved = await page.locator('#hero').locator("text=Artefact LATAM").count();
qa.checks.personVideoEmbedded = await page.locator("[data-person-video]").getAttribute("src").then((src) => src?.startsWith("data:video/mp4"));
qa.checks.transitionCount = await page.locator("[data-section-transition]").count();
qa.checks.transitionVideoEmbedded = await page.locator("[data-transition-video]").first().getAttribute("src").then((src) => src?.startsWith("data:video/mp4"));
qa.checks.typeCaretAfterTyping = await page.locator(".type-caret").count();
await page.screenshot({ path: `${outDir}/desktop-hero.png`, fullPage: false });
await page.evaluate(() => {
  const hero = document.querySelector("#hero");
  const range = Math.max(1, hero.offsetHeight - window.innerHeight);
  window.scrollTo(0, hero.offsetTop + range * 0.52);
});
await page.waitForTimeout(2600);
qa.checks.heroSecondMessage = await page.locator("#hero").locator("text=Artefact is an end-to-end specialized Data & AI consulting company").count();
qa.checks.heroSecondVisible = await page.locator("#hero [data-hero-key='who']").evaluate((el) => {
  const rect = el.getBoundingClientRect();
  const style = getComputedStyle(el);
  return style.opacity === "1" && rect.top < window.innerHeight && rect.bottom > 0;
});
await page.screenshot({ path: `${outDir}/desktop-hero-second.png`, fullPage: false });
await page.locator("#differentiators [data-section-transition]").scrollIntoViewIfNeeded();
await page.evaluate(() => {
  const transition = document.querySelector("#differentiators [data-section-transition]");
  const range = Math.max(1, transition.offsetHeight - window.innerHeight);
  window.scrollTo(0, transition.getBoundingClientRect().top + window.scrollY + range * 0.48);
});
await page.waitForTimeout(500);
qa.checks.transitionTitleVisible = await page.locator("#differentiators [data-transition-title]").evaluate((el) => {
  const style = getComputedStyle(el);
  const rect = el.getBoundingClientRect();
  return Number(style.opacity) > 0.4 && rect.top < window.innerHeight && rect.bottom > 0;
});
qa.checks.menuHiddenOutsideHero = await page.locator(".top-menu").evaluate((el) => Number(getComputedStyle(el).opacity) < 0.1);
qa.checks.menuHintVisibleOutsideHero = await page.locator(".top-shell").evaluate((el) => {
  const style = getComputedStyle(el, "::after");
  return Number(style.opacity) > 0.7;
});
await page.locator(".top-shell").hover({ position: { x: 720, y: 24 } });
await page.waitForTimeout(350);
qa.checks.menuHoverVisibleOutsideHero = await page.locator(".top-menu").evaluate((el) => Number(getComputedStyle(el).opacity) > 0.8);
await page.screenshot({ path: `${outDir}/desktop-transition.png`, fullPage: false });
await page.locator("[data-positioning-chart]").scrollIntoViewIfNeeded();
await page.evaluate(() => {
  const chart = document.querySelector("[data-positioning-chart]");
  const range = Math.max(1, chart.offsetHeight - window.innerHeight);
  window.scrollTo(0, chart.getBoundingClientRect().top + window.scrollY + range * 0.96);
});
await page.waitForTimeout(700);
qa.checks.positioningCompetitorLogos = await page.locator(".competitor-logo img").count();
qa.checks.positioningButtonVisible = await page.locator('[data-case-trigger="positioning"]').evaluate((el) => {
  const style = getComputedStyle(el);
  const rect = el.getBoundingClientRect();
  return Number(style.opacity) > 0.6 && rect.top < window.innerHeight && rect.bottom > 0;
});
await page.locator('[data-case-trigger="positioning"]').click();
await page.waitForTimeout(300);
qa.checks.positioningDialogAfterOpen = await page.locator('dialog[data-case-modal="positioning"][open]').count();
qa.checks.positioningModalArtefactLockup = await page.locator('dialog[data-case-modal="positioning"] .artefact-lockup img[alt="Artefact"]').count();
qa.checks.positioningModalRemovedMatrixCopy = await page.locator('dialog[data-case-modal="positioning"]').locator("text=The matrix compares competitors").count();
await page.keyboard.press("Escape");
await page.waitForTimeout(300);
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
qa.checks.mobileTopMenuLinks = await mobile.locator(".top-menu a").count();
await mobile.screenshot({ path: `${outDir}/mobile.png`, fullPage: false });

await browser.close();
writeFileSync(`${outDir}/qa.json`, JSON.stringify(qa, null, 2));
console.log(JSON.stringify(qa, null, 2));
