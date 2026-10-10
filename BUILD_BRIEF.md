# THE HOUSE — Landing Page Build Instructions

Version 1.0 · Prepared 10 October 2026  
Book: **The House — 2nd Corinthians 5:17**  
Author: **Austine Ojo**  
Scope: A single-book landing page, ready to expand into an author website later.

![The House by Austine Ojo — book thumbnail](assets/the-house-book-thumbnail.jpg)

## 1. Copy-and-paste instruction for the website builder

Build a polished, mobile-first landing page exclusively for **The House by Austine Ojo**, using this document as the content and implementation specification. Reconstruct the visual character of the supplied website video: a spacious gradient background, a prominent book mockup, chapter cards, book artwork, an author portrait, and social links. Modernize the layout for readability and conversion. Include persistent Day, Night, and System appearance choices; all fifteen chapter briefs below; an accessible book thumbnail; search and social metadata; structured data; an XML sitemap; and robots.txt.

Use the supplied artwork unchanged. Preserve the author's name and the book's Christian message. Build the core content into the initial HTML through static generation or server rendering. Use actual text for chapter briefs, not screenshots. Keep the manuscript private: it is a content reference, not an authorized free download. Do not invent prices, formats, testimonials, reviews, dates, author credentials, contact numbers, or purchase destinations. Until a purchase URL is supplied, use **Explore the Chapters** as the primary action and **Enquire on Facebook** as the contact action. Deliver a working preview, editable source, assets, deployment instructions, and a completed validation checklist. Do not publish publicly merely because this specification is supplied.

This is a build brief and content pack, not a recovered source-code export or a deployed website.

## 2. Source evidence and recovery limits

### What was recovered from the video

The supplied `786965.mp4` is approximately 7.95 seconds long and films a laptop screen. It shows:

- A small centered emblem above the site title **The House**.
- A broad purple/mauve-to-blue/teal gradient background.
- A large upright 3D book mockup near the top.
- A multi-column grid of rectangular chapter/page cards with light interiors and yellow/gold edging.
- Additional cover artwork and a yellow text panel further down.
- The supplied portrait of the author in yellow clothing, followed by a short statement and social icons.
- A compact footer.

The tiny text, original card labels, exact colors, font families, footer wording, icon destinations, hosting address, backend, and source code cannot be reliably recovered from this recording. The chapter briefs in this pack are new editorial paraphrases grounded in the book, not claimed transcriptions of the former website. The reference contact sheet is `assets/website-video-reference.jpg`; do not publish it as promotional content.

If the old URL becomes available, inspect public archived captures and accessible cached assets. Do not guess its domain. Restore old URL redirects only if the domain is controlled and the old paths can be established.

### Book evidence

Source: `Book - THE HOUSE,  MAIN EDITION.pdf`.

- Title and scripture reference: PDF page 1.
- Printed ISBN: **978-978-973-668-3**, PDF page 2. It passes the ISBN-13 check-digit calculation, but that does not independently verify registration or edition assignment.
- Publisher as printed: **Mine Shelter Nigeria Limited**, PDF page 2.
- Table of contents: PDF page 4; fifteen chapters.
- Purpose statement: Introduction, PDF page 5 / printed page v.
- Main chapter text: PDF pages 14–195 / printed pages 1–182.
- Further reading follows the chapters; it is not a sixteenth chapter and must not become an unrelated-book storefront.

Do not equate total PDF sheets with edition page count. Do not use a manuscript mention of 2018 as a publication date. Historic publisher contact details are not confirmed current sales contacts.

### Supplied social destination

**Facebook:** https://www.facebook.com/share/1FLTpqYwCx/

Use exactly this supplied URL for now. Its destination could not be independently resolved during preparation. Label it **Visit Facebook** or **Enquire on Facebook**, not “Message now” unless it actually opens messaging. Test it manually before public launch. Use a stable profile/page URL when the owner supplies one. Do not invent Instagram, X, YouTube, WhatsApp, email, or other handles because the old video shows multiple icons. Do not add this share URL to a Person `sameAs` field until the destination's identity is confirmed.

## 3. Goals and audience

