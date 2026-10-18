// The phone menu, and the hero's BUILD / RUN switch, which swaps the words' colour, the
// line under them and the terminal between the two things the agents do.
(function () {
  var head = document.querySelector(".site-head");
  var menu = document.querySelector(".menu-btn");
  if (head && menu) {
    menu.addEventListener("click", function () {
      var open = head.getAttribute("data-open") === "true";
      head.setAttribute("data-open", open ? "false" : "true");
      menu.setAttribute("aria-expanded", open ? "false" : "true");
    });
  }

  var hero = document.querySelector("[data-duo]");
  if (!hero) return;
  var sw = hero.querySelector(".switch");
  var words = hero.querySelectorAll("button.word");
  var panes = document.querySelectorAll("[data-mode-pane]");

  function set(mode) {
    sw.setAttribute("data-mode", mode);
    sw.setAttribute("aria-label", mode === "build" ? "Show what the agents run" : "Show what the agents build");
    words.forEach(function (w) {
      w.setAttribute("aria-pressed", w.getAttribute("data-mode") === mode ? "true" : "false");
    });
    panes.forEach(function (p) {
      p.hidden = p.getAttribute("data-mode-pane") !== mode;
    });
  }
  sw.addEventListener("click", function () {
    set(sw.getAttribute("data-mode") === "build" ? "run" : "build");
  });
  words.forEach(function (w) {
    w.addEventListener("click", function () { set(w.getAttribute("data-mode")); });
  });
  set("build");
})();

// Contact: the form becomes a ready-to-send email, since this site has no server.
(function () {
  var form = document.getElementById("contact-form");
  if (!form) return;
  var copy = document.getElementById("copy-email");
  var addr = document.getElementById("email-address");
  if (copy && addr) {
    copy.addEventListener("click", function () {
      var text = addr.textContent.trim();
      var done = function () { copy.textContent = "Copied"; setTimeout(function () { copy.textContent = "Copy"; }, 1600); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { selectText(addr); });
      } else {
        selectText(addr);
      }
    });
  }
  function selectText(el) {
    var r = document.createRange(); r.selectNodeContents(el);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var f = new FormData(form);
    var subject = "Automation: " + (f.get("area") || "a workflow") + " (" + (f.get("company") || "no company given") + ")";
    var body = (f.get("message") || "") + "\n\n" + (f.get("name") || "") + "\n" + (f.get("company") || "");
    var href = "mailto:" + addr.textContent.trim() + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    var note = document.getElementById("form-status");
    note.textContent = "Your email app should open with this message. If it doesn't, copy the address above and send it from there.";
    window.location.href = href;
  });
})();
