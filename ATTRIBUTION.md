# 归属与许可

本仓库**不包含**任何上游项目的源码，二者均在运行时按固定版本拉取（克隆目录已在 `.gitignore` 中排除）。

## Vincentqyw/cv-arxiv-daily

- 用途：模块 A / B 的论文日更引擎
- 许可：Apache License 2.0
- 地址：https://github.com/Vincentqyw/cv-arxiv-daily
- 固定版本：`2c6fa8569db604f448adb82124a2e352c78da6b0`
- 引用方式：由 `.github/workflows/{llm4or,agentic}-daily.yml` 在运行时拉取到 `.engine/`
- 我们对它的改动：**无源码改动**。仅通过 `config/*.yml` 传入关键词与输出路径。
  另外在 workflow 中对其**依赖**做了一行兼容处理（`arxiv` 2.x 移除了引擎调用的接口），属依赖适配，不涉及上游代码。

## sansan0/TrendRadar

- 用途：模块 C 的资讯聚合引擎
- 许可：**GNU GPL-3.0**
- 地址：https://github.com/sansan0/TrendRadar
- 固定版本：`792bcc3928b1617bba09df34989fd5675c159b86`
- 引用方式：由 `.github/workflows/news-daily.yml` 在运行时拉取到 `.news/`
- 我们对它的改动：**无源码改动**。仅覆盖两个配置文件（`news/config/` 下的 `config.yaml` 与 `frequency_words.txt`），
  其中 `config.yaml` 自上游完整配置派生，只改开关与订阅源。
- 备注：上游在其 Actions 流程中设有 7 天签到机制，并建议长期使用改用 Docker 部署。
  本项目自建流程并以**每日一次**的低频调度运行，属轻量使用。

## GPL-3.0 的传递

由于并入 TrendRadar，本仓库整体以 GPL-3.0 发布。这是"合并为单一平台"这一选择对应的许可取舍。

## 参考清单（仅链接，未复制内容）

- https://github.com/xianchaoxiu/LLM4OR
- https://github.com/punkpeye/awesome-mcp-servers
- https://github.com/a2aproject/A2A
- https://github.com/e2b-dev/awesome-ai-agents

## 数据来源

论文元数据来自 arXiv；资讯来自各订阅源。均遵循相应来源的使用条款。