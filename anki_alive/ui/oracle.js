(() => {
  const ID = "anki-alive-oracle-reveal";
  let hideTimer = null;

  function ensureReveal() {
    let root = document.getElementById(ID);
    if (root) return root;

    root = document.createElement("div");
    root.id = ID;
    root.className = "aa-oracle-reveal";
    root.setAttribute("role", "status");
    root.setAttribute("aria-live", "polite");
    root.setAttribute("aria-atomic", "true");
    root.innerHTML = `
      <p class="aa-oracle-reveal__label">Oracle</p>
      <p class="aa-oracle-reveal__result"></p>
    `;
    document.body.appendChild(root);
    return root;
  }

  function messageFor(payload) {
    const predictedFail = payload.predicted_outcome === "FAIL";
    const recalled = Boolean(payload.actual_recall_success);
    const correct = payload.result === "CORRECT";

    if (correct && predictedFail && !recalled) {
      return "Prediction confirmed — this memory was fragile today.";
    }
    if (correct && !predictedFail && recalled) {
      return "Prediction confirmed — recall held.";
    }
    if (!correct && predictedFail && recalled) {
      return "You recalled it despite the prediction.";
    }
    return "Oracle missed this one — the memory changed the story.";
  }

  function showResolution(payload) {
    const root = ensureReveal();
    const result = root.querySelector(".aa-oracle-reveal__result");
    if (result) result.textContent = messageFor(payload || {});

    root.dataset.reducedMotion = payload && payload.reduced_motion ? "true" : "false";
    root.dataset.visible = "true";

    if (hideTimer !== null) window.clearTimeout(hideTimer);
    hideTimer = window.setTimeout(() => {
      root.dataset.visible = "false";
      hideTimer = null;
    }, 2600);
  }

  window.AnkiAliveOracle = { showResolution };
})();
