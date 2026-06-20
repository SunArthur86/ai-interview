---
id: xhs-infra-005
difficulty: L4
category: ai-harness
subcategory: 推理与部署
tags:
- 量化
- GPTQ
- AWQ
- FP8
- INT4
- 小红书
feynman:
  essence: 将模型参数从高精度压缩到低精度，减少显存和计算开销。
  analogy: 把高清照片压缩成标清，虽然细节少一点，但省空间且传得快。
  first_principle: 如何在保持模型精度的前提下，极小化参数的存储位宽？
  key_points:
  - GPTQ基于Hessian二阶信息进行权重量化
  - AWQ基于激活值保留1%重要权重不被量化
  - SmoothQuant把激活值的难量化特征迁移到权重上
  - FP8依赖特定硬件（如H100）支持，精度损失最小
follow_up:
- INT4量化对生成质量影响有多大？
- AWQ如何确定哪些权重是「重要」的？
- QAT和PTQ在实际中如何选择？
---

# 模型量化方法对比：GPTQ vs AWQ vs FP8 vs SmoothQuant，各有什么优缺点？

## 主流量化方案对比

| 方法 | 类型 | 精度 | 加速 | 适用场景 |
|------|------|------|------|----------|
| **GPTQ** | 后训练(PTQ) | INT4/8 | 2-3x | 通用，精度损失小 |
| **AWQ** | 后训练(PTQ) | INT4/8 | 2-3x | 激活感知，更稳健 |
| **SmoothQuant** | 后训练(PTQ) | INT8 | 1.5-2x | 激活值异常值处理 |
| **FP8** | 后训练/混合 | FP8(E4M3) | 1.5-2x | H100原生支持 |
| **QAT** | 量化感知训练 | 任意 | 2-3x | 精度最高但需训练 |

## 核心区别
- **GPTQ**：基于二阶信息（Hessian）的逐层量化，最小化量化误差
- **AWQ**：识别「重要权重」（对激活值大的通道），保护这些权重
- **SmoothQuant**：将激活异常值迁移到权重端（数学等价），让权重和激活都好量化
- **FP8**：H100硬件原生支持，无需校准数据，精度损失最小

## 小红书实践
- Diffusion/VLM模型量化需注意生成质量
- 推荐场景INT8足够，AIGC生成可能需要FP8
