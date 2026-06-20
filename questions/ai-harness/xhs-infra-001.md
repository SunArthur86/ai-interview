---
id: "xhs-infra-001"
difficulty: "L4"
category: "ai-harness"
subcategory: "推理与部署"
tags:
  - "vLLM"
  - "PagedAttention"
  - "KV Cache"
  - "推理优化"
  - "小红书"
feynman:
  essence: "PagedAttention像OS虚拟内存一样管理KV Cache——把KV Cache分成固定大小的块（block），用块表记录每个序列的块在哪个物理位置，支持非连续存储、动态分配/释放，消除内存碎片和预分配浪费，配合连续批处理让GPU利用率接近100%。"
  analogy: "想象停车场管理：传统方式给每辆车预留最大车位，大量浪费。PagedAttention是划标准小车位，车来分配、走释放，用登记簿记录位置——空间利用率从30%→95%。"
first_principle:
  problem: "大模型推理的核心瓶颈是什么？为什么KV Cache成为主要瓶颈？"
  axioms:
    - "推理时KV Cache随序列长度线性增长，是显存主要消耗者"
    - "传统预分配方式内存利用率仅~30%，碎片化严重"
    - "GPU计算能力远超内存带宽——推理是memory-bound"
follow_up:
  - "PagedAttention的block大小如何选择？"
  - "连续批处理和静态批处理有什么本质区别？"
  - "Radix Tree如何实现多轮对话前缀复用？"
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
