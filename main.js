/* The House — progressive enhancements. The page is fully readable without this file. */
(function () {
  "use strict";
  var root = document.documentElement;
  var STORAGE_KEY = "the-house-theme";
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Appearance: one button cycling System → Day → Night ---------- */
  var ORDER = ["system", "day", "night"];
  var NAMES = { system: "System", day: "Day", night: "Night" };
  var toggle = document.getElementById("theme-toggle");
  var status = document.getElementById("theme-status");

  function readPref() {
    try {
      var v = localStorage.getItem(STORAGE_KEY);
      return v === "day" || v === "night" ? v : "system";
    } catch (e) { return root.getAttribute("data-theme-pref") || "system"; }
  }
  function savePref(p) {
    try {
      if (p === "system") localStorage.removeItem(STORAGE_KEY);
      else localStorage.setItem(STORAGE_KEY, p);
    } catch (e) { /* storage blocked: choice still applies for this visit */ }
  }
  function apply(pref, announce) {
    var dark = pref === "night" || (pref === "system" && mq && mq.matches);
    root.setAttribute("data-theme-pref", pref);
    root.setAttribute("data-theme", dark ? "dark" : "light");
    if (toggle) {
      var next = ORDER[(ORDER.indexOf(pref) + 1) % ORDER.length];
      toggle.setAttribute("aria-label", "Appearance: " + NAMES[pref] + ". Switch to " + NAMES[next]);
      toggle.setAttribute("title", "Appearance: " + NAMES[pref]);
      var label = toggle.querySelector(".theme-toggle-label");
      if (label) label.textContent = NAMES[pref];
    }
    if (announce && status) status.textContent = "Appearance set to " + NAMES[pref];
  }
  var current = root.getAttribute("data-theme-pref") || readPref();
  apply(current, false);

  if (toggle) {
    toggle.addEventListener("click", function () {
      current = ORDER[(ORDER.indexOf(current) + 1) % ORDER.length];
      savePref(current);
      apply(current, true);
    });
  }
  if (mq) {
    var onChange = function () { if (current === "system") apply("system", false); };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  /* ---------- Mobile menu ---------- */
  var menuBtn = document.querySelector(".menu-toggle");
  var nav = document.getElementById("primary-nav");
  function setMenu(open, returnFocus) {
    if (!menuBtn || !nav) return;
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    nav.classList.toggle("is-open", open);
    if (!open && returnFocus) menuBtn.focus();
  }
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = menuBtn.getAttribute("aria-expanded") !== "true";
      setMenu(open);
      if (open) { var first = nav.querySelector("a"); if (first) setTimeout(function () { first.focus(); }, 60); }
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menuBtn.getAttribute("aria-expanded") === "true") setMenu(false, true);
    });
    document.addEventListener("click", function (e) {
      if (menuBtn.getAttribute("aria-expanded") === "true" && !e.target.closest(".site-header")) setMenu(false);
    });
    window.addEventListener("resize", function () { if (window.innerWidth >= 900) setMenu(false); });
  }

  /* ---------- Chapter swipe rail (phones) ---------- */
  var rail = document.getElementById("chapter-list");
  var bar = document.getElementById("rail-bar");
  var count = document.getElementById("rail-count");
  if (rail) {
    var cards = rail.querySelectorAll(".chapter-card");
    var total = cards.length;
    var prev = document.querySelector('[data-rail="prev"]');
    var next = document.querySelector('[data-rail="next"]');
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var currentIndex = function () {
      var left = rail.scrollLeft, best = 0, bestD = Infinity;
      for (var i = 0; i < total; i++) {
        var d = Math.abs(cards[i].offsetLeft - rail.offsetLeft - parseFloat(getComputedStyle(rail).paddingLeft) - left);
        if (d < bestD) { bestD = d; best = i; }
      }
      // at the very end the last cards cannot snap to start
      if (rail.scrollLeft + rail.clientWidth >= rail.scrollWidth - 4) best = total - 1;
      return best;
    };
    var update = function () {
      var i = currentIndex();
      if (bar) bar.style.width = ((i + 1) / total * 100) + "%";
      if (count) count.textContent = pad(i + 1) + " / " + pad(total);
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === total - 1;
    };
    var ticking = false;
    rail.addEventListener("scroll", function () {
      if (ticking) return; ticking = true;
      requestAnimationFrame(function () { update(); ticking = false; });
    }, { passive: true });
    var go = function (dir) {
      var i = Math.max(0, Math.min(total - 1, currentIndex() + dir));
      rail.scrollTo({ left: cards[i].offsetLeft - cards[0].offsetLeft, behavior: reduce ? "auto" : "smooth" });
    };
    if (prev) prev.addEventListener("click", function () { go(-1); });
    if (next) next.addEventListener("click", function () { go(1); });
    rail.addEventListener("keydown", function (e) {
      if (rail.scrollWidth <= rail.clientWidth) return;
      if (e.key === "ArrowRight") { e.preventDefault(); go(1); }
      if (e.key === "ArrowLeft") { e.preventDefault(); go(-1); }
    });
    update();
  }

  /* ---------- Floating WhatsApp button: show after the hero, hide at the order section ---------- */
  var fab = document.getElementById("wa-fab");
  var hero = document.getElementById("top");
  var order = document.getElementById("get-the-book");
  if (fab && hero && "IntersectionObserver" in window) {
    var heroVisible = true, orderVisible = false;
    var sync = function () { fab.classList.toggle("is-visible", !heroVisible && !orderVisible); };
    new IntersectionObserver(function (es) { heroVisible = es[0].isIntersecting; sync(); }, { threshold: 0.05 }).observe(hero);
    if (order) new IntersectionObserver(function (es) { orderVisible = es[0].isIntersecting; sync(); }, { threshold: 0.15 }).observe(order);
  }

  /* ---------- Gentle reveal ---------- */
  if (!reduce && "IntersectionObserver" in window) {
    var targets = document.querySelectorAll(".section-head, .about-intro, .theme-item, .chapter-card, .gallery-item, .book-details, .author-portrait, .author-copy, .order-panel, .bank-panel, .faq-item");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-visible"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.04 });
    for (var t = 0; t < targets.length; t++) {
      var r = targets[t].getBoundingClientRect();
      if (r.top < window.innerHeight) continue;
      // stagger siblings in grids
      var idx = Array.prototype.indexOf.call(targets[t].parentNode.children, targets[t]);
      targets[t].style.transitionDelay = (Math.min(idx, 3) * 70) + "ms";
      targets[t].classList.add("reveal");
      io.observe(targets[t]);
    }
  }

  /* ---------- Copy account numbers ---------- */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest("[data-copy]");
    if (!btn) return;
    var value = btn.getAttribute("data-copy");
    var label = btn.querySelector(".copy-label");
    var done = function () {
      btn.classList.add("is-copied");
      var what = btn.getAttribute("data-copy-what") || "Account number";
      var idle = btn.getAttribute("data-idle") || (label ? label.textContent : "");
      btn.setAttribute("data-idle", idle);
      if (label) label.textContent = "Copied";
      if (status) status.textContent = what === "Link" ? "Link copied" : what + " " + value + " copied";
      setTimeout(function () { btn.classList.remove("is-copied"); if (label) label.textContent = idle; }, 1800);
    };
    var fallback = function () {
      var ta = document.createElement("textarea");
      ta.value = value; ta.setAttribute("readonly", ""); ta.style.position = "absolute"; ta.style.left = "-9999px";
      document.body.appendChild(ta); ta.select();
      try { if (document.execCommand("copy")) done(); } catch (err) { /* number remains selectable */ }
      document.body.removeChild(ta);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(value).then(done, fallback);
    else fallback();
  });

  /* ---------- Native share sheet (phones), offered only where the browser has one ---------- */
  if (navigator.share) {
    var natives = document.querySelectorAll("[data-native-share]");
    for (var n = 0; n < natives.length; n++) natives[n].hidden = false;
    document.addEventListener("click", function (e) {
      var b = e.target.closest && e.target.closest("[data-share-url]");
      if (!b) return;
      navigator.share({ title: b.getAttribute("data-share-title"), text: b.getAttribute("data-share-text"),
                        url: b.getAttribute("data-share-url") }).catch(function () {});
    });
  }

  /* ---------- Lightweight event hooks (no analytics loaded unless configured) ---------- */
  document.addEventListener("click", function (e) {
    var el = e.target.closest && e.target.closest("[data-track]");
    if (!el) return;
    if (window.dataLayer && typeof window.dataLayer.push === "function") {
      window.dataLayer.push({ event: "the_house_click", link: el.getAttribute("data-track") });
    }
  });
})();
