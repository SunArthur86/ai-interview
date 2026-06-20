---
id: xhs-infra-001
difficulty: L4
category: ai-harness
subcategory: 推理与部署
tags:
- vLLM
- PagedAttention
- KV Cache
- 推理优化
- 小红书
feynman:
  essence: 借鉴操作系统虚拟内存分页管理KV Cache，解决显存碎片问题。
  analogy: 像电脑管理内存一样，把KV Cache切成固定页，哪里有空位放哪里。
  first_principle: 如何解决变长序列KV Cache存储导致的显存碎片和浪费问题？
  key_points:
  - 将KV Cache切块（Block）非连续存储，消除显存碎片
  - 通过Block Table管理逻辑到物理的映射
  - 结合Continuous Batching实现动态批处理
  - 支持前缀复用（Radix Tree）共享计算结果
follow_up:
- PagedAttention的block大小如何选择？
- 连续批处理和静态批处理有什么本质区别？
- Radix Tree如何实现多轮对话前缀复用？
---

# 为什么vLLM能加快大模型推理速度？PagedAttention的核心原理是什么？

vLLM通过PagedAttention机制大幅提升推理效率。

## PagedAttention核心机制
1. **块表映射**：借鉴OS虚拟内存分页，将KV Cache分成固定大小block（如16 token/block），用block table映射逻辑序列→物理block
2. **消除碎片**：按需分配block，非连续存储，内存利用率提升30%+
3. **连续批处理（Continuous Batching）**：动态加入/退出请求，GPU利用率接近100%

## 其他关键优化
- Radix Tree前缀复用（多轮对话共享KV）
- 高效attention kernel融合
- 动态batch填充

## 性能提升
- 吞吐量提升2-4x（vs HuggingFace Transformers）
- 内存浪费从60%+降至<4%
- 支持长上下文高并发Serving
