# Artefact LATAM Website - Interaction And Motion Spec

## Purpose

This document specifies how the future Artefact LATAM web page should display and animate each section before implementation begins.

It is not a request to build the page. It is a design and interaction brief for a later build.

Source materials:

- Copy source of truth: `artefact-web-page-copy.md`
- Reference deck: `[WIP] Artefact introduction - LATAM - Why Artefact.pdf`

Core constraints:

- Preserve the general order of the deck.
- Preserve approximately 90% of wording, tone, style, and key messages from the copy.
- Keep final page content in English.
- Allow only conservative copy polish: typos, grammar, and fluency.
- Avoid a sequence of slides pasted vertically.
- Use anchored scrollytelling with sticky moments to preserve the feeling of advancing through a deck.
- Visual theme, colors, type system, and brand styling will be defined elsewhere.

## Global Experience Model

The page should use six anchored sections:

1. Hero / Mission
2. Differentiators
3. Presence
4. Offering
5. Adopt AI
6. Contact

The primary interaction model is "sticky chapters":

- Each main section starts with a short section-title passer, inspired by the deck divider slides.
- The title passer should not become a long empty full-screen slide.
- After the title moment, the section enters one or more sticky scenes.
- The sticky scene keeps a visual anchor fixed while text, cards, counters, or diagrams advance with scroll.
- Motion should feel premium and intentional, not decorative.

Motion budget:

- Strong effects only where they help the narrative: Hero video, Presence map, Offering sticky pyramid, HEINEKEN modal.
- Other areas should use restrained reveals, staggered cards, contextual highlighting, and hover/touch states.

Navigation:

- Desktop: a right-side hidden section rail/menu.
- The rail remains mostly hidden by default and appears on hover.
- It should provide access to the six anchors and show current section/progress.
- Mobile: do not rely on hover. Use a compact fallback or omit the rail if it compromises clarity.

Reduced motion:

- Respect `prefers-reduced-motion`.
- Replace scroll scrub and typed effects with static or simple fade states.
- Keep all content accessible without animation.

## 1. Hero / Mission

### Intent

Open with a strong mission statement and a premium interactive background.

Primary message:

> We accelerate the adoption of data and AI to positively impact people and organizations.

The section should then introduce "Who We Are" and the bridge between Business & Technology.

### Layout

- Full viewport sticky hero.
- Background layer: face video that follows the mouse.
- Foreground layer: mission text, typed or progressively revealed.
- Secondary content: "Who We Are" appears after the mission has landed.
- The Business & Technology bridge can be shown as two poles connected by Artefact in the center.

### Effects

- Typed mission reveal:
  - Reveal by phrase, word, or short text chunk.
  - Do not over-animate every letter if it slows reading.
  - The mission should feel like it is being written into the page.
- Face video:
  - On desktop, mouse position controls the video time so the face appears to follow the cursor.
  - On mobile, use autoplay/loop or a poster because mouse scrub is not available.
- Fade transition:
  - As scroll moves past the opening moment, dim or fade the video so "Who We Are" becomes the focus.

### Technical Note

Reference behavior, not final implementation:

```js
const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));

function updateFaceVideoFromMouse(event, video) {
  if (window.innerWidth < 1024 || !video.duration) return;

  const focusX = window.innerWidth * 0.68;
  const relativeX = event.clientX - focusX;
  const sideRange = relativeX >= 0
    ? Math.max(1, window.innerWidth - focusX)
    : Math.max(1, focusX);

  const progress = clamp(relativeX / sideRange, -1, 1);
  const normalized = (progress + 1) / 2;

  video.currentTime = clamp(normalized * video.duration, 0, video.duration);
}
```

### Mobile Behavior

- Replace mouse-following interaction with autoplay/loop or static poster.
- Keep mission visible without requiring scroll precision.
- Avoid text overlapping the face video.

## 2. Differentiators

### Intent

