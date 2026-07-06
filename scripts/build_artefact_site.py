from __future__ import annotations

import base64
import html
import io
import mimetypes
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = Path("/Users/jose/Documents/artefact-html-skill/assets")
OUT = ROOT / "artefact-latam-website.html"


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f"None of these paths exist: {', '.join(str(path) for path in paths)}")


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0]
    raw = path.read_bytes()
    if mime is None:
        if raw.startswith(b"\x89PNG\r\n\x1a\n"):
            mime = "image/png"
        elif raw.startswith(b"\xff\xd8\xff"):
            mime = "image/jpeg"
        elif raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
            mime = "image/webp"
        elif raw.lstrip().startswith(b"<svg") or path.suffix.lower() == ".svg":
            mime = "image/svg+xml"
        else:
            mime = "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def cropped_png_data_uri(path: Path, box: tuple[int, int, int, int]) -> str:
    from PIL import Image

    image = Image.open(path).convert("RGBA").crop(box)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('ascii')}"


def trimmed_png_data_uri(path: Path) -> str:
    from PIL import Image

    image = Image.open(path).convert("RGBA")
    bbox = image.getbbox()
    if bbox:
        image = image.crop(bbox)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('ascii')}"


def logo_without_solid_background_data_uri(path: Path, background: tuple[int, int, int], tolerance: int = 42) -> str:
    from PIL import Image

    image = Image.open(path).convert("RGBA")
    pixels = image.load()
    bg_r, bg_g, bg_b = background
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            distance = abs(r - bg_r) + abs(g - bg_g) + abs(b - bg_b)
            if distance <= tolerance:
                pixels[x, y] = (255, 255, 255, 0)
            elif a:
                pixels[x, y] = (255, 255, 255, a)

    bbox = image.getbbox()
    if bbox:
        image = image.crop(bbox)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('ascii')}"


def logo_cell(name: str, src: str, categories: list[str] | None = None) -> str:
    category_attr = ""
    if categories:
        category_attr = f' data-industries="{" ".join(categories)}"'
    return f'<div class="logo-cell"{category_attr}><img src="{src}" alt="{html.escape(name)} logo"></div>'


def industry_button(label: str, slug: str, index: int, total: int) -> str:
    ratio = index / max(total - 1, 1)
    start = (0, 34, 68)
    end = (255, 0, 102)
    color = tuple(round(start[i] + (end[i] - start[i]) * ratio) for i in range(3))
    bg = f"rgb({color[0]}, {color[1]}, {color[2]})"
    return (
        f'<button class="industry" type="button" data-industry-filter="{slug}" '
        f'style="--industry-bg:{bg};">'
        f'<span>{html.escape(label)}</span></button>'
    )


def timeline_logo(name: str, path: Path | None, class_name: str = "", src: str | None = None) -> str:
    classes = "genai-logo"
    if class_name:
        classes += f" {class_name}"
    if src:
        return f'<span class="{classes}"><img src="{src}" alt="{html.escape(name)} logo"></span>'
    if path and path.exists():
        raw = path.read_bytes()
        if raw.lstrip().startswith(b"<svg") or path.suffix.lower() == ".svg":
            logo_src = data_uri(path)
        else:
            logo_src = trimmed_png_data_uri(path)
        return f'<span class="{classes}"><img src="{logo_src}" alt="{html.escape(name)} logo"></span>'
    return f'<span class="{classes} logo-fallback">{html.escape(name)}</span>'


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
person_video = data_uri(Path("/Users/jose/Documents/videos_website/assets/videos/person.mp4"))
section_background_video = data_uri(Path("/Users/jose/Documents/videos_website/assets/videos/section_background.mp4"))
globe_background_video = "assets/videos/globe_background.mp4"
bottle_video = data_uri(Path("/Users/jose/Documents/videos_website/assets/videos/beer_green.webm"))
platform_img = data_uri(ASSET_ROOT / "images-examples/15.png")
flow_img = data_uri(ASSET_ROOT / "images-examples/9.png")
stairs_img = data_uri(ASSET_ROOT / "images-examples/16.jpg")
business_depth_img = data_uri(ASSET_ROOT / "images-examples/12.jpg")
technical_depth_img = data_uri(ASSET_ROOT / "images-examples/15.png")

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

client_logo_root = ASSET_ROOT / "clients-logos"
consultancy_logo_root = ASSET_ROOT / "consultancy-logos"
ai_logo_root = ASSET_ROOT / "logos"


def client_logo_path(stem: str) -> Path:
    return first_existing(
        client_logo_root / stem,
        client_logo_root / f"{stem}.png",
        client_logo_root / f"{stem}.webp",
        client_logo_root / f"{stem}.svg",
    )


def client_logo_src(stem: str) -> str:
    path = client_logo_path(stem)
    raw = path.read_bytes()
    if raw.lstrip().startswith(b"<svg") or path.suffix.lower() == ".svg":
        return data_uri(path)
    return trimmed_png_data_uri(path)


industry_segments = [
    ("Financial Services", "financial", [
        ("BNP Paribas", "bnp-paribas-logo"),
        ("GBM", "gbm-logo"),
        ("Livelo", "livelo-logo"),
        ("Pacifico", "pacifico-logo"),
        ("Prudential", "prudential-logo"),
        ("Santander", "santander-logo"),
        ("Visa", "visa-logo"),
    ]),
    ("Retail", "retail", [
        ("Adeo", "adeo-logo"),
        ("Burger King", "burgerking-logo"),
        ("Carrefour", "carrefour-logo"),
        ("Cencosud", "cencosud-logo"),
        ("Chanel", "chanel-logo"),
        ("El Palacio de Hierro", "el-palacio-de-hierro-logo"),
        ("Kering", "kering-logo"),
        ("LVMH", "lvmh-logo"),
        ("OXXO", "oxxo-logo"),
        ("Totto", "totto-logo"),
    ]),
    ("B2B & Industries", "b2b-industries", [
        ("Bunge", "bunge-logo"),
        ("Daikin", "daikin-logo"),
        ("Legrand", "legrand-logo"),
        ("Lipigas", "lipigas-logo"),
        ("Renault", "renault-logo"),
        ("Schneider Electric", "schneider-electric-logo"),
        ("Socovesa", "socovesa-logo"),
        ("SQM", "sqm-logo"),
        ("Suez", "suez-logo"),
        ("Suzano", "suzano-logo"),
        ("Volcan", "volcan-logo"),
    ]),
    ("CPG", "cpg", [
        ("AB InBev", "ab-inbev-logo"),
        ("Agrosuper", "agrosuper-logo"),
        ("Alpina", "alpina-logo"),
        ("Beiersdorf", "beiersdorf-logo"),
        ("Clarins", "clarins-logo"),
        ("Coca-Cola", "coca-cola-logo"),
        ("Danone", "danone-logo"),
        ("FEMSA", "femsa-logo"),
        ("Heineken", "heineken-logo"),
        ("Hershey's", "hersheys-logo"),
        ("L'Oreal", "loreal-logo"),
        ("Mars", "mars-logo"),
        ("Moet Hennessy", "moet-hennessy-logo"),
        ("Mondelez", "mondelez-logo"),
        ("Nestle", "nestle-logo"),
        ("Pernod Ricard", "pernod-ricard-logo"),
        ("Puig", "puig-logo"),
        ("Red Bull", "redbull-logo"),
        ("Unilever", "unilever-logo"),
    ]),
    ("Healthcare & Pharma", "healthcare-pharma", [
        ("Bayer", "bayer-logo"),
        ("Bupa", "bupa-logo"),
        ("J&J", "j&j-logo"),
        ("Opella", "opella-logo"),
        ("Sanofi", "sanofi-logo"),
    ]),
    ("Travels, Transport & Tourism", "travel-transport-tourism", [
        ("Aeromexico", "aeromexico-logo"),
        ("LATAM Airlines", "latam-airlines-logo"),
        ("Sodexo", "sodexo-logo"),
    ]),
    ("Others", "others", [
        ("Grupo Salinas", "grupo-salinas-logo"),
        ("Orange", "orange-logo"),
        ("Tecnologico de Monterrey", "tecnologico-de-monterrey-logo"),
    ]),
]

industry_buttons = "\n".join(
    industry_button(label, slug, index, len(industry_segments))
    for index, (label, slug, _) in enumerate(industry_segments)
)
logo_items = []
for _, slug, items in industry_segments:
    for name, stem in items:
        logo_items.append(logo_cell(name, client_logo_src(stem), [slug]))
logo_track = "\n".join(logo_items + logo_items)
chatgpt_icon = data_uri(ai_logo_root / "chatgpt-logo.webp")
agent_icon = data_uri(ai_logo_root / "agent-logo.png")
genai_stars_icon = cropped_png_data_uri(ai_logo_root / "genai-logo.webp", (60, 45, 430, 400))
bnp_paribas_white_logo = logo_without_solid_background_data_uri(client_logo_root / "bnp-paribas-logo", (0, 128, 83))
heineken_white_logo = trimmed_png_data_uri(first_existing(
    client_logo_root / "heineken-logo.png",
    client_logo_root / "heineken-logo.webp",
    Path("/Users/jose/.codex/skills/artefact-html/assets/clients-logos/heineken-logo.webp"),
    Path("/Users/jose/.codex/skills/artefact-presentations/assets/clients-logos/heineken-logo.webp"),
))
orange_white_logo = trimmed_png_data_uri(client_logo_root / "orange-logo.png")
redbull_white_logo = trimmed_png_data_uri(client_logo_root / "redbull-logo.png")

