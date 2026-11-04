/* FLC website: small progressive enhancements. Everything works without this file; it adds the mobile menu, the
   remembered language, the quest objectives and install checklist (saved on this device), the Party Mode demo and
   skin tabs, the skin comparison slider, copy and share buttons, and the lightbox. */
(function () {
  "use strict";
  var doc = document.documentElement;

  function store(key, value) { try { localStorage.setItem(key, value); } catch (e) {} }
  function read(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }

  /* one polite live region for short confirmations (copied, link sent) */
  var live = document.createElement("p");
  live.className = "sr";
  live.setAttribute("aria-live", "polite");
  document.body.appendChild(live);
  function announce(text) { live.textContent = ""; setTimeout(function () { live.textContent = text; }, 30); }

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

  /* the quest: install steps are objectives you tick; the home page's three objectives read the same record.
     Saved per device only ("flc-install": the ticked step numbers; "flc-accepted": the zip was downloaded). */
  var STEPS = 8;
  function loadSteps() {
    var raw = read("flc-install");
    var list = raw ? raw.split(",").map(Number).filter(function (n) { return n >= 1 && n <= STEPS; }) : [];
    if (read("flc-accepted") === "1" && list.indexOf(1) < 0) list.push(1);
    return list;
  }
  function saveSteps(list) { store("flc-install", list.join(",")); }

  function paintObjectives(fresh) {
    var done = loadSteps();
    var count = {
      download: done.indexOf(1) >= 0 ? 1 : 0,
      folders: (done.indexOf(4) >= 0 ? 1 : 0) + (done.indexOf(5) >= 0 ? 1 : 0),
      flc: done.indexOf(8) >= 0 ? 1 : 0
    };
    document.querySelectorAll("[data-obj]").forEach(function (li) {
      var c = li.querySelector(".objective__count");
      var need = Number(c.getAttribute("data-need"));
      var have = Math.min(need, count[li.getAttribute("data-obj")] || 0);
      var was = li.classList.contains("is-done");
      c.textContent = have + "/" + need;
      li.classList.toggle("is-done", have >= need);
      if (fresh && !was && have >= need) {
        li.classList.add("just-done");
        setTimeout(function () { li.classList.remove("just-done"); }, 600);
      }
    });
  }

  document.querySelectorAll("[data-accept]").forEach(function (a) {
    a.addEventListener("click", function () { store("flc-accepted", "1"); paintObjectives(true); });
  });

  var install = document.querySelector("[data-install]");
  if (install) {
    var boxes = Array.prototype.slice.call(install.querySelectorAll("[data-step]"));
    var countEl = install.querySelector("[data-install-count]");
    install.querySelector("[data-install-total]").textContent = boxes.length;
    var paint = function () {
      var done = loadSteps();
      var activeSet = false;
      boxes.forEach(function (box) {
        var n = Number(box.getAttribute("data-step"));
        var step = box.closest(".step");
        box.checked = done.indexOf(n) >= 0;
        step.classList.toggle("is-done", box.checked);
        var active = !box.checked && !activeSet;
        if (active) activeSet = true;
        step.classList.toggle("is-active", active);
      });
      countEl.textContent = done.length;
    };
    boxes.forEach(function (box) {
      box.addEventListener("change", function () {
        var n = Number(box.getAttribute("data-step"));
        var done = loadSteps().filter(function (x) { return x !== n; });
        if (box.checked) done.push(n);
        if (n === 1 && !box.checked) store("flc-accepted", "0");
        saveSteps(done.sort(function (a, b) { return a - b; }));
        paint();
        paintObjectives(true);
      });
    });
    install.querySelector("[data-install-reset]").addEventListener("click", function () {
      saveSteps([]); store("flc-accepted", "0"); paint(); paintObjectives(false);
    });
    paint();
  }
  paintObjectives(false);

  /* tab sets: the skin comparator and the Party Mode demo (ARIA tablist: arrows, Home, End) */
  document.querySelectorAll("[data-skinner], [data-demo]").forEach(function (root) {
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

  /* skin comparison: the range input moves the edge between the two real captures */
  document.querySelectorAll("[data-compare]").forEach(function (fig) {
    var stage = fig.querySelector(".compare__stage");
    var range = fig.querySelector("[data-compare-range]");
    var set = function () {
      stage.style.setProperty("--pos", range.value + "%");
      stage.style.setProperty("--pos-n", String(range.value / 100));
    };
    range.addEventListener("input", set);
    set();
  });

  /* copy buttons */
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var label = b.querySelector("span");
      var before = label ? label.textContent : "";
      var said = b.getAttribute("data-copied") || "OK";
      var done = function () {
        if (label) {
          label.textContent = said;
          setTimeout(function () { label.textContent = before; }, 1600);
        }
        announce(said);
      };
      if (navigator.clipboard) navigator.clipboard.writeText(b.getAttribute("data-copy")).then(done, function () {});
    });
  });

  /* on a phone: send the download page to your PC (share sheet, or copy the link) */
  var handoff = document.querySelector("[data-handoff]");
  if (handoff && window.matchMedia("(pointer: coarse)").matches) {
    handoff.hidden = false;
    var share = handoff.querySelector("[data-share]");
    share.addEventListener("click", function () {
      var url = share.getAttribute("data-share-url");
      var copied = function () { announce(share.getAttribute("data-done")); share.querySelector("span").textContent = share.getAttribute("data-done"); };
      if (navigator.share) {
        navigator.share({ title: share.getAttribute("data-share-title"), url: url }).catch(function () {});
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(copied, function () {});
      }
    });
  }

  /* lightbox for captures; without <dialog> support the link simply opens the image */
  var dlg = document.querySelector("[data-lightbox-dialog]");
  if (dlg && typeof dlg.showModal === "function") {
    var img = dlg.querySelector("img");
    var cap = dlg.querySelector("figcaption");
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-lightbox]");
      if (!a || a.closest("[data-compare]") || e.ctrlKey || e.metaKey || e.shiftKey) return;
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
