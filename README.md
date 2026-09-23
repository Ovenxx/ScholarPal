# ScholarPal

> 一个统一的研究进展聚合平台：两条线各自日更，一个入口。
> **组合已有开源项目，不自建引擎。**

## 两个模块

| 模块 | 覆盖范围 | 最新一期 |
|---|---|---|
| **A · LLM4OR / L2O** | LLM 用于运筹优化：自动算法设计（FunSearch / ReEvo / EoH）、自动建模（Auto-Formulation）、学习型优化器（L2O / NCO）、VRP 与组合优化求解、求解器智能 | [`docs/llm4or/README.md`](docs/llm4or/README.md) |
| **B · Agentic AI** | Agent loop / harness、上下文工程、MCP 与工具协议、A2A 与多智能体编排、记忆、规划与自我进化 | [`docs/agentic/README.md`](docs/agentic/README.md) |

两个模块的日报都由 GitHub Actions 每日自动生成，直接提交到本仓库。

## 架构：组合了什么，没自建什么

```
arXiv ──┐
        │   ┌────────────── ScholarPal（本仓库）──────────────┐
RSS ────┼──►│  模块 A: config/llm4or.yml   模块 B: config/agentic.yml │
        │   │        │                            │            │
博客 ───┘   │        ▼                            ▼            │
            │   docs/llm4or/                 docs/agentic/     │
            │        └──────────┬───────────────┘              │
            │                   ▼                              │
            │            README.md（统一入口）                   │
            └──────────────────────────────────────────────────┘
```

| 层 | 用的现成项目 | 我们做了什么 |
|---|---|---|
| **论文引擎** | [Vincentqyw/cv-arxiv-daily](https://github.com/Vincentqyw/cv-arxiv-daily)（Apache-2.0） | 只写两份 YAML 关键词配置 + 两个 workflow。引擎**运行时 clone，不入库** |
| **资讯引擎** | [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)（**GPL-3.0**） | **不 fork、不入库**，独立 Docker 部署，见 [`integrations/trendradar.md`](integrations/trendradar.md) |
| **领域导航** | [xianchaoxiu/LLM4OR](https://github.com/xianchaoxiu/LLM4OR) · [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) · [a2aproject/A2A](https://github.com/a2aproject/A2A) | 仅 pinned 链接，不自动化 |

**本仓库自研代码量：0。** 只有配置、workflow 和文档。

## 运行

自动：每天 **06:00 (Asia/Shanghai)** = `0 22 * * *` UTC，两个 workflow 各自独立跑。

手动：GitHub → Actions → 选 `ScholarPal - Module A` 或 `Module B` → Run workflow。

本地跑单个模块：

```bash
pip install arxiv requests pyyaml
git init -q .engine
git -C .engine remote add origin https://github.com/Vincentqyw/cv-arxiv-daily.git
git -C .engine fetch -q --depth 1 origin 2c6fa8569db604f448adb82124a2e352c78da6b0
git -C .engine checkout -q FETCH_HEAD
python .engine/daily_arxiv.py --config_path config/llm4or.yml
```

> 前提：`docs/llm4or/data.json` 必须已存在（空文件 `{}` 即可）。上游引擎用 `"r"` 模式打开它，缺失会直接报错。

## 目录结构

```
ScholarPal/
├─ README.md                  # 统一入口（手写，不会被覆盖）
├─ ATTRIBUTION.md             # 上游项目归属
├─ config/
│  ├─ llm4or.yml              # 模块 A 关键词与输出路径
│  └─ agentic.yml             # 模块 B 关键词与输出路径
├─ docs/
│  ├─ llm4or/                 # 模块 A 日报（自动生成）
│  └─ agentic/                # 模块 B 日报（自动生成）
├─ integrations/
│  └─ trendradar.md           # 资讯流部署说明（GPL 组件，仓外运行）
└─ .github/workflows/
   ├─ llm4or-daily.yml
   └─ agentic-daily.yml
```

## 领域导航（人工维护，季度过一遍）

- **LLM4OR / L2O**：[xianchaoxiu/LLM4OR](https://github.com/xianchaoxiu/LLM4OR) —— 六分类论文库（Surveys / Model Construction / Algorithm Design / Solution Verification / Applications / Datasets）
- **MCP**：[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- **A2A**：[a2aproject/A2A](https://github.com/a2aproject/A2A) —— 协议官方仓，A2A 口径以此为准
- **Agent 生态**：[e2b-dev/awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)

## TODO

- [x] 把上游引擎 pin 到固定 commit SHA（当前 `2c6fa856`）
- [x] LICENSE：MIT（见 `LICENSE`）
- [ ] 部署 TrendRadar 实例并把 arXiv RSS 加进它的订阅源
- [ ] 根 README 自动汇总两个模块最新一期（目前是手写索引）

## 已知上游行为（已核对源码，暂不修改）

- **没有代码链接**：上游已弃用 PapersWithCode API，`Code` 列恒为 `null`。
- **日报会持续累积**：引擎把历史论文合并进 `data.json`，生成的 markdown 包含全部历史记录，会逐日变大。缓解办法只能是降低 `max_results`、定期归档，或日后自行裁剪。
- **生成内容含一处失效相对链接**：`> Usage instructions: [here](./docs/README.md#usage)` 指向上游文档，本仓库没有该文件。
- 以上都源于上游实现，因约定「不自建」而保留原样；如需修正需 fork 并改源码。

## 归属

上游项目的作者与许可见 [`ATTRIBUTION.md`](ATTRIBUTION.md)。本仓库不包含上游源码。