Translate the dense differentiator slides into a multi-scene sticky chapter.

The section must preserve:

- Pure player / market leader claim.
- End-to-end services.
- Agentic AI / GenAI expertise.
- Unique operating model.
- Business depth.
- Anti-vendor lock-in.
- Cloud and LLM agnostic positioning.
- Portability.
- Discreet sources for McKinsey/BCG, UiPath, Forrester, and Gartner.

### Structure

Use four internal scenes.

Scene 1: Pure Player / Market Leader

- Rebuild the positioning chart as a web-native component.
- V1 can use a structured placeholder with axes, competitor zones, and Artefact highlighted.
- Include the McKinsey/BCG source as a contextual note near the claim.

Scene 2: Agents & GenAI Expertise

- Horizontal timeline from pre-2021 to 2024 onwards.
- Scroll advances through:
  - Before ChatGPT.
  - GenAI acceleration.
  - Agentic programs.
- Logos or client references can be placeholders until assets are available.

Scene 3: Unique Operating Model

- Use a sticky diagram with two forces:
  - Business Depth.
  - Technical Expertise.
- Reveal capabilities around each side as the user scrolls.
- The center message should appear once both sides are visible.

Scene 4: AI Revolution + Key Differentiators

- Show the UiPath, Forrester, and Gartner stats as a staggered sequence.
- Then reveal the six differentiator cards:
  - AI & Agentic Pure Player.
  - Business-First Depth.
  - Anti-Vendor Lock-In.
  - All Clouds & LLM Providers.
  - The Power Of The Harness.
  - Designed For Portability.

### Effects

- Sticky split canvas: visual anchor fixed, text/cards advance.
- Timeline progress line for GenAI.
- Diagram nodes reveal in sync with scroll.
- Differentiator cards use stagger reveal.
- Source notes remain visible as small contextual notes, not hidden only in hover.

### Technical Note

Suggested scene activation model:

```js
function getSectionProgress(section) {
  const rect = section.getBoundingClientRect();
  const total = rect.height - window.innerHeight;
  const passed = Math.min(Math.max(-rect.top, 0), total);
  return total > 0 ? passed / total : 0;
}

function getSceneIndex(progress, sceneCount) {
  return Math.min(sceneCount - 1, Math.floor(progress * sceneCount));
}
```

### Mobile Behavior

- Convert the sticky sequence into stacked scenes.
- Keep the timeline readable horizontally if possible; otherwise stack chronological cards.
- Source notes should remain inline under each claim.

## 3. Presence

### Intent

Show Artefact's scale first, then LATAM presence, then industries/clients, and finally the HEINEKEN case as a premium interactive reveal.

Must preserve:

- 27 countries.
- 2,500 employees.
- 36 offices.
- More than 400 Artefactors in LATAM.
- Offices in Sao Paulo, Mexico City, Santiago, and Bogota.
- Industries, clients, and brands.

### Structure

Scene 1: Global Footprint

- Mapamundi video placeholder.
- Future asset: rotating world map that scrubs with scroll.
- Counters appear as scroll advances.

Scene 2: LATAM Presence

- Highlight LATAM footprint on or near the map.
- Show the +400 Artefactors and four offices.

Scene 3: Industries And Clients

- Short industries text.
- Infinite logo carousel.
- Logos pause on hover in desktop.
- Mobile carousel should be touch-friendly and not require hover.

Scene 4: HEINEKEN Trigger

- A clickable beer asset appears as the entry point.
- Clicking opens the HEINEKEN modal.
- The beer asset will be provided later.

### Effects

- Scroll-scrub map video.
- Counter-on-view for key numbers.
- Infinite marquee for logos.
- Clickable beer microinteraction:
  - Hover or focus state.
  - Clear affordance that it opens a case.
  - Accessible button semantics.

### Technical Notes

Scroll-scrub video reference:

