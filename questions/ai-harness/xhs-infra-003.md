---
id: "xhs-infra-003"
difficulty: "L4"
category: "ai-harness"
subcategory: "训练框架"
tags:
  - "DeepSpeed"
  - "ZeRO"
  - "分布式训练"
  - "3D Parallelism"
  - "小红书"
feynman:
  essence: "ZeRO的思路是：传统DP中每张卡都存完整副本（参数+梯度+优化器状态），太浪费了。ZeRO逐步把这些都切片分散到各卡上，需要时再All-Gather收集——用更多通信换更少内存，ZeRO-3最极端（全分片），适合超大模型。"
  analogy: "一个团队10人每人各买一套百科全书太贵。ZeRO方案：每人只买其中几卷，需要查时互相借阅——全集加起来还是一套，但每个人桌上只放1/10，省钱（内存）但借阅（通信）变多了。"
first_principle:
  problem: "分布式训练中的内存冗余从哪来？为什么数据并行会浪费内存？"
  axioms:
    - "DP本质是数据并行——每张卡跑不同batch，但模型副本完全相同"
    - "优化器状态（Adam: 2x params）+ 梯度 + 参数 = 大量重复存储"
    - "切分冗余→增加通信，本质是memory vs communication的tradeoff"
follow_up:
  - "ZeRO-3和FSDP有什么区别？"
  - "3D Parallelism中DP/TP/PP如何配比？"
  - "如何诊断训练中的通信瓶颈？"
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