Help readers understand what the book is about, explore its fifteen chapters, meet the author, and enquire about obtaining a copy. Address Christians seeking a personal relationship with God, growth in their identity in Christ, Scripture meditation, discipleship, and prayer.

The page should feel contemplative, warm, confident, and easy to read. Avoid sensational miracle claims, countdown timers, fabricated scarcity, guaranteed outcomes, and unsupported bestseller badges.

## 4. Page structure and ready-to-use copy

### Header

Text wordmark: **The House**. Navigation: **About the Book**, **Chapters**, **The Author**, **Get the Book**. Include appearance control and an accessible mobile menu. The original emblem is not available as a standalone asset; use a simple text wordmark or a clearly new book symbol rather than pretending to have recovered the old logo.

### Hero — `#top`

Eyebrow: **A Christian book by Austine Ojo**

H1: **The House**

Subtitle: **2nd Corinthians 5:17**

Lead: **Know God for yourself. Grow in your life in Christ.**

Body: *The House invites you to look beyond religious routine and pursue a personal relationship with God. Across fifteen chapters, Austine Ojo explores identity in Christ, the knowledge of God, meditation, discipleship, and a life of prayer.*

Primary button: **Explore the Chapters** → `#chapters`.
Secondary button: **Enquire on Facebook** → supplied Facebook URL.

Use `assets/the-house-book-thumbnail.jpg` as the prominent hero mockup and book thumbnail. It contains its own dark brown square background; use `object-fit: contain` and a compatible surrounding surface. Do not use CSS blend modes that alter the cover lettering. Do not stretch, recolor, redraw, or clip the book.

### About the book — `#about`

Heading: **A call to know the Father personally**

Copy: *What does it mean to live as a new creation in Christ? In The House, Austine Ojo uses 2 Corinthians 5:17 as the central picture for exploring a believer's relationship with God. Drawing on Scripture, everyday illustrations, and personal testimony, he calls readers to seek God Himself, grow in understanding, and live out their faith in daily life.*

Supporting themes:

1. **Identity in Christ** — Consider what it means to represent Christ in the world.
2. **Knowing God** — Explore His presence, power, and the importance of spiritual understanding.
3. **A life of devotion** — Make room for Scripture, meditation, and prayer.
4. **Faith in action** — Reflect on discipleship, service, relationships, and sharing Christ with others.

These are editorial marketing summaries, not quotations or promises of guaranteed results.

### Chapter explorer — `#chapters`

Heading: **Explore the fifteen chapters**

Intro: *Follow the book's journey from your identity as Christ's ambassador to the habits and relationships that shape a life of prayer.*

Use the exact sequence and approved working briefs in section 5. Each card contains a chapter number, title, short brief, and **Read chapter brief** control only where extra detail actually exists. Prefer native `details/summary` for expandable cards. Include an **Expand all / Collapse all** control if useful. All briefs must exist in the initial HTML, remain keyboard accessible, and be searchable even when collapsed. Avoid making visitors click fifteen times merely to learn the chapter names.

Do not use images of printed text as the sole source of chapter content. A miniature cover may decorate the section, but fifteen identical large cover pictures would add clutter.

### Artwork / inside the book — `#inside`

Show the wraparound image and the angled mockup as a restrained two-image gallery. Captions: **The cover of The House** and **The House by Austine Ojo**. An accessible lightbox is optional; if used, support Escape, focus trapping, and focus restoration.

Do not offer the complete PDF for public download. A future **Read a Sample** button must remain absent until a specific excerpt and delivery route are approved. The uploaded website recording is a private design reference, not a book trailer; do not embed it publicly.

### Author — `#author`

Heading: **Meet Austine Ojo**

Portrait: `assets/austine-ojo-portrait.jpg`.

Copy: *Austine Ojo is the author of The House. In the book, he shares Scripture reflections and personal experiences to encourage readers to know God for themselves and develop a personal, conversational relationship with Him.*

This is intentionally a source-grounded short bio. Do not add a ministry title, church leadership role, qualifications, awards, residence, or current business details without confirmation. The uploaded portrait is designated for the author section by this brief; do not perform face identification.

