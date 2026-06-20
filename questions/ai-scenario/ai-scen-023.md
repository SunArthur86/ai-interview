---
id: "ai-scen-023"
difficulty: "L2"
category: "ai-scenario"
subcategory: "LLM推理与部署"
tags:
  - "推理缓存"
  - "语义缓存"
  - "Prefix Cache"
  - "GPTCache"
  - "KV Cache"
  - "成本优化"
feynman:
  essence: "LLM 推理缓存三层策略：① 精确缓存（HASH 完全匹配，最快、召回低）；② 语义缓存（embedding 相似度匹配，召回高、需防串味）；③ Prefix 缓存（共享相同前缀的 KV Cache，如系统提示复用）。三者结合可大幅降低成本和延迟，关键是设相似度阈值、隔离租户、加 TTL、监控命中率。"
  analogy: "语义缓存就像客服知识库——相似的问题不用每次重新查（LLM推理），直接从历史回答中找最相似的复用，省钱又快。"
  key_points:
    - "精确缓存（Exact Match）："
    - "Key：hash(model + prompt + params)"
    - "命中率：低（<5%），但100%正确"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
follow_up:
  - "语义缓存的相似度阈值如何确定？"
  - "如何处理缓存失效后的雪崩问题？"
  - "Prefix缓存对不同长度的Prompt效果如何？"
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
