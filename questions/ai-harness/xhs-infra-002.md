---
id: "xhs-infra-002"
difficulty: "L4"
category: "ai-harness"
subcategory: "推理与部署"
tags:
  - "Speculative Decoding"
  - "投机解码"
  - "推理加速"
  - "小红书"
feynman:
  essence: "投机解码让一个小模型先快速猜测接下来k个词，大模型一次性验证这些猜测——猜对的直接接受，猜错的从错误处重来。因为大模型验证k个token只需1次forward（和生成1个token一样），所以加速效果显著。"
  analogy: "你写作文时，先快速草拟几句话（小模型），然后老师一次性检查（大模型验证）——老师检查3句和检查1句花费差不多时间，但草拟速度很快，所以整体快了很多。"
first_principle:
  problem: "为什么大模型推理是memory-bound？如何打破内存带宽瓶颈？"
  axioms:
    - "自回归生成每次只输出1个token，但需要读取全部KV Cache"
    - "GPU算力远超显存带宽——计算单元在等数据"
    - "并行验证多个token的额外计算开销很小（边际成本递减）"
follow_up:
  - "draft model如何选择？对生成质量有什么影响？"
  - "树状投机和传统线性投机有什么区别？"
  - "Speculative Decoding是否保证无损（lossless）？"
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
