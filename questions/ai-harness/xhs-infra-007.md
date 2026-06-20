---
id: xhs-infra-007
difficulty: L4
category: ai-harness
subcategory: 训练框架
tags:
- 分布式训练
- OOM
- MFU
- Profiler
- 小红书
feynman:
  essence: 利用Profiler工具分析算力、显存和通信瓶颈。
  analogy: 像医生看CT一样，用监控工具定位训练过程堵在哪里。
  first_principle: 如何精准定位并解决分布式训练中的资源瓶颈与异常？
  key_points:
  - OOM通常由大Batch、长序列或未开启Gradient Checkpoint引起
  - 低MFU需区分是Compute Bound、Memory Bound还是Communication Bound
  - Hang常见于网络通信故障或Rank间死锁
  - 核心工具：PyTorch Profiler, Nsight Systems/Compute, NCCL Log
follow_up:
- 如何计算训练的理论MFU？
- 通信-计算overlap具体怎么实现？
- Gradient Checkpoint的代价是什么？
---

# 大模型训练中如何诊断OOM、低MFU和hang？常用的Profiler工具有哪些？

## OOM 诊断

### 显存占用公式
$$Total Memory = Model + Optimizer + Gradients + Activations + KV Cache + Temporary$$

1. **Model Weights (模型参数)**：FP16 时，70B 模型约 140GB。
2. **Optimizer States (优化器状态)**：AdamW 通常需要 FP32 权重备份 + Momentum + Variance（2倍模型大小）。
3. **Gradients (梯度)**：FP16 存储梯度（1倍模型大小）。
4. **Activations (激活值)**：与 Batch Size、Sequence Length、隐藏层维度成正比。

**常见原因 & 解决方案**：
- **原因**：Batch Size 过大、Context Window 过长（KV Cache 爆炸）、未使用 Activation Checkpointing。
- **方案**：
  - **ZeRO-3** (DeepSpeed)：将优化器、梯度、参数切片分布到不同 GPU。
  - **Gradient Checkpointing (Activation Recomputation)**：以计算换显存，前向时不存所有激活，反向时重算。
  - **Sequence Parallel (TP + SP)**：将 Sequence 维度切分，减少单卡 KV Cache 压力。
  - **CPU Offload**：将优化器状态卸载到 CPU（增加通信开销，换显存）。

## 低 MFU 诊断
MFU (Model FLOPs Utilization) = 实际 TFLOPS / 理论峰值 TFLOPS

### 诊断流程与工具
```text
[PyTorch Profiler / Nsight Systems]
         |
   +-----+-----+
   |           |
Compute     Memory
Bound        Bound
   |           |
[检查Kernel] [检查访问]
   |           |
Tensor Core  HBM BW
利用率?      利用率?
```

**常见低 MFU 原因**：
- **通信未 Overlap**：计算与通信未重叠（例如 `torch.nn.parallel.DistributedDataParallel` 梯度同步是阻塞的）。应使用 `torch.distributed.all_reduce` 在反向传播时异步执行，或启用 ZeRO-1/2 的梯度预取。
- **IO 瓶颈**：数据加载慢，GPU 等待 CPU。需设置 `num_workers`、`prefetch_factor`，或使用 WebDataset。
- **Kernel Launch Overhead**：大量小 Kernel 发射。算子融合 可解决。
- **非 MatMul 操作占比高**：LayerNorm、Softmax、Element-wise 操作占比过高，未利用 Tensor Core。

## Hang 诊断
1. **NCCL 调试**：设置环境变量 `NCCL_DEBUG=INFO`，查看通信是否卡在某个 All-Reduce 步骤。
2. **死锁检测**：
   - 检查 `torch.distributed.barrier()` 是否在所有 Rank 一致调用。
   - 避免在一个进程中使用多个 NCCL 通信流导致的资源竞争。
3. **网络拓扑**：检查 InfiniBand (IB) 或 RoCE 的丢包情况（`ibstat`, `perf top`）。
4. **Stack Trace 抓取**：使用 `py-spy dump --pid <pid>` 或 `gdb -p <pid>` 查看进程卡在哪个 Python/C++ 函数（通常卡在 NCCL Kernel 或 GPU Kernel 中）。

## 工具链
| 工具 | 核心用途 | 关键指标 |
|------|----------|----------|
| **PyTorch Profiler** | 整体性能瓶颈分析 | CPU Time, CUDA Time, Memory Usage |
| **Nsight Systems (nsys)** | 系统级时间线可视化 | Kernel Stream, CUDA memcpy, NCCL Call gap |
| **Nsight Compute (ncu)** | 单个 Kernel 深度分析 | Occupancy, Memory L1/L2 Hit, Pipe Utilization |
| **NVLink Topology** | 检查 GPU 互联带宽 | `nvidia-smi topo -m` (P2P/NVLink/SYS) |

## 常见考点
1. **ZeRO-1, 2, 3 的具体区别**：
   - ZeRO-1: 切分 Optimizer States。
   - ZeRO-2: 切分 Optimizer + Gradients。
   - ZeRO-3: 切分 Optimizer + Gradients + Parameters（每卡只存 1/N 参数，通信量最大）。
2. **FlashAttention 如何提升 MFU**：通过 Tiling 和 IO 感知减少 HBM 读写次数，解决 Memory Bound 问题，同时保证数值稳定性。
3. **混合精度训练（AMP）的作用**：使用 FP16/BF16 进行计算，FP32 进行 Master Weights 更新，既加速又保证收敛。BF16 在大模型中为何优于 FP16？（无精度溢出问题，无需 Loss Scaling）。
4. **如何判断是 Compute Bound 还是 Memory Bound**：查看 Nsight Systems 中的 `DRAM Throughput` 和 `SM Throughput`。如果 DRAM 接近满载但 SM 利用率低，则是 Memory Bound。
