---
id: mt-ai-004
difficulty: L4
category: llm-core
categories:
- eng-practice
- llm-core
subcategory: 推理优化
tags:
- 美团
- 面经
- KV Cache
- 推理优化
feynman:
  essence: MLA通过低秩分解压缩KV，比单纯共享头更高效。
  analogy: MQA/GQA是多人硬挤一张桌子，MLA是把桌子折叠成背包，背着走，更省空间且结构完整。
  first_principle: 除了简单的头共享，是否有一种数学上更优的方式来减少KV Cache的存储冗余？
  key_points:
  - MQA/GQA：离散共享KV头，牺牲部分质量
  - MLA：低秩分解压缩KV，损失极小
  - 优势：压缩率更高，性能接近MHA
  - 核心：矩阵吸收技术加速恢复
follow_up:
- GQA 的分组数怎么选？—— 通常选 n_heads/4 到 n_heads/8 之间
- MLA 的训练代价是什么？—— 多了压缩/恢复矩阵的参数和计算
- vLLM 支持 MLA 吗？—— 需要 PagedAttention 的适配
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
