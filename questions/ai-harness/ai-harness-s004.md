---
id: "ai-harness-s004"
difficulty: "L2"
category: "ai-harness"
subcategory: "推理优化"
images:
  - "svg_quantization.svg"
feynman:
  essence: "按使用场景选择部署方案： 1. 云端GPU部署： - vLLM：最高吞吐量，支持PagedAttention - TGI（Text Generation Inf"
  analogy: "Agent 发布就像新药临床试验——先小范围试用（金丝雀），没问题再全量推广（蓝绿切换），随时准备回滚（紧急叫停）。"
  key_points:
    - "vLLM：最高吞吐量，支持PagedAttention"
    - "TGI（Text Generation Inference）：HuggingFace出品"
    - "TensorRT-LLM：NVIDIA出品，极致性能"
first_principle:
  problem: "为什么需要 大模型部署有哪些方案？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Harness Engineering 的核心是工程化——把 LLM 的潜力通过系统设计转化为可靠的生产力"
    - "评测驱动开发——没有 Golden Set 和持续评测，AI 系统就是黑盒"
    - "LLM 应用的可靠性 = 提示工程 + 错误处理 + 降级策略 + 可观测性"
  rebuild: "从工程化出发：① 为什么 LLM 应用需要 Harness？② 可观测性的核心指标？③ 如何做评测和回归？④ 理想的 AI 工程平台是什么样？"
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
