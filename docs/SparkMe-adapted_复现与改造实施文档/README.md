# SparkMe 源码裁剪与需求访谈化改造实施文档

## 1. 实施定位

本项目不根据论文重新实现 SparkMe，也不复现论文实验。

唯一正确的实施路线是：

> 下载官方仓库 → 从现有源码中保留 SparkMe 方法链路 → 删除实验、模拟受访者、离线评估和非必要产品外壳 → 将保留下来的系统原位改造成软件需求访谈工具。

论文只用于理解方法概念和判断源码中的功能边界，不作为逐段手写实现规格。官方源码已经给出的状态模型、Agent 协作、Prompt、工具调用和规划流程均应直接复用。

## 2. 实施规模预估

本工作属于**中等规模的源码裁剪与领域适配**，不是算法重建。

主要工作量来自：

- 官方仓库同时包含方法、基线、数据生成、模拟受访者、评价脚本、标注工具、Web/语音入口和大量实验数据；
- 部分实验设施被核心模块直接导入，删除目录前需要先解除依赖；
- workforce 领域内容分散在 Topic Guide、portrait、多个 Agent Prompt、入口参数和环境变量中；
- 上游两个已知缺陷会直接影响 emergent subtopic 与 strategic question 路径。

审核和实施应采用“目录级资产清点 + import 依赖检查 + 核心路径回归测试”的方式，不需要用论文实验数值进行比对。

## 3. 保留的方法核心

必须保留并继续使用官方实现中的：

- Interviewer；
- Agenda Manager；
- predefined topic/subtopic coverage；
- interview notes 与方法运行所需的 memory；
- emergent insight 与 emergent subtopic；
- Exploration Planner；
- simulated conversation rollouts；
- coverage、cost、emergence 组成的 utility；
- strategic question 生成与回流；
- Session Agenda、Question Bank 以及上述机制依赖的 LLM/tool-call 基础设施。

这些组件共同构成 SparkMe。不得重新设计一套 Topic/Slot 状态机、调度器或评分函数来替代它们。

## 4. 删除范围

以下内容不属于需求访谈交付：

- `baselines/`；
- `dataset_gen/`；
- `evaluation/`；
- `data/workbank_seed/`；
- `data/sample_user_profiles/`；
- LLM 模拟受访者及其 Prompt；
- synthetic user、ground truth、participant profile 与用户研究相关逻辑；
- evaluation logger、评价结果 CSV 和实验统计输出；
- baseline prompt 分支与实验切换参数；
- 标注工具、论文评价辅助脚本；
- 不服务于最终最小调用方式的 Web、云部署和语音外壳；
- workforce 专用 Topic Guide、portrait、示例与说明文本。

“受访者设计”是指模拟受访者、预制画像、ground truth 和实验参与者管理。真实利益相关者提交回答的输入通道仍然必须存在，但不在系统内建模一个隐藏的模拟人格。

运行时的 coverage completion 判断属于 SparkMe 方法本身，不应因名称中出现 evaluator 而误删。离线论文评估脚本和评价日志才属于删除对象。

## 5. 需求访谈化边界

领域改造只作用于：

- 软件项目 Case 输入；
- RE Topic Guide；
- 从回答中维护的最小 stakeholder/project context；
- Interviewer、Agenda Manager、Exploration Planner 的领域措辞和示例；
- 对外的初始化、提问、回答提交和 Transcript 接口。

不得修改：

- Agenda、coverage、emergence 和 rollout 的状态转移；
- utility 的组成；
- Agent 的职责边界；
- planner 的候选生成、预测和选择流程。

Prompt 与代码只承载运行逻辑，不写论文名、Figure、Appendix、仓库来源、版本、commit、哈希或所谓证据说明。必要的参考资料只存在于本实施文档中。

失败处理只要求保护当前保留的 SparkMe 方法主链：当内置 Agent 在一轮处理中异常时，取消本轮尚未完成的并发任务，并恢复该轮开始前的会话内领域状态。该能力不是通用事务系统，不覆盖任意新增插件、外部服务已经产生的副作用、进程崩溃或跨进程恢复。若回滚本身失败，应终止当前会话并重新初始化 Case，不继续在未知状态上原地重试。

本项目不新增每轮持久化检查点、Checkpoint/Resume API 或“任意故障后 100% 无损恢复”契约。保留上游正常结束时所需的持久化行为即可，公共 Transcript 仍只承担对话导出职责。

## 6. 交付形态

最终 `sparkme/` 应是单一、干净的需求访谈实现：

- 不保留 `original`、`re`、`adapted` 等双套运行资产；
- 不保留 workforce 与 RE 两套路由；
- 不保留实验模式开关；
- 不依赖 simulated user、evaluation dataset 或 baseline；
- 不保留 `tests/`、Mock 引擎、pytest 依赖或 `--mock` 运行入口；
- 保留一个最小外部调用接口和必要的会话输出；
- 依赖清单按实际保留代码重新收敛。

## 7. 实施阶段

1. `01_阶段一_官方源码获取与边界确认.md`：下载源码并确认资产边界；
2. `02_阶段二_方法代码提取与交付裁剪.md`：解除实验耦合并裁剪交付；
3. `03_阶段三_核心路径修补与回归测试.md`：修补核心路径缺陷并建立回归测试；
4. `04_阶段四_需求访谈领域资产改造.md`：原位完成需求访谈领域改造；
5. `05_阶段五_需求Case与最小调用接口.md`：提供最小 Case 与调用接口；
6. `06_阶段六_方法完整性与清洁度验收.md`：验证方法完整性和交付清洁度；
7. `07_阶段七_交付去仓库化与纯净封装.md`：在方法验收完成后移除 Git 元数据、开发测试与 Mock、仓库服务文件及运行生成物，形成纯净的 SparkMe 方法交付目录。
