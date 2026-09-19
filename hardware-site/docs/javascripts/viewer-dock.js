/* Keeps the part viewer in sight while the file tables are read.
 *
 * Once the reader scrolls past the viewer, the viewer and its info bar move into a
 * card fixed at the bottom-right corner of the window; a placeholder keeps the page
 * from jumping. Scrolling back up puts it back in the page. The card can be hidden
 * (a small pill brings it back) or expanded (scrolls back to the full-size viewer).
 * On screens narrower than Material's desktop breakpoint nothing docks.
 *
 * Works on the same elements as viewer.js and does not touch its logic.
 */
(function () {
  "use strict";

  const DESKTOP = "(min-width: 76.25em)";   // Material: sidebars visible from here
  const ICON_EXPAND = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M5 5h6v2H7v4H5V5m14 0v6h-2V7h-4V5h6M5 19v-6h2v4h4v2H5m14 0h-6v-2h4v-4h2v6Z"/></svg>';
  const ICON_CLOSE = '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path fill="currentColor" d="M18.3 5.7 12 12l6.3 6.3-1.4 1.4L10.6 13.4 12 12 5.7 5.7l1.4-1.4L12 10.6l6.3-6.3 1.4 1.4Z"/></svg>';
  const ICON_ROBOT = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2a2 2 0 0 1 2 2c0 .7-.4 1.4-1 1.7V7h3a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3v-7a3 3 0 0 1 3-3h3V5.7c-.6-.3-1-1-1-1.7a2 2 0 0 1 2-2m-3 9a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3m6 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3M2 11h1v5H2v-5m19 0h1v5h-1v-5Z"/></svg>';

  function init() {
    const mv = document.getElementById("dh-viewer");
    if (!mv || mv.dataset.dock) return;
    mv.dataset.dock = "1";
    // The bar follows the viewer inside .dh-viewer-block; fall back to a lookup if the
    // Markdown wrapped the viewer in a <p> of its own.
    const bar = mv.nextElementSibling && mv.nextElementSibling.classList.contains("dh-viewer-bar")
      ? mv.nextElementSibling : document.querySelector(".dh-viewer-bar");

    // Wrap viewer + bar so one element can be moved; a placeholder holds the space.
    const wrap = document.createElement("div");
    wrap.className = "dh-viewer-wrap";
    const anchor = document.createElement("div");
    anchor.className = "dh-viewer-anchor";
    mv.parentNode.insertBefore(anchor, mv);
    mv.parentNode.insertBefore(wrap, mv);
    wrap.appendChild(mv);
    if (bar) wrap.appendChild(bar);

    // Card controls (shown only while docked).
    const tools = document.createElement("div");
    tools.className = "dh-dock-tools";
    const expand = document.createElement("button");
    expand.type = "button";
    expand.className = "dh-dock-btn";
    expand.title = "Back to the full-size viewer";
    expand.setAttribute("aria-label", "Back to the full-size viewer");
    expand.innerHTML = ICON_EXPAND;
    const close = document.createElement("button");
    close.type = "button";
    close.className = "dh-dock-btn";
    close.title = "Hide the viewer";
    close.setAttribute("aria-label", "Hide the viewer");
    close.innerHTML = ICON_CLOSE;
    tools.append(expand, close);
    wrap.appendChild(tools);

    const pill = document.createElement("button");
    pill.type = "button";
    pill.className = "dh-dock-pill md-button";
    pill.innerHTML = ICON_ROBOT + "<span>Show the robot</span>";
    pill.hidden = true;
    document.body.appendChild(pill);

    const desktop = window.matchMedia(DESKTOP);
    let docked = false, collapsed = false, ticking = false;

    function headerBottom() {
      const h = document.querySelector(".md-header");
      return h ? h.getBoundingClientRect().bottom : 0;
    }
    function scrolledPast() {
      return anchor.getBoundingClientRect().bottom < headerBottom() + 8;
    }
    function dock() {
      if (docked) return;
      anchor.style.height = wrap.offsetHeight + "px";
      wrap.classList.add("dh-docked");
      docked = true;
    }
    function undock() {
      if (!docked) return;
      wrap.classList.remove("dh-docked");
      anchor.style.height = "";
      docked = false;
    }
    function update() {
      ticking = false;
      const past = desktop.matches && scrolledPast();
      if (!past) { undock(); pill.hidden = true; collapsed = false; return; }
      if (collapsed) { undock(); wrap.classList.add("dh-collapsed"); pill.hidden = false; return; }
      wrap.classList.remove("dh-collapsed");
      pill.hidden = true;
      dock();
    }
    function onScroll() {
      if (ticking) return;
      ticking = true;
      setTimeout(update, 40);   // a short throttle; unlike rAF it also runs in a background tab
    }

    close.addEventListener("click", () => { collapsed = true; update(); });
    pill.addEventListener("click", () => { collapsed = false; update(); });
    expand.addEventListener("click", () => {
      collapsed = false;
      undock();
      anchor.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    desktop.addEventListener("change", onScroll);
    update();
  }

  if (typeof document$ !== "undefined") document$.subscribe(() => { init(); });
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", () => { init(); });
  else init();
})();
