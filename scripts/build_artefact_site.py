from __future__ import annotations

import base64
import html
import mimetypes
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = Path("/Users/jose/Documents/artefact-html-skill/assets")
OUT = ROOT / "artefact-latam-website.html"


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0]
    if mime is None:
        if path.suffix.lower() == ".svg":
            mime = "image/svg+xml"
        elif path.suffix.lower() == ".webp":
            mime = "image/webp"
        else:
            mime = "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def logo_cell(name: str, src: str) -> str:
    return f'<div class="logo-cell"><img src="{src}" alt="{html.escape(name)} logo"></div>'


def card(title: str, body: str) -> str:
    return f'<article class="card reveal"><h3>{title}</h3><p>{body}</p></article>'


def service_card(title: str, body: str) -> str:
    return f'<article class="service-card reveal"><div class="service-icon"></div><h3>{title}</h3><p>{body}</p></article>'


def competitor_logo(name: str, key: str, x: float, y: float, w: float) -> str:
    src = consultancy_logos.get(key)
    if not src:
        return ""
    return (
        f'<div class="competitor-logo" style="--x:{x}; --y:{y}; --w:{w};">'
        f'<img src="{src}" alt="{html.escape(name)} logo"></div>'
    )


def competitor_group(slug: str, title: str, phase: float, box: tuple[float, float, float, float], logos_html: str) -> str:
    x, y, w, h = box
    return f"""
      <div class="competitor-group group-{slug}" data-chart-phase="{phase:.2f}" tabindex="0" style="--x:{x}; --y:{y}; --w:{w}; --h:{h};">
        <h3>{html.escape(title)}</h3>
        <div class="group-frame">{logos_html}</div>
      </div>
    """


def section_transition(title: str) -> str:
    safe_title = html.escape(title)
    return f"""
      <div class="section-transition" data-section-transition>
        <div class="transition-stage">
          <div class="transition-video-wrap" data-transition-video-wrap>
            <video class="transition-video" data-transition-video muted playsinline crossorigin="anonymous" preload="auto"></video>
          </div>
          <div class="transition-shade" aria-hidden="true"></div>
          <div class="transition-title" data-transition-title><h2>{safe_title}</h2></div>
        </div>
      </div>
    """


wordmark = data_uri(ASSET_ROOT / "logos/wordmark.png")
a_icon = data_uri(ASSET_ROOT / "icons/artefact_A_icon.png")
person_video = data_uri(Path("/Users/jose/Documents/workshop_website/assets/videos/person.mp4"))
section_background_video = data_uri(Path("/Users/jose/Documents/workshop_website/assets/videos/section_background.mp4"))
platform_img = data_uri(ASSET_ROOT / "images-examples/15.png")
flow_img = data_uri(ASSET_ROOT / "images-examples/9.png")
stairs_img = data_uri(ASSET_ROOT / "images-examples/16.jpg")

consultancy_logo_files = {
    "accenture": "accenture-logo.webp",
    "acidlabs": "acidlabs-logo.png",
    "bcg": "bgc-logo.svg",
    "capgemini": "capgemini-logo.svg",
    "datatonic": "datatonic-logo.png",
    "deloitte": "deloitte-logo.webp",
    "endava": "endava-logo.png",
    "ey": "ey-logo.webp",
    "faculty": "faculty-logo.webp",
    "fractal": "fractal-logo.png",
    "kpmg": "kpmg-logo.webp",
    "making-science": "makingscience-logo.png",
    "mas-analytics": "masanalytics-logo.png",
    "mckinsey": "mckinsey-logo.png",
    "ml6": "ml6-logo.png",
    "onepoint": "onepoint-logo.webp",
    "pwc": "pwc-logo.webp",
    "quantiphi": "quantiphy-logo.png",
    "sia-partners": "sia-partners-logo.png",
    "tiger-analytics": "tiger-analytics-logo.png",
    "tredence": "tredence-logo.png",
    "unholster": "unholster-logo.webp",
    "unit8": "unit8-logo.png",
    "wavestone": "wavestone-logo.webp",
}
consultancy_logos = {
    key: data_uri(
        ROOT / f"assets/trimmed-consultancy-logos/{Path(filename).stem}-trimmed.png"
        if (ROOT / f"assets/trimmed-consultancy-logos/{Path(filename).stem}-trimmed.png").exists()
        else ASSET_ROOT / f"consultancy-logos/{filename}"
    )
    for key, filename in consultancy_logo_files.items()
    if (ASSET_ROOT / f"consultancy-logos/{filename}").exists()
}

generalist_logos = "".join([
    competitor_logo("McKinsey & Company", "mckinsey", 16, 18, 20),
    competitor_logo("BCG", "bcg", 53, 20, 17),
    competitor_logo("EY", "ey", 16, 50, 16),
    competitor_logo("Sia Partners", "sia-partners", 42, 47, 24),
    competitor_logo("Deloitte", "deloitte", 72, 55, 20),
    competitor_logo("PwC", "pwc", 14, 78, 15),
    competitor_logo("KPMG", "kpmg", 51, 77, 19),
])
it_consulting_logos = "".join([
    competitor_logo("Accenture", "accenture", 72, 12, 22),
    competitor_logo("Capgemini", "capgemini", 70, 32, 24),
    competitor_logo("Onepoint", "onepoint", 52, 58, 20),
    competitor_logo("Wavestone", "wavestone", 48, 78, 22),
    competitor_logo("Acid Labs", "acidlabs", 12, 82, 21),
])
next_gen_logos = "".join([
    competitor_logo("Fractal", "fractal", 42, 18, 22),
    competitor_logo("Tredence", "tredence", 28, 40, 22),
    competitor_logo("Quantiphi", "quantiphi", 60, 40, 22),
    competitor_logo("Tiger Analytics", "tiger-analytics", 18, 64, 26),
])
local_specialist_logos = "".join([
    competitor_logo("MAS Analytics", "mas-analytics", 20, 12, 20),
    competitor_logo("Unit8", "unit8", 25, 38, 16),
    competitor_logo("ML6", "ml6", 58, 37, 17),
    competitor_logo("Faculty", "faculty", 25, 62, 18),
    competitor_logo("Endava", "endava", 56, 61, 22),
    competitor_logo("Datatonic", "datatonic", 18, 83, 20),
    competitor_logo("Unholster", "unholster", 61, 82, 22),
    competitor_logo("Making Science", "making-science", 83, 68, 20),
])

positioning_groups = "\n".join([
    competitor_group("generalists", "Generalists with expertise in data and AI", 0.30, (12, 59, 25, 21), generalist_logos),
    competitor_group("it", "IT consulting firms specializing in data and AI", 0.42, (32, 35, 26, 22), it_consulting_logos),
    competitor_group("nextgen", "Next-Gen IT for Data & AI", 0.54, (66, 20, 25, 20), next_gen_logos),
    competitor_group("local", "Local specialists in various regions", 0.66, (58, 47, 28, 22), local_specialist_logos),
])

logo_paths = [
    ("HEINEKEN", ASSET_ROOT / "clients-logos/heineken-logo.png"),
    ("Carrefour", ASSET_ROOT / "clients-logos/carrefour-logo.png"),
    ("BNP Paribas", ASSET_ROOT / "clients-logos/bnp-paribas-logo.png"),
    ("Orange", ASSET_ROOT / "clients-logos/orange-logo.png"),
    ("Cencosud", ASSET_ROOT / "clients-logos/cencosud-logo.png"),
    ("FEMSA", ASSET_ROOT / "clients-logos/femsa-logo.png"),
    ("Santander", ASSET_ROOT / "clients-logos/santander-logo.png"),
    ("Nestle", ASSET_ROOT / "clients-logos/nestle-logo.png"),
    ("Unilever", ASSET_ROOT / "clients-logos/unilever-logo.png"),
    ("L'Oreal", ASSET_ROOT / "clients-logos/loreal-logo.png"),
    ("Aeromexico", ASSET_ROOT / "clients-logos/aeromexico-logo.png"),
    ("Bupa", ASSET_ROOT / "clients-logos/bupa-logo.png"),
    ("Danone", ASSET_ROOT / "clients-logos/danone-logo.png"),
    ("Mondelez", ASSET_ROOT / "clients-logos/mondelez-logo.png"),
    ("Agrosuper", ASSET_ROOT / "clients-logos/agrosuper-logo.png"),
]
logos = [logo_cell(name, data_uri(path)) for name, path in logo_paths if path.exists()]
logo_track = "\n".join(logos + logos)

industries = [
    "Financial Services",
    "Healthcare",
    "Retail",
    "B2B & Industries",
    "Consumer goods",
    "Travel and hospitality",
    "Automotive",
    "Media and entertainment",
    "Cosmetics and luxury",
    "Telecom and high tech",
    "Commodities and services",
    "Rent-a-car",
]

technical = [
    "AI and Agentic AI expertise",
    "Unified ecosystem orchestration",
    "Secure and cost-effective architectures",
    "Industrialization and scaling",
    "Applied AI Engineering",
]

business = [
    "Deep industry knowledge",
    "Value-driven solutions",
    "Expertise across functions",
    "Change management and adoption",
    "Data & AI governance",
]