Link: **Visit Facebook** → supplied URL.

### Reader questions — `#faq`

**What is The House about?**  
It explores life in Christ, knowing God personally, meditation, discipleship, and prayer through Scripture reflections and the author's experiences.

**Why is 2 Corinthians 5:17 on the cover?**  
The author uses the verse's theme of new life in Christ as the central picture of “the house” throughout the book.

**How many chapters are there?**  
There are fifteen chapters, from “Ambassador” to “Hindrances to Prayers.”

**How can I get a copy?**  
Visit the supplied Facebook page to enquire about current availability, formats, and ordering details.

Do not make claims about stock, delivery, digital access, or price until supplied. Keep FAQs for reader usefulness; do not promise Google FAQ rich results.

### Closing action — `#get-the-book`

Heading: **Begin exploring The House**

Copy: *Discover the themes, explore the chapters, and enquire about getting your copy.*

Buttons: **Enquire on Facebook** and **Explore the Chapters**.

When a valid purchase URL and offer details exist, switch the primary action consistently across the page to **Get Your Copy**, show the verified price/currency and format, and link directly to the ordering route. Never use dead `href="#"` purchase buttons or simulated payment confirmations.

### Footer

Include book title, author name, internal section links, the supplied Facebook link, appearance control if needed, and a human-readable **Page navigation** list. Add a copyright notice using the current year only once the site rights-holder name is confirmed; otherwise use **The House · Austine Ojo** without asserting ownership of every asset. Add policy links only to real pages.

## 5. Fifteen chapter briefs with manuscript references

Use the following as working landing-page copy. They are paraphrases of inspected chapter passages. Page references are for editorial verification and may be hidden from the public card layout. Titles use readable title case; chapter 15 follows its actual chapter heading, “Hindrances to Prayers,” whereas the contents page uses singular “Prayer.” Chapter 3 spacing is normalized to “Everywhere.”

### 01 — Ambassador

**Brief:** What does it mean to represent Christ in everyday life? This chapter uses the role of an ambassador to examine the believer's responsibilities, priorities, and conduct, calling readers to seek God's kingdom rather than make personal gain the centre of their faith.

Source: printed pp. 1–7; PDF pp. 14–20. Particularly pp. 1 and 4.

### 02 — Solution From God

**Brief:** Through biblical examples of choice, warning, and response, this chapter considers how people respond to God's direction. It invites reflection on repentance, responsibility, and the role of parents in teaching their children the ways of God.

Source: printed pp. 8–22; PDF pp. 21–35. Particularly pp. 8, 15 and 22.

### 03 — God Is Everywhere

**Brief:** Reflect on God's presence and the meaning of new life in Christ. Austine Ojo develops the book's central picture of 2 Corinthians 5:17 as “the house,” inviting readers to consider repentance, belonging, and their relationship with the Father through Jesus.

Source: printed pp. 23–29; PDF pp. 36–42. Particularly pp. 23, 26 and 29.

### 04 — Omnipotent God

**Brief:** This chapter reflects on God's unlimited power and the place of His Word in the believer's life. It also challenges the elevation of human ministers above God, urging readers to direct their worship and gratitude to Him.

Source: printed pp. 30–42; PDF pp. 43–55. Particularly pp. 30 and 36.

### 05 — The Almighty Healer Omniscience God

**Brief:** Explore the author's reflections on God as all-knowing and as healer, through Scripture and testimony. The chapter emphasizes faith and discernment, including the need to examine spiritual claims carefully; it explicitly states that trusting God is not a rejection of medical help.

Source: printed pp. 43–52; PDF pp. 56–65. Particularly pp. 43, 48–49 and 52. Preserve the published wording “Omniscience God” in the title rather than silently renaming the chapter.

### 06 — Ask for Knowledge

**Brief:** Why does spiritual understanding matter? Through Scripture and personal testimony, the author reflects on knowledge, patience, and learning to seek God's direction. He connects the pursuit of understanding with the choices and challenges of everyday life.

Source: printed pp. 53–67; PDF pp. 66–80. Particularly pp. 53 and 61–65.

