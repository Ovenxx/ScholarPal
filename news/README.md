# 资讯层（第三个模块）

由 [TrendRadar](https://github.com/sansan0/TrendRadar) 驱动，跟踪论文之外的行业动态。

- **配置**：`config/config.yaml`（自上游完整配置派生，只改开关与订阅源）、`config/frequency_words.txt`
- **运行**：`.github/workflows/news-daily.yml`，每日 06:30（北京时间）
- **产物**：`report/index.html`
- **引擎**：运行时按固定版本拉取上游，不复制进本仓库

## 当前开关状态

| 功能 | 状态 | 说明 |
|---|---|---|
| 热榜平台 | 关闭 | 本模块只跟踪研究/行业信息流 |
| RSS 订阅 | 开启 | arXiv cs.AI / cs.MA / cs.LG / math.OC + Hacker News |
| 关键词筛选 | 开启 | 见 `config/frequency_words.txt`，不消耗 AI 额度 |
| AI 分析 / 翻译 | 关闭 | 需要 AI 接口密钥 |
| 消息推送 | 关闭 | 未配置推送渠道 |

## 开启 AI 分析与翻译

1. 仓库 Settings → Secrets and variables → Actions 添加 `AI_API_KEY`
2. 把 `config/config.yaml` 里 `ai_analysis.enabled`、`ai_translation.enabled` 改为 `true`
3. 模型默认 `deepseek/deepseek-v4-flash`，可在同文件 `ai.model` 更换

开启后 TrendRadar 会对内容做智能筛选、翻译与简报——这是它相对"纯关键词匹配"的主要增量。