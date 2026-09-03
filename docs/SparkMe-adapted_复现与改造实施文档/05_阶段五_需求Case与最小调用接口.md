# 阶段五：需求 Case 与最小调用接口

## 目标

在不重写 SparkMe 方法的前提下，为外部程序提供清晰的需求访谈调用边界。

## 1. Case 输入

最小 Case 包含：

```yaml
case_id:
project_name:
initial_requirements:
```

- `case_id`：调用方用于区分访谈；
- `project_name`：访谈中的项目称谓；
- `initial_requirements`：已有背景、问题陈述或初步需求。

不接收 synthetic profile、ground truth、profession、participant condition 或 evaluation label。

## 2. 对外行为

对外接口至少支持：

1. 使用 Case 初始化会话；
2. 获取首个访谈问题；
3. 提交一条真实受访者回答并获得下一问题；
4. 查询是否结束；
5. 导出公共 Transcript。

接口应是官方 `InterviewSession` 的薄适配层。Agenda、Agent 调度、rollout 和 utility 仍由原方法模块执行，不能在 adapter 中复制一套逻辑。

## 3. 回答提交语义

删除 Dummy Participant 后，回答应通过明确的方法直接写入会话消息流，并触发与官方方法一致的订阅关系：

```text
stakeholder answer
    → Interviewer
    → Agenda Manager
    → Exploration Planner
```

需要保证：

- 同一回答只提交一次；
- 下一问题只有在本轮方法处理成功后对外返回；
- 内置 Interviewer、Agenda Manager 或 Exploration Planner 在本轮异常时，取消尚未完成的本轮并发任务；
- 在现有 SparkMe 会话对象范围内恢复本轮开始前的 chat history、Agenda、Memory、Question Bank 和 Planner 领域状态，使同一回答可以重新提交且不产生重复 Turn。

上述保证是针对当前保留方法组件的会话内有限回滚，不是通用 ACID 事务。它不覆盖后续任意扩展的 Agent 或工具、外部 API 已产生的副作用、进程崩溃和跨进程恢复。若回滚过程本身失败，当前会话状态视为不可信，调用方应终止该会话并重新使用 Case 初始化，而不是继续原地重试。

## 4. 公共 Transcript

公共 Transcript 只保存正常使用所需内容：

- Case 标识与项目名；
- initial requirements；
- 按顺序排列的 interviewer question 与 stakeholder answer；
- 正常结束状态。

不输出：

- Prompt；
- 模型思考或 rollout 详情；
- utility 中间量；
- evaluation 分数；
- 来源、commit、Prompt 哈希、配置快照或版本证据；
- simulated participant profile。

Agenda、notes、coverage、emergent subtopics 和 strategic state 是方法内部状态。保留正常结束会话时所需的内部持久化，但不伪装成公共 Transcript 或证据包。本阶段不新增每轮持久化检查点、Checkpoint/Resume API 或跨进程无损恢复能力。

## 5. 运行配置

只保留实际被源码读取且影响正常运行的设置：

- 使用的模型与 Embedding backend；
- Topic Guide 和 context 路径；
- planner 触发频率、rollout 数、horizon 和 utility 权重；
- 可选的会话长度上限；默认不设 turn cap，由官方 topic completion 或用户结束会话；
- 正常运行所需目录。

删除论文实验模式、baseline 模式、模拟用户 profile 路径和离线评价配置。不要为了“可追溯”额外保存每场访谈配置副本。

## 验收标准

- 任意合法 Case 可初始化；
- initial requirements 对三个 Agent 可见；
- 真实回答无需 UserAgent 或 DummyParticipant 即可驱动完整方法链；
- adapter 不包含 planner、coverage 或 emergence 的复制实现；
- Transcript 契约最小且不泄漏内部规划和证据元数据；
- 无效输入和内置方法组件失败具有明确行为；有限回滚成功后允许重试，回滚失败时明确终止当前会话。

## 阶段产物

- Case 数据模型；
- SparkMe RE 薄适配接口；
- 公共 Transcript 导出；
- 最小文本示例入口。
