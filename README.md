# Agent Eval

Static demo for evaluating AI agent output quality in the browser. The app is designed for GitHub Pages and uses pure HTML, CSS, and JavaScript only.

## Files

- `index.html`: main evaluation dashboard
- `history.html`: local evaluation history from `localStorage`
- `style.css`: shared dark-theme styling
- `js/configs.js`: scoring presets
- `js/strategies.js`: rule-based, statistical, and composite strategies
- `js/evaluator.js`: category scoring and report shaping
- `js/app.js`: dashboard interactions and animated result rendering
- `.nojekyll`: GitHub Pages compatibility

## Run locally

Open `index.html` directly in a browser, or serve the directory with any static file server.

## Scoring model

The evaluator produces 0-100 scores for:

- Accuracy
- Completeness
- Consistency
- Safety
- Relevance

It combines:

- Rule-based checks for hedging, structural markers, contradictions, risky language, and evaluation-specific keywords
- Statistical heuristics for length, entropy, readability, vocabulary diversity, and focus
- Preset weights to generate a composite score

## GitHub Pages

This repo is ready for GitHub Pages as a static site. Keep `.nojekyll` in the root so the `js/` folder is served without Jekyll processing.

## Features
- Animated score gauges
- Side-by-side comparison mode
- Eight evaluation presets
- Click-to-load demo examples
- Expandable criterion findings
- JSON export
- Dark/light theme toggle
- Mobile-friendly responsive layout
- Criterion tooltips
- History page with local trend chart
