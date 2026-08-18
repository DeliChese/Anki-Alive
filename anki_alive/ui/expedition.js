(function () {
  "use strict";

  var noticeTimer = null;

  function root() {
    return document.getElementById("anki-alive-review-strip");
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function setText(id, value) {
    var node = document.getElementById(id);
    if (node) {
      node.textContent = value;
    }
  }

  function setProgress(payload) {
    var container = root();
    if (!container || !payload) {
      return;
    }

    var completed = Number(payload.completed_reviews || 0);
    var target = Math.max(1, Number(payload.target_reviews || 1));
    var percent = clamp(completed / target, 0, 1);
    var next = payload.reviews_to_next_checkpoint;

    setText("aa-review-progress-value", completed + " / " + target);
    setText(
      "aa-review-progress-next",
      next === null || next === undefined ? "Final segment" : "Next · " + next
    );

    var rail = container.querySelector(".aa-review-strip__rail");
    if (rail) {
      rail.setAttribute("aria-valuenow", String(completed));
      rail.setAttribute("aria-valuemax", String(target));
    }

    var fill = document.getElementById("aa-review-progress-fill");
    if (fill) {
      fill.style.setProperty("--aa-progress-ratio", String(percent));
    }
  }

  function showCheckpoint(payload) {
    var container = root();
    var notice = document.getElementById("aa-review-progress-notice");
    if (!container || !notice || !payload) {
      return;
    }

    var target = Number(payload.target_progress || 0);
    notice.textContent = "Checkpoint reached · " + target;
    notice.classList.add("is-visible");

    if (noticeTimer !== null) {
      window.clearTimeout(noticeTimer);
    }
    noticeTimer = window.setTimeout(function () {
      notice.classList.remove("is-visible");
      noticeTimer = null;
    }, container.dataset.focusMode === "true" ? 800 : 1200);
  }

  window.AnkiAliveExpedition = {
    setProgress: setProgress,
    showCheckpoint: showCheckpoint,
  };
})();
