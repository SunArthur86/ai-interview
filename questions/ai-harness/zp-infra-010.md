---
id: "zp-infra-010"
difficulty: "L3"
category: "ai-harness"
subcategory: "工程化"
tags:
  - "智谱"
  - "面经"
  - "MFU"
  - "性能诊断"
  - "训练优化"
feynman:
  essence: "训练诊断 = 搞清楚'GPU 在等什么'。等内存（OOM）→ 减显存。等通信（低 MFU）→ overlap。等数据（hang）→ 修 IO。用 Profiler 看'时间花在哪'。"
  analogy: "训练诊断像体检——Profiler 是 X 光（看内部耗时分布），Nsight 是 CT 扫描（时间线精细分析），NCCL log 是心电图（通信是否健康）。综合判断'哪里堵了'。"
  key_points:
    - "低 MFU → Profiler + Nsight + NCCL → overlap"
    - "OOM → 分析显存组成 → ZeRO/Checkpoint/Offload"
    - "Hang → py-spy + NCCL_DEBUG + CUDA_LAUNCH_BLOCKING"
    - "目标 MFU >50%（千卡）"
first_principle:
  problem: "万卡训练中 GPU 利用率低、显存不够、训练卡死是三大常见问题。如何系统性地定位根因？"
  axioms:
    - "GPU 性能 = 计算 × 利用率 → 利用率低说明有等待"
    - "显存 = 权重+梯度+优化器+激活 → 可逐项分析"
    - "Hang 通常由通信死锁/IO 卡住/CUDA 错误引起"
  rebuild: "从 GPU 执行模型出发：① 时间花在哪（Profiler 时间线）？② 内存去哪了（显存公式逐项）？③ 为什么卡住（通信/IO/错误）？④ 怎么修复（overlap/分片/调参）？"
follow_up:
  - "MFU 怎么计算？ — — 实际 tokens/s × 每 token FLOPs(6N) / GPU 峰值 FLOPS"
  - "Gradient Checkpoint 的重算开销？ — — 约 20-33%（多一次前向计算）"
  - "NCCL All-Reduce 通信怎么调优？ — — 环形 vs 树形、NCCL_NET、overlap"
---

# 【智谱Infra面经】大模型训练低 MFU / OOM / hang 如何诊断？用哪些工具和指标？

**训练性能诊断三板斧：低 MFU / OOM / Hang**

**1. 低 MFU（Model FLOPs Utilization）诊断**

```
MFU = 实际 FLOPS / 峰值 FLOPS
目标: >50%（千卡集群），>60%（单机）
```

诊断流程：
1. **PyTorch Profiler** → 查看 GPU 利用率、kernel 耗时分布
2. **Nsight Systems** → 时间线分析（计算 vs 通信 vs IO 重叠情况）
3. **NCCL 日志** → All-Reduce/All-Gather 通信延迟
4. **常见原因**：
   - 通信未 overlap（计算等通信）
   - Gradient Checkpoint 重算开销
   - 数据加载瓶颈（CPU IO）
   - 小 kernel 太多（kernel launch 开销）

**2. OOM（Out of Memory）诊断**

显存组成：
```
总显存 = 模型权重 + 梯度 + 优化器状态 + 激活值 + KV Cache + 临时缓冲
  权重: P × bytes_per_param (BF16: 2P)
  梯度: P × 2 (BF16)
  优化器: P × 8 (Adam FP32 momentum+variance)
  激活值: L × batch × seq × hidden × layers
```

解决方案：
| 方案 | 节省 | 代价 |
|------|------|------|
| ZeRO-3 分片 | ~8x optimizer | 通信增加 |
| Gradient Checkpoint | ~60% 激活 | 重算开销 20% |
| CPU Offload | 灵活 | PCIe 带宽瓶颈 |
| 混合精度 BF16/FP8 | 2-4x | 精度损失 |
| Sequence Parallel | 长序列激活 | 通信增加 |

**3. Hang（训练卡死）诊断**

常见原因：
- NCCL 通信死锁（部分 GPU 崩溃）
- 数据加载卡住（NFS/网络存储慢）
- CUDA 错误（NaN/Inf 触发 device assert）
- 内存碎片（碎片化导致 alloc 失败）

诊断工具：
- `py-spy dump --pid <PID>` → 查看 Python 调用栈
- `NCCL_DEBUG=INFO` → NCCL 通信日志
- `CUDA_LAUNCH_BLOCKING=1` → 同步执行定位错误
- `nccl-tests` → 通信基准测试
