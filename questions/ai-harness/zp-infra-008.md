---
id: "zp-infra-008"
difficulty: "L4"
category: "ai-harness"
subcategory: "推理优化"
tags:
  - "智谱"
  - "面经"
  - "CUDA"
  - "Kernel"
  - "Roofline"
  - "Nsight"
feynman:
  essence: "评估 Kernel = 看'算力利用率'和'带宽利用率'哪个先到天花板。就像评估一条流水线——是工人手速慢（compute bound）还是传送带送料慢（memory bound）？"
  analogy: "Roofline 图就像'天花板图'——横轴是每个 byte 能做多少计算（AI），纵轴是实际性能。曲线下方是能达到的，曲线上方是做不到的。你的 Kernel 在哪，就知道被什么限制了。"
  key_points:
    - "Roofline: AI < 转折点 = memory bound"
    - "Nsight: occupancy + throughput + stall"
    - "Memory bound → tiling/coalescing"
    - "Compute bound → Tensor Core/流水线"
first_principle:
  problem: "GPU 有峰值算力和峰值带宽两个上限。Kernel 的实际性能受限于哪个？如何判断？如何优化？"
  axioms:
    - "性能 = min(算力上限, 带宽上限 × 算术强度)"
    - "算术强度 = FLOPs / Bytes —— 每搬运一个 byte 做多少计算"
    - "GPU 通过 warp 并行隐藏延迟 —— occupancy 决定隐藏能力"
  rebuild: "从 GPU 执行模型出发：① Kernel 的算术强度是多少（分析 FLOPs/Bytes）？② 落在 Roofline 哪段（compute/memory bound）？③ 具体瓶颈在哪（Nsight stall/conflict/throughput）？④ 怎么优化（tiling/Tensor Core/prefetch）？"
follow_up:
  - "Occupancy 是越高越好吗？—— 不一定，高 occupancy 可能意味着低 per-thread 资源"
  - "怎么判断 Kernel 是否已经最优？—— 与 cuBLAS/cuDNN 对比，看差距"
  - "FlashAttention 的 Kernel 为什么快？—— 减少了 global memory 读写，在 SRAM 内完成分块计算"
---

# 【智谱Infra面经】如何评估一个 CUDA Kernel 的优化空间？怎么判断它是计算 bound 还是内存 bound？

**CUDA Kernel 优化评估流程：**

**1. Roofline 模型分析**
```
Arithmetic Intensity (AI) = FLOPs / Bytes

计算上限 = min(峰值算力, AI × 峰值带宽)

如果 AI > 转折点 → Compute Bound
如果 AI < 转折点 → Memory Bound

转折点 = 峰值算力 / 峰值带宽
  A100: 312 TFLOPS / 2TB/s ≈ 156 FLOPs/Byte
  H100: 989 TFLOPS / 3.35TB/s ≈ 295 FLOPs/Byte
```

**2. Nsight Compute 分析**
- **Occupancy**：活跃 warp 数 / 最大 warp 数
  - 低 occupancy → warp 不足以隐藏延迟
- **Memory Throughput**：实际带宽 / 峰值带宽
  - >80% → 接近 memory bound
- **Compute Throughput**：实际 FLOPS / 峰值 FLOPS
  - >80% → 接近 compute bound
- **Stall Reasons**：
  - `stall_long_scoreboard` → 等待内存
  - `stall_short_scoreboard` → 等待计算
- **Bank Conflict**：shared memory bank 冲突

**3. 具体优化方向**

| 瓶颈类型 | 优化方向 |
|----------|--------|
| **Memory Bound** | Coalesced access、shared mem tiling、减少冗余读写 |
| **Compute Bound** | Tensor Core (WMMA/MMA)、指令流水线、减少非 matmul 计算 |
| **Latency Bound** | 增加并行度（更多 warp/block）、prefetch |
| **Bank Conflict** | 调整 shared mem 布局（padding）、改变访问模式 |

**4. GEMM Kernel 优化示例**
```
朴素 GEMM: 每个元素从 global mem 读多次 → 严重 memory bound
优化: 
  1. Tiling: 把块加载到 shared mem（减少 global 读取）
  2. Register tiling: 每个 thread 负责小块，用寄存器累积
  3. Tensor Core: 用 WMMA/MMA 指令做矩阵乘
  4. Vectorized access: float4 一次读 4 个 float
```
