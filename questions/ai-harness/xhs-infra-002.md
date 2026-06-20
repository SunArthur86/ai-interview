---
id: xhs-infra-002
difficulty: L4
category: ai-harness
subcategory: 推理与部署
tags:
- Speculative Decoding
- 投机解码
- 推理加速
- 小红书
feynman:
  essence: 小模型快速草拟，大模型并行验证，以小博大的推理加速。
  analogy: 经理让实习生先写草稿，自己只负责快速审阅签字，减少加班。
  first_principle: 如何利用廉价计算并行化自回归生成的串行过程？
  key_points:
  - Draft模型串行生成多个候选Token
  - Target模型单次Forward并行验证所有候选
  - 接受正确的前缀，拒绝时从错处回滚
  - 加速比取决于Draft模型的接受率
follow_up:
- draft model如何选择？对生成质量有什么影响？
- 树状投机和传统线性投机有什么区别？
- Speculative Decoding是否保证无损（lossless）？
---

# Speculative Decoding（投机解码）的原理是什么？在高batch场景下如何加速推理？

投机解码通过小模型（draft model）并行生成多个token，大模型验证+修正，实现无损加速。

## 核心流程
1. **Draft阶段**：小模型（如7B）快速生成k个候选token
2. **Verify阶段**：大模型（如70B）并行验证k个token
3. **接受/拒绝**：接受正确前缀，从第一个错误token重新生成

## 加速原理
- 小模型生成速度快10x+
- 大模型并行验证k个token，只多花1次forward
- 期望接受率>70%，等效加速1.5-2.5x

## 变体
- **Medusa**：多头并行投机，无需独立draft model
- **树状投机**：构建候选树，并行验证多条路径
- **PEARL**：基于n-gram的轻量投机

## 高batch场景优势
- GPU利用率更高（验证阶段计算密集）
- 与PagedAttention组合效果好
