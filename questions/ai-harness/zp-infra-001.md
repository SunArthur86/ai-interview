---
id: zp-infra-001
difficulty: L4
category: ai-harness
subcategory: 推理优化
tags:
- 智谱
- 面经
- 量化
- SmoothQuant
- AWQ
- GPTQ
feynman:
  essence: 通过数学变换或优化算法减少权重量化误差
  analogy: 像把行李里的重物（激活值）均匀分摊到各个箱子（权重）里，方便搬运
  first_principle: 如何在极低比特（4bit/8bit）下保持模型推理精度？
  key_points:
  - SmoothQuant通过缩放平衡激活与权重分布
  - AWQ保留重要权重精度，仅量化次要部分
  - GPTQ利用Hessian二阶信息逐列补偿量化误差
  - 三者目标均为降低W4量化带来的精度损失
follow_up:
- SmoothQuant 为什么能平滑？—— 激活异常值集中在少数 channel，通过缩放因子 s 把激活的异常值'转移'到权重端
- AWQ 和 GPTQ 哪个精度更好？—— 通常 AWQ 略优，因为考虑了激活信息；GPTQ 纯权重补偿更通用
- per-tensor/channel/group 哪个最细？—— group 最细（如 group_size=128），channel 次之，tensor 最粗
---

# 【智谱Infra面经】按照量化粒度说明一下 SmoothQuant、AWQ、GPTQ 分别是什么粒度的？它们的作用流程是什么？

**大模型三大量化算法对比（按粒度）：**

| 算法 | 粒度 | 核心思想 | 激活值处理 |
|------|------|----------|-----------|
| **SmoothQuant** | per-channel / per-tensor | 平滑激活值异常值到权重 | 是（激活感知） |
| **AWQ** | per-group / per-channel | 保护激活感知的显著权重 | 是（activation-aware） |
| **GPTQ** | per-column（逐列） | 基于二阶信息（Hessian）的权重补偿 | 否（仅权重量化） |

**SmoothQuant 流程：**
1. 分析激活值的异常 channel（outlier）
2. 将异常值从激活"迁移"到权重：`W' = W · diag(s), X' = X / diag(s)`
3. 对平滑后的 W' 和 X' 分别做 per-channel/per-tensor INT8 量化
4. **粒度最粗**，但计算最简单，适合 W8A8（权重+激活均量化）

**AWQ 流程：**
1. 用少量校准数据找"显著权重"（对激活大的 channel 的权重）
2. 对显著权重做 per-group 缩放保护（不直接量化）
3. 非显著权重正常 INT4 量化
4. **per-group 粒度**，精度高，适合 W4A16（仅权重量化）

**GPTQ 流程：**
1. 逐列量化权重矩阵
2. 每量化一列后，用 Hessian 矩阵的逆补偿剩余列的误差
3. 类似 OBS（Optimal Brain Surgeon）的贪心算法
4. **per-column 粒度**，精度高，适合 W4A16
