// Looping clips (exploded views, demos): click to pause on a frame, click again to
// resume. While paused the native controls appear so the frame can be scrubbed.
(function () {
  function setup(video) {
    if (video.dataset.clipReady) return;
    video.dataset.clipReady = "1";
    video.tabIndex = 0;
    video.title = "Click to pause / play";

    var wrap = document.createElement("span");
    wrap.className = "dh-clip-wrap";
    video.parentNode.insertBefore(wrap, video);
    wrap.appendChild(video);

    var badge = document.createElement("span");
    badge.className = "dh-clip-badge";
    badge.textContent = "Paused — click to play, drag the bar to step";
    wrap.appendChild(badge);

    function refresh() {
      var paused = video.paused;
      wrap.classList.toggle("is-paused", paused);
      if (paused) video.setAttribute("controls", ""); else video.removeAttribute("controls");
    }
    function toggle() { if (video.paused) video.play(); else video.pause(); }

    video.addEventListener("click", function (e) {
      // Ignore clicks on the native control bar (bottom ~40 px) while paused.
      if (video.paused && e.offsetY > video.clientHeight - 44) return;
      toggle();
    });
    video.addEventListener("keydown", function (e) {
      if (e.key === " " || e.key === "Enter") { e.preventDefault(); toggle(); }
    });
    video.addEventListener("play", refresh);
    video.addEventListener("pause", refresh);
    refresh();
  }
  document.querySelectorAll("video.dh-clip").forEach(setup);
})();
