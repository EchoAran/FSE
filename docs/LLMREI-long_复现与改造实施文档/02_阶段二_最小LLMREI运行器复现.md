# 阶段二：最小 LLMREI 运行器复现

## 目标

实现能够独立执行 LLMREI-long 的最小系统。

## 最小架构

```text
Project Context
      +
Official Long Prompt
      +
Conversation History
      ↓
      LLM
      ↓
Next Interviewer Question
```

## 需要实现

### 1. Prompt loader

从 `vendor/long_prompt.txt` 读取官方 Prompt，不在代码中复制一份可漂移版本。

### 2. Context renderer

负责把当前项目背景放入 Prompt。

该层只能做变量填充，不增加新的访谈规则。

### 3. Conversation history

采用简单 message sequence：

```python
[
    {"role": "interviewer", "content": "..."},
    {"role": "interviewee", "content": "..."}
]
```

### 4. LLM client

独立封装：

```python
generate(system_prompt, messages, model_config)
```

### 5. Runner

```python
initialize(project_context)
ask_first_question()
step(interviewee_answer)
```

## 推荐结构

```text
src/
├── runner.py
├── prompt_loader.py
├── context_renderer.py
├── model_client.py
└── transcript.py
```

## 设计约束

runner 不应包含：

- Topic；
- Slot；
- agenda；
- planner；
- question priority；
-显式状态评分。

这些都不是 LLMREI 方法的一部分。

## 验收标准

- 能完成至少 10 轮连续访谈；
- 每个下一问题都由同一个 LLMREI-long Prompt 驱动；
- conversation history 正常累积；
- Prompt 原文件未修改；
- API 异常不会触发另一套访谈策略；
- transcript 可完整保存和恢复。

## 阶段产物

- 最小 runner；
- 一场本地 smoke-test transcript；
- 运行配置文件。

## 下一阶段衔接

下一阶段把通用 project context 替换为软件需求访谈 Case 输入。
