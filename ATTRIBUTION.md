# 归属与许可

本仓库**不包含**任何上游项目的源码，只在运行时获取或在仓库外独立部署。

## Vincentqyw/cv-arxiv-daily

- 用途：模块 A / B 的 arXiv 论文日更引擎
- 许可：Apache License 2.0
- 地址：https://github.com/Vincentqyw/cv-arxiv-daily
- 引用方式：由 `.github/workflows/*.yml` 在运行时 `git clone` 到 `.engine/`（已被 `.gitignore` 排除），**不提交进本仓库**。
- 本仓库对其的唯一改动：无源码改动。仅通过 `config/*.yml`（运行时拷贝为 `config.yaml`）传入关键词与输出路径。

## sansan0/TrendRadar

- 用途：可选的资讯聚合与推送层
- 许可：**GNU GPL-3.0**
- 地址：https://github.com/sansan0/TrendRadar
- 引用方式：**独立部署（Docker），不 fork、不入库**。原因见 `integrations/trendradar.md`：GPL-3.0 具传染性，若将其代码并入本仓库分发，会导致本仓库整体被 GPL 覆盖。

## 参考清单（仅链接，未复制内容）

- https://github.com/xianchaoxiu/LLM4OR
- https://github.com/punkpeye/awesome-mcp-servers
- https://github.com/a2aproject/A2A
- https://github.com/e2b-dev/awesome-ai-agents

## arXiv 数据

论文元数据来自 arXiv，遵循 arXiv 的使用条款与各论文自身的许可。
