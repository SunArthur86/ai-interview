---
id: ai-harness-s004
difficulty: L2
category: ai-harness
subcategory: 推理优化
images:
- svg_quantization.svg
feynman:
  essence: 根据吞吐、延迟和硬件资源匹配最优推理框架。
  analogy: 跑车拉货选卡车(TensorRT)，买菜选代步车，不想买车就打车。
  first_principle: 如何在不同的硬件环境和业务需求下，选择成本最低且体验最好的模型运行方式？
  key_points:
  - 生产环境高吞吐首选vLLM，追求极致性能选TensorRT-LLM
  - 个人和边缘设备轻量化部署推荐Ollama或llama.cpp
  - API方案适合无算力需求的快速接入
  - 部署需权衡显存容量、并发量和响应延迟
---

# 大模型部署有哪些方案？

按使用场景选择部署方案：

1. 云端GPU部署：
- vLLM：最高吞吐量，支持PagedAttention
- TGI（Text Generation Inference）：HuggingFace出品
- TensorRT-LLM：NVIDIA出品，极致性能
- SGLang：结构化生成+RadixAttention

2. 边缘/本地部署：
- Ollama：一键部署，适合个人使用
- llama.cpp：CPU/GPU混合推理，GGUF量化
- LM Studio：桌面GUI

3. API服务：
- OpenAI API、Anthropic API、通义千问API
- 无需GPU，按token付费

4. 私有化部署关键考虑：
- GPU显存：模型大小 × 2 + KV Cache + 框架开销
- 吞吐量：QPS需求
- 延迟：TTFT和TPOT要求
- 并发数：continuous batching

推荐：生产环境用vLLM + AWQ量化，个人用Ollama。
