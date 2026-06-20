---
id: "misc-047"
difficulty: "L2"
category: "ai-basics"
subcategory: "训练与微调"
tags:
  - "IOC"
feynman:
  essence: "**知识蒸馏:** 用大模型(Teacher)的输出训练小模型(Student)."
  analogy: "大语言模型就像读过整个互联网的学者——通过预测「下一个词」生成文本，积累了海量语言模式和知识。"
  key_points:
    - "知识蒸馏: 用大模型(Teacher)的输出训练小模型(Student)."
    - "软标签 vs 硬标签:"
    - "硬标签: one-hot向量 [0, 0, 1, 0] - 信息量少"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "蒸馏和量化的区别?"
  - "如何选择Teacher模型?"
---

# 知识蒸馏在大模型中如何应用?软标签和硬标签的区别是什么

- **知识蒸馏:** 用大模型(Teacher)的输出训练小模型(Student).

- **软标签 vs 硬标签:**
- **硬标签:** one-hot向量 [0, 0, 1, 0] - 信息量少
- **软标签:** 概率分布 [0.1, 0.05, 0.8, 0.05] - 包含类间关系(dark knowledge)

- **温度参数T:** softmax(logits/T),T越大分布越平滑

- **大模型蒸馏方案:**

1. **输出蒸馏** - Student模仿Teacher的输出分布
- Loss = KL(softmax(z_T/T) || softmax(z_S/T))

2. **CoT蒸馏** - 用Teacher生成的思维链训练Student
- DeepSeek-R1-Distill:R1的推理能力蒸馏到7B/14B/32B

3. **特征蒸馏** - Student模仿Teacher的中间层表示

- **效果:**
- R1-Distill-7B 在AIME上达到55.5%(接近o1-mini的56.4%)
- 小模型+蒸馏可以接近大模型的推理能力
