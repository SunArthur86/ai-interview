---
id: "zp-infra-005"
difficulty: "L4"
category: "ai-harness"
subcategory: "推理优化"
tags:
  - "智谱"
  - "面经"
  - "Speculative Decoding"
  - "投机解码"
  - "PEARL"
  - "EAGLE"
feynman:
  essence: "投机解码 = 小模型先'猜'答案，大模型'批改作业'。猜对的部分免费获得，猜错的部分重做。关键是小模型要猜得准且快。"
  analogy: "就像写作文先列提纲——小模型快速写个草稿（draft），大模型快速扫一眼批改（verify）。大部分内容对了就直接用，错了的地方重新写。整体比一个字一个字写快得多。"
  key_points:
    - "基础：小模型猜 + 大模型验 = lossless 加速"
    - "Medusa：无额外模型，多头并行预测"
    - "EAGLE：复用 target 特征，精度更高"
    - "PEARL：节点级 DT 分离，高 batch 优势"
    - "加速比 1.5-3x，数学无损"
first_principle:
  problem: "大模型自回归推理每次只生成 1 个 token，GPU 利用率低（memory-bound）。如何在不损失精度的前提下利用冗余算力？"
  axioms:
    - "自回归推理是 memory-bound（每步只算 1 token）→ 有计算冗余"
    - "小模型和大模型大部分时候输出一致（尤其简单 token）"
    - "大模型可以一次前向验证多个候选 token（计算量相同）"
  rebuild: "从 GPU 利用率出发：① 为什么每步只算 1 token（KV Cache 依赖）？② 如何利用冗余算力（批量验证）？③ 候选从哪来（draft 模型/多头预测）？④ 如何保证无损（拒绝采样修正）？⑤ 如何进一步提升（树状/并行）？"
follow_up:
  - "投机解码接受率多少才有意义？—— 通常 >50% 才有正向加速（draft 开销不能忽略）"
  - "DFlash 是什么？—— 参考工作，结合 PEARL 思路的改进"
  - "高 batch 下投机解码还有用吗？—— 传统方式没用（batch 已打满计算），但并行投机（PEARL）仍有优势"
---

# 【智谱Infra面经】Speculative Decoding / Medusa / EAGLE / PEARL 在推理加速中的实现细节？并行投机 vs 树状投机？

**投机解码核心思想：用小模型（draft）快速生成候选 token，大模型（target）批量验证，加速推理。**

**基础 Speculative Decoding：**
```
1. Draft 模型生成 γ 个候选 token: [t1, t2, ..., tγ]
2. Target 模型一次前向计算所有 γ+1 个位置
3. 逐个验证：如果 draft 猜对 → 免费获得 token
4. 猜错的 token 之后重新用 target 生成
5. 数学保证：最终输出分布与纯 target 完全一致（lossless）
```

**Medusa（多头并行投机）：**
- 不需要单独的 draft 模型
- 在 target 模型上增加多个 prediction head
- 每个 head 预测下一个 token（head1=+1, head2=+2, ...）
- 一次前向预测多个候选
- **优势**：无需额外模型、无 draft-model 对齐问题

**EAGLE（特征级投机）：**
- Draft 模型复用 target 的隐藏层特征（不是 token embedding）
- 更精确的预测 → 更高的接受率
- 支持树状推测（Tree Attention）
- **接受率 60-80%+**

**PEARL（并行投机解码）：**
- DT 分离（Draft-Target Decoupling）
- Draft 和 Target 在不同节点/设备并行运行
- 节点级并行 → 无串行等待
- 高 batch 下优势大

**并行投机 vs 树状投机：**
| 维度 | 树状投机 | 并行投机 |
|------|---------|---------|
| 结构 | 构建候选 token 树 | Draft/Target 节点分离 |
| 验证 | 树形 attention 一次验证 | 流水线式持续生成验证 |
| 延迟 | 单次前向延迟高 | 持续低延迟 |
| 吞吐 | 低 batch 好 | 高 batch 好 |
| 实现 | Medusa/EAGLE | PEARL/DFlash |
