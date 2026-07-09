import type { PredictionData } from "../../types";

interface HeaderProps {
  data: PredictionData;
}

export function Header({ data }: HeaderProps) {
  return (
    <header className="header">
      <h1>2026 世界杯冠军预测系统</h1>
      <p className="subtitle">
        多智能体AI协作 | Elo + 泊松 + LightGBM + DeepSeek 大模型 |
        {data.monte_carlo_iterations.toLocaleString()} 次模拟 |
        模型版本 v{data.model_version}
      </p>
    </header>
  );
}