```js
function scrubVideoByScroll(section, video) {
  if (!video.duration) return;

  const rect = section.getBoundingClientRect();
  const scrollable = rect.height - window.innerHeight;
  const progress = Math.min(Math.max(-rect.top / scrollable, 0), 1);

  video.currentTime = progress * video.duration;
}
```

Counter reference:

```js
function animateCounter(element, target, duration = 900) {
  const start = performance.now();

  function frame(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    element.textContent = Math.round(target * eased).toLocaleString("en-US");

    if (progress < 1) requestAnimationFrame(frame);
  }

  requestAnimationFrame(frame);
}
```

Logo marquee reference:

```css
.logo-track {
  display: flex;
  width: max-content;
  animation: marquee 36s linear infinite;
}

.logo-marquee:hover .logo-track {
  animation-play-state: paused;
}

@keyframes marquee {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}
```

### HEINEKEN Modal

Content order:

1. Title: Our History With HEINEKEN.
2. Metrics:
   - More than R$650M already captured.
   - More than 2,000 people impacted.
   - ROI x19.
3. Journey timeline:
   - First step toward Advanced Analytics.
   - Expansion of scope.
   - Use case sizing, knowledge internalization, and ways of working.
   - Hybrid squads, architecture, and sustainable evolution.
   - Innovation, GenAI, and Agentic acceleration.
4. Value chain use cases.
5. Media, events, and podcasts reference.

Modal behavior:

- Desktop: premium centered overlay or large panel.
- Mobile: full-screen modal.
- Must trap focus while open.
- Must close with button, Escape key, and overlay click if appropriate.

Modal structure reference:

```html
<button type="button" data-case-trigger="heineken">
  <span>Open HEINEKEN case</span>
</button>

<dialog data-case-modal="heineken" aria-labelledby="heineken-title">
  <button type="button" data-modal-close>Close</button>
  <h2 id="heineken-title">Our History With HEINEKEN</h2>
  <!-- Metrics, timeline, and use cases -->
</dialog>
```

## 4. Offering

### Intent

Explain Artefact's end-to-end transformation model in two levels:

1. Transformation pillars.
2. Service families.

Must preserve:

- Vision & Use Cases.
- Operating Model.
- Data Infrastructure & Governance.
- Change Management & Acculturation.
- Strategy & Transformation.
- Data Foundations & BI.
- AI Acceleration.
- IT & Data Platforms.
- Marketing Data-Driven.
- CX & Digital Marketing.
- Global / Pure Player / End-to-End proof.

### Structure

Stage 1: Transformation Pillars

- Sticky split column.
- Pyramid image fixed on one side.
- Text panel on the other side changes as scroll highlights each pyramid layer.
- The pyramid asset will be provided later; use placeholder in v1.

Stage 2: What It Takes To Succeed

- Present Global / Pure Player / End-To-End as three proof columns or cards.
- Keep motion restrained so it does not compete with the pyramid interaction.

Stage 3: Service Families

- Six service family cards.
- Use stagger reveal on entry.
- Cards can support hover expansion if text density requires it.

Stage 4: Tech Agnostic And Certified Across All Clouds

- Use a partner ecosystem block.
- Keep cloud/provider logos as placeholders until assets are available.
- Reinforce agnostic positioning, not vendor dependence.

### Effects

- Sticky split column for the pyramid.
- Scroll-based active state on each layer.
- Text panel updates in sync.
- Service cards use stagger reveal.
- Partner ecosystem uses subtle reveal or carousel if many logos are available.

### Technical Note

Pyramid state model:

```js
const pillars = [
  "vision-use-cases",
  "operating-model",
  "data-infrastructure-governance",
  "change-management-acculturation"
];

function setActivePillar(progress) {
  const index = Math.min(pillars.length - 1, Math.floor(progress * pillars.length));
  document.documentElement.dataset.activePillar = pillars[index];
}
```

### Mobile Behavior

