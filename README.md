# 2026 世界杯冠军预测系统

> 基于**多智能体AI协作**的2026世界杯冠军预测系统，融合统计模型、机器学习和 **DeepSeek大模型**，通过5000次蒙特卡洛模拟，可视化展示冠军预测结果。

## 在线演示

> 👉 **https://lanknight.github.io/worldCup/**

## 项目概述

本项目构建了一个完整的AI世界杯预测系统，具备以下能力：

- **数据采集**：爬取FIFA排名、Elo评分、赛事结果，存储于SQLite
- **特征工程**：计算Elo评分和~25维特征向量
- **四引擎融合**：**Elo评分 + 泊松分布 + LightGBM + DeepSeek大模型** 加权Stacking
- **多Agent协作**：5个专门化Agent通过Orchestrator编排
- **蒙特卡洛推演**：5000次完整锦标赛模拟
- **可视化前端**：React暗色主题Dashboard，GitHub Pages托管

## 系统架构

```
数据采集(爬虫) → SQLite → 特征工程(Elo+25维特征) → 四模型融合预测
                                    ↓
                            5-Agent协作编排
                                    ↓
                          5000次蒙特卡洛推演
                                    ↓
                            JSON静态导出
                                    ↓
                        React前端 → GitHub Pages
```

## 五Agent协作系统

| Agent | 角色 | 职责 |
|-------|------|------|
| **Orchestrator** | 总控调度 | 编排流水线、协调各Agent、输出结论 |
| **DataAgent** | 数据采集 | 爬取数据、校验质量、存入SQLite |
| **PredictionAgent** | 预测执行 | 运行四大模型、加权融合、输出比赛预测 |
| **SimulationAgent** | 模拟推演 | 蒙特卡洛锦标赛模拟、统计概率分布 |
| **LLMAgent** | 大模型分析 | DeepSeek API调用、战术分析、叙事生成 |

## 四模融合预测引擎

| 模型 | 淘汰赛权重 | 说明 |
|------|:----------:|------|
| Elo评分 | 20% | 经典体育评分系统，K=40世界杯因子 |
| 双变量泊松 | 20% | MLE拟合攻防强度，建模比分概率 |
| LightGBM | 45% | 梯度提升树，2014-2022数据训练 |
| **DeepSeek LLM** ⭐ | 15% | 战术分析修正因子（±5%），结构化JSON输出 |

## 项目结构

```
worldCup/
├── backend/src/
│   ├── data/          # 数据模型、SQLite、爬虫、48队+104场比赛常量
│   ├── features/      # Elo引擎、特征计算、特征流水线
│   ├── models/        # Elo、泊松、LightGBM、LLM分析器、融合
│   ├── agents/        # 5个Agent + 总控调度
│   ├── simulation/    # 锦标赛模拟器 + 蒙特卡洛引擎
│   └── export/        # JSON导出器
├── frontend/src/
│   ├── components/    # React仪表盘、对阵树、小组表、图表
│   └── data/          # predictions.json（自动生成）
├── docs/              # 构建产物（GitHub Pages）
├── scripts/           # run_prediction.py（CLI入口）
├── article/           # 论坛参赛文章
└── .github/workflows/ # 部署配置
```

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 22+
- DeepSeek API Key（设置 `DEEPSEEK_API_KEY` 环境变量）

### 安装与运行

```bash
# 1. 安装Python依赖
pip install -r backend/requirements.txt

# 2. 安装前端依赖
cd frontend && npm install && cd ..

# 3. 运行预测流水线（采集数据 → 训练模型 → 模拟推演 → 导出结果）
python scripts/run_prediction.py

# 4. 本地预览前端
cd frontend && npm run dev
```

流水线将依次执行：
1. 加载2026世界杯数据（48支球队、104场比赛）
2. 计算Elo评分和25维特征
3. 训练泊松模型和LightGBM模型
4. 调用 **DeepSeek API** 进行战术分析
5. 执行5000次蒙特卡洛模拟
6. 导出 `predictions.json` 供前端使用

### 部署到GitHub Pages

```bash
# 构建前端
cd frontend && npm run build && cd ..

# 提交并推送
git add -A && git commit -m "update predictions" && git push
```

## 核心技术栈

| 层 | 技术 | 说明 |
|---|------|------|
| 语言 | Python 3.13 | ML生态、爬虫 |
| 数据库 | SQLite | 零配置、便携 |
| ML模型 | LightGBM + scikit-learn | 梯度提升、Platt校准 |
| 统计模型 | scipy + numpy | 泊松分布、MLE拟合 |
| 大模型 | **DeepSeek API** | OpenAI兼容接口 |
| 前端 | React 18 + TypeScript + Vite | 组件化、类型安全 |
| 图表 | Recharts | React原生图表库 |
| 部署 | GitHub Pages | 免费静态托管 |

## 参赛文章

详见 [article/qoder-wc2026-prediction.md](article/qoder-wc2026-prediction.md)

## 开源协议

MIT
