# 2026 FIFA World Cup Champion Prediction System

> Multi-Agent AI prediction system powered by **DeepSeek API**, Elo ratings, Poisson models, and LightGBM.

## Overview

This project predicts the **2026 FIFA World Cup** champion using a multi-agent AI system that combines statistical modeling, machine learning, and large language model analysis. The system:

- Collects World Cup data (teams, matches, results) via web scraping
- Computes Elo ratings and ~25-dimensional feature vectors per match
- Runs a 4-model ensemble: **Elo + Poisson + LightGBM + DeepSeek LLM**
- Simulates the tournament 5,000 times via Monte Carlo
- Visualizes results on an interactive React dashboard
- Deploys to **GitHub Pages** as a static site

## Live Demo

https://LanKnight.github.io/worldCup/

## Architecture

```
Data Collection → Feature Engineering → Prediction Engine → Tournament Simulation → JSON Export → React Frontend
     ↓                    ↓                      ↓                    ↓
  Web Scraping        Elo Ratings          4-Model Ensemble    Monte Carlo 5K×
  SQLite Store        25 Features          DeepSeek LLM        Bracket Builder
```

### 5-Agent System

| Agent | Role |
|-------|------|
| **Orchestrator** | Coordinates the full pipeline |
| **DataAgent** | Scrapes data, validates, stores in SQLite |
| **PredictionAgent** | Runs Elo/Poisson/LightGBM/LLM ensemble |
| **SimulationAgent** | Monte Carlo tournament simulation |
| **LLMAgent** | DeepSeek API tactical analysis & narrative |

### Prediction Models

| Model | Weight (KO) | Description |
|-------|:-----------:|-------------|
| Elo Ratings | 20% | Historical Elo with K=40 World Cup factor |
| Bivariate Poisson | 20% | MLE-fitted attack/defense strengths |
| LightGBM | 45% | Gradient boosting on 2014-2022 data |
| DeepSeek LLM | 15% | Tactical correction factors (±5%) |

## Project Structure

```
worldCup/
├── backend/src/
│   ├── data/          # Data models, SQLite, scraper, constants (48 teams, 104 matches)
│   ├── features/      # Elo engine, base features, feature pipeline
│   ├── models/        # Elo, Poisson, LightGBM, LLM analyzer, ensemble
│   ├── agents/        # 5 agents + orchestrator
│   ├── simulation/    # Tournament simulator + Monte Carlo engine
│   └── export/        # JSON exporter for frontend
├── frontend/src/
│   ├── components/    # React dashboard, bracket, group tables, charts
│   └── data/          # predictions.json (auto-generated)
├── scripts/           # run_prediction.py (CLI entry)
├── article/           # Competition forum article
└── .github/workflows/ # GitHub Pages deployment
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 22+
- DeepSeek API key (set `DEEPSEEK_API_KEY` env var)

### Install & Run

```bash
# 1. Install Python dependencies
pip install -r backend/requirements.txt

# 2. Install frontend dependencies
cd frontend && npm install && cd ..

# 3. Run the prediction pipeline
python scripts/run_prediction.py

# 4. View the frontend
cd frontend && npm run dev
```

The pipeline will:
1. Load 2026 World Cup data (48 teams, 104 matches)
2. Compute Elo ratings and features
3. Train Poisson & LightGBM models
4. Call DeepSeek API for tactical analysis
5. Run 5,000 Monte Carlo simulations
6. Export `predictions.json` for the frontend

## Key Technologies

- **Python**: FastAPI, LightGBM, scikit-learn, scipy, BeautifulSoup4
- **DeepSeek API**: LLM-powered tactical analysis (OpenAI-compatible)
- **React**: TypeScript, Vite, Recharts
- **SQLite**: Zero-config data storage
- **GitHub Pages**: Free static hosting

## Competition Article

See [article/qoder-wc2026-prediction.md](article/qoder-wc2026-prediction.md) for the full write-up.

## License

MIT
