---
id: "bd-ai-006"
difficulty: "L3"
category: "llm-core"
categories:
  - "ai-agent"
  - "eng-practice"
  - "llm-core"
subcategory: "Agent核心框架"
tags:
  - "字节跳动"
  - "面经"
  - "Agent"
  - "工具调用"
  - "规划"
  - "ReAct"
feynman:
  essence: "Agent自主运行的本质是一个\"思考-行动-观察\"的循环——每一步都基于当前状态选择最优行动，观察结果后再决定下一步，直到任务完成。"
  analogy: "就像一个侦探破案——先理解案情（感知），制定调查计划（规划），逐个线索追踪（行动+观察），每次发现新线索就调整方向（决策循环），直到破案（任务完成）。"
  key_points:
    - "核心闭环：感知→规划→行动→观察→决策"
    - "ReAct模式：推理与行动交错进行"
    - "知识通过RAG按需注入，不是全量预加载"
    - "工具原子化+JSON Schema严格定义"
    - "迭代上限+异常恢复保证鲁棒性"
first_principle:
  problem: "为什么Agent需要\"工具+知识+规划\"三者结合？缺一个不行吗？"
  axioms:
    - "LLM本身是静态的——训练后知识不更新，需要工具获取实时信息"
    - "LLM的推理是隐式的——复杂任务需要显式规划才能保证执行质量"
    - "LLM缺乏领域深度——通用知识需要通过RAG补充专业知识"
    - "自主性=感知+决策+行动的闭环——缺任何一环都不构成Agent"
  rebuild: "从\"自主解决问题\"的目标出发：① 需要获取信息（→工具）② 需要领域知识（→RAG）③ 需要分解复杂任务（→规划）④ 需要根据反馈调整（→观察+决策循环）。三者结合才能实现真正的自主性。"
follow_up:
  - "ReAct和Plan-and-Execute的区别？—— ReAct是边想边做（交错推理），Plan-and-Execute是先规划后执行（串行）"
  - "Agent怎么知道任务完成了？—— LLM判断 + 终止条件（如产出包含最终答案格式/达到目标）"
  - "工具调用失败后怎么恢复？—— 错误信息返回给LLM，让其重新选择工具或调整参数"
---

# 【字节面经】Agent如何结合工具、知识、规划实现自主运行？请设计一个完整的执行链路。

Agent自主运行的核心是"感知→规划→行动→观察"的闭环（Perception-Planning-Action-Observation Loop）。以下从架构设计到代码实现进行完整拆解。

**核心架构：ReAct + 工具增强**

```
用户输入
    ↓
[感知层] 意图理解 + 上下文组装
    ↓
[规划层] 任务分解 → 子目标序列
    ↓
┌──→ [行动层] 选择工具 + 参数生成
│         ↓
│    [执行层] 工具调用 → 获取结果
│         ↓
│    [观察层] 结果解析 + 状态更新
│         ↓
│    [决策层] 是否完成？→ 否 → 回到行动层
│                  → 是 → 输出最终答案
└────────────────────────────────┘
```

**1. 感知层 — 上下文组装**
```python
def build_context(user_input, memory, knowledge_base):
    context = {
        "user_query": user_input,
        "conversation_history": memory.get_recent(n=10),
        "relevant_knowledge": knowledge_base.retrieve(user_input, top_k=5),
        "available_tools": get_tool_schemas(),
        "system_prompt": AGENT_SYSTEM_PROMPT
    }
    return context
```

**2. 规划层 — 任务分解**
对于复杂任务，先做ReWOO（Reasoning Without Observation）式的规划：
```python
# 规划Prompt示例
planning_prompt = """
用户需求：{user_query}
可用工具：{tools}
请将任务分解为2-5个子步骤，每个步骤说明：
1. 使用哪个工具
2. 需要什么参数
3. 预期得到什么信息
不要执行，只规划。
"""
# 输出示例
plan = [
    {"step": 1, "tool": "search_api", "params": {"q": "竞品分析"}, "expect": "竞品列表"},
    {"step": 2, "tool": "web_scraper", "params": {"url": "..."}, "expect": "竞品详情"},
    {"step": 3, "tool": "data_analyzer", "params": {}, "expect": "对比分析"}
]
```

**3. 行动层 — 工具选择与调用（ReAct Loop）**
```python
def react_loop(query, tools, max_iterations=10):
    messages = [{"role": "user", "content": query}]
    
    for i in range(max_iterations):
        # LLM推理：选择工具 or 给出最终答案
        response = llm.chat(
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        # 如果LLM选择调用工具
        if response.tool_calls:
            for tool_call in response.tool_calls:
                # 执行工具
                result = execute_tool(tool_call.name, tool_call.arguments)
                # 观察结果加入上下文
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
        else:
            # LLM认为任务完成，返回最终答案
            return response.content
    
    return "达到最大迭代次数，任务未完成"
```

**4. 知识增强 — RAG融合**
```python
def knowledge_augmented_agent(query):
    # Step1: 检索相关知识
    docs = vector_store.similarity_search(query, k=5)
    knowledge = rerank(docs, query, top_k=3)
    
    # Step2: 注入到Agent上下文
    augmented_query = f"""
    相关知识：{knowledge}
    
    用户问题：{query}
    """
    
    # Step3: 正常Agent执行
    return react_loop(augmented_query, tools)
```

**5. 异常处理与恢复**
```python
def robust_tool_execution(tool_name, params):
    try:
        result = execute_tool(tool_name, params)
        # 结果验证
        if validate_result(result, expected_schema):
            return result
        else:
            return {"error": "结果格式异常", "raw": result}
    except TimeoutError:
        return {"error": "工具超时", "retry": True}
    except Exception as e:
        return {"error": str(e)}
```

**设计要点总结：**
1. **工具设计原子化** — 每个工具做一件事，参数用JSON Schema严格定义
2. **规划与执行分离** — 复杂任务先规划再执行，简单任务直接ReAct
3. **知识按需注入** — 不要把所有知识塞进System Prompt，用RAG动态检索
4. **迭代有上限** — max_iterations防止死循环，超出则人工介入
5. **结果可验证** — 每步执行后验证结果，异常时让LLM重新规划
