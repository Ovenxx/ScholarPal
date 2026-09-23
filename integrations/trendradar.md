# 资讯层：TrendRadar 部署说明

**这一层刻意不放进本仓库。** 本文只记录部署方法。

## 为什么仓外部署

[TrendRadar](https://github.com/sansan0/TrendRadar) 使用 **GPL-3.0**。GPL 具传染性：如果把它的代码 fork 进 ScholarPal 并一起分发，ScholarPal 整体都要以 GPL-3.0 发布。

因此约定：**TrendRadar 独立运行（Docker / 它自己的 Actions），ScholarPal 仓库里只放这份说明和配置清单。**

## 它提供什么

- 多平台热点聚合 + **RSS 订阅**
- 关键词精准筛选
- AI 智能筛选新闻 / 翻译 / 分析简报
- 推送渠道：微信、飞书、钉钉、Telegram、邮件、ntfy、bark、Slack
- 自带 **MCP server**，可用自然语言查询
- Docker 部署，数据本地/云端自持

参考数据：62.5k★，最后推送 2026-09-13，GPL-3.0。

## 建议订阅源（按模块分组）

**模块 A · LLM4OR / L2O**

- arXiv `math.OC` / `cs.NE` 最新列表
- arXiv 关键词查询：`LLM for optimization`、`automatic heuristic design`、`learning to optimize`

**模块 B · Agentic AI**

- arXiv `cs.MA` / `cs.CL` 最新列表
- 协议与标准：A2A 官方仓 release、MCP 规范变更
- 厂商工程博客：Anthropic / OpenAI / Google DeepMind 的 agent 相关文章

**共用**

- Hugging Face Daily Papers
- GitHub Trending（可选）

## 部署要点

1. 按上游 README 用 Docker 起服务，或直接 fork 它的仓库跑它自己的 Actions（**在它自己的仓库里**，不要并入 ScholarPal）。
2. 把上面的 RSS 源填进它的订阅配置。
3. 关键词分两组，分别对应模块 A / B，推送时分成两条。
4. 推送渠道按需开启。

## 与项目的协同

TrendRadar 自带 MCP server —— 适合作为「项目二 · 手撕 agent loop」里对接的**第一个真实 MCP 服务端**，不必先自造一个假的。
