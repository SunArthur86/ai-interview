---
id: xhs-infra-006
difficulty: L5
category: ai-harness
subcategory: 推理与部署
tags:
- CUDA
- Kernel
- GEMM
- Tensor Core
- 小红书
feynman:
  essence: 利用Shared Memory分块和Tensor Core硬件加速矩阵乘法。
  analogy: 像搬砖一样，先把砖（数据）搬到脚手架，再快速砌墙，减少来回跑。
  first_principle: 如何最大化利用GPU内存层级和专用计算单元（Tensor Core）？
  key_points:
  - 利用Tiling将数据块加载到Shared Memory复用
  - 合并访存以最大化利用显存带宽
  - 避免Bank Conflict保证Shared Memory并发效率
  - 调用Tensor Core（WMMA API）进行矩阵运算加速
follow_up:
- 如何判断一个Kernel是memory-bound还是compute-bound？
- shared memory tiling的大小如何选择？
- MoE模型的router kernel有什么特殊优化？
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
