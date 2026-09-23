# ScholarPal

> 每天一份列表、一份资讯、一个入口 —— 自动追踪 **LLM4OR / L2O** 与 **Agentic AI** 两个方向的最新进展。
> 用已有开源项目拼装而成，不自建爬虫与聚合引擎。

**打开即用 → <https://ovenxx.github.io/ScholarPal/>**

---

## 你会看到什么

一个两栏界面：

**左栏 · 热搜**
- **学术界热搜** —— 从当天全部候选论文里提炼出的主题，附中文说明
- **工业界热搜** —— 从行业信息流里提炼出的主题

**右栏 · 信息流**，三个标签页：

| 标签页 | 内容 |
|---|---|
| `LLM4OR / L2O` | 用大模型做优化：自动算法设计（FunSearch / ReEvo / 进化式启发式）、自动建模、学习型优化器、车辆路径与组合优化求解、求解器智能 |
| `Agentic AI` | 智能体循环、上下文工程、工具协议、多智能体编排、记忆、规划与自我进化 |
| `行业动态` | 论文之外的工程与产业动态（行业信息源，已排除论文源避免重复） |

每张卡片包含：**模型判断的重要性**、**一句话中文摘要**、技术标签、原文链接，以及 **👍 感兴趣 / 👎 不感兴趣 / 💬 评论**。

**个性化**：点赞与评论会沉淀为"长期记忆"，显示在左栏顶部，并把相关研究排到前面并高亮。第一次打开有一次十几秒的勾选引导，用于冷启动。评论是私密的，只有你自己能看到。

每天北京时间 **06:00 起自动更新**，无需任何操作。

---

## 三个数据模块

| 模块 | 内容 | 产物 |
|---|---|---|
| **A · LLM4OR / L2O** | 关键词过滤后的论文清单 | [`docs/llm4or/README.md`](docs/llm4or/README.md) |
| **B · Agentic AI** | 关键词过滤后的论文清单 | [`docs/agentic/README.md`](docs/agentic/README.md) |
| **C · 行业动态 + 站点构建** | 行业资讯、热搜提炼、卡片评分与摘要、网页生成 | `docs/news.html` · `docs/feed.json` |

模块 C 在同一个任务里完成资讯抓取与站点构建 —— 因为它需要直接读取资讯引擎运行期产出的数据。

---

## 架构：组合了什么，没自建什么

```
        ┌──────────── ScholarPal（本仓库）────────────────┐
arXiv ──┤  config/*.yml ──► docs/llm4or/  docs/agentic/   │
        │                                                  │
RSS ────┤  news/config/* ──► (资讯引擎) ──► docs/news.html  │
        │                        │                         │
        │                        ▼                         │
        │              tools/build_feed.py ──► docs/feed.json
        │                        │                         │
        │                        ▼                         │
        │              docs/index.html（网页应用）           │
        └──────────────────────────────────────────────────┘
                                 │
                    私有记忆库 ScholarPal-memory
```

