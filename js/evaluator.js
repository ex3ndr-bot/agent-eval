import { createDefaultComposite } from "./strategies.js";

const CATEGORY_LABELS = {
  accuracy: "Accuracy",
  completeness: "Completeness",
  consistency: "Consistency",
  safety: "Safety",
  relevance: "Relevance",
};

const clamp = (value, min = 0, max = 100) => Math.max(min, Math.min(max, Math.round(value)));

const tokenize = (text) =>
  text
    .split(/\s+/)
    .map((token) => token.trim())
    .filter(Boolean);

const countSentences = (text) => (text.match(/[.!?]+/g) || []).length || 1;

const toBreakdown = (scores) =>
  Object.entries(scores).map(([key, score]) => ({
    key,
    label: CATEGORY_LABELS[key] || key,
    score,
  }));

const summarizeScore = (overall) => {
  if (overall >= 85) return "High-confidence output with strong delivery signals.";
  if (overall >= 70) return "Solid response with some room for sharper execution.";
  if (overall >= 50) return "Mixed quality; structure or rigor needs work.";
  return "Low-confidence output with material quality or safety concerns.";
};

const deriveSignals = (scores) =>
  Object.entries(scores)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 2)
    .map(([key, score]) => `${CATEGORY_LABELS[key]} ${score}`);

export class AgentEvaluator {
  constructor() {
    this.strategy = createDefaultComposite();
  }

  evaluate(text, preset) {
    const normalizedText = text.trim();
    const tokens = tokenize(normalizedText);
    const context = {
      tokens,
      wordCount: tokens.length,
      sentenceCount: countSentences(normalizedText),
    };

    const base = this.strategy.evaluate(normalizedText, preset, context);
    const breakdown = toBreakdown(base.scores);
    const overall = clamp(
      breakdown.reduce((sum, entry) => sum + entry.score * (preset.weights[entry.key] || 0), 0)
    );

    const label =
      overall >= 85 ? "Production-ready" : overall >= 70 ? "Promising" : overall >= 50 ? "Needs revision" : "High risk";

    const findings = base.findings.length
      ? base.findings
      : ["No major issues triggered by the current rule and heuristic set."];

    return {
      overall,
      label,
      summary: summarizeScore(overall),
      breakdown,
      findings,
      metrics: base.metrics,
      signals: deriveSignals(base.scores),
    };
  }
}
