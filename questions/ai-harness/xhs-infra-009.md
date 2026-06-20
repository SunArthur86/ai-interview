---
id: xhs-infra-009
difficulty: L4
category: ai-harness
subcategory: 推理与部署
tags:
- PD分离
- Prefill-Decode
- vLLM
- 小红书
feynman:
  essence: 将Prefill（计算密集）和Decode（内存密集）拆分到不同资源。
  analogy: 像流水线一样，有人专门负责备料（Prefill），有人专门负责打包。
  first_principle: 如何解决Prefill与Decode阶段资源需求差异导致的整体利用率瓶颈？
  key_points:
  - Prefill阶段计算量大、延迟高，需高算力GPU
  - Decode阶段读显存多、计算小，可用低成本显卡
  - 分离后可针对各自特性独立优化硬件和调度
  - 挑战在于KV Cache在节点间的传输开销
follow_up:
- PD分离的KV Cache传输如何优化？
- 什么场景下PD分离收益最大？
- PD分离和Speculative Decoding能组合吗？
---

# Prefill-Decode分离（PD分离）是什么？为什么能提升推理效率？

PD分离将推理的两个阶段分开调度到不同GPU上。

## 两个阶段的区别
| | Prefill阶段 | Decode阶段 |
|---|---|---|
| 输入 | 整个prompt | 上一步生成的1个token |
| 计算量 | 大（O(N^2)） | 小（O(N)）|
| 特点 | 计算密集 | 内存密集 |
| GPU利用率 | 高 | 低（memory-bound） |

## PD分离策略
1. **Prefill节点**：用高算力GPU（如H100）快速处理prompt
2. **Decode节点**：用多张低成本GPU（如L4）并行decode
3. **KV Cache传输**：Prefill完成后将KV Cache传给Decode节点

## 优势
- Prefill和Decode各自优化到最优
- 资源利用率最大化
- 支持更灵活的弹性调度

## 挑战
- KV Cache传输延迟（可通过RDMA缓解）
- 负载均衡更复杂
- 小红书/美团等场景：长上下文+高并发时效果显著
