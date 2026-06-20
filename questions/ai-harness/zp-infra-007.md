---
id: "zp-infra-007"
difficulty: "L3"
category: "ai-harness"
subcategory: "推理优化"
tags:
  - "智谱"
  - "面经"
  - "FlashAttention"
  - "IO-aware"
  - "内存优化"
feynman:
  essence: "FlashAttention = 不把 N×N 的注意力矩阵写到显存（太慢），而是拆成小块在 GPU 的快速缓存里算完。算得'步骤'没少，但'搬运数据'少了，所以快了。"
  analogy: "算 1000×1000 矩阵——标准方法是全部写在白板上（HBM），算一下读一下。FlashAttention 是每次拿 32×32 的小块到脑子里算（SRAM），算完直接写结果。白板读写少了，所以快。"
  key_points:
    - "核心：分块在 SRAM 计算，减少 HBM 读写"
    - "Online softmax 实现分块注意力"
    - "反向重计算，内存 O(N²)→O(N)"
    - "v2优化分区，v3利用H100异步+FP8"
first_principle:
  problem: "Attention 的计算量是 O(N²d)，HBM 读写也是 O(N²)。但 GPU 算力远大于带宽，所以瓶颈是 IO（memory-bound）。如何减少 IO？"
  axioms:
    - "GPU SRAM 带宽 >> HBM 带宽（约 10x）"
    - "Attention 需要全局 softmax → 似乎无法分块"
    - "Online softmax 可以分块计算归一化"
  rebuild: "从 IO 瓶颈出发：① 为什么慢（HBM 读写 O(N²)）？② 能否避免写 N×N 矩阵（分块计算）？③ softmax 怎么分块（online softmax）？④ 反向传播怎么办（重计算）？⑤ 硬件特性怎么利用（TMA/FP8）？"
follow_up:
  - "为什么 FlashAttention 能加速？—— 不是算得更快，而是减少了 HBM 读写次数"
  - "online softmax 怎么做的？—— 分块计算时维护 running max 和 running sum，逐步归一化"
  - "FlashAttention 反向传播怎么工作？—— 不存 attention matrix，反向时用存的 softmax 统计量重算"
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
