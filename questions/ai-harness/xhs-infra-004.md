---
id: "xhs-infra-004"
difficulty: "L5"
category: "ai-harness"
subcategory: "训练框架"
tags:
  - "FlashAttention"
  - "CUDA"
  - "IO优化"
  - "小红书"
feynman:
  essence: "FlashAttention的洞察是：Attention慢不是因为计算量大，而是因为内存读写量大。通过把QKV切成小块放进GPU的快速SRAM里计算（而不是反复读写慢速显存），并用在线Softmax避免存储N×N中间矩阵，将内存复杂度从O(N²)降到O(N)。"
  analogy: "你有一本1000页的书要做笔记。传统做法：每页都翻一遍再回去查——翻来翻去很慢。FlashAttention：每次撕下10页放桌上快速看完做笔记，看完换下一批——减少翻书次数（内存访问），速度快几倍。"
first_principle:
  problem: "为什么Attention的计算瓶颈是IO而非计算？"
  axioms:
    - "GPU的算力(TFLOPS)远超显存带宽(TB/s)——计算单元在等数据"
    - "标准Attention需要多次读写N×N矩阵到HBM"
    - "SRAM(共享内存)带宽远高于HBM但容量有限（~200KB vs 80GB）"
follow_up:
  - "FlashAttention如何处理causal mask？"
  - "v3的异步加载为什么能提升性能？"
  - "在MoE模型中FlashAttention有什么特殊优化？"
---

# FlashAttention v1/v2/v3的核心改进分别是什么？为什么能减少内存访问？

FlashAttention通过IO-aware的tiling策略将Attention从O(N²)内存降低到O(N)。

## v1核心改进（2022）
- **Tiling分块**：将QKV分成小块加载到SRAM，分块计算attention
- **在线Softmax（Online Softmax）**：不需要完整N×N矩阵，增量更新归一化
- **Kernel融合**：QK^T→softmax→dropout→AV全在一个kernel内
- **内存**：O(N²) → O(N)

## v2改进（2023）
- **更好的工作分区**：减少shared memory bank conflict
- **Warp-level优化**：改进线程分配和reduction
- **减少non-matmul FLOPs**
- A100上加速1.5-2x（vs v1）

## v3改进（2024）
- **H100 Tensor Core FP8支持**
- **异步加载（async loading）**：通过TMA（Tensor Memory Access）
- **低精度计算**：BF16/FP8
- H100上速度接近理论峰值

## 为什么快
- 核心是**减少HBM（显存）读写次数**
- 传统：多次读写N×N矩阵
- FlashAttention：分块在SRAM计算，只读写一次
