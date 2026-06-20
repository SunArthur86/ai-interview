---
id: "misc-050"
difficulty: "L2"
category: "ai-basics"
subcategory: "评估与安全"
tags:
  - "Elasticsearch"
feynman:
  essence: "- *Test-Time Compute:** 在推理时增加计算量(更长的思考链)来提升效果,而非增加模型参数. - *核心洞察:** - 传统Scaling"
  analogy: "Test-Time Compute Scaling 就像考试时多想一会儿——不靠考前死记硬背（增加参数），而是在答题时花更多时间推理和验证（更长 CoT/更多采样），想得越深答得越好。"
  key_points:
    - "Test-Time Compute: 在推理时增加计算量(更长的思考链)来提升效果,而非增加模型参数."
    - "传统Scaling Law:训练时增加计算(更多参数/数据)"
    - "新范式: 推理时增加计算(更长的CoT/更多采样)"
first_principle:
  problem: "为什么需要 Test-Time Compute Scaling?为什么说它是推理模型的新范式？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "如何确定最优的推理时计算量?"
  - "Best-of-N的N如何选择?"
---

# Test-Time Compute Scaling是什么?为什么说它是推理模型的新范式

- **Test-Time Compute:** 在推理时增加计算量(更长的思考链)来提升效果,而非增加模型参数.

- **核心洞察:**
- 传统Scaling Law:训练时增加计算(更多参数/数据)
- **新范式:** 推理时增加计算(更长的CoT/更多采样)

- **三种推理时策略:**

1. **更长推理链**
- o1/R1模型:生成数千token的思维链
- 更多推理步 = 更准确的答案

2. **Best-of-N采样**
- 生成N个答案,用奖励模型/投票选最好的
- N越大效果越好(边际递减)

3. **搜索与验证**
- Tree of Thoughts / MCTS
- 搜索多个推理路径,剪枝低质量分支

- **Scaling对比:**
- 14B模型+推理时搜索 > 70B模型+直接输出(部分任务)
- 意味着**小模型可以通过推理计算超越大模型**

- **影响:**
- 推理成本从「固定」变为「可变」
- 需要在效果和延迟/成本之间权衡
