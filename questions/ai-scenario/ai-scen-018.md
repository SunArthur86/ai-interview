---
id: "ai-scen-018"
difficulty: "L3"
category: "ai-scenario"
subcategory: "AI对话系统设计"
tags:
  - "语音Agent"
  - "ASR"
  - "TTS"
  - "VAD"
  - "实时对话"
  - "打断处理"
  - "端云协同"
feynman:
  essence: "【场景分析】 实时语音Agent是最具挑战的AI系统之一：多模态链路（ASR->LLM->TTS）、低延迟要求、打断处理、状态管理"
  analogy: "AI Agent 就像有自主行动能力的实习生——能理解任务、拆解步骤、使用工具、根据反馈调整。"
  key_points:
    - "音频采集：WebSocket传输音频流（16kHz PCM/Opus）"
    - "VAD（语音活动检测）：Silero VAD检测说话开始/结束"
    - "流式ASR：Whisper-streaming / Paraformer流式版"
first_principle:
  problem: "如果要解决这个问题，最本质的方法论是什么？先理解问题约束，再找最优路径。"
  axioms:
    - "模型本质是数学函数的参数优化——所有能力都来自数据和参数"
    - "质量 > 数量：数据质量决定模型上限，算法决定达到上限的效率"
  rebuild: "从 AI 系统出发：① 核心挑战是什么？② 现有方案如何解决？③ 有哪些 trade-off？④ 如果重新设计你会怎么做？"
follow_up:
  - "如何处理嘈杂环境下的语音识别？"
  - "端侧部署ASR/TTS有哪些技术选型？"
  - "语音Agent如何管理多轮对话的上下文？"
---

# 如何设计一个实时语音AI助手？支持语音输入、实时对话、语音输出，延迟控制在1秒以内。

【场景分析】
实时语音Agent是最具挑战的AI系统之一：多模态链路（ASR->LLM->TTS）、低延迟要求、打断处理、状态管理。

【系统架构】
1. 音频输入处理：
   - 音频采集：WebSocket传输音频流（16kHz PCM/Opus）
   - VAD（语音活动检测）：Silero VAD检测说话开始/结束
   - 流式ASR：Whisper-streaming / Paraformer流式版
   - 延迟优化：分块识别，边说边转
2. 对话推理：
   - LLM流式生成：首Token延迟 < 300ms
   - 上下文管理：多轮对话历史 + 系统人设
   - 工具调用：查天气、设闹钟等
3. 语音合成（TTS）：
   - 流式TTS：逐句合成，不等完整回复
   - 模型：CosyVoice / GPT-SoVITS / Edge-TTS
   - 声纹克隆：可选个性化音色
4. 音频输出：
   - 流式播放：边合成边播放
   - 打断处理：检测到用户说话 → 立即停止播放

【延迟拆解】
VAD判断 50ms + ASR转写 200ms + LLM首字 300ms + TTS首包 200ms + 网络传输 100ms = 总计约850ms

【状态机设计】
States: IDLE -> LISTENING -> THINKING -> SPEAKING -> IDLE
用户打断: SPEAKING -> INTERRUPTED -> LISTENING
- LISTENING：VAD检测到语音 → 流式ASR
- THINKING：ASR完成 → LLM流式生成
- SPEAKING：TTS流式合成 + 播放
- INTERRUPTED：用户打断 → 停止播放 → 回到LISTENING

【打断处理】
1. 停止TTS播放
2. 取消LLM推理（节省Token）
3. 保留已播放内容到上下文
4. 开始处理新的用户输入

【端云协同方案】
- 端侧：VAD + 轻量ASR（快速响应）
- 云端：大模型推理 + TTS
- 混合：简单指令端侧处理，复杂对话云端处理