### 07 — The Church Is Here

**Brief:** Beginning with Peter and John's encounter with the man at the temple gate, this chapter asks what it means for God's presence to be expressed through His people. It challenges readers to look beyond buildings and religious display to a living faith in Christ.

Source: printed pp. 68–79; PDF pp. 81–92. Particularly pp. 68, 70 and 73. Opening subheading: “Rise Up and Walk.”

### 08 — Beware of Wrong Yoke

**Brief:** Consider the relationships, teachings, and influences that shape your walk with God. This chapter warns against deceptive traditions and divided loyalties, encouraging readers to examine their associations and keep their devotion centred on Christ.

Source: printed pp. 80–97; PDF pp. 93–110. Particularly pp. 80, 88 and 96.

### 09 — Train Yourself in Meditation

**Brief:** Make deliberate room for God's Word. This chapter encourages the practice of Scripture meditation, quiet reflection, and personal fellowship with God, presenting these habits as part of growing in understanding and becoming equipped for a life of faith.

Source: printed pp. 98–109; PDF pp. 111–122. Particularly pp. 98, 103 and 109.

### 10 — Pyramid

**Brief:** Using a pyramid as an illustration, the author considers the shared responsibility of encouraging others and bringing people to Christ. The chapter calls readers to care about others' spiritual growth and to make sharing their faith part of daily life.

Source: printed pp. 110–119; PDF pp. 123–132. Particularly pp. 110, 114 and 119. This is an evangelism metaphor, not a financial or recruitment offer.

### 11 — How Fortified Are You for This Venture?

**Brief:** What prepares a believer to serve and share Christ with others? This chapter presents discipleship as a process of training, surrender, and growth, asking readers to examine self-interest and become willing to learn under Christ's direction.

Source: printed pp. 120–132; PDF pp. 133–145. Particularly pp. 120 and 132.

### 12 — What Will You Have Me Do?

**Brief:** Drawing on Paul's encounter with Christ, this chapter explores a response of willing service. It asks readers to consider how renewed life in Christ should shape their direction, obedience, and desire to participate in God's work.

Source: printed pp. 133–142; PDF pp. 146–155. Particularly pp. 133–134, 137 and 142.

### 13 — Stop Seeking God's Hand, Seek His Face

**Brief:** Are you seeking only what God can give, or seeking to know Him? This chapter turns attention to fellowship with God, considering the relationship between asking, faith, patience, and the desire to draw near to the Father.

Source: printed pp. 143–156; PDF pp. 156–169. Particularly pp. 143, 150 and 154–156.

### 14 — Prayer Is Everything

**Brief:** This chapter encourages persistence in prayer and explores different expressions of it, including petition, thanksgiving, and intercession. It connects prayer with love for others, gratitude, commitment, and the integrity of the life behind the words.

Source: printed pp. 157–173; PDF pp. 170–186. Particularly pp. 157, 162–165 and 173.

### 15 — Hindrances to Prayers

**Brief:** Examine the attitudes and habits that the author identifies as obstacles to prayer. With attention to forgiveness, peace in the home, and persistent patterns of sin, the chapter calls readers to honest self-examination and a readiness to change.

Source: printed pp. 174–182; PDF pp. 187–195. Particularly pp. 174–178 and 182.

### Editorial guardrails

Keep these summaries faithful to this book rather than importing another author's framework. Attribute distinctive interpretations to the author where needed. Do not turn spiritual discussions into guaranteed healing, wealth, or prayer-outcome advertising. Preserve any directly quoted Bible translation as printed; these briefs use paraphrase and references instead of introducing a different translation. Do not reproduce extended manuscript pages as marketing copy. Review text in rendered cards for legibility and truncation.

## 6. Visual and responsive specification

