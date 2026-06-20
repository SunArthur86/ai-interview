---
id: "bd-ai-003"
difficulty: "L4"
category: "llm-core"
categories:
  - "ai-agent"
  - "eng-practice"
  - "llm-core"
subcategory: "AI编程"
tags:
  - "字节跳动"
  - "面经"
  - "MCP"
  - "Skills"
  - "Tools"
  - "Function Calling"
feynman:
  essence: "Tools是原子函数调用，Skills是能力封装（Prompt+工具+流程），MCP是标准化的工具服务通信协议。三者从底到顶：MCP/Tools → Skill → Agent。"
  analogy: "Tools像单个螺丝刀（一个函数一个工具），Skill像一本操作手册（教你怎么用一组工具完成一个任务），MCP像一个USB标准（让任何设备都能接任何电脑）。"
  key_points:
    - "Tools：原子函数，Function Calling，粒度最细"
    - "Skills：Prompt+工具+流程的高阶封装"
    - "MCP：标准化Agent与工具服务通信的协议"
    - "选型：简单用Tools，复用用MCP，业务用Skill"
    - "MCP生态爆发中，一次开发多Agent消费"
first_principle:
  problem: "Agent为什么需要不同层级的工具抽象？统一成一种不行吗？"
  axioms:
    - "LLM的上下文窗口有限——太多Tool定义会挤占上下文且降低选择准确率"
    - "工具复用是工程效率的核心——同一个DB查询不应在每个Agent里重写"
    - "协议标准化是生态繁荣的前提——USB之所以成功是因为统一了接口"
  rebuild: "从Agent需要扩展能力的根本需求出发：① 原子操作怎么定义？（Tools）② 怎么跨Agent复用？（MCP标准化协议）③ 复杂业务怎么封装？（Skill打包Prompt+流程）三层抽象分别解决：粒度控制、复用效率、业务建模。"
follow_up:
  - "MCP和传统的API有什么区别？—— MCP是专为LLM设计的协议，包含语义描述和上下文管理，API只管数据传输"
  - "一个MCP Server怎么开发？—— 用TypeScript/Python SDK，实现tools/resources/prompts三个handler，stdio或SSE传输"
  - "Skill能跨Agent平台使用吗？—— 目前不行，各平台Skill格式不同，MCP正在尝试标准化Skill层"
---

# 【字节面经】Skills、Tools、MCP三者的区别是什么？如果自己实现工具服务，选哪种方案？

这三个概念是当前AI Agent生态中最核心的工具能力抽象，但经常被混淆。以下从定义、抽象层级、适用场景三个维度深度拆解。

**1. Tools（工具/Function Calling）**
- **定义：** Agent可直接调用的原子函数，通过JSON Schema声明参数
- **抽象层级：** 最低层——一个函数定义就是一个Tool
- **标准：** OpenAI Function Calling、Anthropic Tool Use
```python
# Tool 定义示例
tools = [{
    "name": "get_weather",
    "description": "获取指定城市的天气",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string"}
        },
        "required": ["city"]
    }
}]
```
- **特点：** 每次调用需要LLM推理选择工具+参数，粒度细，灵活但管理开销大

**2. Skills（技能）**
- **定义：** 封装了Prompt模板+工具链+执行流程的高阶能力包
- **抽象层级：** 最高层——一个Skill可能内部编排多个Tools
- **代表：** Claude Code Skills、Hermes Skills、Semantic Kernel
```
# Skill = Prompt模板 + 工具编排 + 约束
Skill: "代码审查"
  Prompt: "审查以下代码的安全性、性能、可读性..."
  Tools: [read_file, search_code, run_linter]
  Flow: 读代码 → 静态分析 → 生成报告
```
- **特点：** 可复用、可分享、可组合，面向"能力"而非"函数"

**3. MCP (Model Context Protocol)**
- **定义：** Anthropic提出的开放协议，标准化Agent与外部数据/工具服务之间的通信
- **抽象层级：** 中间层——是"传输协议+服务发现"标准
- **架构：**
```
Agent (MCP Client) ↔ MCP Protocol (JSON-RPC) ↔ MCP Server (工具/资源)
                                                    ├── PostgreSQL MCP
                                                    ├── GitHub MCP
                                                    ├── Filesystem MCP
                                                    └── 自定义MCP Server
```
- **核心能力：** Tools（工具调用）、Resources（数据读取）、Prompts（提示模板）
- **特点：** 解耦Agent和工具——一次开发MCP Server，所有支持MCP的Agent都能用

**三者关系：**
```
Skill（最高层能力封装）
  └─ 内部编排多个...
MCP Server / Tools（中层/底层工具）
  └─ 通过MCP协议暴露给...
Agent（消费方）
```

**自实现工具服务选型建议：**

| 场景 | 推荐方案 | 理由 |
|------|---------|------|
| 单Agent简单工具 | 直接用Tools/Function Calling | 开销最小，无需额外服务 |
| 多Agent共享工具 | MCP Server | 一次开发多Agent复用，协议标准化 |
| 复杂业务流程封装 | Skill | 把Prompt+工具+流程打包成可复用能力 |
| 企业内部工具平台 | MCP Server + Skill组合 | MCP做工具层，Skill做业务编排层 |

**我的实践选择：** 如果是自用/小团队，优先MCP——因为生态在快速增长（已有100+ MCP Server），写一个MCP Server就能被Claude Code/Cursor/Hermes等多个Agent消费，ROI最高。Skill适合把领域经验（如"如何做代码安全审计"）固化成可分享的能力包。
