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
# Transparent cut-out of the hero book (made by scripts/cutout_book.py from the thumbnail)
CUTOUT = ("the-house-book-cutout.png", [360, 560, 786])

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
    name, widths = CUTOUT
    src = src_dir / name
    if not src.exists():
        fail(f"missing {src}: run python3 scripts/cutout_book.py")
    im = Image.open(src).convert("RGBA")
    for w in widths:
        h = round(im.height * w / im.width)
        v = im if w == im.width else im.resize((w, h), Image.LANCZOS)
        v.save(out_dir / f"{src.stem}-{w}.webp", "WEBP", quality=86, method=6)
        v.save(out_dir / f"{src.stem}-{w}.png", "PNG", optimize=True)


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
            f'        <li class="chapter-card" id="chapter-{n:02d}" data-num="{n:02d}">\n'
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
             "inLanguage": "en", "about": {"@id": f"{page}#book"},
             "copyrightYear": datetime.now(timezone.utc).year,
             "copyrightHolder": {"@type": "Organization", "name": CONFIG["rightsHolder"]}},
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


def whatsapp_url(with_message=True, message_key="orderMessage"):
    from urllib.parse import quote
    num = re.sub(r"\D", "", CONFIG.get("whatsappNumber", ""))
    if not num:
        return ""
    url = f"https://wa.me/{num}"
    if with_message and CONFIG.get(message_key):
        url += "?text=" + quote(CONFIG[message_key])
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
    copy_icon = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="8" y="8" width="12" height="12" rx="2.5" '
                 'fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" '
                 'fill="none" stroke="currentColor" stroke-width="2"/></svg>')
    for acc in CONFIG["bankAccounts"]["accounts"]:
        num = esc(acc["number"])
        cur = esc(acc["currency"])
        out.append(
            f'          <li class="bank-row">\n'
            f'            <span class="bank-code" aria-hidden="true">{cur}</span>\n'
            f'            <span class="bank-info"><span class="bank-cur">{esc(acc["label"])} ({cur})</span>'
            f'<span class="bank-num" id="acct-{cur.lower()}">{num}</span></span>\n'
            f'            <button type="button" class="copy-btn" data-copy="{num}" aria-describedby="acct-{cur.lower()}">'
            f'{copy_icon}<span class="copy-label">Copy</span><span class="sr-only"> {cur} account number</span></button>\n'
            f'          </li>')
    return "\n".join(out)



# ---------------------------------------------------------------- footer (shared by every page)
FB_PATH = ("M13.5 21v-7.6h2.6l.4-3h-3V8.5c0-.9.3-1.5 1.5-1.5h1.6V4.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3"
           "h2.6V21h3.1Z")
WA_PATH = re.search(r'd="([^"]+)"', WA_ICON).group(1)
X_PATH = "M17.8 3h3.1l-6.8 7.8 8 10.2h-6.3l-4.9-6.4L5.3 21H2.2l7.3-8.3L1.8 3h6.4l4.4 5.8L17.8 3Zm-1.1 16.2h1.7L7.3 4.7H5.5l11.2 14.5Z"
TG_PATH = "M21.4 4.2 2.9 11.3c-1.3.5-1.2 1.2-.2 1.5l4.7 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.4l2.3-2.2 4.7 3.5c.9.5 1.5.2 1.7-.8l3.1-14.6c.3-1.3-.5-1.9-1.4-1.5ZM8.5 14l9.4-5.9c.5-.3.9-.1.5.2l-8 7.2-.3 3.3L8.5 14Z"


def _svg(path, extra=""):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"{extra}><path fill="currentColor" d="{path}"/></svg>'


