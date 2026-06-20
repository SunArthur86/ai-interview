---
id: zp-infra-002
difficulty: L4
category: ai-harness
subcategory: 推理优化
tags:
- 智谱
- 面经
- 量化
- 校准
- MinMax
- Percentile
feynman:
  essence: 确定量化映射的截断范围以最小化信息损失
  analogy: 像拍照调光圈，MinMax怕过曝（异常值），Percentile则裁掉极亮背景
  first_principle: 如何确定浮点数到整数的映射范围最合理？
  key_points:
  - MinMax取绝对最大值，对异常值敏感
  - Percentile按比例截断异常值，鲁棒性强
  - KL散度通过最小化分布差异寻找最优阈值
  - MSE直接优化量化前后的数值误差
follow_up:
- 为什么不用 mean±3σ？—— 大模型激活不一定是高斯分布，可能有重尾
- KL 散度校准具体怎么做？—— 构建参考分布和量化分布的直方图，逐 bin 计算散度
- 校准数据量需要多少？—— 通常 128~512 个样本即可
---

# 【智谱Infra面经】简述 MinMax 和 Percentile 校准算法有什么不同？还知道什么其他校准算法？

**量化校准算法对比：**

**MinMax 校准：**
- 原理：直接取激活值的绝对最大值作为量化范围
- `scale = max(|X|) / 127`（INT8）
- 优点：简单快速
- 缺点：对异常值极度敏感——一个 outlier 就会拉大整个范围
- 适用：分布均匀的权重/激活

**Percentile 校准：**
- 原理：取激活值分布的百分位数（如 99.9%）作为量化范围
- 丢弃极少数 outlier（0.1%），保留 99.9% 的数据在量化范围内
- 优点：对异常值鲁棒
- 缺点：需要排序，计算量略大；可能截断少量信息
- 适用：有长尾分布的激活值（大模型常见）

**其他校准算法：**

1. **KL 散度校准**
   - 目标：找到量化分布与原始分布 KL 散度最小的截断点
   - TensorRT 默认使用此方法
   - 原理：遍历不同截断阈值，计算量化前后分布的 KL 散度，选最小值
   - 优点：理论上最优的信息保留

2. **MSE（均方误差）校准**
   - 目标：找到使量化前后 MSE 最小的截断阈值
   - 原理：网格搜索不同阈值，计算量化前后输出的 MSE
   - 优点：直接优化输出误差
   - 缺点：计算量大

3. **ACIQ（Analytical Clipping for Integer Quantization）**
   - 基于分析公式直接计算最优裁剪点
   - 假设激活服从特定分布（如 Laplace/Gaussian）
