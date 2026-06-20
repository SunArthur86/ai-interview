---
id: "misc-049"
difficulty: "L2"
category: "ai-basics"
subcategory: "评估与安全"
feynman:
  essence: "- *Lost in the Middle现象:** 模型对prompt中间位置的信息关注不足,注意力集中在开头和结尾. - *实验证据:** - 将关键信息放"
  analogy: "大语言模型就像读过整个互联网的学者——通过预测「下一个词」生成文本，积累了海量语言模式和知识。"
  key_points:
    - "Lost in the Middle现象:"
    - "将关键信息放在不同位置测试"
    - "开头和结尾的准确率明显高于中间"
first_principle:
  problem: "追根溯源：为什么LLM存在「Lost in the Middle」问题?如何缓解 的根本原因是什么？背后的设计哲学是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "Naive RAG vs RAG-Fusion如何处理长上下文?"
  - "为什么注意力会集中在开头和结尾?"
---

# 为什么LLM存在「Lost in the Middle」问题?如何缓解

- **Lost in the Middle现象:**

模型对prompt中间位置的信息关注不足,注意力集中在开头和结尾.

- **实验证据:**
- 将关键信息放在不同位置测试
- 开头和结尾的准确率明显高于中间
- 即使上下文窗口足够大也会出现

- **缓解策略:**

1. **重排(Reorder)**
- 将最相关的文档放在开头和结尾
- 中间放次要文档

2. **文档压缩**
- 对长文档先做摘要
- 减少中间冗余内容

3. **地图-减少(Map-Reduce)**
- 将文档分批处理
- 每批生成摘要
- 最后合并摘要

4. **结构化Prompt**
- 用编号列表帮助模型定位信息
- 关键信息用标记强调(<important>...</important>)

5. **长上下文微调**
- 在长文本数据上微调模型
