#!/usr/bin/env python3
"""Static build for The House landing page.

Reads site.config.json + content/chapters.json, renders src/index.template.html,
generates optimized image variants and icons, and writes everything to dist/.

Usage:  python3 scripts/build.py            (requires Pillow: pip install Pillow)
"""
import html
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
CHAPTERS = json.loads((ROOT / "content" / "chapters.json").read_text(encoding="utf-8"))

# Only these images are ever published. The video contact sheet and the manuscript are never copied.
PUBLIC_IMAGES = {
    "the-house-book-thumbnail.jpg": [480, 800, 1200],
    "the-house-wraparound.jpg": [480, 800, 1200],
    "the-house-angled-mockup.jpg": [480, 800, 1200],
    "austine-ojo-portrait.jpg": [400, 700, 1097],
}

PAGE_TITLE = "The House by Austine Ojo | Life in Christ"
PAGE_DESCRIPTION = ("Explore The House by Austine Ojo: 15 chapters on life in Christ, knowing God, "
                    "meditation, discipleship and prayer. View chapter briefs and order the eBook.")


def fail(msg):
    print(f"BUILD FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def esc(s):
    return html.escape(str(s), quote=True)


def origin():
    domain = CONFIG.get("customDomain", "").strip().lower()
    if domain:
        if not re.fullmatch(r"[a-z0-9.-]+\.[a-z]{2,}", domain):
            fail(f"customDomain '{domain}' is not a valid hostname")
        return f"https://{domain}"
    o = CONFIG.get("siteOrigin", "").rstrip("/")
    if not o.startswith("https://") or "example" in o or "localhost" in o:
        fail("siteOrigin in site.config.json must be the real https production origin.")
    return o


# ---------------------------------------------------------------- images
def build_images():
    src_dir = ROOT / "assets"
    out_dir = DIST / "assets" / "img"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, widths in PUBLIC_IMAGES.items():
        src = src_dir / name
        if not src.exists():
            fail(f"missing asset {src}")
        # Original kept byte-for-byte (used for og:image and largest fallback)
        shutil.copy2(src, DIST / "assets" / name)
        im = Image.open(src).convert("RGB")
        stem = src.stem
        for w in widths:
            h = round(im.height * w / im.width)
            v = im if w == im.width else im.resize((w, h), Image.LANCZOS)
            v.save(out_dir / f"{stem}-{w}.webp", "WEBP", quality=82, method=6)
            v.save(out_dir / f"{stem}-{w}.jpg", "JPEG", quality=84, optimize=True, progressive=True)


def house_icon(size, pad_ratio=0.0, rounded=True):
    """A new, simple house monogram (gold on deep plum) — not a copy of any old logo."""
    s = size * 4  # supersample
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bg = (42, 27, 61, 255)
    gold = (232, 198, 107, 255)
    r = int(s * 0.22) if rounded else 0
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=r, fill=bg)
    inset = s * (0.18 + pad_ratio)
    w = s - 2 * inset
    lw = max(4, int(s * 0.075))
    x0, x1 = inset, s - inset
    cx = s / 2
    roof_y = inset + w * 0.05
    eave_y = inset + w * 0.45
    base_y = inset + w * 0.95
    d.line([(x0, eave_y), (cx, roof_y), (x1, eave_y)], fill=gold, width=lw, joint="curve")
    wx0, wx1 = x0 + w * 0.14, x1 - w * 0.14
    d.line([(wx0, eave_y - w * 0.06), (wx0, base_y), (wx1, base_y), (wx1, eave_y - w * 0.06)], fill=gold, width=lw, joint="curve")
    dx0, dx1 = cx - w * 0.11, cx + w * 0.11
    d.line([(dx0, base_y), (dx0, base_y - w * 0.28), (dx1, base_y - w * 0.28), (dx1, base_y)], fill=gold, width=int(lw * 0.85), joint="curve")
    return img.resize((size, size), Image.LANCZOS)


