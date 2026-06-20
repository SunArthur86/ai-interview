---
id: xhs-infra-003
difficulty: L4
category: ai-harness
subcategory: 训练框架
tags:
- DeepSpeed
- ZeRO
- 分布式训练
- 3D Parallelism
- 小红书
feynman:
  essence: 将模型状态（优化器、梯度、参数）切片分散存储，消除冗余。
  analogy: 把大百科全书拆成几卷，每人只保管一部分，用的时候再互相借阅。
  first_principle: 如何在数据并行中突破单卡显存限制以训练超大模型？
  key_points:
  - ZeRO-1切分优化器状态，ZeRO-2切分梯度，ZeRO-3切分参数
  - ZeRO-3通信量最大，需配合Offload或3D并行
  - 通过通信与计算重叠掩盖通信延迟
  - 代价是增加了参数获取时的All-Gather通信
follow_up:
- ZeRO-3和FSDP有什么区别？
- 3D Parallelism中DP/TP/PP如何配比？
- 如何诊断训练中的通信瓶颈？
---

# DeepSpeed ZeRO-1/2/3的区别是什么？ZeRO-3的通信瓶颈如何缓解？

ZeRO（Zero Redundancy Optimizer）通过分片消除数据并行中的冗余。

## 三阶段分片
| 阶段 | 分片内容 | 内存节省 | 通信开销 |
|------|---------|---------|----------|
| ZeRO-1 | Optimizer States | ~4x | =DP |
| ZeRO-2 | + Gradients | ~8x | 略增 |
| ZeRO-3 | + Parameters | ~N倍(卡数) | 大增(All-Gather) |

## ZeRO-3通信瓶颈缓解
1. **通信-计算Overlap**：NCCL stream异步通信
2. **Sequence Parallel**：减少TP通信量
3. **3D Parallelism组合**：DP+TP+PP合理配比
4. **CPU/NVME Offload**：减少显存压力
5. **NCCL环境变量调优**：NCCL_IB_DISABLE=0, NCCL_P2P_DISABLE=1

## 实际经验
- ZeRO-3 + 3D Parallel + overlap 可实现高MFU
- 小红书场景：vLLM魔改适配私有模型
