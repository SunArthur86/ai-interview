---
id: ai-scen-033
difficulty: L2
category: ai-scenario
subcategory: AI评测与监控
tags:
- LLM-as-Judge
- 自动评测
- 偏差校准
- Pairwise
- Cohen's Kappa
- 评分标准
feynman:
  essence: 用强模型评估弱模型，通过校准偏差实现高效自动化评测。
  analogy: 请资深老师阅卷，但要注意老师偏心，要定期核对他的标准。
  first_principle: 如何用低成本、高效率的方式替代人工进行大规模质量评估？
  key_points:
  - 模式：单题打分、AB对比、参考答案三种模式
  - 纠偏：位置互换、不同模型、人工抽检
  - 指标：用Kappa系数衡量与人工的一致性
  - 成本：CI用小模型，正式测评用大模型
follow_up:
- 如何选择合适的Judge模型？
- LLM-as-Judge的评分如何与人工评分对齐？
- 在什么场景下LLM-as-Judge不可靠？
---

# 如何设计LLM-as-Judge评测管道？用大模型自动评测其他模型的输出质量。

【场景分析】
LLM-as-Judge是用大模型自动评测其他模型输出的方法，可大幅提升评测效率，但有固有偏差。

**实战案例**：在模型选型中，发现GPT-4作为Judge总是倾向于给更长的回答打高分。为了公平对比，我们在Prompt中增加了“惩罚冗余信息，重视简洁性”的指令，并引入基于参考答案的ROUGE分数作为辅助校准，最终消除了长度偏差。

【LLM-as-Judge模式】
1. 单答案评分：
   - 输入：问题 + 答案 + 评分标准
   - 输出：1-5分 + 评分理由
   - Prompt设计：详细的Rubric评分细则
2. 答案对比：
   - 输入：问题 + 答案A + 答案B
   - 输出：A更好/B更好/平手 + 理由
   - 优势：相对评价比绝对评分更稳定
3. 参考对比：
   - 输入：问题 + 答案 + 参考答案
   - 评估：答案与参考答案的语义匹配度

**代码示例（Python：消除位置偏差的Pairwise评测）**
```python
def pairwise_compare(query, answer_a, answer_b, judge_llm):
    prompt_template = """
    Query: {query}
    Answer A: {answer_a}
    Answer B: {answer_b}
    Which is better? Output 'A' or 'B'.
    """
    # 第一轮：A在前
    score_1 = judge_llm.generate(prompt_template.format(query, answer_a, answer_b))
    # 第二轮：交换位置，消除位置偏差
    score_2_swapped = judge_llm.generate(prompt_template.format(query, answer_b, answer_a))
    
    # 如果第一轮选A，第二轮选B（即原A），则A稳健胜出
    if score_1 == 'A' and score_2_swapped == 'B':
        return 'A'
    # 其他不一致情况视为平局或需要人工介入
    return 'Tie'
```

【已知偏差与校准】
1. Position Bias（位置偏差）：
   - 倾向于选择第一个或最后一个答案
   - 校准：交换A/B位置跑两次，取一致结果
2. Verbosity Bias（冗长偏差）：
   - 倾向于给更长的答案高分
   - 校准：在评分标准中明确「简洁性」权重
3. Self-Enhancement Bias（自我增强偏差）：
   - GPT-4评价GPT-4的输出时分数偏高
   - 校准：使用不同供应商的模型作为Judge
4. Domain Bias（领域偏差）：
   - Judge模型在某些领域（如法律、医疗）能力不足
   - 校准：领域专家定期抽检校准

【生产实践】
- Judge模型选择：GPT-4o / Claude-3.5-Sonnet（效果最好但贵）
- 成本优化：日常CI用GPT-4o-mini，正式评测用GPT-4o
- 人工校准：每周抽5%样本人工复核，计算Judge与人工的一致性
- 一致性指标：Cohen's Kappa > 0.6 为可接受
- 持续迭代：将人工修正的评分作为Few-shot示例优化Judge Prompt

**对比表格：Pairwise vs Pointwise**

| 特性 | Pointwise (单答案评分) | Pairwise (对比打分) |
| :--- | :--- | :--- |
| **输入** | 单个模型输出 | 两个模型输出 (A vs B) |
| **输出** | 绝对分数 (如 4.2/5) | 相对偏好 (A更好/B更好) |
| **稳定性** | 较低（受评分标准波动影响大） | 较高（人类更容易判断好坏） |
| **适用场景** | 监控质量趋势、设置阈值 | 模型排序、A/B测试决策 |
| **计算成本** | 1次推理/样本 | 1次推理/样本对 (更低) |
| **局限性** | 难以跨模型比较分数 | 无法给出具体的质量分数 |

## 常见考点
1. **Judge模型的能力边界**：当Judge模型能力弱于被测模型时，会出现什么问题？
   *答案要点*：会出现“由于无法理解高深答案而给出低分”的情况，导致评测结果失真。原则是Judge模型的能力必须显著高于（或至少持平于）被测模型。例如测GPT-4o-mini时，用GPT-4o做Judge。
2. **CoT（思维链）对Judge的影响**：让Judge输出理由是否会提高准确性？
   *答案要点*：通常会提高。CoT强迫Judge先分析对错再给分，减少了直觉性错误。但会大幅增加Token消耗和延迟。优化方案是仅输出关键理由而非冗长分析。
3. **Pairwise vs Pointwise 的选择**：什么时候用对比打分，什么时候用绝对打分？
   *答案要点*：模型选型/排名阶段用Pairwise，因为区分度高，能识别微小的质量差异；回归测试/监控阶段用Pointwise（绝对打分），因为需要监控具体的分数波动趋势，且成本相对较低。
