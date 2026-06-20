---
id: "xhs-infra-007"
difficulty: "L4"
category: "ai-harness"
subcategory: "训练框架"
tags:
  - "分布式训练"
  - "OOM"
  - "MFU"
  - "Profiler"
  - "小红书"
feynman:
  essence: "训练诊断三板斧：OOM是内存不够（加切片/检查点）、低MFU是效率低（找瓶颈：计算/内存/通信哪一个是短板）、Hang是卡住了（查死锁/网络）。核心工具是Profiler——它告诉你时间花在哪了。"
  analogy: "诊断像体检：OOM=太胖了要减肥（减少内存占用）；低MFU=虽然没胖但效率低（体检找原因：是贫血还是缺乏锻炼还是沟通不畅）；Hang=心脏骤停（紧急查哪里卡住了）。"
first_principle:
  problem: "大模型训练效率的三个维度是什么？它们之间如何tradeoff？"
  axioms:
    - "训练效率=计算效率x通信效率xIO效率"
    - "三者相互制约：减少通信可能增加计算，减少内存可能增加IO"
    - "MFU是综合指标——它捕捉了所有维度的损失"
follow_up:
  - "如何计算训练的理论MFU？"
  - "通信-计算overlap具体怎么实现？"
  - "Gradient Checkpoint的代价是什么？"
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