| 层 | 用的现成项目 | 我们做了什么 |
|---|---|---|
| **论文引擎** | [Vincentqyw/cv-arxiv-daily](https://github.com/Vincentqyw/cv-arxiv-daily)（Apache-2.0） | 两份关键词配置。引擎**运行时按固定版本拉取，不入库** |
| **资讯引擎** | [sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)（GPL-3.0） | 一份派生配置 + 关键词。引擎同样**运行时拉取，不入库** |
| **热搜 / 评分 / 摘要** | DeepSeek `deepseek-v4-flash` | 一个两百余行的生成脚本 `tools/build_feed.py` |
| **网页应用** | 无依赖的原生页面 | `docs/index.html` 一个文件 |
| **记忆存储** | 一个私有 GitHub 仓库 | 点赞 / 评论的跨设备同步 |

---

## 开启跨设备记忆（可选，一次性）

不配置也能用，只是点赞与评论只留在当前浏览器。要跨设备同步，需要给网页一个读写权限受限的令牌：

1. 打开 <https://github.com/settings/personal-access-tokens/new>
2. **Repository access** → `Only select repositories` → 勾选 **ScholarPal-memory**
3. **Permissions → Repository permissions → Contents** 设为 **Read and write**
4. 生成并复制令牌
5. 打开网页 → 右上角 **「连接记忆」** → 粘贴

令牌只保存在该设备的浏览器本地，不会写入网页源码。每个设备各粘贴一次。

---

## 运行

| 任务 | 时间（北京时间） | 手动触发名 |
|---|---|---|
| 模块 A · LLM4OR / L2O | 06:00 | `ScholarPal - Module A (LLM4OR/L2O) daily` |
| 模块 B · Agentic AI | 06:20 | `ScholarPal - Module B (Agentic AI) daily` |
| 模块 C · 资讯 + 站点构建 | 06:30 | `ScholarPal - Module C (News + Site build) daily` |

三个任务共用一个并发组，串行执行，因此不会互相覆盖提交。

**本地复现生成脚本**（需要 `AI_API_KEY` 环境变量）：

```bash
pip install arxiv requests pyyaml    # 论文引擎依赖
AI_API_KEY=... python tools/build_feed.py
```

---

## 目录结构

```
ScholarPal/
├─ README.md
├─ ATTRIBUTION.md              # 上游归属
├─ LICENSE                     # GPL-3.0
├─ config/                     # 模块 A / B 关键词
│  ├─ llm4or.yml
│  └─ agentic.yml
├─ news/
│  ├─ README.md                # 资讯层说明
│  └─ config/
│     ├─ config.yaml           # 自上游完整配置派生
│     └─ frequency_words.txt   # 资讯关键词
├─ tools/
│  └─ build_feed.py            # 热搜提炼 + 打分 + 摘要
├─ docs/
│  ├─ index.html               # 网页应用（手写，不被覆盖）
│  ├─ feed.json                # 每日生成的数据
│  ├─ news.html                # 资讯引擎原始报告
│  ├─ llm4or/                  # 模块 A 产物
│  └─ agentic/                 # 模块 B 产物
└─ .github/workflows/
   ├─ llm4or-daily.yml
   ├─ agentic-daily.yml
   └─ news-daily.yml
```

---

## 技术取舍

**成本。** 一天只调用 5 次模型：候选先按关键词粗筛，每栏只把 18 条送进模型精评；同时关闭模型内部推理（同一问题从 201 tokens 降到 38，约省五倍）。

**个性化放在浏览器，而不是服务端。** 网页是静态的、公开的；兴趣画像在本地计算并即时重排，云端只负责分类与摘要。记忆存在**私有**仓库里，因此评论不会公开。

**为什么不接第三方后端。** 跨设备同步只需要一个凭证，用你已有的 GitHub 账号即可，不必再注册新服务。

---

## 已知限制

- **热搜是每日快照，不是实时榜。** 静态站点没有常驻服务；真做滚动更新需要一台服务器。
- **资讯关键词按标题匹配**，正文相关但标题不含关键词的条目会漏掉。开启资讯引擎的 AI 筛选可缓解。
- **论文引擎的产物会持续累积**（上游把历史合并进 `data.json`），文件逐日变大；`Code` 列恒为 `null`，因为上游已弃用相关接口。
- **资讯引擎要求热榜开关保持开启**，否则会整体短路、连订阅源也不抓。这一点已写在 `news/README.md` 里。

---

## 许可

本项目以 **GPL-3.0** 发布，见 [`LICENSE`](LICENSE)。

之所以选 GPL-3.0 而非更宽松的许可：本项目并入的资讯引擎采用 GPL-3.0，其条款要求衍生作品沿用同一许可。这是"合并为单一平台"时所接受的取舍。

上游项目的作者与许可见 [`ATTRIBUTION.md`](ATTRIBUTION.md)。本仓库不包含任何上游源码。