- Stack pyramid and text.
- Use one pillar block at a time rather than relying on sticky behavior.
- Service cards become one-column or two-column depending on width.

## 5. Adopt AI

### Intent

Replace the former "OTHER" section with a stronger "Adopt AI" event block.

This should feel like a mini event landing block, while clearly avoiding the claim that the 2025 event is upcoming.

### Content Rules

- Present the next edition as being organized for this year.
- Use placeholder fields for:
  - Venue.
  - Dates.
  - Speakers.
  - Stages.
  - Exhibitors.
  - Ecosystems.
  - Participants.
- Previous-edition metrics can be shown only as historical reference:
  - 600+ speakers.
  - 8 stages.
  - 250+ exhibitors.
  - 7 ecosystems.
  - 20,000+ participants.

### Layout

- Event-style landing block.
- Strong title: Adopt AI.
- Supporting copy explains international summit and adoption-at-scale purpose.
- TBD details appear as placeholders, not fake commitments.
- Previous edition metrics appear in a separate "previous edition reference" band.

### Effects

- Section may use a controlled background video/image later if assets exist.
- Use a restrained entrance reveal for event details.
- Metrics can count up, but label them clearly as previous edition reference.

### Mobile Behavior

- Stack event details and previous metrics.
- Avoid overly large type that causes wrapping problems.

## 6. Contact

### Intent

Close with a sober direct-contact directory, not a heavy CTA or form.

### Layout

- Section title: Contact Us.
- Short closing line from the copy.
- Two contact cards:
  - Andre Fonseca, CEO LATAM, `andre.fonseca@artefact.com`
  - Andres Oksenberg, Managing Partner, `andres.oksenberg@artefact.com`
- Emails should be direct `mailto:` links.
- No form.

### Effects

- Minimal reveal only.
- No color-shift or large dramatic transition unless the final theme requires it.
- Prioritize clarity and trust.

### Technical Note

Contact link reference:

```html
<a href="mailto:andre.fonseca@artefact.com">andre.fonseca@artefact.com</a>
<a href="mailto:andres.oksenberg@artefact.com">andres.oksenberg@artefact.com</a>
```

## Asset Placeholders

The spec assumes the following final assets will be added later:

- Hero face video.
- Presence mapamundi scroll video.
- Offering pyramid image.
- HEINEKEN beer trigger asset.
- Client and partner logos.
- Cloud/provider ecosystem logos.
- Optional Adopt AI media.

Before final assets exist, implementation should use clear placeholders with the same dimensions and interaction hooks.

## Accessibility And QA Requirements

Accessibility:

- All interactive elements must be keyboard accessible.
- HEINEKEN modal must trap focus and restore focus on close.
- Source notes must not be hover-only.
- Motion must respect `prefers-reduced-motion`.
- Videos should not block content if they fail to load.
- Mailto links must be real links, not JavaScript-only interactions.

Desktop QA:

- Hidden right-side rail appears on hover and anchors correctly.
- Hero video mouse scrub works without jank.
- Mission reveal remains readable.
- Differentiators scenes activate in the intended order.
- Presence map scrub and counters work.
- Logo carousel loops seamlessly and pauses on hover.
- HEINEKEN modal opens, closes, and keeps content readable.
- Offering pyramid highlights correct text by scroll position.
- Service cards reveal without layout shift.

Mobile QA:

- Sticky sections degrade into stacked readable content.
- No mouse-only effect is required.
- Videos use autoplay/loop or poster fallback.
- Logo carousel is touch-friendly.
- HEINEKEN modal is full-screen and scrollable.
- Contact cards remain readable and tappable.

Content QA:

- Section order matches the approved six-section structure.
- Copy follows `artefact-web-page-copy.md`.
- English content only in final page.
- Adopt AI does not present the 2025 event as future.
- McKinsey/BCG, UiPath, Forrester, and Gartner sources remain visible and discreet.
