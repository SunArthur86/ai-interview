---
id: "mt-ai-004"
difficulty: "L4"
category: "llm-core"
categories:
  - "eng-practice"
  - "llm-core"
subcategory: "推理优化"
tags:
  - "美团"
  - "面经"
  - "KV Cache"
  - "推理优化"
feynman:
  essence: "GQA/MQA 是'多个头共用一份笔记'（粗暴共享），MLA 是'把多份笔记压缩成摘要再恢复'（智能压缩），压缩率更高且信息损失更小。"
  analogy: "GQA 像 4 个人共用 1 把钥匙（安全但不方便）；MLA 像 4 个人各有一把钥匙，但这把钥匙是从一把'主钥匙'按各自密码推导出来的（既独立又节省空间）。"
  key_points:
    - "GQA/MQA = 离散共享（硬共享 K/V）"
    - "MLA = 连续压缩（低秩分解）"
    - "MLA 压缩率 4-16×，质量接近 MHA"
    - "矩阵吸收技术避免推理时显式恢复"
first_principle:
  problem: "多头的 K/V 之间存在冗余。如何最优地消除冗余而不损失注意力质量？"
  axioms:
    - "MHA 中不同头的 K/V 存在低秩相关性（经验证据）"
    - "离散共享（GQA/MQA）损失信息但简单"
    - "连续压缩（MLA）保留更多信息但计算更复杂"
  rebuild: "从 KV Cache 的瓶颈出发：① 冗余在哪（跨头相关性）？② 粗暴共享 vs 智能压缩的 trade-off？③ 推理时如何避免恢复开销？④ 压缩率和质量的帕累托前沿在哪？"
follow_up:
  - "GQA 的分组数怎么选？—— 通常选 n_heads/4 到 n_heads/8 之间"
  - "MLA 的训练代价是什么？—— 多了压缩/恢复矩阵的参数和计算"
  - "vLLM 支持 MLA 吗？—— 需要 PagedAttention 的适配"
---

# 【美团面经】MLA 是怎么对 KV Cache 做优化的？和 MQA/GQA 相比有什么区别？

**KV Cache 优化方案对比：**

| 方案 | 原理 | KV Cache 压缩率 | 质量损失 |
|------|------|----------------|----------|
| **MHA**（标准） | 每头独立 K/V | 1×（基准） | 无 |
| **MQA** | 所有头共享 1 组 K/V | n_heads× | 较大 |
| **GQA** | 分组共享 K/V（中间态） | n_groups× | 中等 |
| **MLA** | 低秩压缩 + 动态恢复 | ~4-16× | 极小 |

**MLA 具体优化：**
1. **压缩维度** — d_c << n_heads × d_head，只缓存压缩向量
2. **矩阵吸收** — 上投影矩阵 W_UK 可以融合到 Q 的计算中，推理时无需显式恢复 K
3. **质量保持** — 低秩近似的信息损失很小，性能接近 MHA

**MLA vs GQA/MQA 核心区别：**
- GQA/MQA 是**离散共享**（直接让多个头用同一个 K/V）
- MLA 是**连续压缩**（用低秩分解学习最优压缩）
- MLA 更灵活、压缩率更高、质量损失更小
