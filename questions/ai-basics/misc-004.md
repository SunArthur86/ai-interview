---
id: misc-004
difficulty: L2
category: ai-basics
subcategory: 大模型原理
tags:
- IO
- IOC
feynman:
  essence: 缓存历史K/V矩阵,将生成复杂度从平方级降为线性级。
  analogy: 做算术题,已经算过的步骤直接抄答案,不用每次都从头重算。
  first_principle: 如何消除自回归生成中重复计算历史信息的冗余?
  key_points:
  - 显存换时间:用空间存KV换取生成速度
  - 动态增长:每生成一个新词存一次KV
  - 长颈瓶:KV显存占满是提升batch的主要障碍
follow_up:
- PagedAttention如何减少显存碎片?
- GQA为什么能减少KV Cache大小?
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
