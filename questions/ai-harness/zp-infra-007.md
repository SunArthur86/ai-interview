---
id: zp-infra-007
difficulty: L3
category: ai-harness
subcategory: 推理优化
tags:
- 智谱
- 面经
- FlashAttention
- IO-aware
- 内存优化
feynman:
  essence: 利用分块计算避免HBM读写瓶颈，提升IO效率
  analogy: 像做菜先备好小料（分块），在案板上（SRAM）切好，别总跑冰箱（HBM）拿东西
  first_principle: 如何避免GPU显存带宽限制成为长序列计算的瓶颈？
  key_points:
  - 将注意力矩阵分块在SRAM中计算
  - 通过重计算策略大幅降低显存占用
  - v2优化并行度，v3利用H100硬件特性加速
  - 将算法从计算受限转为IO受限的优化
follow_up:
- 为什么 FlashAttention 能加速？—— 不是算得更快，而是减少了 HBM 读写次数
- online softmax 怎么做的？—— 分块计算时维护 running max 和 running sum，逐步归一化
- FlashAttention 反向传播怎么工作？—— 不存 attention matrix，反向时用存的 softmax 统计量重算
---

# 【智谱Infra面经】FlashAttention 的核心原理是什么？v1/v2/v3 各有什么改进？

**FlashAttention 核心思想：减少 HBM（显存）读写，用 SRAM（片上缓存）做分块计算。**

**问题背景：**
- 标准 Attention 需要实例化 N×N 的注意力矩阵 → 写入 HBM → 再读回
- HBM 带宽是瓶颈（不是算力）→ **memory-bound**
- FlashAttention 的洞察：**不实例化 N×N 矩阵，分块在 SRAM 内完成**

**FlashAttention v1 核心技术：**
1. **Tiling（分块）**
   - Q/K/V 分成块：Q_i, K_j, V_j
   - 在 SRAM 内计算 S_ij = Q_i · K_j^T
   - 用 online softmax 分块计算注意力

2. **Recomputation（重计算）**
   - 前向不存 N×N 矩阵
   - 反向时重算注意力（只需存 softmax 归一化因子）
   - 内存从 O(N²) → O(N)

**FlashAttention v2 改进：**
1. 减少非 matmul 计算（优化 softmax 分块）
2. 更好的线程块分配（work partitioning）
3. 减少 shared memory bank conflict
4. 支持更多 head 维度

**FlashAttention v3 改进（H100 专用）：**
1. 利用 H100 的异步数据搬运（TMA + async copy）
2. FP8 支持（FP8 Tensor Core）
3. 计算与数据搬运重叠（prefetch 下一块）
4. H100 上 1.5-2x v2 速度

**效果：**
- 训练加速 2-4x（减少 HBM 读写）
- 内存 O(N²) → O(N)
- 长序列收益更大（N=8K 时加速最明显）

## 常见考点
1. **Online Softmax 是如何实现的？为什么需要两遍 Pass？**（第一遍计算 max，第二遍计算 sum 和 exp，保证数值稳定性）
2. **FlashAttention 是如何利用 Softmax 的数学特性进行分块归约的？**（Softmax 是可分解的行归约操作）
3. **v2 相比 v1 调整了线程块策略是为了解决什么问题？**（v1 并行度不足导致算力利用率不高，v2 通过调整 Tiling 策略提升并行度）
