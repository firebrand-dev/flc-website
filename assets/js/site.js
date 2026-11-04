/* FLC website: small progressive enhancements. Everything works without this file; it only adds the mobile menu,
   the remembered language, gentle reveals, the route line, the skin comparator, copy buttons and the lightbox. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function store(key, value) { try { localStorage.setItem(key, value); } catch (e) {} }

  /* language: a manual choice is remembered and wins over the browser's language */
  document.querySelectorAll("[data-set-lang]").forEach(function (a) {
    a.addEventListener("click", function () { store("flc-lang", a.getAttribute("data-set-lang")); });
  });

  /* mobile menu */
  var btn = document.querySelector("[data-menu-btn]");
  var nav = document.querySelector("[data-nav]");
  if (btn && nav) {
    var setOpen = function (open) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      nav.classList.toggle("is-open", open);
      document.body.classList.toggle("menu-open", open);
      if (open) { var first = nav.querySelector("a"); if (first) first.focus(); }
    };
    btn.addEventListener("click", function () { setOpen(btn.getAttribute("aria-expanded") !== "true"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { setOpen(false); btn.focus(); }
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    window.matchMedia("(min-width: 961px)").addEventListener("change", function (m) { if (m.matches) setOpen(false); });
  }

  /* "The addon" dropdown on wide screens (in the mobile menu its pages are always listed) */
  document.querySelectorAll("[data-dropdown]").forEach(function (group) {
    var toggle = group.querySelector(".nav__toggle");
    var close = function () { toggle.setAttribute("aria-expanded", "false"); };
    toggle.addEventListener("click", function () {
      toggle.setAttribute("aria-expanded", toggle.getAttribute("aria-expanded") === "true" ? "false" : "true");
    });
    group.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") { close(); toggle.focus(); }
    });
    group.addEventListener("focusout", function (e) { if (!group.contains(e.relatedTarget)) close(); });
    document.addEventListener("click", function (e) { if (!group.contains(e.target)) close(); });
  });

  /* reveals */
  var reveals = document.querySelectorAll(".reveal");
  if (!reduce && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* the route on the home page draws itself as you scroll down it */
  var route = document.querySelector("[data-route]");
  if (route && !reduce) {
    var ticking = false;
    var update = function () {
      ticking = false;
      var r = route.getBoundingClientRect();
      var seen = (window.innerHeight * 0.62 - r.top) / r.height;
      route.style.setProperty("--route", Math.max(0, Math.min(1, seen)) * 100 + "%");
    };
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  } else if (route) {
    route.style.setProperty("--route", "100%");
  }

  /* skin comparator: an ARIA tablist (arrow keys, Home, End) */
  document.querySelectorAll("[data-skinner]").forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll('[role="tab"]'));
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { select(tab, false); });
      tab.addEventListener("keydown", function (e) {
        var j = { ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
        if (j === undefined) return;
        e.preventDefault();
        select(tabs[(j + tabs.length) % tabs.length], true);
      });
    });
  });

  /* copy buttons */
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var label = b.querySelector("span");
      var before = label ? label.textContent : "";
      var done = function () {
        if (!label) return;
        label.textContent = b.getAttribute("data-copied") || "OK";
        setTimeout(function () { label.textContent = before; }, 1600);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(b.getAttribute("data-copy")).then(done, function () {});
    });
  });

  /* lightbox for captures; without <dialog> support the link simply opens the image */
  var dlg = document.querySelector("[data-lightbox-dialog]");
  if (dlg && typeof dlg.showModal === "function") {
    var img = dlg.querySelector("img");
    var cap = dlg.querySelector("figcaption");
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-lightbox]");
      if (!a || e.ctrlKey || e.metaKey || e.shiftKey) return;
      e.preventDefault();
      var small = a.getAttribute("data-small");
      img.src = small && window.matchMedia(a.getAttribute("data-small-media")).matches ? small : a.getAttribute("href");
      img.alt = a.querySelector("img") ? a.querySelector("img").alt : "";
      cap.textContent = a.getAttribute("data-caption") || "";
      dlg.showModal();
    });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("close", function () { img.removeAttribute("src"); });
  }

  doc.classList.remove("no-js");
})();
