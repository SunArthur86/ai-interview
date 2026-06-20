---
id: xhs-infra-004
difficulty: L5
category: ai-harness
subcategory: 训练框架
tags:
- FlashAttention
- CUDA
- IO优化
- 小红书
feynman:
  essence: 通过Tiling分块利用高速SRAM，减少对慢速HBM的读写访问。
  analogy: 做心算时把数字记在草稿纸上，而不是每次都去翻书（HBM），快得多。
  first_principle: 如何通过优化内存访问模式（IO-aware）来加速Attention计算？
  key_points:
  - 将大矩阵切分成适合SRAM大小的Tile
  - 在SRAM中完成Softmax计算，仅读写HBM各一次
  - 使用Online Softmax避免存储完整的N²矩阵
  - v2优化并行度，v3利用H100 FP8和TMA硬件特性
follow_up:
- FlashAttention如何处理causal mask？
- v3的异步加载为什么能提升性能？
- 在MoE模型中FlashAttention有什么特殊优化？
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
