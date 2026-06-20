---
id: "misc-004"
difficulty: "L2"
category: "ai-basics"
subcategory: "大模型原理"
tags:
  - "IO"
  - "IOC"
feynman:
  essence: "KV Cache缓存已计算token的Key和Value矩阵,避免重复计算. - *原理:** 生成第t个token时,前t-1个token的K/V不变(因为S"
  analogy: "语义缓存就像客服知识库——相似的问题不用每次重新查（LLM推理），直接从历史回答中找最相似的复用，省钱又快。"
  key_points:
    - "无缓存:O(n²) 次矩阵乘法"
    - "有缓存:O(n) 次矩阵乘法"
    - "显存占用: KV Cache大小 = 2 × n_layers × seq_len × hidden_dim × dtype_size"
first_principle:
  problem: "为什么需要 KV Cache?它为什么能加速自回归生成?有什么代价？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "PagedAttention如何减少显存碎片?"
  - "GQA为什么能减少KV Cache大小?"
---

# 什么是KV Cache?它为什么能加速自回归生成?有什么代价

KV Cache缓存已计算token的Key和Value矩阵,避免重复计算.

- **原理:**
生成第t个token时,前t-1个token的K/V不变(因为Self-Attention需要所有历史K/V).缓存它们后,每步只需计算新token的Q与已有K/V做Attention.

- **加速效果:**
- 无缓存:O(n²) 次矩阵乘法
- 有缓存:O(n) 次矩阵乘法

- **代价:**
1. **显存占用:** KV Cache大小 = 2 × n_layers × seq_len × hidden_dim × dtype_size
- 例如LLaMA-70B, 4K上下文, FP16: ~16GB KV Cache
2. **批量大小受限:** KV Cache占满显存后无法增大batch

- **优化方案:**
- PagedAttention (vLLM) - 操作系统式分页管理KV Cache
- GQA/MQA - 共享K/V减少Cache大小
- 量化KV Cache - INT8/FP8压缩