- Desktop: centered content, maximum width around 1120–1200 px; spacious hero with text and book artwork; chapter grid of three columns.
- Tablet: two-column chapter grid; balanced hero stack when space is constrained.
- Mobile: one column, text before artwork or a compact artwork-first composition; visible call to action; no horizontal overflow at 320 px.
- Pair an elegant readable serif heading with a simple sans-serif body face. Prefer system fonts or limited self-hosted fonts with `font-display: swap`.
- Body type: at least 16 px, generous line spacing, readable measure. Avoid long centred paragraphs.
- Gold accents connect to the cover. Purple, blue, and teal echo the recorded website. Avoid busy cloud imagery behind body text.
- Make the author's portrait comfortably large; retain natural aspect ratio or use a careful head-and-shoulders display crop without modifying the source file.
- Animate sparingly; disable decorative movement under `prefers-reduced-motion`. No autoplay audio, flashing effects, or forced scroll animations.

### Day and Night modes

Provide **Day / Night / System** options with text labels or accessible names. Default to System; respect `prefers-color-scheme`. Persist explicit selection in local storage with graceful fallback if storage is blocked. Apply the selected theme before paint to avoid a flash. Set `color-scheme` so native controls match. System mode must respond when the operating-system preference changes.

Suggested starting tokens, subject to measured contrast:

| Token | Day | Night |
|---|---|---|
| Page | `#FAF8F2` | `#101322` |
| Card surface | `#FFFFFF` | `#1A2033` |
| Main text | `#182033` | `#F4F1E8` |
| Muted text | `#505A6A` | `#B9C2D2` |
| Accent | `#805C08` | `#E8C66B` |
| Link | `#294F92` | `#A6C9FF` |

Day mode may use a soft lavender-to-pale-blue wash; Night mode a deep plum-to-navy gradient with restrained teal at the bottom. Keep card surfaces opaque enough for reliable contrast. Test normal text at 4.5:1, large text at 3:1, and meaningful controls/focus indicators at 3:1. Theme controls must work with keyboard and touch and announce their current state.

## 7. Thumbnail and asset manifest

| Included file | Role | Dimensions | Suggested alt text |
|---|---|---|---|
| `assets/the-house-book-thumbnail.jpg` | Hero, book thumbnail, square social image | 1536 × 1536 | The House by Austine Ojo, a book about life in Christ |
| `assets/the-house-wraparound.jpg` | Cover gallery | 1536 × 1536 | Front, spine and back cover of The House by Austine Ojo |
| `assets/the-house-angled-mockup.jpg` | Secondary book image | 1536 × 1536 | Angled book mockup of The House by Austine Ojo |
| `assets/austine-ojo-portrait.jpg` | Author section | 1097 × 1536 | Austine Ojo, author of The House |
| `assets/website-video-reference.jpg` | Private design-reference contact sheet | Reference only | Not a public site asset |

The thumbnail is the supplied upright mockup, retained unchanged. It is included in this Markdown document and the ZIP. For the website, display responsive sizes and generate optimized delivery variants without altering the artwork. Use the actual intrinsic dimensions on `img` tags; use `object-fit: contain` for book artwork. Give the hero image high fetch priority, and lazy-load below-the-fold gallery/author images.

Use the square thumbnail as a valid initial Open Graph image with its actual dimensions. A separately composed 1200 × 630 social card may later place the existing cover beside “The House” and “Austine Ojo”; do not automatically crop the square book image to a landscape ratio and cut off the title. For X use `summary` with the square image; switch to `summary_large_image` only when an appropriate wide card exists. No X account is needed to provide card metadata.

Create a simple, legible favicon/book monogram as a new site asset, not a miniature full cover full of unreadable text. Provide favicon.ico, an appropriate square PNG, and an apple-touch-icon. Optional web manifest must describe the real site and icons; do not add an unnecessary service worker.

## 8. SEO implementation requirements

### Searchable content and metadata

Use one H1, **The House**; meaningful H2 sections; and H3 chapter headings. Keep title, author, chapter briefs, and navigation in crawlable initial HTML. Use semantic header, nav, main, section, and footer elements; actual anchor links; `lang="en"`; UTF-8; and a mobile viewport. The visible page must match its structured data.

Suggested title: **The House by Austine Ojo | Life in Christ**

Suggested description: **Explore The House by Austine Ojo: 15 chapters on life in Christ, knowing God, meditation, discipleship and prayer. View chapter briefs and enquire.**

