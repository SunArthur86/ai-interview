---
id: "zp-infra-001"
difficulty: "L4"
category: "ai-harness"
subcategory: "推理优化"
tags:
  - "智谱"
  - "面经"
  - "量化"
  - "SmoothQuant"
  - "AWQ"
  - "GPTQ"
feynman:
  essence: "量化 = 把浮点权重压缩成低精度整数。难点是少数'异常值'会拉大量化范围导致精度损失。三个算法用不同策略应对：SmoothQuant 把异常值从激活搬到权重、AWQ 保护重要权重、GPTQ 用二阶信息补偿误差。"
  analogy: "量化像压缩照片——SmoothQuant 是先调整亮度让画面更均匀再压缩；AWQ 是保护人脸区域（重要权重）高质量压缩背景；GPTQ 是逐像素压缩后用周围像素信息补偿误差。"
  key_points:
    - "SmoothQuant：per-channel，激活平滑迁移"
    - "AWQ：per-group，保护显著权重"
    - "GPTQ：per-column，Hessian补偿"
    - "粒度排序：group > channel > tensor"
first_principle:
  problem: "大模型权重分布有长尾（少数 outlier），直接线性量化会导致大部分正常值精度损失。如何选择量化策略和粒度？"
  axioms:
    - "量化误差 ∝ (max - min) / 2^n —— 范围越大误差越大"
    - "激活异常值集中在少数 channel —— 可通过缩放因子迁移"
    - "不同权重列对输出的敏感度不同 —— Hessian 信息可量化敏感度"
  rebuild: "从量化误差来源出发：① 误差怎么产生（outlier 拉大范围）？② 怎么减小范围（分粒度/迁移异常值）？③ 怎么补偿误差（二阶信息/激活感知）？④ 不同粒度的精度-效率 trade-off？"
follow_up:
  - "SmoothQuant 为什么能平滑？—— 激活异常值集中在少数 channel，通过缩放因子 s 把激活的异常值'转移'到权重端"
  - "AWQ 和 GPTQ 哪个精度更好？—— 通常 AWQ 略优，因为考虑了激活信息；GPTQ 纯权重补偿更通用"
  - "per-tensor/channel/group 哪个最细？—— group 最细（如 group_size=128），channel 次之，tensor 最粗"
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
