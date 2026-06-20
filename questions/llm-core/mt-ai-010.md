---
id: mt-ai-010
difficulty: L3
category: llm-core
categories:
- eng-practice
- llm-core
subcategory: AI编程
tags:
- 美团
- 面经
- Cursor
- Windsurf
- AI编程
feynman:
  essence: 利用AI Agent通过IDE深度集成实现编程效率革命。
  analogy: 就像带了个极聪明且懂全项目代码的实习生，你写意图，他写代码。
  first_principle: 如何利用LLM的长上下文与代码理解能力，最大程度减少重复编码劳动？
  key_points:
  - Cursor 适合全流程项目级开发
  - Windsurf 擅长多文件协同编辑
  - Agent 模式能自动处理跨文件修改
  - 核心在于提供清晰的上下文和意图
  - 仍需人工审查业务逻辑
follow_up:
- AI 编程会不会取代程序员？—— 不会，但会用 AI 的取代不会用的
- 怎么控制 AI 编程的质量？—— 小步迭代 + 代码审查 + 自动化测试
- Token 成本怎么优化？—— 精准描述需求、减少不必要的上下文、用便宜模型做简单任务
---

# 【美团面经】使用 Cursor、Windsurf 的使用场景和使用情况如何？

**AI 编程工具实战经验：**

**Cursor：**
- **核心能力**：代码补全、内联编辑（⌘K）、全项目对话（⌘L）、Agent 模式（⌘⇧L）、多文件索引
- **使用场景**：
  - 快速原型开发（从 0 到 1）：利用 Agent 快速搭建项目脚手架
  - 代码重构和迁移：如依赖库升级、框架迁移（React -> Vue）
  - Bug 修复和调试：分析报错栈、定位空指针原因
  - 写测试和文档：自动生成 Unit Tests 和 API 文档
- **优势**：上下文感知强（@Codebase 支持语义检索）、Agent 模式可自动多文件修改、Composer 模式支持跨文件连贯修改
- **劣势**：大型 Monorepo 索引慢、Token 消耗大、有时会产生过度重构

**Windsurf（Codeium）：**
- **核心能力**：Cascade（多步推理编辑）、Flow 模式（理解项目意图）、IDE 集成
- **使用场景**：
  - 复杂功能开发（多文件协作）：修改核心数据结构并同步更新所有引用
  - 代码审查和优化建议：提供类似 Code Review 的修改意见
  - 从需求到代码的全流程：Flow 模式下的 long-context 规划
- **优势**：基于 DeepSeek/Codestral 等强模型、IDE 集成更深（无感交互）、对长尾语言支持好
- **劣势**：社区较小、插件生态不如 Cursor、Agent 的自主性略弱于 Cursor Composer

**技术原理架构对比：**

```
┌─────────────────────────────────────────────────────────────────┐
│                      AI IDE 调用链架构                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  User Input  ──┬──>  Context Builder (RAG)                      │
│  (Prompt)      │    - Embedding Search (@Codebase)               │
│                │    - Recent Files Buffer                       │
│                │    - Syntax Tree (AST) Awareness                │
│                │                                                   │
│                ▼                                                   │
│           LLM Inference (GPT-4o / Claude 3.5 Sonnet)             │
│                │                                                   │
│                ├──>  Mode A: Cursor (.cursorrules)               │
│                │    - Agent Loop: Plan -> Action -> Observe      │
│                │    - Use Tools: LSP, File IO, Browser            │
│                │                                                   │
│                └──>  Mode B: Windsurf (Cascade)                  │
│                     - Diff-Based Generation (Apply Edits)        │
│                     - Flow State Management (Project Memory)     │
└─────────────────────────────────────────────────────────────────┘
```

**## 常见考点**
1. **RAG 上下文检索策略**：面试官可能会问如何处理大型 Monorepo 的索引问题（如：如何划分 Chunk？用向量检索还是符号检索？）。
2. **Agent 的 Loop 机制**：追问 Cursor Agent 的“观察-行动-反思”循环具体是如何实现的（例如：如何检测代码错误并自我修正？）。
3. **Diff 应用策略**：Windsurf Cascade 模式中的 Diff 生成是如何保证代码语法正确性的？(基于 AST 的 Patch 还是 Unified Diff)。
4. **.cursorrules**：如何编写高效的 System Prompt 来规范 AI 的代码风格？