Use the real production origin for a self-referencing canonical URL. Do not use an invented domain in production. Consolidate HTTP/HTTPS, www/non-www, and trailing-slash variants with deliberate permanent redirects. Do not create duplicate pages for chapter filters, theme state, or campaign parameters.

Include Open Graph `og:type=website`, title, description, canonical URL, site name, thumbnail URL, image alt text, dimensions, and image MIME type. Include X card title, description, image, and alt metadata without fabricating a handle. All social images need absolute HTTPS URLs and publicly accessible responses; metadata must be rendered server-side/static so social crawlers can read it.

Use descriptive asset names and natural language around images. No keyword stuffing, hidden SEO text, meta-keywords task, doorway pages, or fabricated local-business locations. Neither SEO tooling nor markup guarantees ranking or a particular thumbnail in search.

### Structured data

Use a JSON-LD graph with **WebSite**, **WebPage**, **Book**, and **Person** entities linked through stable `@id` values. Identify the book as the page's `mainEntity`. Useful verified Book values: name `The House`, author `Austine Ojo`, language `en`, description matching visible copy, image, and the printed ISBN `9789789736683`. Publisher may be `Mine Shelter Nigeria Limited` if the visible book details also identify it.

Omit unverified publication date, edition number, page count, format, ratings, awards, reviews, prices, and stock. Add an Offer or Product representation only when a real, visible offer exists and the current applicable requirements are met. General Book markup is not a promise of eligibility for Google's separate book-related programs. Validate with Schema.org Validator and test supported rich-result types using Google's Rich Results Test. A valid Book entity may have no supported rich-result enhancement.

FAQ copy is useful to readers, but do not build around FAQ rich results: Google's October 2026 documentation states that the feature was discontinued in May 2026. Do not add fake review or breadcrumb markup to a flat one-page site.

### Sitemap and robots

For the initial one-page site, the XML sitemap contains only the absolute canonical homepage URL. Sections such as `#chapters` are anchors, not separate sitemap pages. Include real future policy pages only when they exist, return 200, and are intended for indexing. Do not create fifteen thin pages simply to enlarge the sitemap.

`seo/sitemap.xml.template` and `seo/robots.txt.template` are included. Replace `{{SITE_ORIGIN}}` at build time, XML-escape generated values, and fail the production build if template tokens remain. Serve `/sitemap.xml` with an XML content type and `/robots.txt` as plain text. Add a truthful `lastmod` only when a reliable content-modification date is available; do not update it on every deployment.

Production: allow intended public pages to be crawled and reference the sitemap. Private previews: require authentication where available and add `noindex`; do not rely on robots.txt as a privacy or security control. Do not block crawlers from a page if you expect them to see its `noindex`. Keep the full manuscript out of public assets entirely.

The footer's human-readable section navigation is the page's human sitemap. If the site grows to several real pages, add a proper `/sitemap/` HTML page; it is unnecessary for this first single-book page.

### Performance, discovery, and measurement

Aim for good Core Web Vitals at the 75th percentile of real-user visits: LCP ≤ 2.5 seconds, INP ≤ 200 ms, CLS ≤ 0.1. Use these as targets, not unmeasured claims. Reserve image dimensions; load only essential JavaScript; use responsive optimized images, caching, compression, and modest font payloads. Avoid third-party Facebook embeds when a plain link works.

At launch, verify ownership in Google Search Console and Bing Webmaster Tools, submit the sitemap, inspect the homepage, and review indexing and crawl reports. Verify social previews with available platform inspectors. Add lightweight analytics only with the owner's configuration and appropriate disclosures. Useful events: chapter expansion, Facebook click, and purchase click once available. Do not count outbound clicks as confirmed sales. Keep private personal data out of event payloads.

Answer reader questions naturally with source-grounded content. Good crawling, useful copy, clear author identity, and consistent metadata support search and AI discovery. An optional `llms.txt` is not a Google ranking requirement or a replacement for HTML, robots.txt, or a sitemap.

## 9. Accessibility, interaction, and technical quality