def share_links(o):
    from urllib.parse import quote
    url = f"{o}/"
    text = CONFIG.get("shareText") or PAGE_TITLE
    mail_icon = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="3" y="5" width="18" height="14" rx="2.5" '
                 'fill="none" stroke="currentColor" stroke-width="2"/><path d="m4 7 8 6 8-6" fill="none" stroke="currentColor" '
                 'stroke-width="2" stroke-linejoin="round"/></svg>')
    link_icon = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1.2 1.2" '
                 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1.2-1.2" '
                 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')
    more_icon = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="18" cy="5" r="2.6" fill="none" stroke="currentColor" stroke-width="2"/>'
                 '<circle cx="6" cy="12" r="2.6" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="18" cy="19" r="2.6" fill="none" stroke="currentColor" stroke-width="2"/>'
                 '<path d="m8.3 13.3 7.4 4.4M15.7 6.3 8.3 10.7" stroke="currentColor" stroke-width="2"/></svg>')
    items = [
        ("whatsapp", "WhatsApp", f"https://wa.me/?text={quote(text + ' ' + url)}", _svg(WA_PATH)),
        ("facebook", "Facebook", f"https://www.facebook.com/sharer/sharer.php?u={quote(url, safe='')}", _svg(FB_PATH)),
        ("x", "X", f"https://x.com/intent/post?text={quote(text)}&url={quote(url, safe='')}", _svg(X_PATH)),
        ("telegram", "Telegram", f"https://t.me/share/url?url={quote(url, safe='')}&text={quote(text)}", _svg(TG_PATH)),
        ("email", "Email", f"mailto:?subject={quote(CONFIG['bookTitle'] + ' by ' + CONFIG['author'])}&body={quote(text + chr(10) + chr(10) + url)}", mail_icon),
    ]
    out = []
    for key, name, href, icon in items:
        tgt = '' if href.startswith("mailto:") else ' target="_blank" rel="noopener noreferrer"'
        sr = "" if href.startswith("mailto:") else " (opens in a new tab)"
        out.append(f'<li><a class="share-btn share-{key}" href="{esc(href)}"{tgt} data-track="share-{key}">{icon}'
                   f'<span>{name}</span><span class="sr-only"> — share this book{sr}</span></a></li>')
    out.append(f'<li><button type="button" class="share-btn share-copy" data-copy="{esc(url)}" data-copy-what="Link" data-track="share-copy">'
               f'{link_icon}<span class="copy-label">Copy link</span></button></li>')
    out.append(f'<li hidden data-native-share><button type="button" class="share-btn share-native" data-share-url="{esc(url)}" '
               f'data-share-text="{esc(text)}" data-share-title="{esc(PAGE_TITLE)}" data-track="share-native">{more_icon}<span>More</span></button></li>')
    return "\n          ".join(out)


def footer_html(o, base=""):
    """base is '' on the home page and './' on the policy pages, so section links work from both."""
    year = datetime.now(timezone.utc).year
    sections = [("top", "Home"), ("about", "About the Book"), ("chapters", "Chapters"), ("inside", "Inside the Cover"),
                ("author", "The Author"), ("get-the-book", "Order the eBook"), ("faq", "Reader Questions")]
    nav = "\n          ".join(f'<li><a href="{base}#{sid}">{label}</a></li>' for sid, label in sections)
    holder = esc(CONFIG["rightsHolder"])
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <p class="footer-title">The House</p>
      <p class="footer-sub">2nd Corinthians 5:17 · by {esc(CONFIG["author"])}</p>
      <div class="footer-social">
        <a href="{esc(CONFIG["facebookUrl"])}" target="_blank" rel="noopener noreferrer" data-track="facebook-footer">{_svg(FB_PATH)}<span>Follow {esc(CONFIG["facebookPageName"])}<span class="sr-only"> on Facebook (opens in a new tab)</span></span></a>
        <a href="{esc(whatsapp_url(False))}" target="_blank" rel="noopener noreferrer" data-track="whatsapp-footer">{_svg(WA_PATH)}<span>{esc(CONFIG["whatsappDisplay"])}<span class="sr-only"> on WhatsApp (opens in a new tab)</span></span></a>
      </div>
    </div>
    <nav class="footer-nav" aria-labelledby="footer-nav-title">
      <h2 class="footer-heading" id="footer-nav-title">Page navigation</h2>
      <ul>
          {nav}
      </ul>
    </nav>
  </div>
  <div class="container footer-share" aria-labelledby="footer-share-title">
    <h2 class="footer-heading" id="footer-share-title">Share this book</h2>
    <p class="footer-share-note">Know someone who would be blessed by <cite>The House</cite>? Send them the link.</p>
    <ul class="share-list" role="list">
          {share_links(o)}
    </ul>
  </div>
  <div class="container footer-base">
    <p class="footer-copy">© {year} {holder}. All rights reserved.</p>
    <ul class="footer-legal" role="list">
      <li><a href="{base or './'}privacy.html">Privacy Policy</a></li>
      <li><a href="{base or './'}terms.html">Terms of Use</a></li>
    </ul>
  </div>
