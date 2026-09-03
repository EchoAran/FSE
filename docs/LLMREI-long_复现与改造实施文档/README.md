# LLMREI-long 复现与改造实施文档

> 调研日期：2026-08-31

## 1. 文档目的

本文档用于指导 **LLMREI-long** 的方法级复现与后续需求访谈场景改造。

这里的目标不是复现原论文的实验结果、评价流程或统计分析，而是复现其**访谈方法本身**：

> 使用完整的需求访谈指导 Prompt，结合当前项目背景与对话历史，由单个 LLM 持续生成后续访谈问题。

因此，本实施文档只关注以下内容：

- 论文中定义的方法；
- 官方公开 Prompt；
- 方法运行所需的最小执行逻辑；
- 如何将方法接入新的软件需求访谈 Case；
- 如何保持改造后的实现仍然忠实于原方法。

原论文的访谈数据、人工标注数据、统计结果和评价 notebook 不属于本实施过程的必要依赖。

## 2. 可复现基础

### 2.1 论文

Korn, Gorsch, Vogelsang.  
**LLMREI: Automating Requirements Elicitation Interviews with LLMs**  
IEEE Requirements Engineering Conference 2025.

- DOI：<https://doi.org/10.1109/RE63999.2025.00013>
- 预印本：<https://arxiv.org/abs/2507.02564>

### 2.2 官方公开 Prompt

官方 Zenodo replication package：

<https://zenodo.org/records/15016930>

本复现真正需要的核心文件是：

- `long_prompt.txt`

`short_prompt.txt` 可保留用于溯源，但不参与本实施。

### 2.3 代码可用性

截至本次调研，未发现与论文对应的完整官方 interviewer runtime 仓库。

因此 LLMREI-long 的复现方式是：

> **以官方 long prompt 为核心，补充一个最小多轮对话 runner。**

这类重实现自由度较低，因为方法本身主要由 Prompt 与 conversation history 驱动。

## 3. 改造原则

### 保留

- 官方 long prompt 的核心内容；
- 单 LLM interviewer；
- conversation history 作为长期上下文；
- 由 LLM 自身决定下一问题。

### 可替换

- 原论文场景背景；
- 输入 Case；
- LLM API 封装；
- transcript 存储格式；
- 运行入口。

### 不应加入

- Topic/Slot 显式状态；
- 独立 Scheduler；
- coverage planner；
- 动态结构管理；
- 额外的冲突、依赖、状态机逻辑。

否则实现将不再是 LLMREI-long，而变成新的混合方法。

## 4. 阶段文件

1. `01_阶段一_方法资产确认.md`
2. `02_阶段二_最小LLMREI运行器复现.md`
3. `03_阶段三_需求访谈Case输入改造.md`
4. `04_阶段四_接口与日志规范化.md`
5. `05_阶段五_行为校验与实施收尾.md`
6. `SOURCES.md`