def build_icons():
    icons = DIST / "icons"
    icons.mkdir(parents=True, exist_ok=True)
    house_icon(512).save(icons / "icon-512.png")
    house_icon(192).save(icons / "icon-192.png")
    # apple-touch-icon: full-bleed square (iOS rounds corners itself)
    house_icon(180, rounded=False).save(icons / "apple-touch-icon.png")
    house_icon(256).save(DIST / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    (icons / "icon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<rect width="32" height="32" rx="7" fill="#2A1B3D"/>'
        '<g fill="none" stroke="#E8C66B" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M6 15.5 16 7l10 8.5"/><path d="M9 13.5V25h14V13.5"/><path d="M14 25v-5.5h4V25"/></g></svg>',
        encoding="utf-8")
    manifest = {
        "name": "The House by Austine Ojo",
        "short_name": "The House",
        "description": PAGE_DESCRIPTION,
        "start_url": "./",
        "scope": "./",
        "display": "browser",
        "background_color": "#FAF8F2",
        "theme_color": "#2A1B3D",
        "icons": [
            {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    (DIST / "site.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- html
def chapters_html():
    out = []
    for ch in CHAPTERS:
        n = int(ch["number"])
        out.append(
            f'        <li class="chapter-card" id="chapter-{n:02d}">\n'
            f'          <p class="chapter-num">Chapter {n:02d}</p>\n'
            f'          <h3>{esc(ch["title"])}</h3>\n'
            f'          <p>{esc(ch["summary"])}</p>\n'
            f'        </li>')
    return "\n".join(out)


def json_ld(o):
    page = f"{o}/"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": f"{page}#website", "url": page, "name": CONFIG["siteName"],
             "inLanguage": "en", "about": {"@id": f"{page}#book"}},
            {"@type": "WebPage", "@id": f"{page}#webpage", "url": page, "name": PAGE_TITLE,
             "description": PAGE_DESCRIPTION, "inLanguage": "en",
             "isPartOf": {"@id": f"{page}#website"}, "mainEntity": {"@id": f"{page}#book"},
             "primaryImageOfPage": {"@type": "ImageObject", "url": f"{o}/assets/the-house-book-thumbnail.jpg",
                                    "width": 1536, "height": 1536}},
            {"@type": "Book", "@id": f"{page}#book", "name": CONFIG["bookTitle"],
             "alternativeHeadline": CONFIG["bookSubtitle"],
             "author": {"@id": f"{page}#author"}, "inLanguage": "en", "isbn": CONFIG["isbn"],
             "publisher": {"@type": "Organization", "name": CONFIG["publisher"]},
             "description": ("The House invites you to look beyond religious routine and pursue a personal "
                             "relationship with God. Across fifteen chapters, Austine Ojo explores identity in "
                             "Christ, the knowledge of God, meditation, discipleship, and a life of prayer."),
             "image": f"{o}/assets/the-house-book-thumbnail.jpg",
             "url": page,
             "bookFormat": "https://schema.org/EBook",
             "offers": {"@type": "Offer", "price": CONFIG["offer"]["price"],
                        "priceCurrency": CONFIG["offer"]["currency"], "url": purchase_url(),
                        "seller": {"@type": "Organization", "name": CONFIG["facebookPageName"]}},
             "hasPart": [{"@type": "Chapter", "position": c["number"], "name": c["title"]} for c in CHAPTERS]},
            {"@type": "Person", "@id": f"{page}#author", "name": CONFIG["author"],
             "image": f"{o}/assets/austine-ojo-portrait.jpg"},
        ],
    }
    return json.dumps(graph, indent=2, ensure_ascii=False).replace("</", "<\\/")


def whatsapp_url(with_message=True):
    from urllib.parse import quote
    num = re.sub(r"\D", "", CONFIG.get("whatsappNumber", ""))
    if not num:
        return ""
    url = f"https://wa.me/{num}"
    if with_message and CONFIG.get("orderMessage"):
        url += "?text=" + quote(CONFIG["orderMessage"])
    return url


def purchase_url():
    return CONFIG.get("purchaseUrl", "").strip() or whatsapp_url()


WA_ICON = ('<svg class="btn-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" '
           'd="M12 2a9.9 9.9 0 0 0-8.5 15l-1.4 5 5.1-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-3-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')


def ctas():
    buy = esc(purchase_url())
    price = esc(CONFIG["offer"].get("priceDisplay", ""))
    order_btn = (f'<a class="btn btn-primary" href="{buy}" target="_blank" rel="noopener noreferrer" data-track="order-{{where}}">'
                 f'{WA_ICON}Order the eBook · {price}<span class="sr-only"> on WhatsApp (opens in a new tab)</span></a>')
    chapters_btn = '<a class="btn btn-ghost" href="#chapters" data-track="chapters-{where}">Explore the Chapters</a>'
    primary = order_btn.format(where="hero")
    secondary = chapters_btn.format(where="hero")
    closing = order_btn.format(where="closing")
    faq = (f'Order the eBook for {price}. Transfer to the Hard Truth Gospel Mission account shown in '
           f'<a href="#get-the-book">Order the eBook</a>, then send your proof of payment on WhatsApp to '
           f'<a href="{esc(whatsapp_url(False))}" target="_blank" rel="noopener noreferrer" data-track="whatsapp-faq">'
           f'{esc(CONFIG["whatsappDisplay"])}<span class="sr-only"> (opens in a new tab)</span></a>.')
    return primary, secondary, closing, faq


def bank_accounts_html():
    out = []
    for acc in CONFIG["bankAccounts"]["accounts"]:
        num = esc(acc["number"])
        out.append(
            f'          <li class="bank-card">\n'
            f'            <p class="bank-cur"><span class="bank-code">{esc(acc["currency"])}</span> {esc(acc["label"])} account</p>\n'
            f'            <p class="bank-num" id="acct-{esc(acc["currency"]).lower()}">{num}</p>\n'
            f'            <button type="button" class="copy-btn" data-copy="{num}" aria-describedby="acct-{esc(acc["currency"]).lower()}">'
            f'Copy<span class="sr-only"> {esc(acc["currency"])} account number</span></button>\n'
            f'          </li>')
    return "\n".join(out)


def build_html(o):
    tpl = (ROOT / "src" / "index.template.html").read_text(encoding="utf-8")
    primary, secondary, closing, faq = ctas()
    verification = []
    if CONFIG.get("googleSiteVerification"):
        verification.append(f'<meta name="google-site-verification" content="{esc(CONFIG["googleSiteVerification"])}">')
    if CONFIG.get("bingSiteVerification"):
        verification.append(f'<meta name="msvalidate.01" content="{esc(CONFIG["bingSiteVerification"])}">')
    robots = ('<meta name="robots" content="index, follow, max-image-preview:large">' if CONFIG.get("indexable")
              else '<meta name="robots" content="noindex, nofollow">')
    values = {
        "PAGE_TITLE": esc(PAGE_TITLE),
        "PAGE_DESCRIPTION": esc(PAGE_DESCRIPTION),
        "AUTHOR": esc(CONFIG["author"]),
        "SITE_NAME": esc(CONFIG["siteName"]),
        "CANONICAL": esc(f"{o}/"),
        "OG_IMAGE": esc(f"{o}/assets/the-house-book-thumbnail.jpg"),
        "ROBOTS_META": robots,
        "VERIFICATION_META": "\n".join(verification),
        "VERSION": datetime.now(timezone.utc).strftime("%Y%m%d%H%M"),
        "JSON_LD": json_ld(o),
        "CHAPTERS": chapters_html(),
        "PRIMARY_CTA": primary,
        "SECONDARY_CTA": secondary,
        "CLOSING_CTAS": closing,
        "FAQ_GET_COPY": faq,
        "PRICE_DISPLAY": esc(CONFIG["offer"]["priceDisplay"]),
        "OFFER_FORMAT": esc(CONFIG["offer"]["format"]),
        "WHATSAPP_URL": esc(whatsapp_url(False)),
        "WHATSAPP_DISPLAY": esc(CONFIG["whatsappDisplay"]),
        "FB_PAGE_NAME": esc(CONFIG["facebookPageName"]),
        "ACCOUNT_NAME": esc(CONFIG["bankAccounts"]["accountName"]),
        "BANK_NAME": esc(CONFIG["bankAccounts"]["bank"]),
        "BANK_ACCOUNTS": bank_accounts_html(),
        "FACEBOOK_URL": esc(CONFIG["facebookUrl"]),
        "PUBLISHER": esc(CONFIG["publisher"]),
        "ISBN_DISPLAY": esc(CONFIG["isbnDisplay"]),
    }
    out = tpl
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if left:
        fail(f"unreplaced template tokens: {sorted(set(left))}")
    (DIST / "index.html").write_text(out, encoding="utf-8")


def build_seo(o):
    for name in ("sitemap.xml", "robots.txt"):
        tpl = (ROOT / "seo" / f"{name}.template").read_text(encoding="utf-8")
        val = xml_escape(o) if name.endswith(".xml") else o
        out = tpl.replace("{{SITE_ORIGIN}}", val)
        if not CONFIG.get("indexable") and name == "robots.txt":
            out = "User-agent: *\nAllow: /\n"  # let crawlers see the noindex meta
        if "{{" in out:
            fail(f"unreplaced token in {name}")
        (DIST / name).write_text(out, encoding="utf-8")


def main():
    o = origin()
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    build_images()
    build_icons()
    shutil.copy2(ROOT / "src" / "styles.css", DIST / "styles.css")
    shutil.copy2(ROOT / "src" / "main.js", DIST / "main.js")
    build_html(o)
    build_seo(o)
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    domain = CONFIG.get("customDomain", "").strip().lower()
    if domain:
        (DIST / "CNAME").write_text(domain + "\n", encoding="utf-8")
    # Guardrails: nothing private or placeholder ships
    for p in DIST.rglob("*"):
        low = p.name.lower()
        if p.suffix.lower() in {".pdf", ".mp4", ".mov"} or "video-reference" in low:
            fail(f"private file in build: {p}")
        if p.suffix in {".html", ".xml", ".txt", ".css", ".js", ".webmanifest"}:
            text = p.read_text(encoding="utf-8")
            for bad in ("{{", "localhost", "example.com", "TODO", 'href="#"'):
                if bad in text:
                    fail(f"'{bad}' found in {p.relative_to(DIST)}")
    print(f"Built {sum(1 for _ in DIST.rglob('*') if _.is_file())} files into {DIST} for {o}/")


if __name__ == "__main__":
    main()