genai_early_logos = "\n".join([
    timeline_logo("L'Oreal", client_logo_root / "loreal-logo"),
    timeline_logo("Sodexo", client_logo_root / "sodexo-logo.svg"),
    timeline_logo("Adeo", client_logo_root / "adeo-logo.webp"),
    timeline_logo("Chanel", client_logo_root / "chanel-logo"),
])

genai_early_use_cases = "\n".join([
    '<div class="early-usecase"><span>2018</span>' + timeline_logo("L'Oreal", client_logo_root / "loreal-logo") + '<small>Trendspotting</small></div>',
    '<div class="early-usecase"><span>2020</span>' + timeline_logo("Chanel", client_logo_root / "chanel-logo") + '<small>Augmented agents for call centers</small></div>',
    '<div class="early-usecase"><span>2021-22</span>' + timeline_logo("Sodexo", client_logo_root / "sodexo-logo.svg") + '<small>Product data enrichment</small></div>',
    '<div class="early-usecase"><span>2021-22</span>' + timeline_logo("Adeo", client_logo_root / "adeo-logo.webp") + '<small>Product entity matching</small></div>',
])

genai_acceleration_logos = "\n".join([
    timeline_logo("Samsung", consultancy_logo_root / "samsung-logo.png"),
    timeline_logo("L'Oreal", client_logo_root / "loreal-logo"),
    timeline_logo("Orange", None, "wide orange", orange_white_logo),
    timeline_logo("Renault", client_logo_root / "renault-logo.svg"),
    timeline_logo("BNP Paribas", None, "wide", bnp_paribas_white_logo),
    timeline_logo("LVMH", client_logo_root / "lvmh-logo.png", "wide lvmh"),
    timeline_logo("Kering", client_logo_root / "kering-logo.webp"),
    timeline_logo("Chanel", client_logo_root / "chanel-logo", "wide chanel"),
    timeline_logo("Schneider Electric", client_logo_root / "schneider-electric-logo", "wide"),
    timeline_logo("Red Bull", None, "wide redbull", redbull_white_logo),
    timeline_logo("Legrand", client_logo_root / "legrand-logo"),
    timeline_logo("Burger King", client_logo_root / "burgerking-logo.png", "wide burgerking"),
    timeline_logo("Pernod Ricard", client_logo_root / "pernod-ricard-logo.webp", "pernod"),
    timeline_logo("Moet Hennessy", client_logo_root / "moet-hennessy-logo.png", "wide moet"),
])

genai_agentic_logos = "\n".join([
    timeline_logo("BNP Paribas", None, "wide", bnp_paribas_white_logo),
    timeline_logo("Renault", client_logo_root / "renault-logo.svg"),
    timeline_logo("Carrefour", client_logo_root / "carrefour-logo.svg"),
    timeline_logo("HEINEKEN", None, "wide heineken", heineken_white_logo),
    timeline_logo("Orange", None, "wide orange", orange_white_logo),
])

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

business_pills = "".join(f'<span class="venn-pill business">{item}</span>' for item in business)
technical_pills = "".join(f'<span class="venn-pill technical">{item}</span>' for item in technical)

operating_model_section = f"""
          <article class="scene operating-venn-scene" data-venn-scrolly>
            <div class="operating-venn-copy">
              <div class="eyebrow">Unique operating model</div>
              <h2>A unique operating model bridges business depth and technical expertise.</h2>
              <p>By combining these skills, we design, build, and run AI-native solutions that deliver immediate impact and sustainable competitive advantage.</p>
            </div>
            <div class="operating-venn-panel">
              <div class="venn-pillar left" aria-label="Business depth capabilities">
                {business_pills}
              </div>
              <div class="venn-stage" aria-label="Business depth and technical expertise Venn diagram">
                <div class="venn-circle venn-business">
                  <img src="{business_depth_img}" alt="" aria-hidden="true">
                  <div class="venn-circle-title">Business<br>Depth</div>
                </div>
                <div class="venn-circle venn-technical">
                  <img src="{technical_depth_img}" alt="" aria-hidden="true">
                  <div class="venn-circle-title">Technical<br>Expertise</div>
                </div>
                <div class="venn-lens">
                  <img src="{a_icon}" alt="Artefact">
                  <strong>AI-native solutions</strong>
                  <span>Immediate impact and sustainable competitive advantage</span>
                </div>
              </div>
              <div class="venn-pillar right" aria-label="Technical expertise capabilities">
                {technical_pills}
              </div>
            </div>
          </article>
"""

genai_timeline_section = f"""
          <article class="scene genai-scene">
            <div class="genai-inner">
              <div class="genai-kicker">
                <h2>We've been there since the beginning...</h2>
                <p>We also have strong knowledge of Agents & GenAI, which started well before the hype. We are now supporting large players in the deployment of their Agentic programs.</p>
              </div>
              <div class="genai-timeline genai-vertical" aria-label="Artefact GenAI and Agentic AI timeline">
                <article class="genai-row first early-arc">
                  <div class="genai-moment">
                    <div class="moment-copy">
                      <span>GPT 1, 2 & 3<br>to ChatGPT</span>
                      <strong>2018-2022</strong>
                    </div>
                    <img class="moment-icon chatgpt" src="{chatgpt_icon}" alt="ChatGPT logo">
                    <span class="moment-dot" aria-hidden="true"></span>
                  </div>
                  <div class="genai-story early-arc-story">
                    <div class="story-copy">
                      <p class="story-eyebrow">Up to ChatGPT</p>
                      <h3>Early GenAI use cases emerged progressively, well before the hype.</h3>
                      <p>From GPT 1, 2 & 3 to ChatGPT, Artefact worked on early GenAI premises that later became a board-level acceleration topic.</p>
                    </div>
                    <div class="genai-logo-field before early-usecases">
                      {genai_early_use_cases}
                    </div>
                  </div>
                </article>
                <article class="genai-row">
                  <div class="genai-moment">
                    <div class="moment-copy">
                      <span>GenAI acceleration</span>
                      <strong>2021-2023</strong>
                    </div>
                    <img class="moment-icon genai-stars" src="{genai_stars_icon}" alt="GenAI stars">
                    <span class="moment-dot" aria-hidden="true"></span>
                  </div>
                  <div class="genai-story">
                    <div class="story-copy">
                      <p class="story-eyebrow">GenAI acceleration</p>
                      <h3>New opportunities emerged to design and deploy enterprise-grade AI solutions.</h3>
                      <p>Artefact supported large players across industries, functions, and ecosystems as GenAI moved from promising pilots to scaled business use cases.</p>
                    </div>
                    <div class="genai-logo-field">
                      {genai_acceleration_logos}
                    </div>
                  </div>
                </article>
                <article class="genai-row last">
                  <div class="genai-moment">
                    <div class="moment-copy">
                      <span>Agentic programs</span>
                      <strong>2024 onwards</strong>
                    </div>
                    <img class="moment-icon agent" src="{agent_icon}" alt="Agentic AI icon">
                    <span class="moment-dot" aria-hidden="true"></span>
                  </div>
                  <div class="genai-story agentic">
                    <div class="story-copy">
                      <p class="story-eyebrow">Agentic programs</p>
                      <h3>Enterprise-wide programs now design, deploy, and scale autonomous AI agents.</h3>
                      <p>We help clients move from isolated AI tools to modular, secure, vendor-agnostic architectures and AI-native workflows.</p>
                    </div>
                    <div class="genai-logo-field agentic">
                      {genai_agentic_logos}
                    </div>
                  </div>
                </article>
              </div>
            </div>
          </article>
"""

