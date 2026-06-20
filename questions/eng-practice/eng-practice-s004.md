---
id: eng-practice-s004
difficulty: L2
category: eng-practice
subcategory: 工程化实战
images:
- svg_quantization.svg
feynman:
  essence: 通过模型路由、缓存和上下文压缩等手段降低AI运行开销。
  analogy: 像省油驾驶：市区用小排量车（小模型），走熟路不查地图（缓存），少带不必要的行李（精简Prompt）。
  first_principle: 如何在保证模型效果的前提下，最大化降低推理与交互的计算资源成本？
  key_points:
  - 根据任务难度路由选择不同大小的模型
  - 利用语义缓存避免重复计算
  - 压缩历史上下文减少Token输入
  - 高频场景考虑自建或量化部署
---

# LLM应用的token成本如何优化？

Token成本是LLM应用的主要运营成本。

1. **模型选择**：
   - 简单任务用小模型（GPT-3.5/GLM-4-Flash）
   - 复杂任务才用大模型（GPT-4/Claude）
   - 路由策略：用小模型判断难度，分流到不同模型

2. **Prompt优化**：
   - 精简system prompt
   - 压缩对话历史
   - 使用摘要替代完整历史

3. **缓存策略**：
   - Semantic Cache：相同/相似问题命中缓存
   - Prompt Caching（API层）：前缀缓存

4. **批量处理**：
   - Batch API（OpenAI Batch）：50%折扣

5. **上下文管理**：
   - RAG减少不必要的context
   - 动态截断

6. **自建部署**：
   - 高频使用时自建模型更便宜
   - 用vLLM+量化
