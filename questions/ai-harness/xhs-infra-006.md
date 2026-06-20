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

## GEMM 优化层次（从底到顶）

### 1. 内存访问优化
- **Coalescing（合并访问）**：保证 Warp 内 32 个线程访问连续的全局内存地址，合并为 1-2 个内存事务（128B）。
- **Shared Memory Tiling（分块）**：利用 Shared Memory 作为软件管理 Cache，将全局内存数据分块复用。
  - 原理：计算 $C = A \times B$，将 A 和 B 切分为 tile 存入 SM，每个线程计算多个元素，减少全局内存访问次数（$O(N^3) \to O(N^2)$）。
- **Bank Conflict 消除**：
  - Shared Memory 分为 32 个 Bank，32 位宽。如果 32 个线程访问同一个 Bank 的不同地址（Stride 为 32 的倍数）会导致冲突。
  - **解决方案**：Padding（维度加 1），或使用 `float4`/`ldg` 向量加载。

### 2. Tensor Core 利用
- **WMMA（Warp Matrix Multiply-Accumulate）API**：
  - 利用 Warp 级别的矩阵指令。
  - **输入**：FP16/BF16 (A, B矩阵)，**累加**：FP32 (C矩阵)。
  - **形状**：16x16x16 (MMA.16x16x16) 或 8x8x32 (早期 Volta)。
- **Hopper (H100) FP8 支持**：引入 FMA 指令，支持 E4M3/E5M2 格式，吞吐量翻倍。
- **数据布局转换**：Tensor Core 要求数据按行/列主序交错存储（如 TN, NN 布局），否则无法利用硬件加速。

### 3. Tiling 策略与流水线

```text
GEMM Tiling & Pipeline 逻辑图

Global Memory (DRAM)
   |      | 
   v      v
+---------------------+
| Shared Mem (Tile A) | <--- Block (32x32 threads)
| Shared Mem (Tile B) | <--- Warp 负责 Sub-C 的计算
+---------------------+
   |      | (Registers)
   v      v
Registers (Thread Fragment)
   |      |
   +--->[ Accumulate (Tensor Core) ]
```

- **Grid/Block 划分**：
  - Grid: `(M/BM, N/BN)`
  - Block: `(BM, BN, BK)`，通常使用 2D 线程块 `(32, 32)`。
- **Double Buffering / Pipeline**：
  - 在计算当前 Tile 的同时，异步加载下一个 Tile (`cp.async`)，隐藏内存延迟。

### 4. Roofline 模型分析
- **公式**：`Performance = min { Peak Compute, Bandwidth * Arithmetic Intensity }`
- **诊断**：
  - 用 `Nsight Compute` 查看 `Memory Throughput` 和 `Compute Throughput`。
  - 如果 **Mem bound**（内存受限，Stall Long）：优化 Shared Memory 读写、增加 Cache Reuse、使用 `__restrict__` 指针。
  - 如果 **Compute bound**（计算受限）：增大 Tile 尺寸、使用 Tensor Core、优化指令流水线。

### 关键指标
- **Occupancy（占用率）**：并非越高越好，足够掩盖延迟即可（通常 >50% 即可）。过高可能意味着 Register/Shared 使用不足。
- **IPC (Instructions Per Cycle)**：衡量指令发射效率。
- **FLOPs Utilization**：实际算力 / 理论峰值（A100 312 TFLOPS FP16 Tensor Core）。

## 常见考点
1. **Shared Memory Bank Conflict 的具体场景**：如果 `int array[32]`，线程 `tid` 访问 `array[tid * 32]`，会访问同一个 Bank，导致 32-way Serialize。如何通过 Padding 解决？
2. **Tensor Core 的对齐要求**：使用 WMMA API 时，内存指针需要对齐多少字节？（通常 16B 或 32B，视数据类型而定）。
3. **Warp Divergence 对 GEMM 的影响**：虽然 GEMM 分支较少，但在处理边界（矩阵维度不是 Tile 大小的倍数）时如何避免分歧？（使用边界检查或 Padding 矩阵）。
4. **L2 Cache 的作用**：在计算密集型 GEMM 中，L2 Cache 的命中率是否重要？通常不如 Shared Memory 关键，但在数据量大无法全部放入 Shared 时，L2 Cache Replay 是主要瓶颈之一。
