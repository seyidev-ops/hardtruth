/* The House — progressive enhancements. The page is fully readable without this file. */
(function () {
  "use strict";
  var root = document.documentElement;
  var STORAGE_KEY = "the-house-theme";
  var mq = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  /* ---------- Appearance: Day / Night / System ---------- */
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
  function apply(pref) {
    var dark = pref === "night" || (pref === "system" && mq && mq.matches);
    root.setAttribute("data-theme-pref", pref);
    root.setAttribute("data-theme", dark ? "dark" : "light");
    var buttons = document.querySelectorAll("[data-theme-choice]");
    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute("aria-pressed", buttons[i].getAttribute("data-theme-choice") === pref ? "true" : "false");
    }
  }
  var current = root.getAttribute("data-theme-pref") || readPref();
  apply(current);

  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest("[data-theme-choice]");
    if (!btn) return;
    current = btn.getAttribute("data-theme-choice");
    savePref(current);
    apply(current);
  });

  if (mq) {
    var onChange = function () { if (current === "system") apply("system"); };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("primary-nav");
  function setMenu(open, returnFocus) {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    nav.classList.toggle("is-open", open);
    if (!open && returnFocus) toggle.focus();
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") !== "true";
      setMenu(open);
      if (open) { var first = nav.querySelector("a"); if (first) first.focus(); }
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") setMenu(false, true);
    });
    document.addEventListener("click", function (e) {
      if (toggle.getAttribute("aria-expanded") === "true" && !e.target.closest(".site-header")) setMenu(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 860) setMenu(false);
    });
  }

  /* ---------- Gentle reveal (skipped for reduced motion) ---------- */
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce && "IntersectionObserver" in window) {
    var targets = document.querySelectorAll(".theme-item, .chapter-card, .gallery-item, .author-portrait, .faq-item, .cta-panel");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-visible"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    for (var t = 0; t < targets.length; t++) {
      var r = targets[t].getBoundingClientRect();
      if (r.top < window.innerHeight) continue; // already on screen: leave visible
      targets[t].classList.add("reveal");
      io.observe(targets[t]);
    }
  }

  /* ---------- Copy account numbers ---------- */
  document.addEventListener("click", function (e) {
    var btn = e.target.closest && e.target.closest("[data-copy]");
    if (!btn) return;
    var value = btn.getAttribute("data-copy");
    var label = btn.querySelector(".sr-only");
    var done = function () {
      var original = btn.firstChild.nodeValue;
      btn.classList.add("is-copied");
      btn.firstChild.nodeValue = "Copied";
      setTimeout(function () { btn.classList.remove("is-copied"); btn.firstChild.nodeValue = original; }, 1800);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(value).then(done, function () { /* blocked: number stays selectable on the page */ });
    } else {
      var ta = document.createElement("textarea");
      ta.value = value; ta.setAttribute("readonly", ""); ta.style.position = "absolute"; ta.style.left = "-9999px";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); done(); } catch (err) { /* user can select the number manually */ }
      document.body.removeChild(ta);
    }
  });

  /* ---------- Lightweight event hooks (no analytics loaded unless configured) ---------- */
  document.addEventListener("click", function (e) {
    var el = e.target.closest && e.target.closest("[data-track]");
    if (!el) return;
    var name = el.getAttribute("data-track");
    if (window.dataLayer && typeof window.dataLayer.push === "function") {
      window.dataLayer.push({ event: "the_house_click", link: name });
    }
  });
})();
