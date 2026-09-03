# 阶段三：需求访谈 Case 输入改造

## 目标

使复现后的 LLMREI-long 能接受任意软件项目的初始需求描述，同时不改变原方法的访谈策略。

## Case 输入

建议统一为：

```yaml
case_id:
project_name:
initial_requirements:
```

其中真正进入 interviewer 的核心内容是：

`initial_requirements`

## 改造方式

### 1. Project Context

将 `initial_requirements` 放入 LLMREI 的项目背景区域。

如果官方 Prompt 没有明确占位符，则在 renderer 中增加最小上下文块，例如：

```text
Project background:
{initial_requirements}
```

这属于输入适配，而不是方法修改。

### 2. 不做自动扩写

不得根据初始需求额外生成：

- Topic Guide；
- requirement checklist；
- Slot；
- missing requirements；
- 隐藏问题列表。

否则会改变 LLMREI 的方法能力边界。

### 3. Context 长度处理

若输入过长，只允许采用统一、透明的长度控制规则，例如：

- 保留原文；
- 超过模型 context 时进行确定性截断；
- 记录截断行为。

不应使用另一个 LLM 对 Case 自动总结后再作为默认输入，因为这会增加额外方法组件。

## 验收标准

- 任意 Case 只需提供 initial requirements 即可运行；
- 不依赖原论文场景；
- 不需要完整需求文档；
- 不生成额外结构；
- renderer 与官方 Prompt 内容分离。

## 阶段产物

- `case_schema.py`
- `context_renderer.py`
- 3–5 个不同软件 Case smoke tests。

## 下一阶段衔接

下一阶段统一接口与日志，使系统可以被外部程序稳定调用。
