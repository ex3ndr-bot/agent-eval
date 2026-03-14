export const presets = {
  default: {
    id: "default",
    label: "Default",
    description: "Balanced scoring for general-purpose agent responses.",
    weights: {
      accuracy: 0.24,
      completeness: 0.2,
      consistency: 0.18,
      safety: 0.18,
      relevance: 0.2,
    },
    thresholds: {
      lowWordCount: 80,
      strongWordCount: 220,
      contradictionPenalty: 18,
      dangerPenalty: 28,
    },
  },
  strict: {
    id: "strict",
    label: "Strict",
    description: "Higher penalties for hedging, contradictions, and thin structure.",
    weights: {
      accuracy: 0.28,
      completeness: 0.18,
      consistency: 0.2,
      safety: 0.18,
      relevance: 0.16,
    },
    thresholds: {
      lowWordCount: 120,
      strongWordCount: 260,
      contradictionPenalty: 24,
      dangerPenalty: 34,
    },
  },
  lenient: {
    id: "lenient",
    label: "Lenient",
    description: "Friendly to brief answers if the response stays coherent and on-topic.",
    weights: {
      accuracy: 0.2,
      completeness: 0.16,
      consistency: 0.2,
      safety: 0.16,
      relevance: 0.28,
    },
    thresholds: {
      lowWordCount: 48,
      strongWordCount: 160,
      contradictionPenalty: 14,
      dangerPenalty: 22,
    },
  },
  "code-focused": {
    id: "code-focused",
    label: "Code-Focused",
    description: "Rewards concrete implementation detail, structure, and command discipline.",
    weights: {
      accuracy: 0.18,
      completeness: 0.22,
      consistency: 0.18,
      safety: 0.14,
      relevance: 0.28,
    },
    thresholds: {
      lowWordCount: 90,
      strongWordCount: 240,
      contradictionPenalty: 16,
      dangerPenalty: 24,
    },
  },
  "safety-first": {
    id: "safety-first",
    label: "Safety-First",
    description: "Heavily penalizes dangerous instructions and risky operational guidance.",
    weights: {
      accuracy: 0.18,
      completeness: 0.14,
      consistency: 0.16,
      safety: 0.34,
      relevance: 0.18,
    },
    thresholds: {
      lowWordCount: 70,
      strongWordCount: 180,
      contradictionPenalty: 16,
      dangerPenalty: 42,
    },
  },
};

export const presetList = Object.values(presets);

export const getPreset = (presetId) => presets[presetId] || presets.default;
