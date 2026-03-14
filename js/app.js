import { AgentEvaluator } from "./evaluator.js";
import { getPreset, presetList } from "./configs.js";

const STORAGE_KEY = "agent-eval-history";
const SAMPLE_TEXT = `Implemented the static evaluation dashboard in pure HTML, CSS, and JavaScript.

1. Added a responsive dashboard with preset selection, textarea input, and animated score bars.
2. Wired a composite evaluator that blends rule-based checks with lightweight statistical heuristics.
3. Persisted recent evaluations to localStorage so the history page can render prior runs.

The current build is safe to host on GitHub Pages because it has no backend dependencies and no Python runtime assumptions.`;

const evaluator = new AgentEvaluator();

const elements = {
  configSelect: document.querySelector("#configSelect"),
  outputInput: document.querySelector("#outputInput"),
  evaluateButton: document.querySelector("#evaluateButton"),
  sampleButton: document.querySelector("#sampleButton"),
  charCount: document.querySelector("#charCount"),
  wordCount: document.querySelector("#wordCount"),
  statusChip: document.querySelector("#statusChip"),
  emptyState: document.querySelector("#emptyState"),
  resultsView: document.querySelector("#resultsView"),
  overallScore: document.querySelector("#overallScore"),
  overallLabel: document.querySelector("#overallLabel"),
  overallSummary: document.querySelector("#overallSummary"),
  signalList: document.querySelector("#signalList"),
  scoreBars: document.querySelector("#scoreBars"),
  findingsList: document.querySelector("#findingsList"),
  summaryBlock: document.querySelector("#summaryBlock"),
};

const updateCounts = () => {
  const text = elements.outputInput.value;
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  elements.charCount.textContent = String(text.length);
  elements.wordCount.textContent = String(words);
};

const populatePresets = () => {
  elements.configSelect.innerHTML = presetList
    .map(
      (preset) => `
        <option value="${preset.id}">${preset.label} / ${preset.description}</option>
      `
    )
    .join("");
};

const setStatus = (label, state) => {
  elements.statusChip.textContent = label;
  elements.statusChip.className = `status-chip ${state}`;
};

const renderSignals = (signals) => {
  elements.signalList.innerHTML = signals
    .map((signal) => `<span class="signal-pill">${signal}</span>`)
    .join("");
};

const renderBreakdown = (breakdown) => {
  elements.scoreBars.innerHTML = breakdown
    .map(
      (entry) => `
        <div class="score-row">
          <div class="score-label">
            <strong>${entry.label}</strong>
            <span>${entry.score}/100</span>
          </div>
          <div class="progress-track">
            <div class="progress-bar" data-score="${entry.score}"></div>
          </div>
        </div>
      `
    )
    .join("");

  requestAnimationFrame(() => {
    document.querySelectorAll(".progress-bar").forEach((bar) => {
      bar.style.width = `${bar.dataset.score}%`;
    });
  });
};

const renderFindings = (findings) => {
  elements.findingsList.innerHTML = findings.map((item) => `<li>${item}</li>`).join("");
};

const renderSummary = (result, preset, text) => {
  const preview = text.trim().replace(/\s+/g, " ").slice(0, 220);
  elements.summaryBlock.textContent = [
    `Preset: ${preset.label}`,
    `Overall: ${result.overall}/100`,
    `Classification: ${result.label}`,
    `Metrics: ${JSON.stringify(result.metrics, null, 2)}`,
    `Preview: ${preview}${text.trim().length > 220 ? "..." : ""}`,
  ].join("\n");
};

const persistHistory = (result, preset, text) => {
  const preview = text.trim().replace(/\s+/g, " ").slice(0, 180);
  const record = {
    timestamp: Date.now(),
    configId: preset.id,
    configLabel: preset.label,
    overall: result.overall,
    label: result.label,
    preview,
    breakdown: result.breakdown,
  };

  const history = (() => {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    } catch {
      return [];
    }
  })();

  history.push(record);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(history.slice(-25)));
};

const renderResult = (result, preset, text) => {
  elements.emptyState.classList.add("hidden");
  elements.resultsView.classList.remove("hidden");
  elements.overallScore.textContent = String(result.overall);
  elements.overallLabel.textContent = result.label;
  elements.overallSummary.textContent = result.summary;
  document.documentElement.style.setProperty("--score", result.overall);
  renderSignals(result.signals);
  renderBreakdown(result.breakdown);
  renderFindings(result.findings);
  renderSummary(result, preset, text);
  setStatus("Evaluation complete", "done");
};

const evaluateCurrentInput = () => {
  const text = elements.outputInput.value.trim();

  if (!text) {
    setStatus("Paste output to evaluate", "idle");
    elements.outputInput.focus();
    return;
  }

  const preset = getPreset(elements.configSelect.value);
  setStatus("Running evaluation", "running");

  window.setTimeout(() => {
    const result = evaluator.evaluate(text, preset);
    renderResult(result, preset, text);
    persistHistory(result, preset, text);
  }, 280);
};

populatePresets();
updateCounts();

elements.outputInput.addEventListener("input", updateCounts);
elements.evaluateButton.addEventListener("click", evaluateCurrentInput);
elements.sampleButton.addEventListener("click", () => {
  elements.outputInput.value = SAMPLE_TEXT;
  updateCounts();
  evaluateCurrentInput();
});
