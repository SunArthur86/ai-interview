---
id: "xhs-infra-009"
difficulty: "L4"
category: "ai-harness"
subcategory: "推理与部署"
tags:
  - "PD分离"
  - "Prefill-Decode"
  - "vLLM"
  - "小红书"
feynman:
  essence: "推理的Prefill（读prompt）和Decode（生成token）阶段特性完全不同——前者计算密集后者内存密集。把它们拆到不同GPU上各自优化，比在一个GPU上串行做两件事效率高得多。"
  analogy: "餐厅厨房分工：备菜（Prefill，需要大灶猛火快速搞定）和摆盘上菜（Decode，需要精细操作但不费火力）分开——备菜组用大炒锅，上菜组用小炖锅，各司其职效率最高。"
first_principle:
  problem: "为什么Prefill和Decode阶段的GPU利用率差异巨大？"
  axioms:
    - "Prefill处理N个token做N^2次attention——计算密集"
    - "Decode每次只生成1个token但需读取全部KV Cache——内存密集"
    - "两种阶段的计算/内存比例相差10x+——不适合在同一硬件上最优运行"
follow_up:
  - "PD分离的KV Cache传输如何优化？"
  - "什么场景下PD分离收益最大？"
  - "PD分离和Speculative Decoding能组合吗？"
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
