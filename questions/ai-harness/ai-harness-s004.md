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

1. **云端GPU部署：**
- vLLM：最高吞吐量，支持PagedAttention
- TGI（Text Generation Inference）：HuggingFace出品
- TensorRT-LLM：NVIDIA出品，极致性能
- SGLang：结构化生成+RadixAttention

2. **边缘/本地部署：**
- Ollama：一键部署，适合个人使用
- llama.cpp：CPU/GPU混合推理，GGUF量化
- LM Studio：桌面GUI

3. **API服务：**
- OpenAI API、Anthropic API、通义千问API
- 无需GPU，按token付费

4. **私有化部署关键考虑：**
- GPU显存：模型大小 × 2 + KV Cache + 框架开销
- 吞吐量：QPS需求
- 延迟：TTFT和TPOT要求
- 并发数：continuous batching

推荐：生产环境用vLLM + AWQ量化，个人用Ollama。

- **补充：推理架构选型决策树**
- **追求极致吞吐**: TensorRT-LLM (需编译，部署周期长)。
- **快速迭代/兼容性好**: vLLM 或 TGI (支持 HuggingFace 模型直接加载)。
- **多模态/复杂控制流**: SGLang (支持 RadixAttention 和复杂的并发原语)。
- **显存受限**: llama.cpp (支持 GGUF 4bit/5bit 量化，CPU 推理兜底)。

### 实战案例
在高并发客服场景下，直接使用 vLLM 默认配置曾导致长请求占满显存阻塞短请求（Head-of-Line Blocking）。实战中通过开启 `max_num_seqs` 限制并精细化调整 `gpu_memory_utilization` 为 0.9，配合 Prefix Caching 解决了该问题。

### 推理框架对比
| 特性 | vLLM | TGI (Text Generation Inference) | TensorRT-LLM | llama.cpp |
| :--- | :--- | :--- | :--- | :--- |
| **核心优势** | PagedAttention，高吞吐 | HF 生态集成，安全性高 | 极致性能，CUDA Kernel 优化 | 极低资源消耗，量化支持好 |
| **部署难度** | 低（Python 直接调用） | 中（Docker 容器化） | 高（需 C++ 编译 Engine） | 极低（二进制运行） |
| **量化支持** | AWQ, GPTQ, BitsAndBytes | bitsandbytes, exl2 | FP8, INT4, INT8 | GGUF (Q2_K ~ Q8_0)
|
**适用硬件** | NVIDIA GPU 优先 | NVIDIA GPU | NVIDIA GPU (H100/A100 佳) | CPU (x86/ARM/Apple) + GPU |
| **最佳场景** | 通用高并发推理 | 企业级，需鉴权/审计 | 极低延迟，大规模生产 | 端侧设备，个人电脑 |

### 代码示例 (vLLM 离线推理)
```python
from vllm import LLM, SamplingParams

# 初始化模型，开启量化加载（需提前安装对应量化库）
llm = LLM(model="TheBloke/Llama-2-7b-AWQ", quantization="awq")

# 配置采样参数
sampling_params = SamplingParams(temperature=0.7, top_p=0.95, max_tokens=100)

# 批量推理
prompts = ["Hello, my name is", "The future of AI is"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Prompt: {output.prompt!r}, Generated text: {output.outputs[0].text!r}")
```

## 常见考点
1. **vLLM 和 TGI 如何选择？**
   - vLLM 吞吐通常更高，PagedAttention 优势明显；TGI 集成 HF 生态更好，对最新模型支持较快，且安全性增强功能较多。
2. **AWQ 和 GPTQ 量化的区别？**
   - AWQ (Activation-aware Weight Quantization) 仅量化权重，激活值保持精度，推理速度通常比 GPTQ 快且精度略高，是 vLLM 推荐方案。
3. **TensorRT-LLM 的主要优势是什么？**
   - 利用 NVIDIA GPU 的 Tensor Core 和 FP8 优化，推理性能通常是 SOTA，但模型构建耗时较长。
