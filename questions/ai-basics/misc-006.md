---
id: misc-006
difficulty: L2
category: ai-basics
subcategory: 大模型原理
tags:
- IOC
images:
- svg_bpe.svg
feynman:
  essence: 通过统计频率迭代合并字符对,构建平衡词表以高效压缩文本。
  analogy: 积木拼词,常用词做成整块大积木,生僻词用小积木拼,省材料。
  first_principle: 如何将文本切分成既不泛滥也不过碎的合理单元?
  key_points:
  - BPE看频率合并,WordPiece看似然合并
  - SentencePiece把空格当字符处理,语言通用性强
  - 大模型选它是为了平衡词表大小和编码效率
follow_up:
- 为什么中文在LLaMA中token效率低?
- 如何评估一个Tokenizer的好坏?
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
