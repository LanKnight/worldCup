import { useState } from "react";
import predictionData from "./data/predictions.json";
import type { PredictionData } from "./types";
import { Header } from "./components/Layout/Header";
import { Dashboard } from "./components/Dashboard/Dashboard";
import { BracketView } from "./components/Bracket/BracketView";
import { GroupStageGrid } from "./components/GroupStage/GroupStageGrid";
import { ChampionOdds } from "./components/ChampionOdds/ChampionOdds";
import "./App.css";

type Tab = "dashboard" | "bracket" | "groups" | "odds";

function App() {
  const data = predictionData as PredictionData;
  const [activeTab, setActiveTab] = useState<Tab>("dashboard");

  return (
    <div className="app">
      <Header data={data} />
      <nav className="tab-nav">
        {([
          ["dashboard", "仪表盘"],
          ["bracket", "淘汰赛对阵"],
          ["groups", "小组赛"],
          ["odds", "夺冠概率"],
        ] as [Tab, string][]).map(([tab, label]) => (
          <button
            key={tab}
            className={`tab-btn ${activeTab === tab ? "active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {label}
          </button>
        ))}
      </nav>
      <main className="main-content">
        {activeTab === "dashboard" && <Dashboard data={data} />}
        {activeTab === "bracket" && <BracketView data={data} />}
        {activeTab === "groups" && <GroupStageGrid data={data} />}
        {activeTab === "odds" && <ChampionOdds data={data} />}
      </main>
      <footer className="footer">
        <p>
          技术栈：Python + LightGBM + DeepSeek API | {data.monte_carlo_iterations.toLocaleString()} 次蒙特卡洛模拟
          | 生成时间：{new Date(data.generated_at).toLocaleString()}
        </p>
      </footer>
    </div>
  );
}

export default App;
