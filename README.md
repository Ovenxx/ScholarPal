# ScholarPal

> 一个统一的研究进展平台：三条线每日自动更新，一个入口。
> **组合已有开源项目，不自建引擎。**

## 三个模块

| 模块 | 覆盖范围 | 产物 |
|---|---|---|
| **A · LLM4OR / L2O** | 用大模型做优化：自动算法设计（FunSearch / ReEvo / 进化式启发式）、自动建模、学习型优化器、车辆路径与组合优化求解、求解器智能 | [`docs/llm4or/README.md`](docs/llm4or/README.md) |
| **B · Agentic AI** | 智能体循环、上下文工程、工具协议、多智能体编排、记忆、规划与自我进化 | [`docs/agentic/README.md`](docs/agentic/README.md) |
| **C · 行业资讯** | 论文之外的动态：模型与智能体的行业进展、开源生态、协议演进（按关键词从订阅源筛选） | [网页报告](https://ovenxx.github.io/ScholarPal/) |

模块 A/B 每天 06:00、06:20（北京时间）产出论文清单；模块 C 每天 06:30 产出资讯报告。全部自动提交到本仓库。

## 架构：组合了什么，没自建什么

```
arXiv ──┐
        │   ┌────────────── ScholarPal（本仓库）──────────────┐
订阅源 ─┼──►│  A/B: config/*.yml        C: news/config/*      │
        │   │      │                        │                 │
        │   │      ▼                        ▼                 │
        │   │  docs/llm4or/  docs/agentic/  news/report/      │
        │   │      └───────────┬────────────┘                 │
        │   │                  ▼                              │
        │   │           README.md（统一入口）                   │
        └───┴──────────────────────────────────────────────────┘
```

| 层 | 用的现成项目 | 我们做了什么 |
|---|---|---|
| **论文引擎**（A/B） | [Vincentqyw/cv-arxiv-daily](https://github.com/Vincentqyw/cv-arxiv-daily)（Apache-2.0） | 两份关键词配置 + 两个 workflow。引擎**运行时按固定版本拉取，不入库** |
| **资讯引擎**（C） | [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)（GPL-3.0） | 一份派生配置 + 关键词 + 一个 workflow。引擎同样**运行时拉取，不入库** |
| **领域导航** | [xianchaoxiu/LLM4OR](https://github.com/xianchaoxiu/LLM4OR) · [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) · [a2aproject/A2A](https://github.com/a2aproject/A2A) | 仅 pinned 链接，不自动化 |

**本仓库自研代码量：0（只有配置、workflow 与文档）。**

## 运行

| 模块 | 时间（北京时间） | 手动触发 |
|---|---|---|
| A · LLM4OR / L2O | 06:00 | Actions → `ScholarPal - Module A (LLM4OR/L2O) daily` |
| B · Agentic AI | 06:20 | Actions → `ScholarPal - Module B (Agentic AI) daily` |
| C · 行业资讯 | 06:30 | Actions → `ScholarPal - Module C (News / Industry) daily` |

## 入口

- **网页版行业动态报告**：<https://ovenxx.github.io/ScholarPal/> （每日自动更新）
- **两份论文清单**：[LLM4OR / L2O](docs/llm4or/README.md) · [Agentic AI](docs/agentic/README.md)
- **网页版源码**：`docs/index.html`（由模块 C 每日覆盖）

## 目录结构

```
ScholarPal/
├─ README.md
├─ ATTRIBUTION.md             # 上游归属
├─ LICENSE                    # GPL-3.0
├─ config/                    # 模块 A / B
│  ├─ llm4or.yml
│  └─ agentic.yml
├─ docs/
│  ├─ index.html              # 模块 C 产物（网页入口）
│  ├─ llm4or/                 # 模块 A 产物
│  └─ agentic/                # 模块 B 产物
├─ news/                      # 模块 C
│  ├─ README.md
│  ├─ config/
│  │  ├─ config.yaml
│  │  └─ frequency_words.txt
└─ .github/workflows/
   ├─ llm4or-daily.yml
   ├─ agentic-daily.yml
   └─ news-daily.yml
```

## 领域导航（人工维护，季度过一遍）

- **LLM4OR / L2O**：[xianchaoxiu/LLM4OR](https://github.com/xianchaoxiu/LLM4OR) —— 六分类论文库
- **MCP**：[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- **A2A**：[a2aproject/A2A](https://github.com/a2aproject/A2A) —— 协议官方仓
- **Agent 生态**：[e2b-dev/awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents)

## TODO

- [x] 上游引擎固定版本（A/B 与 C 均已固定）
- [x] LICENSE：GPL-3.0
- [x] 并入资讯层（模块 C）
- [ ] 配置 `AI_API_KEY` 以启用模块 C 的 AI 筛选、翻译与分析
- [ ] 根 README 自动汇总最新一期（目前为手写索引）

## 已知上游行为（已核对源码，暂不修改）

**论文引擎（A/B）**
- `Code` 列恒为 `null`：上游已弃用 PapersWithCode 接口。
- 日报会持续累积：引擎把历史论文合并进 `data.json`，产物会逐日变大。
- 产物内含一处失效相对链接（`./docs/README.md#usage`），指向上游文档。

**资讯引擎（C）**
- 关键词按**标题**匹配，因此 arXiv 订阅源命中率取决于标题措辞；开启 AI 筛选可显著改善。
- 本地存储模式下运行环境不保留历史，"新增"判定能力有限；需要跨天对比需接入远程存储。

## 许可

本项目以 **GPL-3.0** 发布，见 [`LICENSE`](LICENSE)。

之所以是 GPL-3.0 而非更宽松的许可：本平台并入的资讯引擎 TrendRadar 采用 GPL-3.0，其条款要求衍生作品沿用同一许可。这是本项目选择"并成一个平台"时接受的取舍。

上游项目的作者与许可见 [`ATTRIBUTION.md`](ATTRIBUTION.md)。本仓库不包含任何上游源码。