---
id: "misc-043"
difficulty: "L2"
category: "ai-basics"
subcategory: "评估与安全"
tags:
  - "IO"
feynman:
  essence: "- *AI红队测试:** 模拟攻击者,主动发现模型的安全漏洞. - *常见攻击面:** 1. **越狱(Jailbreak)** - 角色扮演绕过(DAN模式)"
  analogy: "Prompt 就像给 AI 的工作指令——指令越清晰、上下文越充分，AI 完成质量越高。"
  key_points:
    - "AI红队测试: 模拟攻击者,主动发现模型的安全漏洞."
    - "越狱(Jailbreak)"
    - "角色扮演绕过(DAN模式)"
first_principle:
  problem: "为什么需要 AI红队测试(Red Teaming)?常见的攻击面有哪些？如果不存在它会怎样？它解决了什么根本问题？"
  axioms:
    - "Scaling Law：模型能力与参数量、数据量、算力正相关"
    - "Self-Attention 的本质是加权求和——O(n²) 复杂度是并行计算的代价"
    - "位置编码让 Transformer 感知顺序——Self-Attention 本身是排列不变的"
  rebuild: "从数学本质出发：① 这个技术的数学基础是什么？② 为什么这个数学结构有效？③ 工程上如何高效实现？④ 资源约束下如何优化？"
follow_up:
  - "如何防御编码绕过攻击?"
  - "Garak扫描覆盖哪些漏洞类型?"
---

# 什么是AI红队测试(Red Teaming)?常见的攻击面有哪些

- **AI红队测试:** 模拟攻击者,主动发现模型的安全漏洞.

- **常见攻击面:**

1. **越狱(Jailbreak)**
- 角色扮演绕过(DAN模式)
- 编码绕过(Base64/Unicode/低资源语言)
- 多轮逐步引导

2. **Prompt Injection**
- 直接/间接指令注入
- 参见basics-035

3. **数据投毒(Data Poisoning)**
- 在训练数据中植入后门
- 微调攻击

4. **模型窃取**
- 大量API调用蒸馏小模型
- 探测模型参数

5. **隐私泄露**
- 训练数据提取攻击
- 成员推断攻击

- **红队工具:** Garak(开源LLM漏洞扫描)、PyRIT(微软)、PAIR(自动越狱)
