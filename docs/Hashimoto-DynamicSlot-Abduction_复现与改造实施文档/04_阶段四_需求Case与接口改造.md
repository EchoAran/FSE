# 阶段四：需求 Case 与接口改造

## 目标

把系统整理成可以接受任意软件需求 Case 的可复用访谈组件。

## Case

建议：

```yaml
case_id:
project_name:
initial_requirements:
```

## 初始化

```text
Fixed RE Initial Slots
        +
Case Initial Requirements
        ↓
Interview State
```

`initial_requirements` 作为背景上下文。

除非后续找到原论文明确说明 self-assessment 会预填 Slot，否则不要自行增加复杂预填算法。

## 推荐接口

```python
class DynamicSlotInterviewer:
    def initialize(self, case):
        ...
    def get_first_question(self):
        ...
    def step(self, interviewee_answer):
        ...
    def export_transcript(self):
        ...
```

## 内部状态

系统内部仍然维护：

- slots；
- abduction history；
- target slots；

这些只服务于方法运行，不额外设计证据导出接口，也不混入对外 transcript。

## 停止

保留原生规则：

- predefined maximum turns；
- slot filling rate > 80%。

同时把最大轮数做成配置项。

## 验收标准

- 不再依赖 nurse-specific input；
- 任意软件 Case 可初始化；
- Initial Slots 不随 Case 改变；
- 内部 state 不作为额外证据输出；
- 原停止逻辑仍可使用。

## 阶段产物

- Case adapter；
- interviewer API；
- config schema。

## 下一阶段衔接

阶段五进行方法忠实性检查，确认改造没有变成新的访谈算法。
