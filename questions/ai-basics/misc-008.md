---
id: misc-008
difficulty: L2
category: ai-basics
subcategory: 大模型原理
tags:
- Elasticsearch
feynman:
  essence: 模型规模突破临界阈值后,小模型不具备的能力突然显现。
  analogy: 水加热到100度突然沸腾,量变引起质变,不到这个度就只是温水。
  first_principle: 模型性能与规模及数据量之间的函数关系是什么?
  key_points:
  - Scaling Law指导:模型越大,性能越好,但有性价比最优解
  - 涌现往往在10B参数以上出现
  - Chinchilla定律:参数量与训练token数约1:20时最优
follow_up:
- Chinchilla最优比例对数据准备有什么指导?
- 涌现能力是真实的还是评估假象?
---

# 大模型的涌现能力(Emergent Abilities)是什么?Scaling Law如何指导模型训练

- **涌现能力:** 模型规模超过某个阈值后突然出现的能力(小模型完全没有)

- **典型涌现能力:**
- 算术推理(多位数加法)
- 符号推理(不规则模式匹配)
- 多步推理
- 指令跟随

- **涌现的临界点:** 通常在10B参数以上

- **Scaling Law (Kaplan et al. 2020):**
Loss ≈ A/N^α + B/D^β + L∞
- N = 参数量, D = 数据量
- 关键发现:**计算预算固定时,大模型+少数据 > 小模型+多数据**

- **Chinchilla最优策略 (DeepMind 2022):**
- 数据量D ≈ 20 × 参数量N
- 即70B模型应训练1.4T tokens
- 很多早期模型(如LLaMA-65B 1.4T tokens)接近最优

- **争议:** 2023年斯坦福研究质疑涌现能力可能是评估指标的假象(非平滑指标导致的阶跃)