html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Artefact | Data & AI</title>
  <link rel="icon" href="{a_icon}">
  <style>
    :root {{
      --navy:#002244;
      --deep:#0d1634;
      --mid:#273275;
      --purple:#752e7d;
      --magenta:#ff0066;
      --ink:#0f172a;
      --body:#475569;
      --muted:#94a3b8;
      --line:#e2e8f0;
      --soft:#f8fafc;
      --surface:#fff;
      --grad:linear-gradient(90deg,#002244 0%,#273275 34%,#752e7d 62%,#ff0066 100%);
      --shadow:0 28px 80px rgba(15,23,42,.14);
    }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{
      margin:0;
      font-family:Roboto, Arial, sans-serif;
      color:var(--ink);
      background:#000613;
      overflow-x:hidden;
    }}
    body.modal-open {{ overflow:hidden; }}
    img {{ max-width:100%; display:block; }}
    a {{ color:inherit; }}
    .top-band {{
      position:fixed;
      top:0;
      left:0;
      right:0;
      z-index:30;
      height:5px;
      background:var(--grad);
    }}
    .top-shell {{
      position:fixed;
      top:0;
      left:0;
      right:0;
      z-index:40;
      height:84px;
      display:flex;
      justify-content:center;
      align-items:flex-start;
      padding-top:16px;
      pointer-events:auto;
    }}
    .top-shell::after {{
      content:"";
      position:absolute;
      top:18px;
      left:50%;
      width:92px;
      height:4px;
      border-radius:999px;
      background:linear-gradient(90deg, rgba(0,34,68,.44), rgba(255,0,102,.72));
      box-shadow:0 8px 24px rgba(15,23,42,.18);
      opacity:0;
      transform:translateX(-50%) scaleX(.72);
      transition:opacity .24s ease, transform .24s ease;
    }}
    .brand-nav {{
      position:absolute;
      left:max(24px, calc(50% - 590px));
      display:flex;
      align-items:center;
      gap:12px;
      padding:0;
      border:0;
      border-radius:0;
      background:transparent;
      box-shadow:none;
      text-decoration:none;
      pointer-events:auto;
    }}
    .brand-nav img:first-child {{
      width:128px;
      height:auto;
      filter:brightness(0) invert(1);
    }}
    body[data-active-section="differentiators"] .brand-nav img:first-child {{
      filter:none;
    }}
    .brand-nav img:last-child {{ width:24px; height:24px; }}
    .top-menu {{
      display:flex;
      align-items:center;
      gap:4px;
      padding:6px;
      border:1px solid rgba(255,255,255,.12);
      border-radius:999px;
      background:rgba(8, 15, 31, .72);
      box-shadow:0 24px 64px rgba(0,0,0,.32);
      backdrop-filter:blur(14px) saturate(130%);
      -webkit-backdrop-filter:blur(14px) saturate(130%);
      pointer-events:auto;
      opacity:1;
      transform:translateY(0) scale(1);
      transition:opacity .24s ease, transform .24s ease, background .28s ease, border-color .28s ease;
      transform-origin:top center;
    }}
    body:not([data-active-section="hero"]) .top-menu {{
      opacity:0;
      transform:translateY(-18px) scale(.96);
      pointer-events:none;
    }}
    body:not([data-active-section="hero"]) .top-shell::after {{
      opacity:1;
      transform:translateX(-50%) scaleX(1);
    }}
    body:not([data-active-section="hero"]) .top-shell:hover .top-menu,
    body:not([data-active-section="hero"]) .top-shell:focus-within .top-menu {{
      opacity:1;
      transform:translateY(0) scale(1);
      pointer-events:auto;
    }}
    body:not([data-active-section="hero"]) .top-shell:hover::after,
    body:not([data-active-section="hero"]) .top-shell:focus-within::after {{
      opacity:0;
      transform:translateX(-50%) scaleX(.72);
    }}
    .top-menu a {{
      display:flex;
      align-items:center;
      justify-content:center;
      min-height:38px;
      padding:0 18px;
      border-radius:999px;
      color:rgba(255,255,255,.58);
      text-decoration:none;
      font-size:12px;
      font-weight:800;
      text-transform:uppercase;
      letter-spacing:.08em;
      border:1px solid transparent;
      white-space:nowrap;
      transition:background .28s ease, color .28s ease, border-color .28s ease, box-shadow .28s ease;
    }}
    .top-menu a:hover,
    .top-menu a:focus-visible,
    .top-menu a.active {{
      color:#fff;
      background:rgba(255,255,255,.06);
      border-color:rgba(255,255,255,.08);
      box-shadow:inset 0 1px 1px rgba(255,255,255,.06);
    }}
    .section {{ position:relative; }}
    .container {{
      width:min(1180px, calc(100% - 48px));
      margin:0 auto;
    }}
    .divider {{
      min-height:42vh;
      display:flex;
      align-items:center;
      color:#fff;
      background:
        radial-gradient(circle at 82% 20%, rgba(255,0,102,.32), transparent 38%),
        var(--grad);
    }}
    .divider h2 {{
      margin:0;
      font-size:clamp(34px, 7vw, 78px);
      line-height:.95;
      font-weight:300;
      letter-spacing:0;
      text-transform:uppercase;
    }}
    .section-transition {{
      position:relative;
      height:220vh;
      min-height:1280px;
      overflow:clip;
      background:transparent;
    }}
    .transition-stage {{
      position:sticky;
      top:0;
      height:100svh;
      min-height:640px;
      display:grid;
      place-items:center;
      isolation:isolate;
      overflow:hidden;
      background:
        radial-gradient(circle at 84% 18%, rgba(255,0,102,.12), transparent 30%),
        radial-gradient(circle at 18% 72%, rgba(39,50,117,.18), transparent 34%),
        linear-gradient(135deg,#000510 0%, #020b1e 46%, #061229 100%);
    }}
    .transition-video-wrap {{
      position:absolute;
      inset:0;
      z-index:0;
      transform:translate3d(0,0,0) scale(1.05);
      transform-origin:center;
      will-change:transform;
    }}
    .transition-video {{
      width:100%;
      height:100%;
      object-fit:cover;
      transform:scale(1.35);
      opacity:0;
      filter:blur(28px) saturate(.8) contrast(1.05) brightness(.42);
      will-change:opacity, filter;
    }}
    .transition-shade {{
      position:absolute;
      inset:0;
      z-index:1;
      background:
        linear-gradient(180deg, rgba(0,5,16,.72), rgba(0,5,16,.12) 48%, rgba(0,5,16,.76)),
        radial-gradient(circle at 50% 50%, transparent 0 34%, rgba(0,5,16,.25) 78%);
      pointer-events:none;
    }}
    .transition-title {{
      position:relative;
      z-index:2;
      width:min(1180px, calc(100% - 48px));
      color:#fff;
      text-align:left;
      opacity:0;
      transform:translate3d(0,34vh,0);
      will-change:transform, opacity;
    }}
    .transition-title h2 {{
      margin:0;
      max-width:1120px;
      font-size:clamp(54px, 8vw, 112px);
      line-height:.86;
      font-weight:300;
      letter-spacing:0;
      text-transform:uppercase;
      text-shadow:0 28px 80px rgba(0,0,0,.38);
    }}
    .transition-title h2::before {{
      content:"";
      display:block;
      width:82px;
      height:6px;
      margin-bottom:28px;
      border-radius:999px;
      background:var(--magenta);
    }}
    .transition-loader {{
      position:fixed;
      inset:0;
      z-index:60;
      display:grid;
      place-items:center;
      color:#fff;
      background:#000;
      font-size:24px;
      font-family:Roboto, Arial, sans-serif;
      transition:opacity .35s ease, visibility .35s ease;
    }}
    .transition-loader.is-hidden {{
      opacity:0;
      visibility:hidden;
      pointer-events:none;
    }}
    .eyebrow {{
      color:var(--magenta);
      font-size:12px;
      font-weight:800;
      letter-spacing:.08em;
      text-transform:uppercase;
    }}
    h1,h2,h3,p {{ margin-top:0; }}
    h1 {{
      font-size:clamp(42px, 7vw, 84px);
      line-height:.96;
      letter-spacing:0;
      max-width:920px;
      margin-bottom:24px;
    }}
    h2 {{
      font-size:clamp(32px, 5vw, 54px);
      line-height:1.03;
      letter-spacing:0;
      margin-bottom:18px;
    }}
    h3 {{
      font-size:22px;
      line-height:1.15;
      margin-bottom:12px;
    }}
    p, li {{
      color:var(--body);
      font-size:17px;
      line-height:1.58;
    }}
    .hero {{
      min-height:205vh;
      padding:0 0 84px;
      background:
        radial-gradient(circle at 78% 20%, rgba(255,0,102,.12), transparent 30%),
        radial-gradient(circle at 18% 72%, rgba(39,50,117,.18), transparent 34%),
        linear-gradient(135deg,#000510 0%, #020b1e 46%, #061229 100%);
      overflow:clip;
    }}
    .hero-grid {{
      position:sticky;
      top:0;
      min-height:100svh;
      display:grid;
      grid-template-columns:minmax(0,1.08fr) minmax(360px,.92fr);
      gap:clamp(30px, 4vw, 58px);
      align-items:center;
      padding-top:74px;
    }}
    .hero-copy-stack {{
      position:relative;
      min-height:clamp(430px, 66vh, 660px);
    }}
    .mission {{
      position:absolute;
      left:0;
      top:50%;
      width:100%;
      min-height:6.7em;
      max-width:900px;
      color:#fff;
      font-size:clamp(34px, 5.1vw, 62px);
      font-style:italic;
      padding-left:clamp(60px, 6.5vw, 96px);
      opacity:0;
      pointer-events:none;
      transform:translateY(calc(-50% + 22px));
      transition:opacity .42s ease, transform .42s ease;
    }}
    .mission.is-visible {{
      opacity:1;
      transform:translateY(-50%);
    }}
    .hero-message[data-hero-key="who"] {{
      top:45%;
      font-size:clamp(32px, 4.35vw, 52px);
    }}
    .hero-message[data-hero-key="who"].is-visible {{
      transform:translateY(-45%);
    }}
    .hero-message[data-hero-key="who"] .hero-period {{
      color:var(--magenta);
    }}
    .mission::before {{
      content:"\\201C";
      position:absolute;
      left:0;
      top:-0.17em;
      color:var(--magenta);
      font-size:2.35em;
      line-height:1;
      font-style:normal;
      font-weight:900;
    }}
    .mission strong {{ color:var(--magenta); }}
    .mission .type-caret {{
      display:inline-block;
      width:.08em;
      height:.82em;
      margin-left:.06em;
      background:var(--magenta);
      transform:translateY(.09em);
      animation:caret 880ms steps(1) infinite;
    }}
    .hero-copy {{
      max-width:850px;
      margin-top:18px;
      padding:28px;
      border-top:1px solid var(--line);
      border-radius:8px;
      background:rgba(255,255,255,.045);
      border:1px solid rgba(226,232,240,.14);
    }}
    .hero-copy p:first-of-type {{
      font-size:22px;
      color:var(--ink);
      font-weight:700;
    }}
    .hero-visual {{
      position:relative;
      min-height:650px;
      border-radius:10px;
      overflow:hidden;
      background:transparent;
      box-shadow:none;
      transform-style:preserve-3d;
      isolation:isolate;
      -webkit-mask-image:radial-gradient(ellipse 57% 76% at 54% 52%, #000 0 54%, rgba(0,0,0,.82) 66%, transparent 84%);
      mask-image:radial-gradient(ellipse 57% 76% at 54% 52%, #000 0 54%, rgba(0,0,0,.82) 66%, transparent 84%);
    }}
    .hero-visual::before {{
      content:"";
      position:absolute;
      inset:0;
      background:
        radial-gradient(circle at 42% 42%, rgba(255,0,102,.10), transparent 28%),
        linear-gradient(90deg, rgba(1,8,23,.62), transparent 38%, rgba(1,8,23,.38));
      z-index:1;
      mix-blend-mode:normal;
    }}
    .person-video {{
      width:100%;
      height:100%;
      min-height:650px;
      object-fit:cover;
      object-position:right bottom;
      filter:grayscale(0.03) saturate(1.08) contrast(1.26) brightness(0.86);
      opacity:.98;
      mix-blend-mode:multiply;
    }}
    .hero-visual .bridge {{
      position:absolute;
      z-index:2;
      left:22px;
      right:22px;
      bottom:22px;
      display:grid;
      grid-template-columns:1fr auto 1fr;
      align-items:center;
      gap:12px;
      color:#fff;
    }}
    .bridge strong {{
      display:block;
      font-size:18px;
      line-height:1;
    }}
    .bridge small {{
      color:rgba(255,255,255,.75);
      font-weight:700;
    }}
    .bridge-mark {{
      width:62px;
      height:62px;
      display:grid;
      place-items:center;
      border-radius:50%;
      background:rgba(255,255,255,.95);
    }}
    .bridge-mark img {{ width:36px; height:36px; min-height:0; object-fit:contain; }}
    .who-block {{
      margin-top:-30px;
      padding-bottom:10px;
    }}
    .sticky-chapter {{
      padding:96px 0;
      background:#fff;
    }}
    .chapter-grid {{
      display:grid;
      grid-template-columns:360px minmax(0,1fr);
      gap:48px;
      align-items:start;
    }}
    .chapter-aside {{
      position:sticky;
      top:96px;
    }}
    .chapter-aside p {{ font-size:18px; }}
    .scene {{
      min-height:72vh;
      display:grid;
      align-items:center;
      padding:38px 0;
      border-top:1px solid var(--line);
    }}
    .card, .service-card, .proof-card, .source-card {{
      border:1px solid var(--line);
      border-radius:8px;
      background:#fff;
      box-shadow:0 12px 34px rgba(15,23,42,.06);
    }}
    .card, .service-card {{ padding:24px; }}
    .card h3, .service-card h3, .proof-card h3 {{ color:var(--ink); }}
    .positioning {{
      display:grid;
      grid-template-columns:1fr 330px;
      gap:24px;
      align-items:stretch;
    }}
    #differentiators .sticky-chapter {{
      background:#f8fafc;
      color:var(--ink);
    }}
    #differentiators .chapter-aside h2,
    #differentiators .scene h2,
    #differentiators .card h3 {{
      color:var(--ink);
    }}
    #differentiators .chapter-aside p,
    #differentiators .card p,
    #differentiators .bullet-list li {{
      color:var(--body);
    }}
    .positioning-scrolly {{
      min-height:280vh;
      padding:0;
      border-top:0;
      align-items:start;
    }}
    .positioning-stage {{
      position:sticky;
      top:0;
      min-height:100svh;
      display:flex;
      flex-direction:column;
      justify-content:center;
      gap:14px;
      padding:82px 0 30px;
    }}
    .positioning-title {{
      max-width:1120px;
      margin:0 auto;
      width:100%;
    }}
    .positioning-title .eyebrow {{
      color:var(--magenta);
      margin-bottom:10px;
    }}
    .positioning-title h2 {{
      max-width:1000px;
      margin:0;
      color:var(--magenta) !important;
      font-size:clamp(34px, 4.2vw, 58px);
      line-height:1.02;
      font-weight:400;
      letter-spacing:0;
    }}
    .positioning-board {{
      position:relative;
      width:min(1120px, calc(100vw - 64px));
      height:clamp(520px, 62svh, 660px);
      margin:0 auto;
      border:1px solid rgba(15,23,42,.12);
      border-radius:18px;
      background:#fff;
      box-shadow:
        0 28px 80px rgba(15,23,42,.18),
        0 2px 8px rgba(15,23,42,.08);
      overflow:hidden;
      isolation:isolate;
    }}
    .positioning-axes {{
      position:absolute;
      inset:0;
      width:100%;
      height:100%;
      z-index:1;
      pointer-events:none;
    }}
    .axis-line {{
      stroke:var(--magenta);
      stroke-width:2.2;
      stroke-linecap:round;
      stroke-dasharray:1;
      stroke-dashoffset:calc(1 - var(--axis-progress, 0));
      transition:stroke-dashoffset .08s linear;
    }}
    .axis-arrow {{
      fill:var(--magenta);
      opacity:var(--axis-progress, 0);
    }}
    .axis-label {{
      position:absolute;
      z-index:2;
      color:var(--magenta);
      font-size:15px;
      line-height:1;
      font-weight:900;
      letter-spacing:0;
      opacity:var(--label-progress, 0);
      transform:translateY(calc((1 - var(--label-progress, 0)) * 10px));
      transition:opacity .12s linear, transform .12s linear;
    }}
    .axis-label.x {{
      right:6.6%;
      bottom:3.8%;
    }}
    .axis-label.y {{
      left:4.9%;
      top:26%;
      writing-mode:vertical-rl;
      transform:rotate(180deg) translateY(calc((1 - var(--label-progress, 0)) * -10px));
    }}
    .competitor-group {{
      position:absolute;
      left:calc(var(--x) * 1%);
      top:calc(var(--y) * 1%);
      width:calc(var(--w) * 1%);
      height:calc(var(--h) * 1%);
      z-index:4;
      opacity:var(--phase-progress, 0);
      transform:translate3d(0, calc((1 - var(--phase-progress, 0)) * 22px), 0);
      transition:opacity .12s linear, transform .12s linear;
    }}
    .competitor-group h3 {{
      position:absolute;
      left:50%;
      bottom:calc(100% + 10px);
      z-index:8;
      margin:0;
      max-width:260px;
      min-width:190px;
      padding:10px 12px;
      border:1px solid rgba(255,0,102,.22);
      border-radius:8px;
      background:#fff;
      box-shadow:0 18px 40px rgba(15,23,42,.16);
      color:var(--magenta);
      font-size:13px;
      line-height:1.14;
      font-weight:900;
      letter-spacing:0;
      opacity:0;
      pointer-events:none;
      transform:translate(-50%, 6px);
      transition:opacity .18s ease, transform .18s ease;
    }}
    .competitor-group.group-nextgen h3 {{
      top:calc(100% + 8px);
      bottom:auto;
    }}
    .competitor-group:hover h3,
    .competitor-group:focus-within h3 {{
      opacity:1;
      transform:translate(-50%, 0);
    }}
    .group-frame {{
      position:relative;
      width:100%;
      height:100%;
      min-height:96px;
      border:1.5px dotted rgba(255,0,102,.64);
      background:rgba(255,255,255,.42);
    }}
    .competitor-logo {{
      position:absolute;
      left:calc(var(--x) * 1%);
      top:calc(var(--y) * 1%);
      width:calc(var(--w) * 1%);
      transform:translate(-50%, -50%);
      display:grid;
      place-items:center;
    }}
    .competitor-logo img {{
      display:block;
      width:100%;
      max-height:34px;
      object-fit:contain;
      filter:grayscale(1) contrast(.95) brightness(.72);
      opacity:.78;
    }}
    .artefact-position {{
      position:absolute;
      right:3.6%;
      top:5.4%;
      z-index:5;
      width:218px;
      opacity:var(--artefact-progress, 0);
      transform:translate3d(0, calc((1 - var(--artefact-progress, 0)) * 20px), 0) scale(calc(.96 + var(--artefact-progress, 0) * .04));
      transition:opacity .12s linear, transform .12s linear;
    }}
    .artefact-position h3 {{
      margin:0 0 6px;
      color:var(--magenta);
      font-size:14px;
      line-height:1;
      font-weight:900;
      text-align:center;
    }}
    .artefact-badge {{
      display:grid;
      place-items:center;
      min-height:54px;
      background:#002244;
      box-shadow:0 18px 36px rgba(15,23,42,.18);
    }}
    .artefact-badge img:first-child {{
      width:128px;
      filter:brightness(0) invert(1);
    }}
    .positioning-detail-trigger {{
      position:absolute;
      right:1.2%;
      bottom:7.4%;
      z-index:6;
      width:54px;
      height:54px;
      display:grid;
      place-items:center;
      border:1px solid rgba(255,0,102,.26);
      border-radius:999px;
      background:#fff;
      box-shadow:0 16px 40px rgba(15,23,42,.18);
      cursor:pointer;
      opacity:var(--button-progress, 0);
      transform:translateY(calc((1 - var(--button-progress, 0)) * 14px));
      transition:opacity .12s linear, transform .12s linear, box-shadow .2s ease;
    }}
    .positioning-detail-trigger:hover,
    .positioning-detail-trigger:focus-visible {{
      box-shadow:0 18px 44px rgba(255,0,102,.22);
      outline:2px solid rgba(255,0,102,.36);
      outline-offset:3px;
    }}
    .positioning-detail-trigger img {{
      width:28px;
      height:28px;
    }}
    .matrix {{
      position:relative;
      min-height:390px;
      border:1px solid var(--line);
      border-radius:8px;
      background:
        linear-gradient(90deg, rgba(0,34,68,.06) 1px, transparent 1px),
        linear-gradient(0deg, rgba(0,34,68,.06) 1px, transparent 1px),
        linear-gradient(135deg, #fff, #f8fafc);
      background-size:64px 64px, 64px 64px, auto;
      overflow:hidden;
    }}
    .axis {{
      position:absolute;
      color:var(--body);
      font-size:12px;
      font-weight:800;
      letter-spacing:.08em;
      text-transform:uppercase;
    }}
    .axis.x {{ bottom:14px; left:50%; transform:translateX(-50%); }}
    .axis.y {{ left:-38px; top:50%; transform:rotate(-90deg) translateY(-50%); }}
    .zone {{
      position:absolute;
      padding:10px 12px;
      border-radius:8px;
      background:#fff;
      border:1px solid var(--line);
      color:var(--body);
      font-size:13px;
      font-weight:700;
      box-shadow:0 10px 24px rgba(15,23,42,.07);
    }}
    .zone.artefact {{
      right:38px;
      top:48px;
      color:#fff;
      background:var(--grad);
      border:0;
      transform:scale(1.08);
    }}
    .z1 {{ left:42px; bottom:74px; }}
    .z2 {{ left:145px; top:166px; }}
    .z3 {{ right:135px; top:122px; }}
    .z4 {{ left:85px; top:82px; }}
    .bullet-list {{
      display:grid;
      gap:10px;
      padding:0;
      margin:0;
      list-style:none;
    }}
    .bullet-list li {{
      position:relative;
      padding-left:22px;
      font-size:15px;
      line-height:1.38;
    }}
    .bullet-list li::before {{
      content:"";
      position:absolute;
      left:0;
      top:.62em;
      width:8px;
      height:8px;
      background:var(--magenta);
      border-radius:50%;
    }}
    .source-note {{
      margin-top:16px;
      color:#64748b;
      font-size:12px;
      line-height:1.45;
    }}
    .timeline {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:18px;
      position:relative;
    }}
    .timeline::before {{
      content:"";
      position:absolute;
      left:6%;
      right:6%;
      top:34px;
      height:3px;
      background:var(--grad);
    }}
    .time-card {{
      position:relative;
      z-index:1;
      padding:22px;
      border-radius:8px;
      border:1px solid var(--line);
      background:#fff;
      box-shadow:0 16px 38px rgba(15,23,42,.07);
    }}
    .time-dot {{
      width:18px;
      height:18px;
      border-radius:50%;
      background:var(--magenta);
      margin-bottom:18px;
      box-shadow:0 0 0 8px rgba(255,0,102,.1);
    }}
    .operating {{
      display:grid;
      grid-template-columns:1fr 260px 1fr;
      gap:22px;
      align-items:center;
    }}
    .node-list {{
      display:grid;
      gap:12px;
    }}
    .node {{
      padding:13px 14px;
      border:1px solid var(--line);
      border-radius:8px;
      background:#fff;
      color:var(--body);
      font-weight:700;
      font-size:14px;
    }}
    .core {{
      min-height:260px;
      display:grid;
      place-items:center;
      text-align:center;
      color:#fff;
      padding:26px;
      border-radius:50%;
      background:var(--grad);
      box-shadow:var(--shadow);
    }}
    .core img {{ width:64px; margin:0 auto 12px; filter:drop-shadow(0 8px 14px rgba(0,0,0,.18)); }}
    .stat-strip {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:18px;
    }}
    .source-card {{
      padding:24px;
      min-height:210px;
    }}
    .source-card .num {{
      display:block;
      color:var(--magenta);
      font-size:54px;
      font-weight:900;
      line-height:1;
      margin-bottom:12px;
    }}
    .diff-grid {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:18px;
      margin-top:28px;
    }}
    .presence {{
      background:var(--soft);
    }}
    .map-panel {{
      min-height:620px;
      display:grid;
      grid-template-columns:1fr 360px;
      gap:30px;
      align-items:center;
      padding:34px;
      border-radius:10px;
      background:#fff;
      border:1px solid var(--line);
      box-shadow:var(--shadow);
    }}
    .world {{
      position:relative;
      min-height:440px;
      border-radius:8px;
      overflow:hidden;
      background:
        radial-gradient(circle at 30% 45%, rgba(255,0,102,.24), transparent 18%),
        radial-gradient(circle at 55% 38%, rgba(39,50,117,.28), transparent 22%),
        linear-gradient(135deg,#0d1634,#273275 55%,#752e7d);
    }}
    .world img {{
      position:absolute;
      inset:0;
      width:100%;
      height:100%;
      object-fit:cover;
      opacity:.34;
      mix-blend-mode:screen;
    }}
    .map-svg {{
      position:absolute;
      inset:8%;
      opacity:.95;
    }}
    .pulse {{
      animation:pulse 2s infinite;
      transform-origin:center;
    }}
    .metric-grid {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:14px;
      margin-top:20px;
    }}
    .metric {{
      padding:18px;
      border-radius:8px;
      background:#fff;
      border:1px solid var(--line);
    }}
    .metric strong {{
      display:block;
      color:var(--navy);
      font-size:38px;
      line-height:1;
      margin-bottom:8px;
    }}
    .latam-list {{
      display:grid;
      grid-template-columns:repeat(2,1fr);
      gap:10px;
      margin-top:18px;
    }}
    .office {{
      padding:13px;
      border:1px solid var(--line);
      border-radius:8px;
      background:#fff;
      font-weight:800;
      color:var(--ink);
    }}
    .industry-grid {{
      display:grid;
      grid-template-columns:repeat(4,1fr);
      gap:10px;
      margin:26px 0;
    }}
    .industry {{
      min-height:58px;
      display:flex;
      align-items:center;
      padding:12px;
      border-radius:8px;
      border:1px solid var(--line);
      background:#fff;
      color:var(--body);
      font-weight:700;
      font-size:14px;
    }}
    .logo-marquee {{
      overflow:hidden;
      border:1px solid var(--line);
      border-radius:8px;
      background:#fff;
      padding:18px 0;
      mask-image:linear-gradient(90deg, transparent, #000 7%, #000 93%, transparent);
    }}
    .logo-track {{
      display:flex;
      width:max-content;
      animation:marquee 36s linear infinite;
    }}
    .logo-marquee:hover .logo-track {{ animation-play-state:paused; }}
    .logo-cell {{
      width:172px;
      height:68px;
      display:grid;
      place-items:center;
      padding:14px 22px;
      filter:grayscale(1);
      opacity:.78;
      transition:filter .2s ease, opacity .2s ease;
    }}
    .logo-cell:hover {{ filter:grayscale(0); opacity:1; }}
    .logo-cell img {{
      max-height:40px;
      max-width:126px;
      object-fit:contain;
    }}
    .heineken-trigger {{
      margin-top:28px;
      display:grid;
      grid-template-columns:120px minmax(0,1fr) auto;
      gap:20px;
      align-items:center;
      width:100%;
      padding:22px;
      border:1px solid rgba(0,34,68,.18);
      border-radius:8px;
      background:
        linear-gradient(120deg, rgba(0,34,68,.96), rgba(39,50,117,.92)),
        #0d1634;
      color:#fff;
      text-align:left;
      cursor:pointer;
      box-shadow:var(--shadow);
    }}
    .beer-mark {{
      height:116px;
      border-radius:8px;
      background:
        radial-gradient(circle at 50% 18%, #fff 0 12%, transparent 13%),
        linear-gradient(90deg, transparent 30%, rgba(255,255,255,.8) 31% 36%, transparent 37%),
        linear-gradient(180deg, #f5d46f, #d28f19 66%, #6f3e06);
      clip-path:polygon(28% 0,72% 0,78% 100%,22% 100%);
      box-shadow:inset 0 0 0 2px rgba(255,255,255,.28), 0 15px 38px rgba(0,0,0,.22);
    }}
    .heineken-trigger h3 {{ color:#fff; margin-bottom:6px; }}
    .heineken-trigger p {{ color:rgba(255,255,255,.76); margin:0; }}
    .arrow-pill {{
      width:46px;
      height:46px;
      border-radius:50%;
      display:grid;
      place-items:center;
      background:var(--magenta);
      font-size:25px;
    }}
    .offering {{
      background:#fff;
    }}
    .pillar-wrap {{
      display:grid;
      grid-template-columns:430px minmax(0,1fr);
      gap:42px;
      align-items:start;
    }}
    .pyramid {{
      position:sticky;
      top:100px;
      min-height:470px;
      display:grid;
      place-items:center;
      border-radius:10px;
      overflow:hidden;
      background:var(--deep);
      box-shadow:var(--shadow);
    }}
    .pyramid img {{
      position:absolute;
      inset:0;
      width:100%;
      height:100%;
      object-fit:cover;
      opacity:.32;
    }}
    .pyramid-levels {{
      position:relative;
      z-index:1;
      width:min(330px, 80%);
      display:flex;
      flex-direction:column;
      gap:8px;
      transform:rotate(-8deg);
    }}
    .level {{
      min-height:64px;
      display:grid;
      place-items:center;
      color:#fff;
      text-align:center;
      font-weight:900;
      font-size:13px;
      text-transform:uppercase;
      background:linear-gradient(90deg, #002244, #273275, #ff0066);
      clip-path:polygon(12% 0,88% 0,100% 100%,0 100%);
      opacity:.48;
      transition:opacity .25s ease, transform .25s ease;
    }}
    [data-active-pillar="vision"] .level:nth-child(1),
    [data-active-pillar="model"] .level:nth-child(2),
    [data-active-pillar="data"] .level:nth-child(3),
    [data-active-pillar="change"] .level:nth-child(4) {{
      opacity:1;
      transform:scale(1.04);
    }}
    .pillar-card {{
      min-height:54vh;
      display:grid;
      align-content:center;
      padding:28px;
      border-top:1px solid var(--line);
    }}
    .proof-grid {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:18px;
      margin-top:28px;
    }}
    .proof-card {{
      padding:24px;
    }}
    .service-grid {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:18px;
      margin-top:28px;
    }}
    .service-icon {{
      width:42px;
      height:42px;
      border-radius:8px;
      background:var(--grad);
      margin-bottom:16px;
    }}
    .ecosystem {{
      margin-top:36px;
      display:grid;
      grid-template-columns:1fr 1.3fr;
      gap:24px;
      align-items:stretch;
    }}
    .clouds {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:12px;
    }}
    .clouds span {{
      display:grid;
      place-items:center;
      min-height:74px;
      border:1px solid var(--line);
      border-radius:8px;
      background:#fff;
      font-weight:900;
      color:var(--navy);
    }}
    .adopt {{
      color:#fff;
      background:
        linear-gradient(90deg, rgba(0,34,68,.95), rgba(39,50,117,.82), rgba(255,0,102,.7)),
        url("{flow_img}") center/cover;
    }}
    .adopt p {{ color:rgba(255,255,255,.82); }}
    .event-grid {{
      display:grid;
      grid-template-columns:1.1fr .9fr;
      gap:30px;
      align-items:start;
      padding:100px 0;
    }}
    .event-panel {{
      padding:28px;
      border:1px solid rgba(255,255,255,.24);
      border-radius:8px;
      background:rgba(13,22,52,.62);
    }}
    .tbd-grid {{
      display:grid;
      grid-template-columns:repeat(2,1fr);
      gap:10px;
      margin-top:22px;
    }}
    .tbd {{
      padding:13px;
      border-radius:8px;
      background:rgba(255,255,255,.1);
      border:1px solid rgba(255,255,255,.16);
      font-weight:800;
    }}
    .previous {{
      display:grid;
      grid-template-columns:repeat(5,1fr);
      gap:10px;
      margin-top:20px;
    }}
    .previous div {{
      padding:16px 10px;
      border-radius:8px;
      background:rgba(255,255,255,.1);
      text-align:center;
    }}
    .previous strong {{
      display:block;
      font-size:28px;
      line-height:1;
    }}
    .contact {{
      padding:100px 0;
      background:#fff;
    }}
    .contact-wrap {{
      display:grid;
      grid-template-columns:1fr 1fr;
      gap:26px;
      align-items:stretch;
      margin-top:28px;
    }}
    .contact-card {{
      padding:28px;
      border:1px solid var(--line);
      border-radius:8px;
      background:#fff;
      box-shadow:0 14px 40px rgba(15,23,42,.07);
    }}
    .contact-card a {{
      color:var(--magenta);
      font-weight:900;
      overflow-wrap:anywhere;
    }}
    footer {{
      padding:26px 0;
      color:#fff;
      background:transparent;
    }}
    footer .container {{
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:20px;
    }}
    footer img {{ width:112px; filter:brightness(0) invert(1); }}
    .reveal {{
      opacity:0;
      transform:translateY(18px);
      transition:opacity .55s ease, transform .55s ease;
    }}
    .reveal.visible {{
      opacity:1;
      transform:translateY(0);
    }}
    dialog {{
      width:min(1060px, calc(100% - 32px));
      max-height:92vh;
      border:0;
      border-radius:10px;
      padding:0;
      box-shadow:0 30px 100px rgba(15,23,42,.34);
      overflow:hidden;
    }}
    dialog::backdrop {{ background:rgba(2,6,23,.62); }}
    .modal-body {{
      max-height:92vh;
      overflow:auto;
      padding:34px;
      background:#fff;
    }}
    .modal-head {{
      display:flex;
      justify-content:space-between;
      gap:20px;
      align-items:flex-start;
      border-bottom:1px solid var(--line);
      padding-bottom:18px;
      margin-bottom:22px;
    }}
    .close {{
      border:1px solid var(--line);
      background:#fff;
      color:var(--ink);
      border-radius:8px;
      min-width:44px;
      height:44px;
      font-size:24px;
      cursor:pointer;
    }}
    .positioning-modal {{
      width:min(1240px, calc(100% - 32px));
    }}
    .positioning-modal .modal-body {{
      color:#fff;
      padding:28px 34px 30px;
      background:
        radial-gradient(circle at 82% 0%, rgba(255,0,102,.28), transparent 34%),
        linear-gradient(135deg,#000613 0%, #061229 52%, #160015 100%);
    }}
    .positioning-modal .modal-head {{
      align-items:flex-start;
      border-bottom-color:rgba(226,232,240,.18);
      margin-bottom:26px;
    }}
    .modal-brand {{
      display:flex;
      align-items:center;
      gap:12px;
      margin-bottom:12px;
    }}
    .modal-brand img:first-child {{
      width:142px;
      filter:brightness(0) invert(1);
    }}
    .modal-brand img:last-child {{
      width:24px;
      height:24px;
    }}
    .positioning-modal .modal-head h2 {{
      max-width:980px;
      color:#fff;
      font-size:clamp(36px, 4.1vw, 56px);
      line-height:.96;
      letter-spacing:0;
    }}
    .positioning-modal .close {{
      border-color:rgba(255,255,255,.22);
      background:rgba(255,255,255,.06);
      color:#fff;
    }}
    .archetype-comparison {{
      display:grid;
      grid-template-columns:minmax(0,1.05fr) minmax(360px,.95fr);
      border:1px solid rgba(255,255,255,.14);
      border-radius:22px;
      overflow:hidden;
      background:rgba(255,255,255,.05);
      box-shadow:0 28px 78px rgba(0,0,0,.32);
    }}
    .comparison-head {{
      padding:26px 28px 18px;
    }}
    .comparison-head h3 {{
      margin:0;
      color:#fff;
      font-size:clamp(24px, 2.3vw, 34px);
      line-height:1.08;
      letter-spacing:0;
    }}
    .comparison-head.competitor-head {{
      background:rgba(255,255,255,.04);
    }}
    .comparison-head.artefact-head {{
      display:flex;
      align-items:center;
      justify-content:flex-start;
      background:linear-gradient(145deg, rgba(255,0,102,.72), rgba(117,46,125,.68) 58%, rgba(39,50,117,.5));
    }}
    .comparison-head .artefact-lockup {{
      width:250px;
      padding:0;
      background:transparent;
      box-shadow:none;
      opacity:.94;
      filter:drop-shadow(0 14px 30px rgba(0,0,0,.22));
    }}
    .comparison-head .artefact-lockup img {{
      width:100%;
      filter:brightness(0) invert(1);
    }}
    .comparison-row {{
      display:grid;
      grid-column:1 / -1;
      grid-template-columns:minmax(0,1.05fr) minmax(360px,.95fr);
      border-top:1px dashed rgba(255,255,255,.66);
    }}
    .comparison-row:first-of-type {{ border-top:1px dashed rgba(255,255,255,.66); }}
    .competitor-cell {{
      display:grid;
      grid-template-columns:minmax(150px,.85fr) minmax(0,1fr);
      gap:22px;
      padding:15px 28px;
      background:rgba(255,255,255,.04);
    }}
    .artefact-cell {{
      padding:15px 28px 15px 34px;
      background:linear-gradient(145deg, rgba(255,0,102,.72), rgba(117,46,125,.68) 58%, rgba(39,50,117,.5));
    }}
    .competitor-cell strong {{
      color:#fff;
      font-size:17px;
      line-height:1.12;
    }}
    .competitor-cell p {{
      margin:0;
      color:rgba(255,255,255,.78);
      font-size:16px;
      line-height:1.28;
    }}
    .artefact-cell ul {{
      margin:0;
      padding:0 0 0 22px;
      color:#fff;
      font-size:15px;
      line-height:1.18;
    }}
    .artefact-cell li + li {{ margin-top:4px; }}
    .modal-metrics {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:14px;
      margin:24px 0;
    }}
    .archetype-grid {{
      display:grid;
      grid-template-columns:repeat(2, minmax(0,1fr));
      gap:14px;
      margin-top:22px;
    }}
    .archetype-card {{
      padding:18px;
      border:1px solid var(--line);
      border-radius:8px;
      background:#fff;
      box-shadow:0 12px 28px rgba(15,23,42,.06);
    }}
    .archetype-card h3 {{
      margin:0 0 8px;
      color:var(--ink);
      font-size:18px;
    }}
    .archetype-card p {{
      margin:0;
      color:var(--body);
      font-size:14px;
      line-height:1.45;
    }}
    .archetype-card.highlight {{
      border-color:rgba(255,0,102,.28);
      background:linear-gradient(135deg, rgba(255,0,102,.08), #fff 42%);
    }}
    .journey {{
      display:grid;
      grid-template-columns:repeat(5,1fr);
      gap:12px;
      margin:18px 0 26px;
    }}
    .journey div {{
      padding:14px;
      border-radius:8px;
      border:1px solid var(--line);
      background:var(--soft);
      font-weight:800;
      color:var(--ink);
      font-size:14px;
    }}
    .usecases {{
      columns:2;
      column-gap:32px;
      padding-left:18px;
    }}
    button:focus-visible, a:focus-visible {{
      outline:3px solid rgba(255,0,102,.5);
      outline-offset:3px;
    }}
    body {{
      color:#f8fafc;
      background:
        radial-gradient(circle at 84% 12%, rgba(255,0,102,.12), transparent 28%),
        radial-gradient(circle at 18% 42%, rgba(39,50,117,.18), transparent 34%),
        linear-gradient(135deg,#000510 0%, #020b1e 48%, #061229 100%);
      background-attachment:fixed;
    }}
    p, li {{ color:#cbd5e1; }}
    h1, h2, h3 {{ color:#f8fafc; }}
    .hero {{ background:transparent; }}
    .mission strong {{ color:#ff2f83; }}
    .hero-copy {{
      border-top-color:rgba(226,232,240,.22);
    }}
    .hero-copy p:first-of-type {{
      color:#fff;
    }}
    .hero-visual {{
      border:0;
      box-shadow:none;
    }}
    .divider {{
      background:
        radial-gradient(circle at 84% 18%, rgba(255,0,102,.12), transparent 30%),
        radial-gradient(circle at 18% 70%, rgba(39,50,117,.14), transparent 30%);
    }}
    .sticky-chapter {{ background:transparent; }}
    .chapter-aside p,
    .event-panel p,
    .contact p {{ color:#cbd5e1; }}
    .scene,
    .pillar-card {{
      border-top-color:rgba(226,232,240,.16);
    }}
    .card, .service-card, .proof-card, .source-card {{
      background:rgba(255,255,255,.055);
      border-color:rgba(226,232,240,.18);
      box-shadow:0 24px 70px rgba(0,0,0,.24);
    }}
    .card h3, .service-card h3, .proof-card h3 {{ color:#fff; }}
    .matrix {{
      border-color:rgba(226,232,240,.18);
      background:
        linear-gradient(90deg, rgba(255,255,255,.07) 1px, transparent 1px),
        linear-gradient(0deg, rgba(255,255,255,.07) 1px, transparent 1px),
        linear-gradient(135deg, rgba(255,255,255,.06), rgba(255,255,255,.025));
    }}
    .axis {{ color:#cbd5e1; }}
    .zone {{
      background:rgba(255,255,255,.09);
      border-color:rgba(226,232,240,.18);
      color:#e2e8f0;
      box-shadow:0 14px 34px rgba(0,0,0,.2);
    }}
    .time-card,
    .node,
    .metric,
    .office,
    .industry,
    .contact-card {{
      background:rgba(255,255,255,.06);
      border-color:rgba(226,232,240,.18);
      color:#f8fafc;
      box-shadow:0 20px 55px rgba(0,0,0,.22);
    }}
    .node,
    .office,
    .industry {{ color:#f8fafc; }}
    .source-note {{ color:#94a3b8; }}
    .presence {{ background:transparent; }}
    .map-panel {{
      background:
        linear-gradient(135deg, rgba(255,255,255,.07), rgba(255,255,255,.025));
      border-color:rgba(226,232,240,.18);
      box-shadow:0 34px 90px rgba(0,0,0,.34);
    }}
    .metric strong {{
      color:#fff;
    }}
    .logo-marquee {{
      background:rgba(255,255,255,.06);
      border-color:rgba(226,232,240,.16);
    }}
    .logo-cell {{
      background:rgba(255,255,255,.92);
      border-radius:8px;
      margin:0 7px;
      filter:grayscale(1);
      opacity:.86;
    }}
    .offering {{ background:transparent; }}
    .pyramid {{
      border:1px solid rgba(255,255,255,.16);
      box-shadow:0 34px 90px rgba(0,0,0,.34);
    }}
    .clouds span {{
      background:rgba(255,255,255,.06);
      border-color:rgba(226,232,240,.18);
      color:#fff;
    }}
    .contact {{ background:transparent; }}
    .contact-card a {{ color:#ff4f98; }}
    dialog {{
      background:#010817;
    }}
    .modal-body {{
      background:
        radial-gradient(circle at 88% 0%, rgba(255,0,102,.12), transparent 28%),
        linear-gradient(180deg,#010817,#07152d);
      color:#f8fafc;
    }}
    .modal-head {{
      border-bottom-color:rgba(226,232,240,.16);
    }}
    .close {{
      background:rgba(255,255,255,.08);
      color:#fff;
      border-color:rgba(226,232,240,.22);
    }}
    .journey div {{
      background:rgba(255,255,255,.06);
      border-color:rgba(226,232,240,.18);
      color:#f8fafc;
    }}
    @keyframes rise {{
      to {{ opacity:1; transform:translateY(0); }}
    }}
    @keyframes caret {{
      0%, 48% {{ opacity:1; }}
      49%, 100% {{ opacity:0; }}
    }}
    @keyframes pulse {{
      0%,100% {{ opacity:.68; transform:scale(1); }}
      50% {{ opacity:1; transform:scale(1.18); }}
    }}
    @keyframes marquee {{
      from {{ transform:translateX(0); }}
      to {{ transform:translateX(-50%); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      *, *::before, *::after {{
        animation-duration:.01ms !important;
        animation-iteration-count:1 !important;
        scroll-behavior:auto !important;
        transition-duration:.01ms !important;
      }}
      .reveal {{ opacity:1; transform:none; }}
      .logo-track {{ animation:none; flex-wrap:wrap; width:auto; justify-content:center; }}
    }}
    @media (max-width: 980px) {{
      .top-shell {{
        top:0;
        height:76px;
        padding:12px 16px 0;
      }}
      .brand-nav {{ left:16px; }}
      .brand-nav img:first-child {{ width:116px; }}
      .top-menu {{
        max-width:min(100%, calc(100vw - 32px));
        overflow-x:auto;
        scrollbar-width:none;
      }}
      .top-menu::-webkit-scrollbar {{ display:none; }}
      .top-menu a {{ flex:0 0 auto; }}
      .container {{ width:min(100% - 32px, 720px); }}
      .section-transition {{
        height:168vh;
        min-height:980px;
      }}
      .transition-stage {{ min-height:560px; }}
      .transition-title {{ width:calc(100% - 32px); }}
      .transition-title h2 {{
        font-size:clamp(46px, 13vw, 80px);
      }}
      .positioning-scrolly {{ min-height:240vh; }}
      .positioning-stage {{
        padding:118px 0 36px;
        gap:14px;
      }}
      .positioning-board {{
        width:calc(100vw - 32px);
        height:min(640px, 72svh);
        border-radius:14px;
      }}
      .positioning-title h2 {{ font-size:clamp(34px, 9vw, 50px); }}
      .axis-label {{ font-size:12px; }}
      .axis-label.y {{ left:5%; top:23%; }}
      .axis-label.x {{ right:5%; bottom:4%; }}
      .competitor-group h3 {{ font-size:11px; }}
      .competitor-logo img {{ max-height:24px; }}
      .artefact-position {{
        width:148px;
        right:3%;
        top:5.5%;
      }}
      .artefact-position h3 {{ font-size:10px; }}
      .artefact-badge {{
        min-height:42px;
      }}
      .artefact-badge img:first-child {{
        width:92px;
      }}
      .positioning-detail-trigger {{
        width:46px;
        height:46px;
        right:2%;
        bottom:8%;
      }}
      .archetype-comparison {{
        grid-template-columns:1fr;
        border-radius:14px;
      }}
      .comparison-head {{ padding:22px; }}
      .artefact-head {{ grid-row:3; }}
      .comparison-row {{
        grid-template-columns:1fr;
      }}
      .competitor-cell {{
        grid-template-columns:1fr;
        padding:18px 22px;
      }}
      .artefact-cell {{ padding:18px 22px; }}
      .competitor-cell strong {{ font-size:18px; }}
      .competitor-cell p,
      .artefact-cell ul {{ font-size:16px; }}
      .positioning-modal .modal-head h2 {{
        font-size:clamp(38px, 10vw, 54px);
      }}
      .hero {{ padding-top:0; }}
      .hero-grid {{
        align-items:start;
        padding-top:132px;
      }}
      .hero-copy-stack {{ min-height:360px; }}
      .mission {{
        top:0;
        min-height:0;
        padding-left:clamp(34px, 9vw, 48px);
        transform:translateY(18px);
      }}
      .mission.is-visible {{ transform:none; }}
      .hero-message[data-hero-key="who"] {{
        top:0;
        font-size:clamp(32px, 9vw, 40px);
      }}
      .hero-message[data-hero-key="who"].is-visible {{ transform:none; }}
      .mission::before {{
        top:-.08em;
        font-size:1.72em;
      }}
      .hero-grid, .chapter-grid, .positioning, .operating, .map-panel, .pillar-wrap, .ecosystem, .event-grid {{
        grid-template-columns:1fr;
      }}
      .hero-visual, .person-video {{ min-height:460px; }}
      .chapter-aside, .pyramid {{ position:relative; top:auto; }}
      .scene {{ min-height:auto; }}
      .timeline, .stat-strip, .diff-grid, .metric-grid, .proof-grid, .service-grid, .contact-wrap, .modal-metrics {{
        grid-template-columns:1fr;
      }}
      .industry-grid, .latam-list, .tbd-grid, .clouds {{
        grid-template-columns:repeat(2,1fr);
      }}
      .previous {{ grid-template-columns:repeat(2,1fr); }}
      .journey {{ grid-template-columns:1fr; }}
      .usecases {{ columns:1; }}
      .heineken-trigger {{ grid-template-columns:82px 1fr; }}
      .heineken-trigger .arrow-pill {{ display:none; }}
    }}
    @media (max-width: 560px) {{
      h1 {{ font-size:40px; }}
      .brand-nav {{ top:2px; transform:scale(.94); transform-origin:left center; }}
      .top-menu {{ padding:5px; }}
      .top-menu a {{
        min-height:34px;
        padding:0 14px;
        font-size:11px;
      }}
      .hero-visual, .person-video {{ min-height:390px; }}
      .bridge {{ grid-template-columns:1fr !important; }}
      .bridge-mark {{ display:none; }}
      .divider {{ min-height:30vh; }}
      .section-transition {{
        height:150vh;
        min-height:880px;
      }}
      .transition-title h2 {{ font-size:clamp(38px, 13vw, 58px); }}
      .industry-grid, .latam-list, .tbd-grid, .previous, .clouds {{ grid-template-columns:1fr; }}
      .modal-body {{ padding:22px; }}
      footer .container {{ align-items:flex-start; flex-direction:column; }}
    }}
  </style>
</head>
<body data-active-pillar="vision" data-active-section="hero">
  <div class="transition-loader" data-transition-loader>Loading... <span data-transition-progress>0</span>%</div>
  <div class="top-band"></div>
  <header class="top-shell">
    <a class="brand-nav" href="#hero" aria-label="Artefact">
      <img src="{wordmark}" alt="Artefact">
      <img src="{a_icon}" alt="">
    </a>
    <nav class="top-menu" aria-label="Sections">
      <a href="#hero">Mission</a>
      <a href="#differentiators">Key Differentiators</a>
      <a href="#presence">Presence</a>
      <a href="#offering">Offering</a>
      <a href="#adopt-ai">Adopt AI</a>
      <a href="#contact">Contact</a>
    </nav>
  </header>

  <main>
    <section id="hero" class="hero section">
      <div class="container hero-grid">
        <div class="hero-copy-stack" data-hero-copy-stack>
          <h1 class="mission hero-message is-visible" data-hero-message data-hero-key="mission" data-typewriter="We accelerate the adoption of data and AI to positively impact people and organizations." data-emphasis="data and AI" aria-label="We accelerate the adoption of data and AI to positively impact people and organizations."></h1>
          <h1 class="mission hero-message" data-hero-message data-hero-key="who" data-typewriter="Artefact is an end-to-end specialized Data &amp; AI consulting company bridging the gap between Business &amp; Technology." data-emphasis="bridging the gap between Business &amp; Technology" aria-label="Artefact is an end-to-end specialized Data & AI consulting company bridging the gap between Business & Technology."></h1>
        </div>
        <div class="hero-visual" data-person-video-wrap aria-hidden="true">
          <video class="person-video" data-person-video muted playsinline preload="auto" loop src="{person_video}"></video>
        </div>
      </div>
    </section>

    <section id="differentiators" class="section">
      {section_transition("Key Differentiators")}
      <div class="sticky-chapter">
        <div class="container">
          <article class="scene positioning-scrolly" data-positioning-chart>
            <div class="positioning-stage">
              <div class="positioning-title">
                <div class="eyebrow">Market positioning</div>
                <h2>We are the world's leading pure player consulting firm in Data & AI.</h2>
              </div>
              <div class="positioning-board" aria-label="Market positioning matrix comparing Artefact with consulting competitors">
                <svg class="positioning-axes" viewBox="0 0 1000 690" preserveAspectRatio="none" aria-hidden="true">
                  <defs>
                    <marker id="axis-arrowhead" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth">
                      <path d="M0,0 L10,5 L0,10 Z" class="axis-arrow"></path>
                    </marker>
                  </defs>
                  <path class="axis-line axis-y-line" pathLength="1" d="M80 622 L80 74" marker-end="url(#axis-arrowhead)"></path>
                  <path class="axis-line axis-x-line" pathLength="1" d="M80 622 L922 622" marker-end="url(#axis-arrowhead)"></path>
                </svg>
                <div class="axis-label y">End-to-end services</div>
                <div class="axis-label x">Level of Specialization in Data/AI</div>
                {positioning_groups}
                <div class="artefact-position" data-chart-phase="0.78">
                  <h3>Pure Player - Market Leader</h3>
                  <div class="artefact-badge">
                    <img src="{wordmark}" alt="Artefact">
                  </div>
                </div>
                <button class="positioning-detail-trigger" type="button" data-case-trigger="positioning" data-chart-phase="0.86" aria-label="Open competitor archetype details">
                  <img src="{a_icon}" alt="">
                </button>
              </div>
              <p class="source-note">Source note: Independent analysis by McKinsey and BCG conducted during the acquisition of Artefact by the investment fund Cinven.</p>
            </div>
          </article>
          <div class="chapter-grid">
            <aside class="chapter-aside">
              <div class="eyebrow">Why Artefact</div>
              <h2>The leading pure player turns AI ambition into deployed business value.</h2>
              <p>Artefact combines a high level of specialization in Data & AI with the ability to deliver end-to-end services, including specific business expertise and Data/AI implementation.</p>
            </aside>
            <div>
            <article class="scene">
              <div>
                <h2>Agents and GenAI expertise started well before the hype.</h2>
                <p>Artefact was already working on early GenAI premises and use cases before ChatGPT. We are now supporting large players in the deployment of their Agentic programs.</p>
                <div class="timeline">
                  <div class="time-card reveal"><div class="time-dot"></div><h3>Before ChatGPT</h3><p>Augmented agents for call centers, product data enrichment, product entity matching, and early enterprise experimentation with GPT models.</p></div>
                  <div class="time-card reveal"><div class="time-dot"></div><h3>2021-2023</h3><p>The acceleration of GenAI created new opportunities to design and deploy enterprise-grade AI solutions.</p></div>
                  <div class="time-card reveal"><div class="time-dot"></div><h3>2024 onwards</h3><p>Enterprise-wide Agentic programs now design, deploy, and scale autonomous AI agents.</p></div>
                </div>
              </div>
            </article>
            <article class="scene">
              <div>
                <h2>A unique operating model bridges business depth and technical expertise.</h2>
                <div class="operating">
                  <div class="node-list reveal">{''.join(f'<div class="node">{item}</div>' for item in business)}</div>
                  <div class="core reveal"><div><img src="{a_icon}" alt=""><strong>AI-native solutions that deliver immediate impact and sustainable competitive advantage.</strong></div></div>
                  <div class="node-list reveal">{''.join(f'<div class="node">{item}</div>' for item in technical)}</div>
                </div>
              </div>
            </article>
            <article class="scene">
              <div>
                <h2>The AI revolution is exploding, and Artefact is leading the shift in the corporate space.</h2>
                <div class="stat-strip">
                  <div class="source-card reveal"><span class="num">37%</span><p>of IT executives at $1B+ companies are already deploying AI agents.</p><p class="source-note">Source: UiPath.</p></div>
                  <div class="source-card reveal"><span class="num">83%</span><p>of automation leaders plan to accelerate Agentic AI investment in the next 12 months.</p><p class="source-note">Source: Forrester.</p></div>
                  <div class="source-card reveal"><span class="num">33%</span><p>of enterprise software applications will embed Agentic AI capabilities in their solutions by 2028.</p><p class="source-note">Source: Gartner.</p></div>
                </div>
                <div class="diff-grid">
                  {card("AI & Agentic Pure Player", "Unlike other consultancies, we do not split focus. We master the bleeding edge of Agentic & AI solutions to deliver end-to-end, state-of-the-art, value-driven solutions.")}
                  {card("Business-First Depth", "We solve real business problems. We understand industry-specific workflows, creating alignment of interest through outcome-based commitment.")}
                  {card("Anti-Vendor Lock-In", "We preserve your intellectual independence and prevent dependence on a single tech provider to run core corporate processes.")}
                  {card("All Clouds & LLM Providers", "We design completely agnostic architectures across Google, AWS, Microsoft, and any foundational or LLM tool.")}
                  {card("The Power Of The Harness", "Models are becoming commodities. Our value sits in clean data environments, integrations, orchestration, and guardrails.")}
                  {card("Designed For Portability", "We architect multi-provider portability for technology, regulation, geopolitics, and national-security volatility.")}
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
      </div>
    </section>

    <section id="presence" class="presence section">
      {section_transition("Presence")}
      <div class="sticky-chapter">
        <div class="container">
          <div class="map-panel reveal">
            <div class="world">
              <img src="{platform_img}" alt="">
              <svg class="map-svg" viewBox="0 0 900 430" role="img" aria-label="Global and LATAM footprint">
                <path d="M108 120 C166 72 234 76 302 110 C362 138 395 108 442 92 C514 66 608 74 690 116 C778 160 806 234 756 292 C708 348 602 350 516 310 C452 280 408 276 344 316 C258 368 142 348 82 284 C28 226 48 164 108 120Z" fill="rgba(255,255,255,.14)" stroke="rgba(255,255,255,.55)" stroke-width="2"/>
                <circle class="pulse" cx="314" cy="282" r="18" fill="#ff0066"/>
                <circle cx="314" cy="282" r="5" fill="#fff"/>
                <path d="M314 282 C390 230 514 222 626 170" fill="none" stroke="#ff0066" stroke-width="3" stroke-dasharray="8 8"/>
                <path d="M314 282 C260 210 205 180 145 146" fill="none" stroke="#fff" stroke-width="2" stroke-dasharray="7 8" opacity=".7"/>
              </svg>
            </div>
            <div>
              <div class="eyebrow">Global footprint</div>
              <h2>Artefact operates globally and scales with LATAM depth.</h2>
              <p>Artefact is a leading global partner in Data & AI consulting, with the critical mass required to support transformation at scale.</p>
              <div class="metric-grid">
                <div class="metric"><strong data-count="27">27</strong><span>countries</span></div>
                <div class="metric"><strong data-count="2500">2,500</strong><span>employees</span></div>
                <div class="metric"><strong data-count="36">36</strong><span>offices</span></div>
              </div>
              <p style="margin-top:22px;"><strong>In LATAM, Artefact has more than 400 Artefactors and 4 offices.</strong></p>
              <div class="latam-list">
                <div class="office">Sao Paulo<br><small>250 Artefactors</small></div>
                <div class="office">Mexico City</div>
                <div class="office">Santiago</div>
                <div class="office">Bogota</div>
              </div>
            </div>
          </div>

          <div style="padding-top:80px;">
            <div class="eyebrow">Industries and regional partners</div>
            <h2>Artefact works across sectors where data, AI, and adoption unlock measurable value.</h2>
            <p>Our 1000+ clients, including 300 international brands, trust us across banking, insurance, travel, hospitality, automotive, media, entertainment, cosmetics, luxury, telecom, high tech, commodities, services, retail, selective distribution, consumer packaged goods, healthcare, and mobility.</p>
            <div class="industry-grid">{''.join(f'<div class="industry reveal">{item}</div>' for item in industries)}</div>
            <div class="logo-marquee" aria-label="Selected client logos"><div class="logo-track">{logo_track}</div></div>
            <button class="heineken-trigger reveal" type="button" data-case-trigger="heineken">
              <span class="beer-mark" aria-hidden="true"></span>
              <span><h3>Our History With HEINEKEN</h3><p>A multi-year Advanced Analytics journey that created products throughout the entire value chain and scaled AI as a business unit.</p></span>
              <span class="arrow-pill" aria-hidden="true">›</span>
            </button>
          </div>
        </div>
      </div>
    </section>

    <section id="offering" class="offering section">
      {section_transition("Offering")}
      <div class="sticky-chapter">
        <div class="container">
          <div class="eyebrow">End-to-end transformation</div>
          <h2>Artefact connects the world of business with technology from ambition to adoption.</h2>
          <p>We help companies define their future state, quantify ambitions, identify and prioritize high-impact use cases, build the right data and technology foundations, and drive adoption across the organization.</p>
          <div class="pillar-wrap">
            <div class="pyramid" aria-label="Transformation pillars">
              <img src="{stairs_img}" alt="">
              <div class="pyramid-levels">
                <div class="level">Vision & Use Cases</div>
                <div class="level">Operating Model</div>
                <div class="level">Data Infrastructure & Governance</div>
                <div class="level">Change Management & Acculturation</div>
              </div>
            </div>
            <div data-pillar-region>
              <article class="pillar-card" data-pillar="vision"><h3>Vision And Use Cases</h3><p>Define the future state of the business, quantify ambitions, and prioritize high-impact use cases.</p></article>
              <article class="pillar-card" data-pillar="model"><h3>Operating Model</h3><p>Create an efficient operating model and deliver use cases through adapted methodologies, organization, tools, and governance.</p></article>
              <article class="pillar-card" data-pillar="data"><h3>Data Infrastructure And Data Governance</h3><p>Build a cutting-edge technology ecosystem. Treat data as an asset so it becomes high-quality, reliable, and useful.</p></article>
              <article class="pillar-card" data-pillar="change"><h3>Change Management And Acculturation</h3><p>Manage change at scale to engage everyone, from leaders to team members.</p></article>
            </div>
          </div>

          <div style="padding-top:80px;">
            <h2>Artefact gives you what it takes to succeed in Data & AI-driven transformation at scale.</h2>
            <div class="proof-grid">
              <div class="proof-card reveal"><h3>Global</h3><p>We have the critical mass required to enable full transformation at scale. Artefact's footprint covers 5 continents and 27 countries, and 50% of our projects involve more than 2 offices.</p></div>
              <div class="proof-card reveal"><h3>Pure Player</h3><p>Being a pure player in Data & AI and GenAI helps us focus on the details that make the difference between an industrialized deployment and a POC, supported by our AI R&D Center and internal toolbox, Skaff.</p></div>
              <div class="proof-card reveal"><h3>End-To-End</h3><p>We frame, build, and run, from idea creation to project management and operation, with AI experts, Data Scientists, Data Engineers, Digital Experts, and specific adoption programs.</p></div>
            </div>
          </div>

          <div style="padding-top:80px;">
            <h2>Our end-to-end Data, AI, AI agents, and digital solutions cover the full transformation agenda.</h2>
            <p>Generative AI and AI agent offerings accounted for 50% of our revenue in 2024, and we expect them to reach approximately 65% in 2026.</p>
            <div class="service-grid">
              {service_card("Strategy & Transformation", "We guide companies from strategy to operations and adoption, using data to accelerate transformation and create value. Our hackathons, GenAI Academy, and School of Data help companies train and upskill their teams.")}
              {service_card("Data Foundations & BI", "We build solid data foundations and develop AI solutions tailored to each sector and department, with effective governance and data management frameworks for value creation and regulatory compliance.")}
              {service_card("AI Acceleration", "We help companies accelerate AI and Agentic AI initiatives, from opportunity identification and business framing to solution design, deployment, adoption, and scaling.")}
              {service_card("IT & Data Platforms", "We treat data as a strategic asset and offer scalable, secure cloud services, enabling smarter decision-making and IT optimization across leading cloud service providers.")}
              {service_card("Marketing Data-Driven", "Our marketing specialists, data scientists, and analysts manage campaigns using advanced multichannel strategies and customer data platforms to increase marketing return on investment.")}
              {service_card("CX & Digital Marketing", "We use advanced digital strategies and media management, combining artificial intelligence and creativity to deliver personalized and engaging consumer experiences.")}
            </div>
            <div class="ecosystem">
              <div class="card reveal"><h3>Tech agnostic and certified across all clouds.</h3><p>AI is the new source of business innovation. Our engineers build tech-agnostic solutions, combining custom code, open-source code, and software, backed by alliances with leading cloud providers.</p></div>
              <div class="clouds reveal">
                <span>Google Cloud</span><span>AWS</span><span>Microsoft</span><span>SAP</span><span>Databricks</span><span>Snowflake</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="adopt-ai" class="adopt section">
      {section_transition("Adopt AI")}
      <div class="container event-grid">
        <div>
          <div class="eyebrow" style="color:#fff;">International summit by Artefact</div>
          <h2>Adopt AI</h2>
          <p>Adopt AI is Artefact's international summit dedicated to accelerating AI adoption across companies, industries, and ecosystems.</p>
          <p>The next edition is being organized for this year. Adopt AI brings together business leaders, technology partners, AI experts, and ecosystem builders to move from AI ambition to adoption at scale.</p>
          <p>The summit is designed to connect the people and organizations shaping the future of AI, with practical conversations, real-world use cases, and concrete pathways for enterprise adoption.</p>
        </div>
        <div class="event-panel reveal">
          <h3>Details to be confirmed</h3>
          <div class="tbd-grid">
            <div class="tbd">Venue</div><div class="tbd">Dates</div><div class="tbd">Speakers</div><div class="tbd">Stages</div><div class="tbd">Exhibitors</div><div class="tbd">Ecosystems</div><div class="tbd">Participants</div>
          </div>
          <h3 style="margin-top:28px;">Previous edition reference</h3>
          <div class="previous">
            <div><strong>600+</strong><small>speakers</small></div>
            <div><strong>8</strong><small>stages</small></div>
            <div><strong>250+</strong><small>exhibitors</small></div>
            <div><strong>7</strong><small>ecosystems</small></div>
            <div><strong>20,000+</strong><small>participants</small></div>
          </div>
        </div>
      </div>
    </section>

    <section id="contact" class="contact section">
      {section_transition("Contact")}
      <div class="container">
        <div class="eyebrow">Contact Us</div>
        <h2>Accelerate your Data, AI, and Agentic AI transformation with Artefact LATAM.</h2>
        <p>To explore how Artefact can help accelerate your Data, AI, and Agentic AI transformation, contact:</p>
        <div class="contact-wrap">
          <article class="contact-card reveal"><h3>Andre Fonseca</h3><p>CEO LATAM</p><a href="mailto:andre.fonseca@artefact.com">andre.fonseca@artefact.com</a></article>
          <article class="contact-card reveal"><h3>Andres Oksenberg</h3><p>Managing Partner</p><a href="mailto:andres.oksenberg@artefact.com">andres.oksenberg@artefact.com</a></article>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      <img src="{wordmark}" alt="Artefact">
      <span>Data & AI transformation | LATAM</span>
    </div>
  </footer>

  <dialog class="positioning-modal" data-case-modal="positioning" aria-labelledby="positioning-title">
    <div class="modal-body">
      <div class="modal-head">
        <div>
          <div class="eyebrow">Competitive archetypes</div>
          <h2 id="positioning-title">Why Artefact is positioned as the Data & AI pure player.</h2>
        </div>
        <button class="close" type="button" data-modal-close aria-label="Close">×</button>
      </div>
      <div class="archetype-comparison">
        <div class="comparison-head competitor-head">
          <h3>Archetypes of competitors</h3>
        </div>
        <div class="comparison-head artefact-head">
          <div class="artefact-lockup"><img src="{wordmark}" alt="Artefact"></div>
        </div>
        <div class="comparison-row">
          <div class="competitor-cell">
            <strong>Generalists with expertise in Data & AI</strong>
            <p>Global, multifunctional consulting firms with a limited offering in Data & AI.</p>
          </div>
          <div class="artefact-cell">
            <ul>
              <li>Greater technical expertise in Data & AI</li>
              <li>End-to-end services</li>
              <li>Price advantage</li>
            </ul>
          </div>
        </div>
        <div class="comparison-row">
          <div class="competitor-cell">
            <strong>IT consulting firms</strong>
            <p>Global IT consulting firms with an expanding business portfolio.</p>
          </div>
          <div class="artefact-cell">
            <ul>
              <li>Greater technical expertise in Data & AI</li>
              <li>Greater business expertise</li>
              <li>Responsiveness and speed of execution</li>
            </ul>
          </div>
        </div>
        <div class="comparison-row">
          <div class="competitor-cell">
            <strong>Next-Gen IT for Data & AI</strong>
            <p>Global firms offering specialized consulting services in data and AI.</p>
          </div>
          <div class="artefact-cell">
            <ul>
              <li>Specialized technical capabilities to address highly complex needs</li>
              <li>More agile and flexible</li>
              <li>Price advantages</li>
            </ul>
          </div>
        </div>
        <div class="comparison-row">
          <div class="competitor-cell">
            <strong>Local specialists</strong>
            <p>Local firms specializing in Data & AI.</p>
          </div>
          <div class="artefact-cell">
            <ul>
              <li>Global network supported by nearshoring hubs</li>
              <li>Sophisticated deployment and scaling capabilities</li>
              <li>Greater depth of services</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </dialog>

  <dialog data-case-modal="heineken" aria-labelledby="heineken-title">
    <div class="modal-body">
      <div class="modal-head">
        <div>
          <div class="eyebrow">Case module</div>
          <h2 id="heineken-title">Our History With HEINEKEN</h2>
          <p>We built a journey together with HEINEKEN, using AI as a business unit to bring value through Advanced Analytics.</p>
        </div>
        <button class="close" type="button" data-modal-close aria-label="Close">×</button>
      </div>
      <p>Together, Artefact and HEINEKEN created products throughout the entire value chain, scaling Advanced Analytics from initial use cases into a broader operating model for data-driven business impact.</p>
      <div class="modal-metrics">
        <div class="metric"><strong>+R$650M</strong><span>already captured through the use cases developed.</span></div>
        <div class="metric"><strong>+2,000</strong><span>people impacted at HEINEKEN.</span></div>
        <div class="metric"><strong>x19</strong><span>ROI on the investment in Artefact's resources.</span></div>
      </div>
      <h3>Journey timeline</h3>
      <div class="journey">
        <div>First step toward Advanced Analytics.</div>
        <div>Expansion of scope to other areas.</div>
        <div>Use case sizing, knowledge internalization, and ways of working.</div>
        <div>Hybrid squads, architecture, and sustainable evolution.</div>
        <div>Innovation, GenAI, and Agentic acceleration.</div>
      </div>
      <h3>Value chain use cases</h3>
      <ul class="usecases">
        <li>Profitability modeling.</li>
        <li>Credit recommendation.</li>
        <li>Turnover forecasting.</li>
        <li>Optimization of beer coloring.</li>
        <li>Thermal energy optimization.</li>
        <li>Automation of brewery reports.</li>
        <li>Stock shortage forecasting.</li>
        <li>Transportation optimization.</li>
        <li>Planning optimization.</li>
        <li>Inventory policy optimization.</li>
        <li>MROI.</li>
        <li>Sales channel segmentation.</li>
        <li>B2B analysis.</li>
        <li>Product selection for e-commerce.</li>
      </ul>
      <p>The partnership also created a joint vision through cases in the media, events, and podcasts.</p>
    </div>
  </dialog>

  <script>
    const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const sections = [...document.querySelectorAll(".section")];
    const navLinks = [...document.querySelectorAll(".top-menu a")];
    const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
    const smooth = (value) => value * value * (3 - 2 * value);

    const revealObserver = new IntersectionObserver((entries) => {{
      for (const entry of entries) {{
        if (entry.isIntersecting) entry.target.classList.add("visible");
      }}
    }}, {{ threshold: 0.14 }});
    document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

    function setActiveNav() {{
      const midpoint = window.innerHeight * 0.46;
      let active = sections[0].id;
      for (const section of sections) {{
        const rect = section.getBoundingClientRect();
        if (rect.top <= midpoint && rect.bottom >= midpoint) {{
          active = section.id;
          break;
        }}
      }}
      document.body.dataset.activeSection = active;
      navLinks.forEach((link) => link.classList.toggle("active", link.getAttribute("href") === "#" + active));
    }}
    window.addEventListener("scroll", setActiveNav, {{ passive: true }});
    setActiveNav();

    const heroMessageEls = [...document.querySelectorAll("[data-hero-message]")];
    if (heroMessageEls.length) {{
      const hero = document.querySelector("#hero");
      const heroMessages = heroMessageEls.map((el) => {{
        const text = el.dataset.typewriter || "";
        const emphasis = (el.dataset.emphasis || "").split("|").filter(Boolean);
        const emphasisRanges = emphasis
          .map((phrase) => {{
            const start = text.indexOf(phrase);
            return start >= 0 ? {{ start, end: start + phrase.length }} : null;
          }})
          .filter(Boolean);

        return {{
          el,
          key: el.dataset.heroKey || "",
          text,
          emphasisRanges
        }};
      }});
      let currentHeroMessage = "";
      let typingToken = 0;

      const renderType = (message, count, done = false) => {{
        const escapeHtml = (value) => value
          .replace(/&/g, "&amp;")
          .replace(/</g, "&lt;")
          .replace(/>/g, "&gt;");

        let marked = "";
        let cursor = 0;
        const visibleEnd = Math.min(count, message.text.length);
        const ranges = [...message.emphasisRanges].sort((a, b) => a.start - b.start);

        for (const range of ranges) {{
          if (range.end <= cursor || range.start >= visibleEnd) continue;
          const normalEnd = Math.min(range.start, visibleEnd);
          if (cursor < normalEnd) {{
            marked += escapeHtml(message.text.slice(cursor, normalEnd));
            cursor = normalEnd;
          }}

          const strongStart = Math.max(range.start, cursor);
          const strongEnd = Math.min(range.end, visibleEnd);
          if (strongStart < strongEnd) {{
            marked += `<strong>${{escapeHtml(message.text.slice(strongStart, strongEnd))}}</strong>`;
            cursor = strongEnd;
          }}
        }}

        if (cursor < visibleEnd) {{
          marked += escapeHtml(message.text.slice(cursor, visibleEnd));
        }}
        if (message.key === "who" && done && marked.endsWith(".")) {{
          marked = marked.slice(0, -1) + '<span class="hero-period">.</span>';
        }}
        message.el.innerHTML = marked + (done ? "" : '<span class="type-caret" aria-hidden="true"></span>');
      }};

      const typeHeroMessage = (message) => {{
        if (!message || currentHeroMessage === message.key) return;
        currentHeroMessage = message.key;
        typingToken += 1;
        const localToken = typingToken;
        heroMessages.forEach((item) => {{
          item.el.classList.toggle("is-visible", item.key === message.key);
          if (item.key !== message.key) item.el.innerHTML = "";
        }});

        if (prefersReduced) {{
          renderType(message, message.text.length, true);
          return;
        }}

        let i = 1;
        renderType(message, i);
        const tick = () => {{
          if (localToken !== typingToken) return;
          i = Math.min(message.text.length, i + 1);
          renderType(message, i, i >= message.text.length);
          if (i < message.text.length) window.setTimeout(tick, i < 18 ? 24 : 18);
        }};
        window.setTimeout(tick, 120);
      }};

      const setHeroMessageByScroll = () => {{
        if (!hero) return;
        const range = Math.max(1, hero.offsetHeight - window.innerHeight);
        const progress = clamp((window.scrollY - hero.offsetTop) / range);
        typeHeroMessage(progress > 0.30 ? heroMessages[1] : heroMessages[0]);
      }};

      setHeroMessageByScroll();
      window.addEventListener("scroll", setHeroMessageByScroll, {{ passive: true }});
    }}

    const personVideoWrap = document.querySelector("[data-person-video-wrap]");
    const personVideo = document.querySelector("[data-person-video]");
    let targetPersonTime = 0;
    let renderedPersonTime = 0;
    let personScrubFrame = null;

    const setupPersonVideo = () => {{
      if (!personVideo || prefersReduced) return;

      const setMobilePlayback = () => {{
        if (window.innerWidth < 1024) {{
          personVideo.autoplay = true;
          personVideo.muted = true;
          personVideo.playsInline = true;
          personVideo.play().catch(() => {{}});
        }} else {{
          personVideo.pause();
          targetPersonTime = personVideo.currentTime || 0;
          renderedPersonTime = targetPersonTime;
        }}
      }};

      const stepPersonScrub = () => {{
        if (window.innerWidth < 1024 || !personVideo.duration) {{
          personScrubFrame = null;
          return;
        }}

        const difference = targetPersonTime - renderedPersonTime;

        if (Math.abs(difference) < 0.004) {{
          renderedPersonTime = targetPersonTime;
          if (!personVideo.seeking) {{
            personVideo.currentTime = renderedPersonTime;
          }}
          personScrubFrame = null;
          return;
        }}

        if (personVideo.seeking) {{
          personScrubFrame = requestAnimationFrame(stepPersonScrub);
          return;
        }}

        renderedPersonTime += difference * 0.16;
        personVideo.currentTime = renderedPersonTime;

        personScrubFrame = requestAnimationFrame(stepPersonScrub);
      }};

      const requestPersonScrub = () => {{
        if (personScrubFrame === null) {{
          personScrubFrame = requestAnimationFrame(stepPersonScrub);
        }}
      }};

      const handlePersonMouseMove = (event) => {{
        if (window.innerWidth < 1024 || !personVideo.duration) return;

        const personFocusX = window.innerWidth * 0.68;
        const relativeMouseX = event.clientX - personFocusX;
        const sideRange = relativeMouseX >= 0
          ? Math.max(1, window.innerWidth - personFocusX)
          : Math.max(1, personFocusX);
        const centeredProgress = clamp(relativeMouseX / sideRange, -1, 1);
        const easedProgress = Math.sign(centeredProgress) * smooth(Math.abs(centeredProgress));
        targetPersonTime = clamp(((easedProgress + 1) / 2) * personVideo.duration, 0, personVideo.duration);

        requestPersonScrub();
      }};

      setMobilePlayback();
      window.addEventListener("resize", setMobilePlayback);
      window.addEventListener("mousemove", handlePersonMouseMove, {{ passive: true }});
    }};
    setupPersonVideo();

    const transitionVideoSrc = "{section_background_video}";
    const transitionLoader = document.querySelector("[data-transition-loader]");
    const transitionProgress = document.querySelector("[data-transition-progress]");
    const transitionItems = [...document.querySelectorAll("[data-section-transition]")].map((transition) => {{
      const video = transition.querySelector("[data-transition-video]");
      const wrap = transition.querySelector("[data-transition-video-wrap]");
      const title = transition.querySelector("[data-transition-title]");
      return {{
        transition,
        video,
        wrap,
        title,
        currentTarget: 0,
        targetProgress: 0,
        renderedProgress: 0,
        scrubRaf: null,
        seekPending: false,
        parallaxX: 0,
        parallaxY: 0,
        targetX: 0,
        targetY: 0,
        raf: null
      }};
    }});

    const hideTransitionLoader = () => {{
      if (transitionLoader) transitionLoader.classList.add("is-hidden");
    }};

    const updateTransitionProgress = (video) => {{
      if (!transitionProgress || !video.duration || !video.buffered.length) return;
      const bufferedEnd = video.buffered.end(video.buffered.length - 1);
      transitionProgress.textContent = String(Math.min(100, Math.round((bufferedEnd / video.duration) * 100)));
    }};

    const renderTransitionItem = (item, progress) => {{
      const eased = smooth(progress);
      const titleOpacity = clamp(progress / .18) * clamp((1 - progress) / .22);
      const titleY = 34 - progress * 72;
      const videoOpacity = .28 + eased * .72;
      const blur = Math.round((1 - eased) * 28);
      const brightness = .58 + eased * .48;

      item.title.style.opacity = titleOpacity.toFixed(3);
      item.title.style.transform = `translate3d(0, ${{titleY.toFixed(2)}}vh, 0)`;
      item.video.style.opacity = videoOpacity.toFixed(3);
      item.video.style.filter = `blur(${{blur}}px) saturate(${{(.82 + eased * .35).toFixed(2)}}) contrast(1.08) brightness(${{brightness.toFixed(2)}})`;

      if (item.video.duration) {{
        const usableDuration = Math.min(6, item.video.duration);
        item.currentTarget = progress * usableDuration;
      }}
    }};

    const seekTransitionVideo = (item) => {{
      const video = item.video;
      if (!video || !video.duration) return;

      if (video.seeking) {{
        item.seekPending = true;
        return;
      }}

      const delta = item.currentTarget - video.currentTime;
      const maxSeekStep = 0.045;
      const seekThreshold = 0.018;

      if (Math.abs(delta) > seekThreshold) {{
        const boundedDelta = Math.max(-maxSeekStep, Math.min(maxSeekStep, delta));
        video.currentTime = video.currentTime + boundedDelta;
      }}
    }};

    const stepTransitionScrub = (item) => {{
      item.renderedProgress += (item.targetProgress - item.renderedProgress) * .052;

      if (Math.abs(item.targetProgress - item.renderedProgress) < .0008) {{
        item.renderedProgress = item.targetProgress;
      }}

      renderTransitionItem(item, item.renderedProgress);
      seekTransitionVideo(item);

      if (Math.abs(item.targetProgress - item.renderedProgress) > .0008 || item.seekPending) {{
        item.scrubRaf = requestAnimationFrame(() => stepTransitionScrub(item));
      }} else {{
        item.scrubRaf = null;
      }}
    }};

    const requestTransitionScrub = (item, progress) => {{
      item.targetProgress = progress;
      if (item.scrubRaf === null) {{
        item.scrubRaf = requestAnimationFrame(() => stepTransitionScrub(item));
      }}
    }};

    const updateSectionTransitions = () => {{
      for (const item of transitionItems) {{
        const rect = item.transition.getBoundingClientRect();
        const travel = Math.max(1, item.transition.offsetHeight - window.innerHeight);
        const progress = clamp(-rect.top / travel);
        requestTransitionScrub(item, progress);
      }}
    }};

    const animateTransitionParallax = (item) => {{
      item.parallaxX += (item.targetX - item.parallaxX) * .08;
      item.parallaxY += (item.targetY - item.parallaxY) * .08;
      item.wrap.style.transform = `translate3d(${{item.parallaxX.toFixed(2)}}px, ${{item.parallaxY.toFixed(2)}}px, 0) scale(1.05)`;

      if (Math.abs(item.targetX - item.parallaxX) > .05 || Math.abs(item.targetY - item.parallaxY) > .05) {{
        item.raf = requestAnimationFrame(() => animateTransitionParallax(item));
      }} else {{
        item.raf = null;
      }}
    }};

    const handleTransitionMouseMove = (event) => {{
      const moveX = ((event.clientX / window.innerWidth) - .5) * 2;
      const moveY = ((event.clientY / window.innerHeight) - .5) * 2;

      for (const item of transitionItems) {{
        item.targetX = moveX * -30;
        item.targetY = moveY * -30;
        if (item.raf === null) item.raf = requestAnimationFrame(() => animateTransitionParallax(item));
      }}
    }};

    const setupSectionTransitions = () => {{
      if (!transitionItems.length) {{
        hideTransitionLoader();
        return;
      }}

      for (const item of transitionItems) {{
        item.video.addEventListener("progress", () => updateTransitionProgress(item.video));
        item.video.addEventListener("canplay", hideTransitionLoader, {{ once: true }});
        item.video.addEventListener("loadedmetadata", () => {{
          item.currentTarget = 0;
          item.targetProgress = 0;
          item.renderedProgress = 0;
          item.video.currentTime = 0;
          renderTransitionItem(item, 0);
          updateSectionTransitions();
        }});
        item.video.addEventListener("seeked", () => {{
          if (item.seekPending) {{
            item.seekPending = false;
            if (item.scrubRaf === null) {{
              item.scrubRaf = requestAnimationFrame(() => stepTransitionScrub(item));
            }}
          }}
        }});
        item.video.src = transitionVideoSrc;
        item.video.load();
      }}

      window.addEventListener("scroll", updateSectionTransitions, {{ passive: true }});
      window.addEventListener("resize", updateSectionTransitions);
      window.addEventListener("mousemove", handleTransitionMouseMove, {{ passive: true }});
      window.setTimeout(hideTransitionLoader, 5000);
      updateSectionTransitions();
    }};
    setupSectionTransitions();

    const positioningCharts = [...document.querySelectorAll("[data-positioning-chart]")];
    const updatePositioningCharts = () => {{
      for (const chart of positioningCharts) {{
        const stage = chart.querySelector(".positioning-board");
        if (!stage) continue;

        const rect = chart.getBoundingClientRect();
        const travel = Math.max(1, chart.offsetHeight - window.innerHeight);
        const progress = clamp(-rect.top / travel);
        const axisProgress = smooth(clamp((progress - .04) / .18));
        const labelProgress = smooth(clamp((progress - .14) / .12));

        stage.style.setProperty("--axis-progress", axisProgress.toFixed(3));
        stage.style.setProperty("--label-progress", labelProgress.toFixed(3));

        for (const item of stage.querySelectorAll("[data-chart-phase]")) {{
          const phase = Number(item.dataset.chartPhase || 0);
          const itemProgress = smooth(clamp((progress - phase) / .11));

          if (item.classList.contains("artefact-position")) {{
            item.style.setProperty("--artefact-progress", itemProgress.toFixed(3));
          }} else if (item.classList.contains("positioning-detail-trigger")) {{
            item.style.setProperty("--button-progress", itemProgress.toFixed(3));
          }} else {{
            item.style.setProperty("--phase-progress", itemProgress.toFixed(3));
          }}
        }}
      }}
    }};
    if (positioningCharts.length) {{
      window.addEventListener("scroll", updatePositioningCharts, {{ passive: true }});
      window.addEventListener("resize", updatePositioningCharts);
      updatePositioningCharts();
    }}

    const counters = [...document.querySelectorAll("[data-count]")];
    const counted = new WeakSet();
    function animateCounter(element, target, duration = 900) {{
      const start = performance.now();
      function frame(now) {{
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        element.textContent = Math.round(target * eased).toLocaleString("en-US");
        if (progress < 1) requestAnimationFrame(frame);
      }}
      requestAnimationFrame(frame);
    }}
    const counterObserver = new IntersectionObserver((entries) => {{
      for (const entry of entries) {{
        if (entry.isIntersecting && !counted.has(entry.target)) {{
          counted.add(entry.target);
          if (!prefersReduced) animateCounter(entry.target, Number(entry.target.dataset.count));
        }}
      }}
    }}, {{ threshold: .65 }});
    counters.forEach((counter) => counterObserver.observe(counter));

    const pillarCards = [...document.querySelectorAll("[data-pillar]")];
    function setActivePillar() {{
      let active = "vision";
      const threshold = window.innerHeight * .42;
      for (const card of pillarCards) {{
        const rect = card.getBoundingClientRect();
        if (rect.top <= threshold) active = card.dataset.pillar;
      }}
      document.body.dataset.activePillar = active;
    }}
    window.addEventListener("scroll", setActivePillar, {{ passive: true }});
    setActivePillar();

    const modals = [...document.querySelectorAll("[data-case-modal]")];
    let lastFocus = null;

    function modalFocusables(modal) {{
      return [...modal.querySelectorAll('a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])')];
    }}
    function openModal(modal) {{
      lastFocus = document.activeElement;
      document.body.classList.add("modal-open");
      modal.showModal();
      const close = modal.querySelector("[data-modal-close]");
      if (close) close.focus();
    }}
    function closeModal(modal) {{
      modal.close();
      document.body.classList.remove("modal-open");
      if (lastFocus) lastFocus.focus();
    }}

    document.querySelectorAll("[data-case-trigger]").forEach((trigger) => {{
      trigger.addEventListener("click", () => {{
        const modal = document.querySelector(`[data-case-modal="${{trigger.dataset.caseTrigger}}"]`);
        if (modal) openModal(modal);
      }});
    }});

    for (const modal of modals) {{
      modal.querySelectorAll("[data-modal-close]").forEach((button) => {{
        button.addEventListener("click", () => closeModal(modal));
      }});
      modal.addEventListener("click", (event) => {{
        const rect = modal.getBoundingClientRect();
        const inDialog = event.clientX >= rect.left && event.clientX <= rect.right && event.clientY >= rect.top && event.clientY <= rect.bottom;
        if (!inDialog) closeModal(modal);
      }});
      modal.addEventListener("cancel", (event) => {{
        event.preventDefault();
        closeModal(modal);
      }});
      modal.addEventListener("keydown", (event) => {{
        if (event.key !== "Tab") return;
        const items = modalFocusables(modal);
        const first = items[0];
        const last = items[items.length - 1];
        if (!first || !last) return;
        if (event.shiftKey && document.activeElement === first) {{
          event.preventDefault();
          last.focus();
        }} else if (!event.shiftKey && document.activeElement === last) {{
          event.preventDefault();
          first.focus();
        }}
      }});
    }}
  </script>
</body>
</html>
"""


html_doc = "\n".join(line.rstrip() for line in html_doc.splitlines()) + "\n"
OUT.write_text(html_doc, encoding="utf-8")
print(OUT)
