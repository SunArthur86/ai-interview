---
id: "xhs-infra-006"
difficulty: "L5"
category: "ai-harness"
subcategory: "推理与部署"
tags:
  - "CUDA"
  - "Kernel"
  - "GEMM"
  - "Tensor Core"
  - "小红书"
feynman:
  essence: "GPU计算矩阵乘法的瓶颈不是运算单元（算力充足），而是把数据从显存搬到计算单元的速度。优化的核心是：用分块（tiling）让数据在快速的shared memory中复用，用Tensor Core做硬件加速的矩阵乘，并消除bank conflict让内存访问并行化。"
  analogy: "厨房做菜：厨师（计算单元）速度很快，但食材（数据）存在远处的仓库（全局内存）。优化就是：1）在灶台旁放小冰箱（shared memory）放常用食材；2）用大锅（Tensor Core）一次炒多人份；3）规划取菜路线让助手们不撞车（消除bank conflict）。"
first_principle:
  problem: "为什么GPU矩阵乘法的瓶颈是数据搬运而非计算？"
  axioms:
    - "GPU TFLOPS >> HBM带宽(TB/s)——计算速度远超数据供给速度"
    - "矩阵乘法中每个数据被多次复用——搬运一次算多次"
    - "SRAM带宽远高于HBM但容量极小（~200KB vs 80GB）"
follow_up:
  - "如何判断一个Kernel是memory-bound还是compute-bound？"
  - "shared memory tiling的大小如何选择？"
  - "MoE模型的router kernel有什么特殊优化？"
---

# CUDA Kernel优化：如何写一个高效的GEMM（矩阵乘法）？bank conflict和Tensor Core如何优化？

## GEMM优化层次（从底到顶）

### 1. 内存访问优化
- **Coalescing**：线程访问连续内存地址（32线程x4字节=128B对齐）
- **Shared Memory Tiling**：将矩阵分块加载到shared memory，减少全局内存访问
- **Bank Conflict消除**：shared memory分32个bank，避免多线程访问同一bank
  - Padding技巧：在数组维度加padding打破冲突

### 2. Tensor Core利用
- **WMMA（Warp Matrix Multiply-Accumulate）**API
- 输入FP16/BF16，累加FP32
- 16x16x16矩阵乘法单时钟周期完成
- H100 FP8支持：E4M3/E5M2

### 3. Tiling策略
- Grid: (M/BM, N/BN)
- Block: (BM, BN, BK)
- 每个block: 加载A[BM×BK]和B[BK×BN]到shared mem
- 用Tensor Core做矩阵乘累加

### 4. Roofline分析
- 用Nsight Compute查看算力/带宽利用率
- 如果mem bound > 60%：优化内存访问
- 如果compute bound：增加Tensor Core利用率

### 关键指标
- Occupancy（SM占用率）
- Bandwidth utilization
- L2 cache hit rate