</footer>"""


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
        "ORDER_URL": esc(purchase_url()),
        "PAPERBACK_URL": esc(whatsapp_url(True, "paperbackMessage")),
        "WHATSAPP_DISPLAY": esc(CONFIG["whatsappDisplay"]),
        "FB_PAGE_NAME": esc(CONFIG["facebookPageName"]),
        "ACCOUNT_NAME": esc(CONFIG["bankAccounts"]["accountName"]),
        "BANK_NAME": esc(CONFIG["bankAccounts"]["bank"]),
        "BANK_ACCOUNTS": bank_accounts_html(),
        "FACEBOOK_URL": esc(CONFIG["facebookUrl"]),
        "PUBLISHER": esc(CONFIG["publisher"]),
        "ISBN_DISPLAY": esc(CONFIG["isbnDisplay"]),
        "FOOTER": footer_html(o),
    }
    out = tpl
    for k, v in values.items():
        out = out.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[A-Z_]+\}\}", out)
    if left:
        fail(f"unreplaced template tokens: {sorted(set(left))}")
    (DIST / "index.html").write_text(out, encoding="utf-8")
    build_policies(o, robots)



POLICIES = {
    "privacy": ("Privacy Policy",
                "How Hard Truth Gospel Mission handles information when you visit this site or order The House by Austine Ojo."),
    "terms": ("Terms of Use",
              "Terms for using this site and buying The House by Austine Ojo: the eBook licence, ordering, payment and problems with an order."),
}


def build_policies(o, robots):
    tpl = (ROOT / "src" / "policy.template.html").read_text(encoding="utf-8")
    shared = {
        "AUTHOR": esc(CONFIG["author"]), "RIGHTS_HOLDER": esc(CONFIG["rightsHolder"]),
        "YEAR": str(datetime.now(timezone.utc).year), "PUBLISHER": esc(CONFIG["publisher"]),
        "ISBN_DISPLAY": esc(CONFIG["isbnDisplay"]), "PRICE_DISPLAY": esc(CONFIG["offer"]["priceDisplay"]),
        "ACCOUNT_NAME": esc(CONFIG["bankAccounts"]["accountName"]), "BANK_NAME": esc(CONFIG["bankAccounts"]["bank"]),
        "WHATSAPP_URL": esc(whatsapp_url(False)), "WHATSAPP_DISPLAY": esc(CONFIG["whatsappDisplay"]),
    }
    for slug, (title, desc) in POLICIES.items():
        body = (ROOT / "content" / f"{slug}.html").read_text(encoding="utf-8")
        for k, v in shared.items():
            body = body.replace("{{" + k + "}}", v)
        values = dict(shared)
        values.update({
            "POLICY_TITLE": esc(title), "POLICY_DESCRIPTION": esc(desc), "POLICY_BODY": body.rstrip(),
            "POLICIES_UPDATED": esc(CONFIG["policiesUpdated"]), "SITE_NAME": esc(CONFIG["siteName"]),
            "CANONICAL": esc(f"{o}/{slug}.html"), "OG_IMAGE": esc(f"{o}/assets/the-house-book-thumbnail.jpg"),
            "ROBOTS_META": robots, "VERSION": datetime.now(timezone.utc).strftime("%Y%m%d%H%M"),
            "FOOTER": footer_html(o, "./"),
        })
        out = tpl
        for k, v in values.items():
            out = out.replace("{{" + k + "}}", v)
        left = re.findall(r"\{\{[A-Z_]+\}\}", out)
        if left:
            fail(f"unreplaced tokens in {slug}.html: {sorted(set(left))}")
        (DIST / f"{slug}.html").write_text(out, encoding="utf-8")


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
