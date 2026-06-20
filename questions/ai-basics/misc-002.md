---
id: misc-002
difficulty: L2
category: ai-basics
subcategory: 大模型原理
tags:
- IO
- OOM
images:
- svg_rope.svg
feynman:
  essence: 利用旋转矩阵将绝对位置信息转化为相对位置信息，增强长文本外推能力。
  analogy: 在向量空间旋转向量代表位置，像时针转过的角度代表时间差。
  first_principle: 如何在不破坏Self-Attention置换不变性的前提下引入序列顺序？
  key_points:
  - 通过旋转复数向量注入位置信息
  - 本质上关注相对位置而非绝对位置
  - 是目前大模型主流的位置编码方式
follow_up:
- RoPE如何实现长度外推(NTK-aware/YaRN/Dynamic Scaling)?
---

# 主流大模型使用的位置编码有哪些?RoPE的原理和优势是什么

位置编码让Transformer感知token顺序(Self-Attention本身是排列不变的).

- **方案对比:**
| 方案 | 类型 | 外推性 | 代表模型 |
|------|------|--------|----------|
| Sinusoidal | 绝对 | 差 | 原始Transformer |
| Learned PE | 绝对 | 无 | BERT/GPT-2 |
| ALiBi | 相对 | 强 | BLOOM |
| **RoPE** | 相对 | **强** | **LLaMA/Qwen/GLM** |

- **RoPE原理:**
通过旋转矩阵将位置信息编码到Q和K中:
q_m · k_nᵀ = Re((q · R(m))^* · (k · R(n)))
其中R(i)是角度为i·θ的旋转矩阵

- **优势:**
1. 相对位置感知 - 只依赖m-n
2. 长度外推 - 训练4K可推理32K+
3. 计算高效 - 只需矩阵乘法
