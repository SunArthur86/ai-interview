---
id: ai-scen-018
difficulty: L3
category: ai-scenario
subcategory: AI对话系统设计
tags:
- 语音Agent
- ASR
- TTS
- VAD
- 实时对话
- 打断处理
- 端云协同
feynman:
  essence: 构建全链路流式语音处理管道，通过ASR/LLM/TTS并行和状态机管理实现毫秒级响应。
  analogy: 像同声传译，耳朵听进去的同时脑子在转，嘴巴马上说出来，还能随时被打断。
  first_principle: 如何在处理听、想、说三个串行步骤时，将端到端延迟压缩到人类可接受的范围？
  key_points:
  - 采用流式ASR和流式TTS，配合LLM流式生成。
  - 使用VAD检测语音活动，设计状态机管理交互。
  - 打断时立即停止TTS和LLM，保留上下文。
  - 端云协同优化延迟，简单指令端侧执行。
follow_up:
- 如何处理嘈杂环境下的语音识别？
- 端侧部署ASR/TTS有哪些技术选型？
- 语音Agent如何管理多轮对话的上下文？
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