Provide a skip-to-content link, visible focus states, logical tab order, labelled icon buttons, and minimum comfortable touch targets around 44 × 44 px. Mobile navigation must report expanded state and close predictably. Avoid sticky elements covering focused controls. Test at 200% zoom, in both themes, and with reduced motion. Native links must remain usable without JavaScript.

If external links open a new tab, use `rel="noopener noreferrer"` and make the behavior clear. Never require an account to read chapter summaries. Do not add email collection, a contact form, a cart, or a payment backend without a working service and clearly defined behavior. If those features are added later, implement real loading/error/success states, validation, abuse protection, and appropriate policies.

Use portable source control and a documented production build. Store content in a structured data file with chapter number, title, summary, and source page ranges. Keep origin, purchase URL, approved social links, and offer fields in one configuration file. Do not scatter placeholder domains through components. Preserve backups of source, content, assets, DNS settings, and deployment notes to avoid repeating the previous hosting loss.

## 10. Remaining launch inputs

| Input | Current state | Builder behavior |
|---|---|---|
| Production domain | Not supplied | Build preview; block production SEO generation until configured |
| Old website URL | Not supplied/readable | No claim of server or archive recovery |
| Purchase URL | Not supplied | Use chapter exploration and Facebook enquiry |
| Price, currency, formats, delivery | Not confirmed | Omit offer claims and checkout schema |
| Facebook stable page URL | Share link supplied | Use supplied link; manually validate before launch |
| Author extended biography | Not supplied | Use the short source-grounded bio |
| Public sample permission | Not supplied | No PDF download or sample CTA |
| Rights-holder name for footer | Not confirmed | Use simple book/author credit |
| Analytics and verification IDs | Not supplied | Leave integrations disabled |

These are launch configuration items, not reasons to stop building a functional preview.

## 11. Acceptance checklist

- [ ] Only The House is promoted; Austine Ojo is spelled correctly throughout.
- [ ] All fifteen titles appear in the correct order with source-grounded briefs.
- [ ] Hero thumbnail, gallery images, and author portrait load without stretching or clipping.
- [ ] No manuscript, private contact sheet, or laptop recording is accidentally deployed.
- [ ] Primary and secondary actions work; no placeholder checkout or invented offers.
- [ ] Day, Night, and System work across reloads and operating-system changes.
- [ ] Navigation, cards, focus, contrast, zoom, and reduced-motion behavior are checked.
- [ ] Layout works at 320, 375, 768, and 1440 px widths with no horizontal overflow.
- [ ] Initial HTML contains title, author, all chapter briefs, canonical, and social metadata.
- [ ] JSON-LD parses and references correct absolute production URLs.
- [ ] Sitemap parses; every listed URL returns 200 and matches its canonical.
- [ ] Robots rules and indexing directives match preview versus production intent.
- [ ] Social thumbnail preview is checked; no expectation that every platform crops identically.
- [ ] No fake reviews, rich-result claims, credentials, prices, or sales counters appear.
- [ ] No `{{...}}` tokens, TODOs, localhost URLs, or test domains appear in the public build.
- [ ] Performance is measured; failures and unmeasured field data are reported honestly.
- [ ] Source, configuration, assets, and recovery/deployment instructions are handed over.

## 12. Current technical references

Consult current primary documentation when implementing. Checked during preparation on 10 October 2026:

- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Build and submit a sitemap: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Canonical URLs: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- Image SEO: https://developers.google.com/search/docs/appearance/google-images
- Core Web Vitals: https://developers.google.com/search/docs/appearance/core-web-vitals
- Documentation updates, including FAQ retirement and llms.txt clarification: https://developers.google.com/search/updates
- Schema.org vocabulary and validation: https://schema.org/Book and https://validator.schema.org/

## 13. Pack contents and use

Unzip the complete pack, keep this Markdown file beside the `assets` and `seo` folders, and give the folder to the website builder. The thumbnail embedded above uses a relative path so it travels with the pack. The separately downloadable Markdown contains the complete instructions but needs the ZIP's assets for local image display.

Included assets are copies of the supplied images. The source book and video remain separate inputs; this pack intentionally does not distribute the entire manuscript. The SEO files are templates awaiting a real origin, not files to upload unchanged.
