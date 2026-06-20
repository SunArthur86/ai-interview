---
id: zp-infra-005
difficulty: L4
category: ai-harness
subcategory: 推理优化
tags:
- 智谱
- 面经
- Speculative Decoding
- 投机解码
- PEARL
- EAGLE
feynman:
  essence: 用低成本草稿预测并用高质量模型验证，变串行为并行
  analogy: 大师让徒弟先画草图（Draft），大师只需检查并修改错误，比大师从头画快
  first_principle: 如何在不牺牲生成质量的前提下，利用并行计算减少推理延迟？
  key_points:
  - Draft模型生成候选，Target模型并行验证
  - Medusa利用多头输出，EAGLE利用特征层预测
  - Pearl通过节点解耦实现流水线并行
  - 数学保证输出分布与原模型一致
follow_up:
- 投机解码接受率多少才有意义？—— 通常 >50% 才有正向加速（draft 开销不能忽略）
- DFlash 是什么？—— 参考工作，结合 PEARL 思路的改进
- 高 batch 下投机解码还有用吗？—— 传统方式没用（batch 已打满计算），但并行投机（PEARL）仍有优势
---

# 【智谱Infra面经】Speculative Decoding / Medusa / EAGLE / PEARL 在推理加速中的实现细节？并行投机 vs 树状投机？

**投机解码核心思想：用小模型快速生成候选 token，大模型批量验证，加速推理。**

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
- 支持树状推测
- **接受率 60-80%+**

**PEARL（并行投机解码）：**
- DT 分离
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
| 实现 | Medusa/EAGLE | PEARL |
