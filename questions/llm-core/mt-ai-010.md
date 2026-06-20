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
- **核心能力**：代码补全、内联编辑（⌘K）、全项目对话（⌘L）、Agent 模式
- **使用场景**：
  - 快速原型开发（从 0 到 1）
  - 代码重构和迁移
  - Bug 修复和调试
  - 写测试和文档
- **优势**：上下文感知强（读取整个 codebase）、Agent 模式可自动多文件修改
- **劣势**：大型项目 token 消耗大、有时修改不精确

**Windsurf（Codeium）：**
- **核心能力**：Cascade（多步推理编辑）、Flow 模式（理解项目意图）
- **使用场景**：
  - 复杂功能开发（多文件协作）
  - 代码审查和优化建议
  - 从需求到代码的全流程
- **优势**：更注重项目级理解、IDE 集成更深
- **劣势**：社区较小、插件生态不如 Cursor

**Claude Code / Codex CLI：**
- 终端 Agent，可执行命令、读写文件、运行测试
- 适合自动化流水线和 CI/CD

**实践经验总结：**
1. **补全**：Cursor Tab > Copilot（上下文更长）
2. **重构**：Agent 模式多文件修改效率高 10×
3. **调试**：粘贴错误 + 让 AI 分析，快速定位
4. **最佳实践**：描述清楚意图、提供上下文、小步迭代
5. **局限**：复杂业务逻辑仍需人工审查、大型项目上下文窗口限制
