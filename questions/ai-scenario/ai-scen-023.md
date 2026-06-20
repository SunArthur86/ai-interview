---
id: ai-scen-023
difficulty: L2
category: ai-scenario
subcategory: LLM推理与部署
tags:
- 推理缓存
- 语义缓存
- Prefix Cache
- GPTCache
- KV Cache
- 成本优化
feynman:
  essence: 通过复用计算结果或中间状态，减少重复推理以降低延迟和Token消耗。
  analogy: 像考试时的记忆库，完全一样直接抄答案，意思相似稍作修改，开头一样直接接续写。
  first_principle: 如何在保证生成结果一致性的前提下，通过复用历史计算来最大化节省算力？
  key_points:
  - 精确缓存保正确，语义缓存提覆盖，Prefix缓存加速首字
  - 语义缓存需警惕否定词陷阱与阈值设定
  - 分层存储与多级淘汰策略平衡命中与成本
  - LLM推理引擎内部复用KV Cache是终极加速手段
follow_up:
- 语义缓存的相似度阈值如何确定？
- 如何处理缓存失效后的雪崩问题？
- Prefix缓存对不同长度的Prompt效果如何？
---

# 如何设计LLM推理的缓存策略？通过精确缓存、语义缓存和Prefix缓存降低成本和延迟。

【场景分析】
LLM推理缓存可大幅降低成本和延迟。缓存策略需要平衡命中率、正确性、新鲜度。

【缓存层次】
1. 精确缓存（Exact Match）：
   - Key：hash(model + prompt + params)
   - 命中率：低（<5%），但100%正确
   - 适用：FAQ类固定问答、系统Prompt
   - 实现：Redis，TTL=24h
2. 语义缓存（Semantic Cache）：
   - Key：prompt的Embedding向量
   - 命中：新Query与缓存Query的余弦相似度 > 阈值（0.95）
   - 命中率：20-40%（取决于场景）
   - 风险：语义相似但意图不同 → 误命中
   - 实现：GPTCache / 自建向量缓存
3. Prefix缓存（Prefix Cache）：
   - Key：Prompt的公共前缀（系统Prompt、Few-shot示例）
   - 命中方式：复用已计算的KV Cache
   - 优势：不影响生成质量，仅加速推理
   - 实现：vLLM Automatic Prefix Caching

【缓存策略设计】
- 写入策略：Write-through（同步写）或 Write-behind（异步写）
- 淘汰策略：LRU + TTL + 主动失效
- 失效条件：模型版本变更、Prompt模板更新、用户反馈差评
- 分层存储：热数据Redis，温数据SSD，冷数据归档

【语义缓存的风险控制】
- 阈值调优：相似度阈值越高越安全但命中率越低
- 上下文验证：缓存的答案中引用的上下文是否仍有效
- 用户确认：命中缓存时标注「相似问题历史回答」
- 否定词检测：「北京天气」vs「北京不是晴天」语义相似但含义相反

【效果评估】
| 缓存类型 | 命中率 | 延迟降低 | 成本降低 |
| 精确缓存 | 5% | 99% | 5% |
| 语义缓存 | 30% | 95% | 30% |
| Prefix缓存 | 80%（前缀） | 40% | 无直接成本降低 |