ai_shift_section = f"""
          <article class="scene ai-shift-section reveal">
            <div class="ai-shift-left">
              <div class="ai-shift-copy">
                <h2>The <strong>AI revolution</strong> is exploding.</h2>
              </div>
              <div class="ai-bars" aria-label="Agentic AI adoption indicators">
                <div class="ai-bar-wrap today" style="--bar-height:42%;">
                  <span class="bar-timing">Today</span>
                  <div class="ai-bar">
                    <div class="ai-bar-fill purple">
                      <strong data-count="37" data-suffix="%" data-count-start>37%</strong>
                      <p>of IT executives at $1B+ companies are already deploying AI agents.</p>
                      <small>Source: UiPath.</small>
                    </div>
                  </div>
                </div>
                <div class="ai-bar-wrap year" style="--bar-height:62%;">
                  <span class="bar-timing">In a year</span>
                  <div class="ai-bar">
                    <div class="ai-bar-fill navy">
                      <strong data-count="83" data-suffix="%" data-count-start>83%</strong>
                      <p>of automation leaders plan to accelerate Agentic AI investment in the next 12 months.</p>
                      <small>Source: Forrester.</small>
                    </div>
                  </div>
                </div>
                <div class="ai-bar-wrap future" style="--bar-height:82%;">
                  <span class="bar-timing">By 2028</span>
                  <div class="ai-bar">
                    <div class="ai-bar-fill magenta">
                      <strong data-count="33" data-suffix="%" data-count-start>33%</strong>
                      <p>of enterprise software applications will embed Agentic AI capabilities in their solutions.</p>
                      <small>Source: Gartner.</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="ai-shift-right">
              <h2><img src="{wordmark}" alt="Artefact"> <span>is leading the shift<br>in the corporate space.</span></h2>
              <div class="ai-shift-modules">
                <article>
                  <h3>End-to-end transformation programmes</h3>
                  <p>Proven results of AI programmes with leading companies such as HEINEKEN, Carrefour, BNP Paribas, and Orange.</p>
                </article>
                <article>
                  <h3>Processes redesign & use cases</h3>
                  <p>Re-engineering business workflows from the ground up to integrate AI and autonomous agents natively across core corporate functions.</p>
                </article>
                <article>
                  <h3>AI & Agentic AI tech foundations</h3>
                  <p>Modular, secure, cost-effective, vendor-agnostic architectures across clouds and LLM providers, built to scale without technical debt.</p>
                </article>
                <article>
                  <h3>AI readiness: adoption and operating model</h3>
                  <p>Upskilling talents and teams to focus on AI augmentation and high-value strategic execution, shifting culture toward an AI-first mindset.</p>
                </article>
              </div>
            </div>
          </article>
"""

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
      opacity:1;
      transform:translateY(0);
      transition:opacity .24s ease, transform .24s ease;
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
    body:not([data-active-section="hero"]) .brand-nav {{
      opacity:0;
      transform:translateY(-16px);
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
    body:not([data-active-section="hero"]) .top-shell:hover .brand-nav,
    body:not([data-active-section="hero"]) .top-shell:focus-within .brand-nav {{
      opacity:1;
      transform:translateY(0);
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
      top:41%;
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
    .genai-scene {{
      min-height:auto;
      width:100vw;
      margin-left:calc(50% - 50vw);
      padding:100px 0 108px;
      border-top:0;
      background:
        radial-gradient(circle at 88% 12%, rgba(255,0,102,.16), transparent 28%),
        radial-gradient(circle at 16% 45%, rgba(40,199,255,.12), transparent 32%),
        linear-gradient(135deg,#000510 0%, #061229 48%, #111b46 100%);
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
      padding-bottom:0;
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
    .genai-kicker {{
      max-width:960px;
      margin-bottom:44px;
    }}
    .genai-kicker h2 {{
      max-width:900px;
      margin-bottom:14px;
      font-size:clamp(42px, 5.7vw, 80px);
      line-height:.92;
      color:#fff;
    }}
    .genai-kicker p {{
      max-width:780px;
      color:#cbd5e1;
      font-size:18px;
    }}
    .genai-inner {{
      width:min(100% - 64px, 1180px);
      margin:0 auto;
    }}
    .genai-timeline {{
      position:relative;
      display:grid;
      gap:26px;
      background:
        radial-gradient(circle at 12% 6%, rgba(40,199,255,.16), transparent 26%),
        radial-gradient(circle at 90% 28%, rgba(255,0,102,.18), transparent 31%),
        linear-gradient(145deg, rgba(255,255,255,.055), rgba(255,255,255,.02));
      border:1px solid rgba(255,255,255,.14);
      border-radius:24px;
      padding:34px;
      box-shadow:0 34px 90px rgba(0,0,0,.34);
    }}
    .genai-row {{
      display:grid;
      grid-template-columns:minmax(250px, 340px) minmax(0, 1fr);
      gap:34px;
      align-items:stretch;
      min-height:198px;
    }}
    .genai-moment {{
      position:relative;
      display:grid;
      grid-template-columns:minmax(0, 1fr) 74px 42px;
      gap:18px;
      align-items:center;
      padding:8px 0;
    }}
    .genai-moment::before {{
      content:"";
      position:absolute;
      right:20px;
      top:-44px;
      bottom:-44px;
      width:2px;
      background:linear-gradient(180deg, rgba(255,255,255,.18), rgba(255,255,255,.94), rgba(255,255,255,.18));
    }}
    .genai-row.first .genai-moment::before {{ top:50%; }}
    .genai-row.last .genai-moment::before {{ bottom:50%; }}
    .moment-copy {{
      text-align:right;
      color:#fff;
    }}
    .moment-copy span {{
      display:block;
      margin-bottom:12px;
      color:#e2e8f0;
      font-size:18px;
      line-height:1.1;
    }}
    .moment-copy strong {{
      display:block;
      color:#fff;
      font-size:clamp(28px, 2.8vw, 38px);
      font-style:italic;
      line-height:1;
      letter-spacing:0;
    }}
    .moment-icon {{
      position:relative;
      z-index:2;
      width:62px;
      height:62px;
      object-fit:contain;
      justify-self:center;
      filter:brightness(0) invert(1) drop-shadow(0 12px 22px rgba(0,0,0,.24));
    }}
    .moment-icon.genai-stars {{
      width:66px;
      height:66px;
    }}
    .moment-icon.agent {{
      width:60px;
      height:60px;
    }}
    .moment-dot {{
      position:relative;
      z-index:3;
      width:38px;
      height:38px;
      border:3px solid #fff;
      border-radius:50%;
      background:#101a3c;
      box-shadow:0 0 0 6px rgba(255,255,255,.13), 0 18px 30px rgba(0,0,0,.28);
    }}
    .moment-dot::after {{
      content:"";
      position:absolute;
      inset:7px;
      border-radius:50%;
      background:linear-gradient(135deg, #fff, #dbeafe);
    }}
    .genai-story {{
      display:grid;
      grid-template-columns:minmax(0, .95fr) minmax(320px, 1.05fr);
      gap:28px;
      align-items:center;
      min-height:198px;
      padding:26px 28px;
      border-radius:16px;
      border:1px solid rgba(255,255,255,.14);
      background:rgba(255,255,255,.07);
      backdrop-filter:blur(16px);
      box-shadow:0 22px 70px rgba(0,0,0,.18);
    }}
    .genai-row.early-arc {{
      min-height:260px;
    }}
    .genai-row.early-arc .genai-moment {{
      min-height:260px;
    }}
    .genai-story.early-arc-story {{
      min-height:260px;
      grid-template-columns:minmax(0, 1.05fr) minmax(340px, .95fr);
      padding:34px 38px;
      background:linear-gradient(135deg, rgba(255,255,255,.075), rgba(255,0,102,.1));
    }}
    .genai-story.early-arc-story h3 {{
      max-width:660px;
      font-size:clamp(30px, 2.45vw, 42px);
    }}
    .genai-story.early-arc-story p:not(.story-eyebrow) {{
      max-width:600px;
      font-size:18px;
    }}
    .genai-story.early-arc-story .genai-logo-field {{
      justify-content:center;
      gap:24px 34px;
    }}
    .genai-logo-field.before.early-usecases {{
      display:grid;
      grid-template-columns:repeat(2, minmax(132px, 1fr));
      gap:16px;
      align-items:stretch;
    }}
    .early-usecase {{
      display:grid;
      grid-template-rows:auto 58px auto;
      place-items:center;
      gap:8px;
      min-height:126px;
      padding:14px 12px;
      border:1px solid rgba(255,255,255,.12);
      border-radius:14px;
      background:rgba(255,255,255,.055);
    }}
    .early-usecase span {{
      color:var(--magenta);
      font-size:12px;
      font-weight:900;
      letter-spacing:.08em;
    }}
    .early-usecase small {{
      color:#cbd5e1;
      font-size:12px;
      font-weight:700;
      line-height:1.2;
      text-align:center;
    }}
    .early-usecase .genai-logo {{
      width:132px;
      height:58px;
    }}
    .early-usecase .genai-logo img {{
      max-width:124px;
      max-height:48px;
    }}
    .genai-story.agentic {{
      background:linear-gradient(135deg, rgba(255,255,255,.075), rgba(255,0,102,.14));
    }}
    .genai-story .story-eyebrow {{
      margin:0 0 10px;
      color:var(--magenta);
      font-size:12px;
      font-weight:900;
      letter-spacing:.12em;
      text-transform:uppercase;
    }}
    .genai-story h3 {{
      margin:0 0 10px;
      color:#fff;
      font-size:clamp(24px, 2vw, 32px);
      line-height:1.05;
    }}
    .genai-story p {{
      margin:0;
      color:#cbd5e1;
      font-size:16px;
      line-height:1.45;
    }}
    .genai-logo-field {{
      display:flex;
      flex-wrap:wrap;
      align-items:center;
      justify-content:flex-start;
      gap:18px 26px;
      min-height:72px;
      padding:0;
    }}
    .genai-logo-field.before {{
      display:flex;
    }}
    .genai-logo-field.agentic {{
      gap:18px 28px;
    }}
    .genai-logo {{
      display:grid;
      place-items:center;
      width:122px;
      height:52px;
      color:#fff;
      font-weight:900;
      filter:drop-shadow(0 12px 12px rgba(0,0,0,.3));
    }}
    .genai-logo img {{
      display:block;
      max-width:100%;
      max-height:100%;
      object-fit:contain;
      filter:brightness(0) invert(1);
    }}
    .genai-logo:not(.wide) img {{
      max-width:112px;
      max-height:42px;
    }}
    .genai-logo.wide {{
      width:168px;
      height:56px;
    }}
    .genai-logo.wide img {{
      max-width:160px;
      max-height:50px;
    }}
    .genai-logo.redbull img {{
      max-width:142px;
      max-height:64px;
    }}
    .genai-logo.heineken img {{
      max-width:158px;
      max-height:48px;
    }}
    .genai-logo.orange img {{
      max-width:142px;
      max-height:40px;
    }}
    .genai-logo.lvmh img {{
      max-width:132px;
      max-height:32px;
    }}
    .genai-logo.chanel img {{
      max-width:138px;
      max-height:48px;
    }}
    .genai-logo.burgerking img {{
      max-width:150px;
      max-height:36px;
      filter:brightness(0) invert(1);
    }}
    .genai-logo.pernod img {{
      max-width:104px;
      max-height:56px;
    }}
    .genai-logo.moet img {{
      max-width:156px;
      max-height:34px;
    }}
    .genai-logo.logo-fallback {{
      padding:8px 12px;
      border:1px solid rgba(255,255,255,.28);
      border-radius:999px;
      background:rgba(255,255,255,.17);
      font-size:17px;
      letter-spacing:.02em;
      box-shadow:0 12px 26px rgba(0,0,0,.12);
    }}
    .genai-logo.wide.logo-fallback {{
      min-width:150px;
      font-size:20px;
    }}
    .operating-venn-scene {{
      display:block;
      margin-top:56px;
      padding:0;
      border-top:0;
      min-height:185vh;
    }}
    .operating-venn-copy {{
      max-width:920px;
      margin:0 0 12px;
    }}
    .operating-venn-copy h2 {{
      max-width:850px;
      margin-bottom:14px;
      font-size:clamp(34px, 4vw, 54px);
      line-height:1;
    }}
    .operating-venn-copy p {{
      max-width:760px;
      font-size:18px;
      color:#64748b;
    }}
    .operating-venn-panel {{
      position:sticky;
      top:48px;
      display:grid;
      grid-template-columns:minmax(180px, .72fr) minmax(520px, 1.55fr) minmax(180px, .72fr);
      gap:24px;
      align-items:center;
      min-height:650px;
      padding:36px;
      border-radius:24px;
      background:
        radial-gradient(circle at 50% 22%, rgba(255,0,102,.08), transparent 28%),
        linear-gradient(180deg, #fff 0%, #f8fafc 100%);
      border:1px solid rgba(226,232,240,.9);
      box-shadow:0 36px 90px rgba(0,5,16,.32);
      overflow:hidden;
    }}
    .operating-venn-panel::after {{
      content:"";
      position:absolute;
      left:50%;
      top:18px;
      width:120px;
      height:5px;
      border-radius:999px;
      transform:translateX(-50%);
      background:linear-gradient(90deg, rgba(0,34,68,.38), rgba(255,0,102,.78));
      opacity:.48;
    }}
    .venn-pillar {{
      position:relative;
      z-index:4;
      display:grid;
      gap:16px;
    }}
    .venn-pillar.left {{ justify-items:end; }}
    .venn-pillar.right {{ justify-items:start; }}
    .venn-pill {{
      display:grid;
      place-items:center;
      min-height:62px;
      width:min(100%, 250px);
      padding:14px 18px;
      border-radius:10px;
      color:#fff;
      text-align:center;
      font-size:16px;
      line-height:1.16;
      font-weight:800;
      box-shadow:0 18px 42px rgba(15,23,42,.14);
      transition:opacity .55s ease, transform .55s ease, filter .55s ease;
    }}
    .venn-pill.business {{
      background:linear-gradient(135deg, #ff0066, #d90063);
    }}
    .venn-pill.technical {{
      background:linear-gradient(135deg, #273275, #0d1f56);
    }}
    .venn-stage {{
      position:relative;
      min-height:520px;
      isolation:isolate;
      transform:translateY(24px);
    }}
    .venn-circle {{
      position:absolute;
      top:54px;
      width:58%;
      aspect-ratio:1;
      border-radius:50%;
      overflow:hidden;
      display:grid;
      place-items:center;
      border:2px solid rgba(255,255,255,.78);
      box-shadow:0 26px 80px rgba(15,23,42,.17);
      transition:opacity .45s ease, transform .45s cubic-bezier(.22,1,.36,1), filter .45s ease;
    }}
    .venn-circle img {{
      position:absolute;
      inset:-8%;
      width:116%;
      height:116%;
      object-fit:cover;
      opacity:.18;
      filter:saturate(1.08) contrast(1.06);
      mix-blend-mode:normal;
    }}
    .venn-business {{
      left:4%;
      background:linear-gradient(135deg, rgba(255,0,102,.94), rgba(198,0,96,.91));
    }}
    .venn-technical {{
      right:4%;
      background:linear-gradient(135deg, rgba(39,50,117,.93), rgba(0,34,68,.94));
    }}
    .venn-circle-title {{
      position:absolute;
      z-index:2;
      top:50%;
      max-width:136px;
      color:#fff;
      text-align:center;
      font-size:clamp(19px, 1.65vw, 23px);
      font-weight:900;
      line-height:1.05;
      text-transform:uppercase;
      letter-spacing:.02em;
      text-shadow:0 12px 28px rgba(0,0,0,.22);
    }}
    .venn-business .venn-circle-title {{
      left:8%;
      transform:translateY(-50%);
    }}
    .venn-technical .venn-circle-title {{
      right:6%;
      transform:translateY(-50%);
    }}
    .venn-lens {{
      position:absolute;
      z-index:5;
      left:50%;
      top:41%;
      width:28%;
      min-width:180px;
      aspect-ratio:.82 / 1;
      transform:translate(-50%, -50%);
      display:grid;
      align-content:center;
      justify-items:center;
      gap:10px;
      padding:24px 18px;
      border-radius:50%;
      background:
        radial-gradient(circle at 50% 12%, rgba(255,255,255,.28), transparent 32%),
        linear-gradient(160deg, rgba(117,46,125,.94), rgba(54,40,104,.97));
      border:1px solid rgba(255,255,255,.7);
      color:#fff;
      text-align:center;
      box-shadow:0 24px 76px rgba(15,23,42,.26);
      transition:opacity .45s ease, transform .45s cubic-bezier(.22,1,.36,1), filter .45s ease;
    }}
    .venn-lens img {{
      width:74px;
      filter:brightness(0) invert(1) drop-shadow(0 12px 18px rgba(255,255,255,.2));
    }}
    .venn-lens strong {{
      display:block;
      font-size:20px;
      line-height:1.06;
    }}
    .venn-lens span {{
      display:none;
      max-width:180px;
      color:#e2e8f0;
      font-size:13px;
      font-weight:700;
      line-height:1.3;
    }}
    .js-enabled .operating-venn-scene .venn-pill,
    .js-enabled .operating-venn-scene .venn-circle,
    .js-enabled .operating-venn-scene .venn-lens {{
      opacity:0;
      filter:blur(8px);
      pointer-events:none;
    }}
    .js-enabled .operating-venn-scene .venn-pill.business,
    .js-enabled .operating-venn-scene .venn-business {{
      transform:translateX(-28px) scale(.96);
    }}
    .js-enabled .operating-venn-scene .venn-pill.technical,
    .js-enabled .operating-venn-scene .venn-technical {{
      transform:translateX(28px) scale(.96);
    }}
    .js-enabled .operating-venn-scene .venn-lens {{
      transform:translate(-50%, -50%) scale(.88);
    }}
    .js-enabled .operating-venn-scene.venn-step-1 .venn-pill.business,
    .js-enabled .operating-venn-scene.venn-step-1 .venn-business,
    .js-enabled .operating-venn-scene.venn-step-2 .venn-pill.business,
    .js-enabled .operating-venn-scene.venn-step-2 .venn-business,
    .js-enabled .operating-venn-scene.venn-step-3 .venn-pill.business,
    .js-enabled .operating-venn-scene.venn-step-3 .venn-business,
    .js-enabled .operating-venn-scene.venn-step-2 .venn-pill.technical,
    .js-enabled .operating-venn-scene.venn-step-2 .venn-technical,
    .js-enabled .operating-venn-scene.venn-step-3 .venn-pill.technical,
    .js-enabled .operating-venn-scene.venn-step-3 .venn-technical,
    .js-enabled .operating-venn-scene.venn-step-3 .venn-lens {{
      opacity:1;
      filter:none;
      pointer-events:auto;
    }}
    .js-enabled .operating-venn-scene.venn-step-1 .venn-pill.business,
    .js-enabled .operating-venn-scene.venn-step-1 .venn-business,
    .js-enabled .operating-venn-scene.venn-step-2 .venn-pill.business,
    .js-enabled .operating-venn-scene.venn-step-2 .venn-business,
    .js-enabled .operating-venn-scene.venn-step-3 .venn-pill.business,
    .js-enabled .operating-venn-scene.venn-step-3 .venn-business,
    .js-enabled .operating-venn-scene.venn-step-2 .venn-pill.technical,
    .js-enabled .operating-venn-scene.venn-step-2 .venn-technical,
    .js-enabled .operating-venn-scene.venn-step-3 .venn-pill.technical,
    .js-enabled .operating-venn-scene.venn-step-3 .venn-technical {{
      transform:none;
    }}
    .js-enabled .operating-venn-scene.venn-step-3 .venn-lens {{
      transform:translate(-50%, -50%) scale(1);
    }}
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
    .ai-shift-section {{
      width:100vw;
      margin-left:calc(50% - 50vw);
      min-height:100svh;
      display:grid;
      grid-template-columns:1fr 1fr;
      align-items:stretch;
      padding:0;
      border-top:0;
      background:#fff;
      overflow:hidden;
    }}
    .ai-shift-left {{
      min-height:100svh;
      display:grid;
      grid-template-rows:.28fr .72fr;
      align-items:stretch;
      gap:18px;
      padding:clamp(36px, 4.8vw, 58px) clamp(28px, 4.2vw, 60px) clamp(30px, 4vw, 48px);
      color:var(--ink);
      background:#fff;
    }}
    .ai-shift-copy {{
      display:grid;
      align-items:center;
    }}
    .ai-shift-copy h2 {{
      max-width:620px;
      margin:0;
      color:var(--navy) !important;
      font-size:clamp(34px, 3.7vw, 54px);
      font-weight:400;
      line-height:1.08;
      letter-spacing:0;
    }}
    .ai-shift-copy strong {{
      font-weight:900;
    }}
    .ai-bars {{
      align-self:end;
      display:grid;
      grid-template-columns:1fr 1.15fr 1.15fr;
      align-items:end;
      gap:0;
      min-height:440px;
      max-width:780px;
    }}
    .ai-bar-wrap {{
      display:grid;
      grid-template-rows:auto minmax(0, 1fr);
      align-items:end;
      min-width:0;
    }}
    .bar-timing {{
      display:block;
      margin:0 0 14px;
      color:#525a66;
      font-size:17px;
      font-weight:900;
      letter-spacing:.04em;
      text-transform:uppercase;
    }}
    .ai-bar {{
      position:relative;
      height:410px;
      display:flex;
      align-items:flex-end;
    }}
    .ai-bar-fill {{
      width:100%;
      height:var(--bar-height);
      display:flex;
      flex-direction:column;
      justify-content:center;
      gap:7px;
      padding:18px 17px;
      color:#fff;
      transform:scaleY(.02);
      transform-origin:bottom;
      transition:transform 1.05s cubic-bezier(.22,1,.36,1);
      box-shadow:inset 0 0 0 1px rgba(255,255,255,.16);
    }}
    .ai-bar-fill.purple {{ background:#493d86; }}
    .ai-bar-fill.navy {{ background:#002b73; }}
    .ai-bar-fill.magenta {{ background:#e80b78; }}
    .ai-shift-section.visible .ai-bar-fill {{
      transform:scaleY(1);
    }}
    .ai-bar-fill strong {{
      display:block;
      align-self:flex-end;
      color:#fff;
      font-size:clamp(30px, 2.7vw, 44px);
      font-weight:900;
      line-height:1;
    }}
    .ai-bar-fill p {{
      margin:0;
      color:#fff;
      font-size:clamp(13px, 1.05vw, 17px);
      font-weight:800;
      line-height:1.18;
      text-align:center;
    }}
    .ai-bar-fill small {{
      color:rgba(255,255,255,.88);
      font-size:clamp(11px, .9vw, 14px);
      font-weight:800;
      line-height:1.2;
      text-align:center;
    }}
    .today .ai-bar-fill {{
      padding:14px 12px;
      gap:6px;
    }}
    .today .ai-bar-fill strong {{
      font-size:clamp(28px, 2.35vw, 38px);
    }}
    .today .ai-bar-fill p {{
      font-size:clamp(11px, .9vw, 14px);
      line-height:1.12;
    }}
    .today .ai-bar-fill small {{
      font-size:clamp(12px, .95vw, 14px);
    }}
    .ai-shift-right {{
      min-height:100svh;
      display:grid;
      grid-template-rows:.28fr .72fr;
      align-items:stretch;
      gap:26px;
      padding:clamp(36px, 4.8vw, 58px) clamp(28px, 4.2vw, 60px);
      background:
        linear-gradient(180deg, rgba(255,0,102,.94) 0%, rgba(117,46,125,.9) 42%, rgba(0,34,68,1) 100%);
      color:#fff;
    }}
    .ai-shift-right h2 {{
      margin:0;
      align-self:center;
      color:#fff !important;
      text-align:center;
      font-size:clamp(28px, 2.55vw, 42px);
      font-weight:400;
      line-height:1.08;
    }}
    .ai-shift-right h2 img {{
      display:inline-block;
      width:min(230px, 28vw);
      margin:0 10px -8px 0;
      filter:brightness(0) invert(1);
    }}
    .ai-shift-right h2 span {{
      display:inline;
    }}
    .ai-shift-modules {{
      display:grid;
      gap:14px;
      align-self:start;
    }}
    .ai-shift-modules article {{
      padding:14px 20px;
      border-radius:14px;
      background:#fff;
      color:#0f172a;
      text-align:center;
      border:1px solid rgba(15,23,42,.22);
      box-shadow:0 12px 24px rgba(0,0,0,.26);
      opacity:0;
      transform:translateY(26px);
      transition:opacity .7s ease, transform .7s cubic-bezier(.22,1,.36,1);
    }}
    .ai-shift-section.visible .ai-shift-modules article {{
      opacity:1;
      transform:none;
    }}
    .ai-shift-section.visible .ai-shift-modules article:nth-child(2) {{ transition-delay:.08s; }}
    .ai-shift-section.visible .ai-shift-modules article:nth-child(3) {{ transition-delay:.16s; }}
    .ai-shift-section.visible .ai-shift-modules article:nth-child(4) {{ transition-delay:.24s; }}
    .ai-shift-modules h3 {{
      margin:0 0 6px;
      color:#05070d;
      font-size:clamp(16px, 1.18vw, 20px);
      line-height:1.08;
      text-transform:uppercase;
      letter-spacing:0;
    }}
    .ai-shift-modules p {{
      margin:0;
      color:#111827;
      font-size:clamp(13px, 1.08vw, 18px);
      line-height:1.18;
    }}
    .presence {{
      background:var(--soft);
    }}
    .presence .sticky-chapter {{
      padding-top:0;
    }}
    .presence-globe-scrolly {{
      width:100vw;
      margin-left:calc(50% - 50vw);
      min-height:188vh;
      border-radius:0;
      overflow:clip;
      background:#00040c;
      color:#fff;
    }}
    .presence-globe-stage {{
      position:sticky;
      top:0;
      min-height:100svh;
      display:grid;
      grid-template-columns:minmax(0, 1fr) minmax(420px, 1fr);
      align-items:stretch;
      isolation:isolate;
      background:#00040c;
    }}
    .presence-globe-visual {{
      position:relative;
      min-height:100svh;
      overflow:hidden;
      background:#00040c;
    }}
    .presence-globe-visual video {{
      position:absolute;
      inset:-3% -6% -3% -2%;
      width:108%;
      height:106%;
      object-fit:cover;
      object-position:center center;
      opacity:calc(.72 + (var(--presence-progress, 0) * .18));
      filter:saturate(1.04) contrast(1.1) brightness(calc(.58 + (var(--presence-progress, 0) * .14)));
      transform:scale(calc(1.04 - (var(--presence-progress, 0) * .018))) translate3d(calc(20px - (var(--presence-progress, 0) * 8px)), 0, 0);
      will-change:transform, filter, opacity;
    }}
    .presence-globe-visual::after {{
      content:"";
      position:absolute;
      inset:0;
      background:
        linear-gradient(90deg, rgba(0,4,12,.04) 0%, rgba(0,4,12,.08) 56%, #00040c 100%),
        radial-gradient(circle at 78% 50%, rgba(0,4,12,.18), rgba(0,4,12,.72) 74%);
      pointer-events:none;
    }}
    .presence-globe-copy {{
      min-height:100svh;
      display:grid;
      align-content:center;
      padding:clamp(48px, 7vw, 92px) clamp(34px, 7vw, 104px) clamp(42px, 6vw, 76px) clamp(28px, 4.6vw, 76px);
      background:
        radial-gradient(circle at 72% 22%, rgba(255,0,102,.14), transparent 30%),
        linear-gradient(90deg, rgba(0,4,12,.74), #00040c 28%, #00040c 100%);
    }}
    .presence-globe-copy .eyebrow {{
      color:var(--magenta);
      margin-bottom:10px;
    }}
    .presence-globe-copy h2 {{
      margin:0;
      max-width:720px;
      color:#fff;
      font-size:clamp(40px, 4.7vw, 72px);
      line-height:1.04;
      letter-spacing:0;
      font-weight:400;
    }}
    .globe-metrics {{
      display:grid;
      gap:18px;
      margin-top:clamp(38px, 8vh, 84px);
      max-width:560px;
      justify-self:end;
    }}
    .globe-metric {{
      display:flex;
      align-items:baseline;
      justify-content:flex-end;
      gap:13px;
      opacity:0;
      transform:translate3d(0, 16px, 0);
      transition:opacity .66s ease, transform .66s cubic-bezier(.22,1,.36,1);
    }}
    .globe-metric.is-visible {{
      opacity:1;
      transform:translate3d(0, 0, 0);
    }}
    .globe-metric strong {{
      color:#fff;
      font-size:clamp(36px, 4vw, 58px);
      line-height:.94;
      font-weight:900;
      letter-spacing:0;
      transition:color .36s ease;
    }}
    .globe-metric span {{
      color:#f8fafc;
      font-size:clamp(22px, 2.35vw, 38px);
      line-height:1;
      font-weight:400;
      transition:color .36s ease;
    }}
    .globe-metric.is-visible strong,
    .globe-metric.is-visible span {{
      color:var(--magenta);
    }}
    .globe-latam {{
      margin-top:30px;
      padding-top:26px;
      border-top:1px solid rgba(255,255,255,0);
      opacity:0;
      transform:translate3d(0, 16px, 0);
      transition:opacity .72s ease, transform .72s cubic-bezier(.22,1,.36,1), border-color .72s ease;
    }}
    .globe-latam.is-visible {{
      opacity:1;
      transform:translate3d(0, 0, 0);
      border-color:rgba(255,255,255,.16);
    }}
    .globe-latam strong {{
      display:block;
      color:#fff;
      font-size:clamp(28px, 3vw, 44px);
      line-height:1.04;
      margin-bottom:14px;
    }}
    .globe-latam p {{
      margin:0;
      color:#cbd5e1;
      font-size:clamp(16px, 1.25vw, 21px);
      line-height:1.45;
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
      grid-template-columns:repeat(7,minmax(0,1fr));
      gap:12px;
      margin:30px 0 34px;
    }}
    .industry {{
      min-height:96px;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:16px 14px;
      border-radius:8px;
      border:0;
      background:var(--industry-bg, #002244);
      color:#fff;
      font:inherit;
      font-weight:900;
      font-size:clamp(12px, .86vw, 15px);
      line-height:1.14;
      text-align:center;
      box-shadow:0 18px 38px rgba(15,23,42,.14);
      cursor:pointer;
      transition:transform .22s ease, box-shadow .22s ease, filter .22s ease;
    }}
    .industry:hover,
    .industry:focus-visible {{
      transform:translateY(-3px);
      box-shadow:0 24px 48px rgba(15,23,42,.2);
      filter:saturate(1.08);
    }}
    .industry.is-active {{
      box-shadow:0 0 0 3px rgba(255,0,102,.22), 0 24px 48px rgba(15,23,42,.2);
    }}
    .industry span {{
      display:block;
    }}
    .logo-marquee {{
      overflow:hidden;
      border:1px solid var(--line);
      border-radius:8px;
      background:#fff;
      padding:22px 0;
      mask-image:linear-gradient(90deg, transparent, #000 7%, #000 93%, transparent);
    }}
    .logo-track {{
      display:flex;
      width:max-content;
      animation:marquee 96s linear infinite;
    }}
    .logo-marquee.is-filtered .logo-track {{
      animation-duration:24s;
    }}
    .logo-marquee:hover .logo-track {{ animation-play-state:paused; }}
    .logo-cell {{
      width:172px;
      height:76px;
      display:grid;
      place-items:center;
      flex:0 0 172px;
      padding:15px 24px;
      opacity:1;
      transition:opacity .22s ease, transform .22s ease;
    }}
    .logo-cell.is-filtered-out {{ display:none; }}
    .logo-cell:hover {{ transform:translateY(-2px); }}
    .logo-cell img {{
      max-height:46px;
      max-width:132px;
      object-fit:contain;
    }}
    .presence-after-globe {{
      width:100vw;
      margin-left:calc(50% - 50vw);
      padding:92px 0 84px;
      background:#fff;
      color:var(--ink);
    }}
    .presence-after-inner {{
      width:min(1180px, calc(100% - 48px));
      margin:0 auto;
    }}
    .presence-after-inner h2 {{
      color:var(--ink);
      max-width:900px;
    }}
    .presence-after-inner p {{
      max-width:1040px;
      color:#475569;
    }}
    .heineken-bottle-scrolly {{
      width:100vw;
      margin-left:calc(50% - 50vw);
      min-height:176vh;
      overflow:clip;
      background:
        radial-gradient(circle at 72% 30%, rgba(255,0,102,.13), transparent 32%),
        radial-gradient(circle at 18% 70%, rgba(0,34,68,.34), transparent 38%),
        linear-gradient(135deg,#00040c 0%, #001126 56%, #08000d 100%);
      color:#fff;
      border-top:0;
    }}
    .heineken-bottle-stage {{
      position:sticky;
      top:0;
      min-height:100svh;
      display:grid;
      place-items:center;
      isolation:isolate;
      overflow:hidden;
    }}
    .heineken-bottle-stage::before {{
      content:"";
      position:absolute;
      inset:0;
      z-index:1;
      background:
        linear-gradient(90deg, rgba(0,4,12,.9), transparent 30%, transparent 70%, rgba(0,4,12,.76)),
        radial-gradient(circle at 50% 50%, transparent 0 28%, rgba(0,4,12,.58) 76%);
      pointer-events:none;
    }}
    .heineken-bottle-copy {{
      position:absolute;
      z-index:5;
      top:clamp(72px, 10vh, 110px);
      left:min(8vw, 110px);
      width:min(680px, calc(100% - 48px));
      opacity:calc(.35 + (var(--heineken-progress, 0) * .65));
      transform:translate3d(0, calc(22px - (var(--heineken-progress, 0) * 22px)), 0);
    }}
    .heineken-bottle-copy h2 {{
      margin:0;
      color:var(--magenta);
      font-size:clamp(13px, 1.35vw, 21px);
      line-height:1;
      font-weight:500;
      letter-spacing:.01em;
      text-transform:uppercase;
    }}
    .heineken-history-title {{
      position:relative;
      z-index:2;
      display:flex;
      align-items:center;
      justify-content:center;
      gap:clamp(16px, 2.4vw, 34px);
      margin:0;
      width:min(1180px, calc(100% - 48px));
      color:rgba(255,255,255,.68);
      font-size:clamp(34px, 4.72vw, 80px);
      line-height:.94;
      letter-spacing:0;
      font-weight:900;
      opacity:var(--heineken-text-opacity, 0);
      clip-path:inset(0 var(--heineken-text-clip, 100%) 0 0);
      transition:opacity .18s linear;
      pointer-events:auto;
      text-shadow:0 22px 70px rgba(0,5,16,.48);
      transform:translateX(clamp(-120px, -6vw, -52px));
    }}
    .heineken-history-title span {{
      display:block;
      white-space:nowrap;
    }}
    .heineken-logo-link {{
      appearance:none;
      display:grid;
      place-items:center;
      width:clamp(170px, 18vw, 280px);
      min-width:0;
      padding:12px 0;
      border:0;
      background:transparent;
      cursor:pointer;
      transform:translateY(.04em);
    }}
    .heineken-logo-link img {{
      width:100%;
      max-height:clamp(50px, 7vw, 96px);
      object-fit:contain;
      filter:drop-shadow(0 18px 42px rgba(255,0,102,.34));
    }}
    .heineken-logo-link:hover img,
    .heineken-logo-link:focus-visible img {{
      filter:drop-shadow(0 0 28px rgba(255,0,102,.65));
    }}
    .heineken-bottle-video-wrap {{
      position:absolute;
      z-index:3;
      left:50%;
      top:auto;
      bottom:0;
      width:min(38.4vw, 608px);
      height:min(92.8svh, 832px);
      min-width:416px;
      transform:translate3d(var(--heineken-bottle-x, -34vw), 0, 0);
      transform-origin:center;
      pointer-events:none;
      filter:drop-shadow(0 36px 80px rgba(255,0,102,.38));
      will-change:transform;
    }}
    .heineken-bottle-video-wrap::after {{
      display:none;
    }}
    .heineken-bottle-video {{
      width:100%;
      height:100%;
      object-fit:cover;
      object-position:center;
      filter:hue-rotate(240deg) saturate(2.45) contrast(1.14) brightness(1.02);
      mix-blend-mode:normal;
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
      max-height:96vh;
      border:0;
      border-radius:10px;
      padding:0;
      box-shadow:0 30px 100px rgba(15,23,42,.34);
      overflow:hidden;
    }}
    dialog::backdrop {{ background:rgba(2,6,23,.62); }}
    .modal-body {{
      max-height:96vh;
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
      padding:22px 28px 24px;
      background:
        radial-gradient(circle at 82% 0%, rgba(255,0,102,.28), transparent 34%),
        linear-gradient(135deg,#000613 0%, #061229 52%, #160015 100%);
    }}
    .positioning-modal .modal-head {{
      align-items:flex-start;
      border-bottom-color:rgba(226,232,240,.18);
      padding-bottom:14px;
      margin-bottom:18px;
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
      font-size:clamp(30px, 3.2vw, 44px);
      line-height:.98;
      letter-spacing:0;
    }}
    .positioning-modal .close {{
      border-color:rgba(255,255,255,.22);
      background:rgba(255,255,255,.06);
      color:#fff;
      min-width:40px;
      height:40px;
      font-size:22px;
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
      padding:18px 24px 14px;
    }}
    .comparison-head h3 {{
      margin:0;
      color:#fff;
      font-size:clamp(22px, 1.9vw, 28px);
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
      width:210px;
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
      gap:18px;
      padding:12px 24px;
      background:rgba(255,255,255,.04);
    }}
    .artefact-cell {{
      padding:12px 24px 12px 30px;
      background:linear-gradient(145deg, rgba(255,0,102,.72), rgba(117,46,125,.68) 58%, rgba(39,50,117,.5));
    }}
    .competitor-cell strong {{
      color:#fff;
      font-size:15px;
      line-height:1.12;
    }}
    .competitor-cell p {{
      margin:0;
      color:rgba(255,255,255,.78);
      font-size:14px;
      line-height:1.22;
    }}
    .artefact-cell ul {{
      margin:0;
      padding:0 0 0 18px;
      color:#fff;
      font-size:13.5px;
      line-height:1.14;
    }}
    .artefact-cell li + li {{ margin-top:3px; }}
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
    #differentiators .genai-scene .genai-kicker h2 {{
      color:#fff !important;
      -webkit-text-fill-color:#fff;
      opacity:1;
      mix-blend-mode:normal;
    }}
    #differentiators .genai-scene .genai-kicker p {{
      color:#e2e8f0 !important;
      opacity:1;
    }}
    #differentiators .genai-story .story-eyebrow {{
      color:var(--magenta) !important;
    }}
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
    .node,
    .metric,
    .office,
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
      background:#fff;
      border-radius:8px;
      margin:0 7px;
      filter:none;
      opacity:1;
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
      .hero-grid, .chapter-grid, .positioning, .map-panel, .pillar-wrap, .ecosystem, .event-grid {{
        grid-template-columns:1fr;
      }}
      .presence-globe-scrolly {{
        min-height:168vh;
      }}
      .presence-globe-stage {{
        grid-template-columns:1fr;
      }}
      .presence-globe-visual {{
        position:absolute;
        inset:0;
        min-height:100%;
      }}
      .presence-globe-visual video {{
        inset:-2% -26% 22% -18%;
        width:144%;
        height:82%;
        opacity:.52;
      }}
      .presence-globe-visual::after {{
        background:
          linear-gradient(180deg, rgba(0,4,12,.08) 0%, #00040c 58%, #00040c 100%),
          radial-gradient(circle at 50% 24%, transparent 0 22%, rgba(0,4,12,.72) 76%);
      }}
      .presence-globe-copy {{
        position:relative;
        z-index:1;
        padding:112px 24px 56px;
        background:linear-gradient(180deg, rgba(0,4,12,.38), #00040c 62%);
      }}
      .globe-metrics {{
        justify-self:stretch;
      }}
      .globe-metric {{
        justify-content:flex-start;
      }}
      .heineken-bottle-scrolly {{
        min-height:150vh;
      }}
      .heineken-bottle-copy {{
        top:88px;
        left:24px;
      }}
      .heineken-history-title {{
        flex-direction:column;
        gap:8px;
        align-items:flex-start;
        justify-content:center;
        font-size:clamp(30px, 10.4vw, 58px);
        transform:translateX(-18px);
      }}
      .heineken-logo-link {{
        width:min(300px, 72vw);
      }}
      .heineken-bottle-video-wrap {{
        width:min(69vw, 368px);
        height:74svh;
        min-width:208px;
        top:auto;
        bottom:0;
      }}
      .operating-venn-scene {{
        margin-top:40px;
        min-height:auto;
      }}
      .operating-venn-copy h2 {{
        font-size:clamp(32px, 9vw, 48px);
      }}
      .operating-venn-panel {{
        position:relative;
        top:auto;
        grid-template-columns:1fr;
        min-height:0;
        padding:22px;
        gap:22px;
        border-radius:18px;
      }}
      .venn-stage {{
        grid-row:1;
        min-height:430px;
        transform:none;
      }}
      .venn-pillar {{
        grid-template-columns:repeat(2, minmax(0, 1fr));
        gap:12px;
      }}
      .venn-pillar.left,
      .venn-pillar.right {{
        justify-items:stretch;
      }}
      .venn-pill {{
        width:100%;
        min-height:56px;
        font-size:14px;
        padding:12px 14px;
      }}
      .venn-circle {{
        width:64%;
        top:38px;
      }}
      .venn-business {{ left:0; }}
      .venn-technical {{ right:0; }}
      .venn-lens {{
        width:38%;
        min-width:190px;
      }}
      .venn-lens img {{
        width:68px;
      }}
      .venn-lens strong {{
        font-size:18px;
      }}
      .venn-lens span {{
        font-size:12px;
      }}
      .ai-shift-section {{
        grid-template-columns:1fr;
        min-height:0;
      }}
      .ai-shift-left,
      .ai-shift-right {{
        min-height:auto;
        padding:48px 24px;
      }}
      .ai-bars {{
        min-height:480px;
        max-width:none;
      }}
      .ai-bar {{
        height:430px;
      }}
      .ai-bar-fill {{
        padding:20px 16px;
      }}
      .ai-shift-right {{
        gap:28px;
      }}
      .ai-shift-right h2 img {{
        width:min(280px, 70vw);
      }}
      .hero-visual, .person-video {{ min-height:460px; }}
      .chapter-aside, .pyramid {{ position:relative; top:auto; }}
      .scene {{ min-height:auto; }}
      .stat-strip, .diff-grid, .metric-grid, .proof-grid, .service-grid, .contact-wrap, .modal-metrics {{
        grid-template-columns:1fr;
      }}
      .genai-kicker h2 {{
        font-size:clamp(38px, 10vw, 54px);
      }}
      .genai-inner {{
        width:min(100% - 32px, 720px);
      }}
      .genai-timeline {{
        gap:18px;
        padding:18px;
      }}
      .genai-row {{
        grid-template-columns:1fr;
        gap:14px;
        min-height:0;
      }}
      .genai-moment {{
        grid-template-columns:1fr 54px 34px;
        min-height:118px;
        padding:0;
      }}
      .genai-moment::before {{
        right:16px;
      }}
      .moment-copy span {{
        font-size:15px;
      }}
      .moment-copy strong {{
        font-size:28px;
      }}
      .moment-icon {{
        width:48px;
        height:48px;
      }}
      .moment-icon.genai-stars {{
        width:52px;
        height:52px;
      }}
      .moment-dot {{
        width:30px;
        height:30px;
        border-width:2px;
      }}
      .moment-dot::after {{
        inset:6px;
      }}
      .genai-story {{
        grid-template-columns:1fr;
        gap:20px;
        padding:22px;
      }}
      .genai-row.early-arc,
      .genai-row.early-arc .genai-moment,
      .genai-story.early-arc-story {{
        min-height:0;
      }}
      .genai-story.early-arc-story {{
        grid-template-columns:1fr;
        padding:24px;
      }}
      .genai-story.early-arc-story h3 {{
        font-size:26px;
      }}
      .genai-story.early-arc-story p:not(.story-eyebrow) {{
        font-size:16px;
      }}
      .genai-logo-field.before.early-usecases {{
        grid-template-columns:1fr;
      }}
      .genai-story h3 {{
        font-size:24px;
      }}
      .genai-logo-field,
      .genai-logo-field.before,
      .genai-logo-field.agentic {{
        display:flex;
        justify-content:flex-start;
        min-height:0;
        padding:0;
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
      .operating-venn-panel {{ padding:16px; }}
      .ai-shift-left,
      .ai-shift-right {{
        padding:40px 18px;
      }}
      .ai-bars {{
        grid-template-columns:1fr;
        gap:14px;
        min-height:0;
      }}
      .ai-bar-wrap {{
        grid-template-columns:94px minmax(0, 1fr);
        grid-template-rows:1fr;
        align-items:center;
        gap:10px;
      }}
      .bar-timing {{
        margin:0;
        font-size:13px;
      }}
      .ai-bar {{
        height:180px;
      }}
      .ai-bar-fill {{
        min-height:150px;
      }}
      .venn-stage {{ min-height:350px; }}
      .venn-pillar {{ grid-template-columns:1fr; }}
      .venn-circle {{
        width:69%;
        top:34px;
      }}
      .venn-circle-title {{
        display:none;
      }}
      .venn-lens {{
        width:42%;
        min-width:150px;
        padding:20px 14px;
      }}
      .venn-lens img {{ width:52px; }}
      .venn-lens strong {{ font-size:15px; }}
      .venn-lens span {{ display:none; }}
      .heineken-bottle-copy h2 {{ font-size:clamp(12px, 4vw, 21px); }}
      .heineken-bottle-video-wrap {{
        width:83vw;
        height:70svh;
        opacity:.92;
      }}
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
          {operating_model_section}
          {genai_timeline_section}
          {ai_shift_section}
        </div>
      </div>
    </section>

    <section id="presence" class="presence section">
      {section_transition("Presence")}
      <div class="sticky-chapter">
        <div class="container">
          <article class="presence-globe-scrolly reveal" data-presence-globe>
            <div class="presence-globe-stage">
              <div class="presence-globe-visual" aria-hidden="true">
                <video data-presence-video muted playsinline preload="auto" src="{globe_background_video}"></video>
              </div>
              <div class="presence-globe-copy">
              <div class="eyebrow">Global footprint</div>
              <h2>Artefact operates globally and scales with LATAM depth.</h2>
                <div class="globe-metrics" aria-label="Artefact footprint indicators">
                  <div class="globe-metric" data-presence-step="1"><strong data-count="27" data-count-start>0</strong><span>Countries</span></div>
                  <div class="globe-metric" data-presence-step="2"><strong data-count="2500" data-count-start>0</strong><span>Employees</span></div>
                  <div class="globe-metric" data-presence-step="3"><strong data-count="36" data-count-start>0</strong><span>Offices</span></div>
                  <div class="globe-latam" data-presence-step="4">
                    <strong><span data-count="400" data-prefix="+" data-count-start>+0</span> Artefactors in LATAM</strong>
                    <p>Regional offices in Sao Paulo, Mexico City, Santiago, and Bogota.</p>
                  </div>
                </div>
              </div>
            </div>
          </article>

          <div class="presence-after-globe">
            <div class="presence-after-inner">
              <div class="eyebrow">Industries and regional partners</div>
              <h2>Artefact works across sectors where data, AI, and adoption unlock measurable value.</h2>
              <p>Our 1000+ clients, including 300 international brands, trust us across financial services, retail, B2B and industrial markets, CPG, healthcare and pharma, travel, transport, tourism, and other strategic ecosystems.</p>
              <div class="industry-grid" data-industry-filters>{industry_buttons}</div>
              <div class="logo-marquee" aria-label="Selected client logos" data-logo-marquee><div class="logo-track">{logo_track}</div></div>
            </div>
          </div>

          <article class="heineken-bottle-scrolly reveal" data-heineken-bottle>
            <div class="heineken-bottle-stage">
              <div class="heineken-bottle-copy">
                <h2>A memorable example</h2>
              </div>
              <h2 class="heineken-history-title">
                <span>Our history with</span>
                <button class="heineken-logo-link" type="button" data-case-trigger="heineken" aria-label="Open HEINEKEN case">
                  <img src="{heineken_white_logo}" alt="HEINEKEN logo">
                </button>
              </h2>
              <div class="heineken-bottle-video-wrap" aria-hidden="true">
                <video class="heineken-bottle-video" data-heineken-video muted playsinline loop preload="auto" src="{bottle_video}"></video>
              </div>
            </div>
          </article>
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
    document.documentElement.classList.add("js-enabled");
    const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const sections = [...document.querySelectorAll(".section")];
    const navLinks = [...document.querySelectorAll(".top-menu a")];
    const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
    const smooth = (value) => value * value * (3 - 2 * value);
    const vennScrolly = document.querySelector("[data-venn-scrolly]");
    const presenceGlobe = document.querySelector("[data-presence-globe]");
    const presenceVideo = document.querySelector("[data-presence-video]");
    const heinekenBottle = document.querySelector("[data-heineken-bottle]");
    const heinekenVideo = document.querySelector("[data-heineken-video]");
    let targetPresenceTime = 0;
    let renderedPresenceTime = 0;
    let presenceScrubFrame = null;

    function updateVennScrolly() {{
      if (!vennScrolly) return;
      vennScrolly.classList.remove("venn-step-0", "venn-step-1", "venn-step-2", "venn-step-3");
      if (prefersReduced) {{
        vennScrolly.classList.add("venn-step-3");
        return;
      }}
      const rect = vennScrolly.getBoundingClientRect();
      const travel = Math.max(1, rect.height - window.innerHeight * .75);
      const progress = clamp((window.innerHeight * .35 - rect.top) / travel);
      let step = 0;
      if (progress > .14) step = 1;
      if (progress > .40) step = 2;
      if (progress > .86) step = 3;
      vennScrolly.classList.add(`venn-step-${{step}}`);
    }}

    function stepPresenceScrub() {{
      if (!presenceVideo || !presenceVideo.duration || prefersReduced) {{
        presenceScrubFrame = null;
        return;
      }}

      const difference = targetPresenceTime - renderedPresenceTime;
      if (Math.abs(difference) < .01) {{
        renderedPresenceTime = targetPresenceTime;
        if (!presenceVideo.seeking) presenceVideo.currentTime = renderedPresenceTime;
        presenceScrubFrame = null;
        return;
      }}

      if (!presenceVideo.seeking) {{
        renderedPresenceTime += difference * .12;
        presenceVideo.currentTime = renderedPresenceTime;
      }}
      presenceScrubFrame = requestAnimationFrame(stepPresenceScrub);
    }}

    function requestPresenceScrub() {{
      if (presenceScrubFrame === null) {{
        presenceScrubFrame = requestAnimationFrame(stepPresenceScrub);
      }}
    }}

    function updatePresenceGlobe() {{
      if (!presenceGlobe) return;
      const rect = presenceGlobe.getBoundingClientRect();
      const travel = Math.max(1, presenceGlobe.offsetHeight - window.innerHeight);
      const progress = prefersReduced ? 1 : clamp(-rect.top / travel);
      const eased = smooth(progress);
      presenceGlobe.style.setProperty("--presence-progress", eased.toFixed(3));

      presenceGlobe.querySelectorAll("[data-presence-step]").forEach((item) => {{
        const step = Number(item.dataset.presenceStep || 1);
        const threshold = .13 + (step - 1) * .15;
        item.classList.toggle("is-visible", prefersReduced || progress >= threshold);
      }});

      if (presenceVideo && presenceVideo.duration && !prefersReduced) {{
        const usableDuration = Math.min(8, presenceVideo.duration);
        targetPresenceTime = eased * usableDuration;
        requestPresenceScrub();
      }}
    }}

    function updateHeinekenBottle() {{
      if (!heinekenBottle) return;
      const rect = heinekenBottle.getBoundingClientRect();
      const travel = Math.max(1, heinekenBottle.offsetHeight - window.innerHeight);
      const progress = prefersReduced ? 1 : clamp(-rect.top / travel);
      const eased = smooth(progress);
      const bottleX = -42 + eased * 56;
      const textProgress = smooth(clamp((progress - .1) / .56));

      heinekenBottle.style.setProperty("--heineken-progress", eased.toFixed(3));
      heinekenBottle.style.setProperty("--heineken-bottle-x", `${{bottleX.toFixed(2)}}vw`);
      heinekenBottle.style.setProperty("--heineken-text-opacity", textProgress.toFixed(3));
      heinekenBottle.style.setProperty("--heineken-text-clip", `${{((1 - textProgress) * 100).toFixed(2)}}%`);

      if (heinekenVideo && heinekenVideo.duration && !prefersReduced && !heinekenVideo.seeking) {{
        heinekenVideo.pause();
        heinekenVideo.currentTime = Math.min(heinekenVideo.duration - .05, eased * heinekenVideo.duration);
      }}
    }}

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
    window.addEventListener("scroll", updateVennScrolly, {{ passive: true }});
    window.addEventListener("scroll", updatePresenceGlobe, {{ passive: true }});
    window.addEventListener("scroll", updateHeinekenBottle, {{ passive: true }});
    window.addEventListener("resize", updateVennScrolly);
    window.addEventListener("resize", updatePresenceGlobe);
    window.addEventListener("resize", updateHeinekenBottle);
    if (presenceVideo) {{
      presenceVideo.addEventListener("loadedmetadata", () => {{
        renderedPresenceTime = 0;
        targetPresenceTime = 0;
        presenceVideo.currentTime = 0;
        updatePresenceGlobe();
      }});
    }}
    if (heinekenVideo) {{
      heinekenVideo.addEventListener("loadedmetadata", () => {{
        heinekenVideo.pause();
        heinekenVideo.currentTime = 0;
        updateHeinekenBottle();
      }});
    }}
    setActiveNav();
    updateVennScrolly();
    updatePresenceGlobe();
    updateHeinekenBottle();

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
      const prefix = element.dataset.prefix || "";
      const suffix = element.dataset.suffix || "";
      const start = performance.now();
      function frame(now) {{
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        element.textContent = prefix + Math.round(target * eased).toLocaleString("en-US") + suffix;
        if (progress < 1) requestAnimationFrame(frame);
      }}
      requestAnimationFrame(frame);
    }}
    const counterObserver = new IntersectionObserver((entries) => {{
      for (const entry of entries) {{
        if (entry.isIntersecting && !counted.has(entry.target)) {{
          counted.add(entry.target);
          const target = Number(entry.target.dataset.count);
          const prefix = entry.target.dataset.prefix || "";
          const suffix = entry.target.dataset.suffix || "";
          if (!prefersReduced) animateCounter(entry.target, target);
          else entry.target.textContent = prefix + target.toLocaleString("en-US") + suffix;
        }}
      }}
    }}, {{ threshold: .65 }});
    counters.forEach((counter) => {{
      if (counter.hasAttribute("data-count-start")) {{
        const prefix = counter.dataset.prefix || "";
        const suffix = counter.dataset.suffix || "";
        counter.textContent = prefersReduced ? prefix + Number(counter.dataset.count).toLocaleString("en-US") + suffix : prefix + "0" + suffix;
      }}
      counterObserver.observe(counter);
    }});

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

    const industryFilterButtons = [...document.querySelectorAll("[data-industry-filter]")];
    const logoCells = [...document.querySelectorAll("[data-industries]")];
    const logoMarquee = document.querySelector("[data-logo-marquee]");
    const logoTrack = document.querySelector("[data-logo-marquee] .logo-track");
    let activeIndustryFilter = null;

    function setIndustryFilter(filter) {{
      activeIndustryFilter = activeIndustryFilter === filter ? null : filter;
      industryFilterButtons.forEach((button) => {{
        const active = button.dataset.industryFilter === activeIndustryFilter;
        button.classList.toggle("is-active", active);
        button.setAttribute("aria-pressed", active ? "true" : "false");
      }});
      logoCells.forEach((cell) => {{
        const visible = !activeIndustryFilter || (cell.dataset.industries || "").split(" ").includes(activeIndustryFilter);
        cell.classList.toggle("is-filtered-out", !visible);
      }});
      if (logoMarquee) {{
        logoMarquee.classList.toggle("is-filtered", Boolean(activeIndustryFilter));
      }}
      if (logoTrack) {{
        logoTrack.style.animation = "none";
        void logoTrack.offsetHeight;
        logoTrack.style.animation = "";
      }}
    }}

    industryFilterButtons.forEach((button) => {{
      button.setAttribute("aria-pressed", "false");
      button.addEventListener("click", () => setIndustryFilter(button.dataset.industryFilter));
    }});

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
