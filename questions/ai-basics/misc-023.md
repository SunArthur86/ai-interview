---
id: "misc-023"
difficulty: "L2"
category: "ai-basics"
subcategory: "推理优化"
tags:
  - "IO"
  - "IOC"
feynman:
  essence: "- *挑战:** 128K上下文,KV Cache可达80GB+(70B模型),Attention O(n²)计算 - *KV Cache优化:** 1. *"
  analogy: "语义缓存就像客服知识库——相似的问题不用每次重新查（LLM推理），直接从历史回答中找最相似的复用，省钱又快。"
  key_points:
    - "挑战: 128K上下文,KV Cache可达80GB+(70B模型),Attention O(n²)计算"
    - "KV Cache优化:"
    - "量化KV Cache - INT8/FP8,减少50%显存"
first_principle:
  problem: "从第一性原理看：处理100K+长上下文推理时,KV Cache和Attention如何优化 的根本优势/劣势来源于什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "Attention Sink是什么?为什么 StreamingLLM需要它?"
  - "YaRN长度外推的原理?"
---

# 处理100K+长上下文推理时,KV Cache和Attention如何优化

- **挑战:** 128K上下文,KV Cache可达80GB+(70B模型),Attention O(n²)计算

- **KV Cache优化:**
1. **量化KV Cache** - INT8/FP8,减少50%显存
2. **PagedAttention** - 分页管理消除碎片
3. **KV Cache Offloading** - 不活跃部分放到CPU/SSD

- **Attention优化:**
1. **Ring Attention** - 多GPU环形分片,支持百万token
2. **稀疏Attention** - 只关注局部窗口+全局token
3. **滑动窗口注意力** - Mistral用SWA,固定窗口大小
4. **StreamingLLM** - 保留attention sink + 滑动窗口,支持无限长度推理
