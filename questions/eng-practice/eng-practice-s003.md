---
id: eng-practice-s003
difficulty: L2
category: eng-practice
subcategory: 工程化实战
images:
- svg_rag.svg
feynman:
  essence: 防止模型生成虚假事实的各种技术手段组合。
  analogy: 让考生开卷考试（RAG），告诉他不会就空着（Prompt约束），考后还要核对答案（后验证）。
  first_principle: 如何约束模型的生成行为，确保其输出内容符合事实真相？
  key_points:
  - 使用RAG提供真实上下文减少编造
  - 通过Prompt指令要求模型不确定时拒答
  - 调整采样温度降低输出的随机性
  - 利用后处理或第二模型进行事实核查
---

# 如何处理LLM的幻觉（Hallucination）问题？

幻觉：LLM生成看似合理但实际不正确的内容。

**原因**：
1. 训练数据中有错误信息
2. 模型过度泛化
3. 缺乏实时知识
4. Prompt不清晰

**解决方案**：

1. **RAG（检索增强生成）**: 提供外部知识来源，让模型有据可依

2. **Prompt工程**:
   - '如果不确定，请回答不知道'
   - '请基于以下上下文回答'
   - 要求引用来源

3. **解码策略**:
   - 降低temperature（减少创造性）
   - 使用更保守的top_p
   - Constrained decoding（限制输出范围）

4. **后处理验证**:
   - 事实核查模型
   - 用另一个LLM验证
   - 与知识库做一致性检查

5. **对齐训练**:
   - RLHF/DPO让模型学会拒绝不确定的问题

6. **工具增强**: 让模型调用搜索/计算器而非编造
