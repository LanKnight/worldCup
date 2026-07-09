import type { PredictionData } from "../../types";

interface HeaderProps {
  data: PredictionData;
}

export function Header({ data }: HeaderProps) {
  return (
    <header className="header">
      <h1>2026 FIFA World Cup Champion Prediction</h1>
      <p className="subtitle">
        Multi-Agent AI System | Elo + Poisson + LightGBM + DeepSeek LLM |
        {data.monte_carlo_iterations.toLocaleString()} Simulations |
        Model v{data.model_version}
      </p>
    </header>
  );
}
