---
id: "zp-infra-006"
difficulty: "L3"
category: "ai-harness"
subcategory: "推理优化"
tags:
  - "智谱"
  - "面经"
  - "GQA"
  - "KV Cache"
  - "注意力机制"
feynman:
  essence: "GQA = 让多个 Q 头共用一组 KV。不像 MQA 那样粗暴地让所有人共用一份（质量差），而是分组共享——4-8 组，既省 KV Cache 又不太损质量。"
  analogy: "32 个人开会——MHA 是每人一份会议纪要（最精确但最耗内存），MQA 是所有人共用一份（最省但信息丢失），GQA 是分成 8 组每组一份（平衡点）。"
  key_points:
    - "MHA→MQA→GQA：质量递减、KV Cache 递减"
    - "GQA g=8 时质量接近 MHA"
    - "KV Cache 减少 4-8x"
    - "GLM-4 用 GQA 支撑长上下文推理"
first_principle:
  problem: "MHA 的 KV Cache 随头数线性增长。但不同头的 KV 是否存在冗余？如何减少冗余而不损失太多质量？"
  axioms:
    - "不同头的 K/V 存在跨头相关性——不是完全独立的"
    - "共享粒度越粗（MQA）质量损失越大"
    - "GQA 的分组是 MHA 和 MQA 之间的连续插值"
  rebuild: "从 KV Cache 瓶颈出发：① 冗余在哪（跨头相似性）？② 共享多少（MHA→GQA→MQA 的帕累托前沿）？③ 质量损失可控吗（g=4-8 经验最优）？④ 对长上下文的影响（KV 减少是关键）？"
follow_up:
  - "GQA 的分组数怎么选？—— 通常 h/4 ~ h/8，需要实验验证"
  - "GQA 训练时和 MHA 有什么区别？—— K/V 投影矩阵更小，其他不变"
  - "MLA 和 GQA 有什么区别？—— MLA 是低秩压缩（动态恢复），GQA 是离散共享"
---

# 【智谱Infra面经】GLM-4 为什么选择 GQA？GQA vs MHA/MQA 的头数/维度权衡？KV Cache 节省多少？

**注意力机制演进：MHA → MQA → GQA**

| 机制 | Q 头数 | K/V 头数 | KV Cache | 质量 |
|------|--------|---------|----------|------|
| **MHA** | h | h | 1×（基准） | 最好 |
| **MQA** | h | 1 | h× | 差 |
| **GQA** | h | h/g（g组） | g× | 接近MHA |

**GLM-4 选择 GQA 的原因：**
1. **KV Cache 减少**：GLM-4 用 GQA（典型 4-8 组），KV Cache 减少 4-8x
2. **推理吞吐提升**：KV 读写量减少 → memory-bound 缓解 → 吞吐提升
3. **质量保持**：GQA 在 4-8 组时质量接近 MHA，远好于 MQA
4. **长上下文友好**：KV Cache 减少后，128K~1M 上下文推理可行

**KV Cache 计算示例：**
```
假设 32 层 × 32 Q头 × 128 维 × seq_len

MHA: KV Cache = 2 × 32 × 32 × 128 × seq
GQA(g=8): KV Cache = 2 × 32 × 4 × 128 × seq  (减少 8x)
MQA: KV Cache = 2 × 32 × 1 × 128 × seq      (减少 32x)
```

**为什么不用 MQA？**
- MQA 所有 Q 头共享 1 组 KV → 表达能力损失大
- GQA 是 MHA 和 MQA 的折中：分组共享既减少 KV 又保持质量
- 实验表明 GQA g=8 时几乎所有 benchmark 都接近 MHA
