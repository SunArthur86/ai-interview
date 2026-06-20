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

## OOM诊断
1. **分析显存占用**：参数 + 梯度 + 优化器状态 + 激活值 + KV Cache
2. **常见原因**：batch size过大、序列过长、未用Gradient Checkpoint
3. **解决方案**：
   - 减小batch / Gradient Accumulation
   - Sequence Parallel减少激活内存
   - ZeRO-3 + CPU Offload

## 低MFU诊断
MFU (Model FLOPs Utilization) = 实际TFLOPS / 理论峰值TFLOPS

**诊断流程**：
1. PyTorch Profiler / Nsight Systems 定位bottleneck
2. 检查：计算bound / 内存bound / 通信bound
3. NCCL日志分析通信开销

**常见低MFU原因**：
- 通信未overlap（All-Reduce等待）
- 数据加载IO瓶颈
- Kernel launch开销
- 非matmul操作占比高

## Hang诊断
1. NCCL debug日志：NCCL_DEBUG=INFO
2. 检查死锁（rank间同步不一致）
3. 检查网络拓扑（InfiniBand连接）
4. py-spy dump 抓取stack trace

## 工具链
| 工具 | 用途 |
|------|------|
| PyTorch Profiler | 整体性能分析 |
| Nsight Systems | 系统级时间线 |
| Nsight Compute | Kernel级分析 |
| NCCL日志 | 通信诊断 |
