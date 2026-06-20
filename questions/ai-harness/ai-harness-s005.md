---
id: ai-harness-s005
difficulty: L3
category: ai-harness
subcategory: 推理优化
images:
- svg_kvcache.svg
feynman:
  essence: 通过分块、量化、共享和裁剪手段压缩KV Cache显存占用。
  analogy: 做笔记：只记重点(GQA)、用缩写(量化)、撕掉旧页、共用开头。
  first_principle: 如何在不显著影响模型效果的前提下，最大程度减少推理过程中的显存占用？
  key_points:
  - PagedAttention解决显存碎片和浪费问题
  - GQA/MQA通过减少KV头数大幅降低显存占用
  - 量化将FP16降至INT8/4，显著节省内存
  - 滑动窗口和Offloading进一步处理长序列低频数据
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
