---
id: "misc-020"
difficulty: "L2"
category: "ai-basics"
subcategory: "推理优化"
tags:
  - "IO"
feynman:
  essence: "- *vLLM三大核心创新:** - *1. PagedAttention(KV Cache管理)** - 类操作系统的虚拟内存分页管理 - 将KV Cache"
  analogy: "大语言模型就像读过整个互联网的学者——通过预测「下一个词」生成文本，积累了海量语言模式和知识。"
  key_points:
    - "vLLM三大核心创新:"
    - "1. PagedAttention(KV Cache管理)"
    - "类操作系统的虚拟内存分页管理"
first_principle:
  problem: "为什么需要 vLLM的核心技术创新?为什么比HuggingFace推理快10倍？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "PagedAttention如何处理变长序列?"
  - "Prefix Caching在什么场景下效果最好?"
---

# vLLM的核心技术创新是什么?为什么比HuggingFace推理快10倍

- **vLLM三大核心创新:**

- **1. PagedAttention(KV Cache管理)**
- 类操作系统的虚拟内存分页管理
- 将KV Cache分为固定大小block
- 按需分配block,消除显存碎片
- 显存利用率从~20%提升到~96%

- **2. Continuous Batching(连续批处理)**
- 每个token步都可动态加入/移除请求
- 吞吐量提升**2-4倍**

- **3. Prefix Caching(前缀缓存)**
- 共享system prompt的KV Cache

- **性能对比:** LLaMA-7B (A100): HF Pipeline ~5 tok/s -> vLLM ~50 tok/s = **10x加速**
