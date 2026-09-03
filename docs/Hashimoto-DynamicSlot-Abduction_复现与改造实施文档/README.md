# Hashimoto Dynamic Slot Generation + Abduction 复现与改造实施文档

> 调研日期：2026-08-31

## 1. 文档目的

本文档用于复现 Hashimoto 等人在 COLING 2025 提出的 **Dynamic Slot Generation + Abduction** 访谈方法，并将其从护士职业访谈改造为软件需求访谈系统。

目标是复现**方法与系统运行逻辑**，而不是复现原论文中的用户模拟实验、信息命中率或人工评价结果。

## 2. 方法核心

该方法的核心是：

```text
Conversation
    ↓
Slot Filling
    ↓
Dynamic Slot Generation
    ↓
Abductive Reasoning
    ↓
Question Generation
```

系统显式维护 Slot 集合，根据受访者回答持续填充已有 Slot，并在需要时动态生成新的 Slot。

Proposed Method 2 进一步通过 abduction：

```text
Observed Surprising Fact C
        ↓
Hypothesized Reason A
        ↓
New Slot for probing A
```

生成值得进一步探索的新问题方向。

## 3. 可复现基础

### 3.1 正式论文

Hashimoto et al.  
**A Career Interview Dialogue System using Large Language Model-based Dynamic Slot Generation**  
COLING 2025.

<https://aclanthology.org/2025.coling-main.106/>

### 3.2 论文中公开的系统资产

Appendix A 公开：

- Dynamic Slot Generation Prompt；
- Abduction Prompt；
- Slot Filling Prompt；
- Question Generation Prompt；
- 输出 JSON 示例；
- 最大新 Slot 数量；
- Abduction History；
- 原始 Initial Slot Set；
- 模型配置；
- 终止条件。

### 3.3 DialBB

原系统使用 DialBB 的 state-transition network block：

<https://github.com/c4a-ri/dialbb>

但原应用的完整 DialBB 配置未公开。

### 3.4 代码可用性

截至本次调研，未发现该具体 career interview system 的完整官方代码库。

因此需要做：

> **faithful method-level reimplementation**

而不是 exact source-code reproduction。

## 4. 改造边界

### 保留

- Slot Filling；
- Dynamic Slot Generation；
- Abduction；
- Abduction History；
- 基于 Slot 的 Question Generation；
- 原 Prompt 结构和 JSON 语义。

### 替换

- Nurse/career domain；
- Initial Slot Set；
- self-assessment 输入；
- persona；
- 领域措辞。

### 不加入

- Topic 层；
- conflict/uncertain state；
- dependency graph；
-独立 scheduler；
-本文的 runtime requirement state。

## 5. 阶段文件

1. `01_阶段一_方法规格抽取.md`
2. `02_阶段二_核心系统重实现.md`
3. `03_阶段三_RE领域适配.md`
4. `04_阶段四_需求Case与接口改造.md`
5. `05_阶段五_忠实性校验与实施收尾.md`
6. `SOURCES.md`
