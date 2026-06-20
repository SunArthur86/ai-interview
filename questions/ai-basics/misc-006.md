---
id: "misc-006"
difficulty: "L2"
category: "ai-basics"
subcategory: "大模型原理"
tags:
  - "IOC"
images:
  - "svg_bpe.svg"
feynman:
  essence: "- *BPE (Byte Pair Encoding):** - 从字符级开始,迭代合并最高频字节对 - GPT/GPT-2/GPT-3/LLaMA使用 - *"
  analogy: "三种分词算法就像三种切肉方式——BPE 按频率切（合并高频对，GPT 系）、WordPiece 按似然概率切（BERT）、SentencePiece 不管空格直接在原始文本上切（T5/LLaMA）。"
  key_points:
    - "BPE (Byte Pair Encoding):"
    - "从字符级开始,迭代合并最高频字节对"
    - "GPT/GPT-2/GPT-3/LLaMA使用"
first_principle:
  problem: "它们本质上为什么不同？各自的设计目标和适用场景是什么？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "为什么中文在LLaMA中token效率低?"
  - "如何评估一个Tokenizer的好坏?"
---

# BPE、WordPiece、SentencePiece分词算法有什么区别?为什么大模型多用BPE

- **BPE (Byte Pair Encoding):**
- 从字符级开始,迭代合并最高频字节对
- GPT/GPT-2/GPT-3/LLaMA使用

- **WordPiece:**
- 类似BPE,但使用似然而非频率作为合并标准
- BERT使用

- **SentencePiece:**
- 不依赖空格预处理,直接在原始文本上操作
- 支持BPE和Unigram两种算法
- T5/LLaMA/GLM使用

- **大模型倾向BPE的原因:**
1. **子词覆盖好** - 高频词完整编码,低频词拆为子词
2. **多语言友好** - 不依赖空格分词
3. **编码效率高** - 相同文本token数更少
4. **可逆性** - 任何字节序列都能被编码

- **实际影响:**
- 中文在LLaMA的BPE中通常1字=1-2 token(效率低)
- Qwen/GLM针对中文优化了词表,中文编码效率更高
