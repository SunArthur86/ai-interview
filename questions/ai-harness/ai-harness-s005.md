---
id: "ai-harness-s005"
difficulty: "L3"
category: "ai-harness"
subcategory: "推理优化"
images:
  - "svg_kvcache.svg"
feynman:
  essence: "KV Cache是LLM推理的主要显存开销（可达总显存的80%+）： 1. PagedAttention（vLLM）： - 分块管理KV Cache - 消除内"
  analogy: "语义缓存就像客服知识库——相似的问题不用每次重新查（LLM推理），直接从历史回答中找最相似的复用，省钱又快。"
  key_points:
    - "PagedAttention（vLLM）："
    - "分块管理KV Cache"
    - "MQA极端减少（1个KV头）"
first_principle:
  problem: "从第一性原理看：LLM中的KV Cache如何优化 的根本优势/劣势来源于什么？"
  axioms:
    - "Harness Engineering 的核心是工程化——把 LLM 的潜力通过系统设计转化为可靠的生产力"
    - "评测驱动开发——没有 Golden Set 和持续评测，AI 系统就是黑盒"
    - "LLM 应用的可靠性 = 提示工程 + 错误处理 + 降级策略 + 可观测性"
  rebuild: "从工程化出发：① 为什么 LLM 应用需要 Harness？② 可观测性的核心指标？③ 如何做评测和回归？④ 理想的 AI 工程平台是什么样？"
---

# LLM中的KV Cache如何优化？

KV Cache是LLM推理的主要显存开销（可达总显存的80%+）：

1. PagedAttention（vLLM）：
- 分块管理KV Cache
- 消除内部碎片
- 按需分配

2. GQA/MQA：
- 减少KV的头数
- MQA极端减少（1个KV头）
- GQA折中（如Llama3-8B用8个KV头vs32个Q头）

3. KV Cache量化：
- FP16 → INT8：减少50%内存
- KV Cache INT4量化：减少75%

4. Sliding Window Attention：
- 只保留最近W个token的KV Cache
- 超出窗口的丢弃（如Mistral用4096窗口）

5. KV Cache Offloading：
- 将不活跃的KV Cache移到CPU内存
- 需要时再加载回GPU

6. Prefix Sharing：
- 多请求共享相同system prompt的KV Cache
