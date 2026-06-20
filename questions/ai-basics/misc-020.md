---
id: misc-020
difficulty: L2
category: ai-basics
subcategory: 推理优化
tags:
- IO
feynman:
  essence: 引入操作系统分页管理与连续批处理，极致优化显存与吞吐。
  analogy: 像餐厅服务员根据客人用餐节奏动态拼桌，不让空座位浪费。
  first_principle: 如何解决LLM推理中显存浪费严重且无法动态批处理的性能瓶颈？
  key_points:
  - PagedAttention消除显存碎片
  - Continuous Batching动态调度
  - 前缀缓存复用计算结果
  - 推理速度相比HF提升10倍
follow_up:
- PagedAttention如何处理变长序列?
- Prefix Caching在什么场景下效果最好?
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
