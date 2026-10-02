# RQ2 需求访谈流程质量评估报告

## 1. 来源与覆盖总览

### 来源清单与就绪状态 (Source Inventory Statuses)
- 评估案例总数 (Total Cases): 69
- 来源条目总数 (Total Items): 276
  - 就绪 (ready): 276
  - 来源不完整 (source_incomplete): 0
  - 输入错误 (input_error): 0

### 结束观察分布 (Ending Observations)
- 达到轮数上限 (turn_limit_reached): 0
- 未知/其他 (unknown): 276

### 访谈轮数统计 (Interview Length / Completed Turns by Method)
| 方法 | 最小轮数 (Min) | 最大轮数 (Max) | 中位数 (Median) |
| --- | --- | --- | --- |
| hashimoto | 1 | 14 | 5.0000 |
| llmrei-long | 6 | 48 | 15.0000 |
| sparkme | 23 | 55 | 38.0000 |
| proposed_method | 26 | 82 | 48.0000 |

### 历史记录说明 (Historical Human Ratings)
- 人工评分表中未纳入当前评估的合法非 ready 历史行数量: 0

### 覆盖情况 (Coverage)

| 方法 | 评价者 | 维度 | 预期数 | 有效评分数 | 待评数 | 失败数 | 可评分率 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hashimoto | llm_expert_1 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | llm_expert_1 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | llm_expert_1 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | llm_expert_2 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | llm_expert_2 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | llm_expert_2 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | human_expert_1 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | human_expert_1 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | human_expert_1 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | human_expert_2 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | human_expert_2 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| hashimoto | human_expert_2 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | llm_expert_1 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | llm_expert_1 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | llm_expert_1 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | llm_expert_2 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | llm_expert_2 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | llm_expert_2 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | human_expert_1 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | human_expert_1 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | human_expert_1 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | human_expert_2 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | human_expert_2 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| llmrei-long | human_expert_2 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | llm_expert_1 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | llm_expert_1 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | llm_expert_1 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | llm_expert_2 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | llm_expert_2 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | llm_expert_2 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | human_expert_1 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | human_expert_1 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | human_expert_1 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | human_expert_2 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | human_expert_2 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| sparkme | human_expert_2 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | llm_expert_1 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | llm_expert_1 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | llm_expert_1 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | llm_expert_2 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | llm_expert_2 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | llm_expert_2 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | human_expert_1 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | human_expert_1 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | human_expert_1 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | human_expert_2 | local_coherence | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | human_expert_2 | transition_quality | 69 | 69 | 0 | 0 | 1.0000 |
| proposed_method | human_expert_2 | contingent_responsiveness | 69 | 69 | 0 | 0 | 1.0000 |

## 2. 评分分布与中心趋势

### 评分描述统计 (Score Summary)

| 方法 | 评价者 | 维度 | 样本数 (N) | 均值 | 中位数 | Q1 | Q3 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hashimoto | llm_expert_1 | local_coherence | 69 | 2.3188 | 2.0000 | 2.0000 | 3.0000 |
| hashimoto | llm_expert_1 | transition_quality | 69 | 1.8261 | 2.0000 | 1.0000 | 2.0000 |
| hashimoto | llm_expert_1 | contingent_responsiveness | 69 | 2.1594 | 2.0000 | 2.0000 | 3.0000 |
| hashimoto | llm_expert_2 | local_coherence | 69 | 2.3333 | 2.0000 | 2.0000 | 3.0000 |
| hashimoto | llm_expert_2 | transition_quality | 69 | 1.7971 | 2.0000 | 1.0000 | 2.0000 |
| hashimoto | llm_expert_2 | contingent_responsiveness | 69 | 2.1594 | 2.0000 | 2.0000 | 3.0000 |
| hashimoto | human_expert_1 | local_coherence | 69 | 2.2899 | 2.0000 | 2.0000 | 3.0000 |
| hashimoto | human_expert_1 | transition_quality | 69 | 1.8696 | 2.0000 | 2.0000 | 2.0000 |
| hashimoto | human_expert_1 | contingent_responsiveness | 69 | 2.0870 | 2.0000 | 2.0000 | 3.0000 |
| hashimoto | human_expert_2 | local_coherence | 69 | 2.3623 | 2.0000 | 2.0000 | 3.0000 |
| hashimoto | human_expert_2 | transition_quality | 69 | 1.7826 | 2.0000 | 1.0000 | 2.0000 |
| hashimoto | human_expert_2 | contingent_responsiveness | 69 | 2.1449 | 2.0000 | 2.0000 | 3.0000 |
| llmrei-long | llm_expert_1 | local_coherence | 69 | 3.1159 | 3.0000 | 3.0000 | 3.0000 |
| llmrei-long | llm_expert_1 | transition_quality | 69 | 2.8551 | 3.0000 | 3.0000 | 3.0000 |
| llmrei-long | llm_expert_1 | contingent_responsiveness | 69 | 3.0290 | 3.0000 | 3.0000 | 3.0000 |
| llmrei-long | llm_expert_2 | local_coherence | 69 | 3.0870 | 3.0000 | 3.0000 | 3.0000 |
| llmrei-long | llm_expert_2 | transition_quality | 69 | 2.8986 | 3.0000 | 3.0000 | 3.0000 |
| llmrei-long | llm_expert_2 | contingent_responsiveness | 69 | 3.0290 | 3.0000 | 3.0000 | 3.0000 |
| llmrei-long | human_expert_1 | local_coherence | 69 | 3.6377 | 4.0000 | 3.0000 | 4.0000 |
| llmrei-long | human_expert_1 | transition_quality | 69 | 3.0580 | 3.0000 | 3.0000 | 3.0000 |
| llmrei-long | human_expert_1 | contingent_responsiveness | 69 | 3.1739 | 3.0000 | 3.0000 | 3.0000 |
| llmrei-long | human_expert_2 | local_coherence | 69 | 3.5652 | 4.0000 | 3.0000 | 4.0000 |
| llmrei-long | human_expert_2 | transition_quality | 69 | 3.0000 | 3.0000 | 3.0000 | 3.0000 |
| llmrei-long | human_expert_2 | contingent_responsiveness | 69 | 3.0290 | 3.0000 | 3.0000 | 3.0000 |
| sparkme | llm_expert_1 | local_coherence | 69 | 2.6522 | 3.0000 | 2.0000 | 3.0000 |
| sparkme | llm_expert_1 | transition_quality | 69 | 2.7681 | 3.0000 | 2.0000 | 3.0000 |
| sparkme | llm_expert_1 | contingent_responsiveness | 69 | 2.4203 | 2.0000 | 2.0000 | 3.0000 |
| sparkme | llm_expert_2 | local_coherence | 69 | 2.6232 | 3.0000 | 2.0000 | 3.0000 |
| sparkme | llm_expert_2 | transition_quality | 69 | 2.7536 | 3.0000 | 2.0000 | 3.0000 |
| sparkme | llm_expert_2 | contingent_responsiveness | 69 | 2.4058 | 2.0000 | 2.0000 | 3.0000 |
| sparkme | human_expert_1 | local_coherence | 69 | 2.6087 | 3.0000 | 2.0000 | 3.0000 |
| sparkme | human_expert_1 | transition_quality | 69 | 3.1594 | 3.0000 | 3.0000 | 3.0000 |
| sparkme | human_expert_1 | contingent_responsiveness | 69 | 2.4638 | 2.0000 | 2.0000 | 3.0000 |
| sparkme | human_expert_2 | local_coherence | 69 | 2.6667 | 3.0000 | 2.0000 | 3.0000 |
| sparkme | human_expert_2 | transition_quality | 69 | 3.0145 | 3.0000 | 3.0000 | 3.0000 |
| sparkme | human_expert_2 | contingent_responsiveness | 69 | 2.6232 | 3.0000 | 2.0000 | 3.0000 |
| proposed_method | llm_expert_1 | local_coherence | 69 | 3.8696 | 4.0000 | 4.0000 | 4.0000 |
| proposed_method | llm_expert_1 | transition_quality | 69 | 3.4638 | 3.0000 | 3.0000 | 4.0000 |
| proposed_method | llm_expert_1 | contingent_responsiveness | 69 | 3.8841 | 4.0000 | 4.0000 | 4.0000 |
| proposed_method | llm_expert_2 | local_coherence | 69 | 3.8696 | 4.0000 | 4.0000 | 4.0000 |
| proposed_method | llm_expert_2 | transition_quality | 69 | 3.4348 | 3.0000 | 3.0000 | 4.0000 |
| proposed_method | llm_expert_2 | contingent_responsiveness | 69 | 3.8261 | 4.0000 | 4.0000 | 4.0000 |
| proposed_method | human_expert_1 | local_coherence | 69 | 3.9710 | 4.0000 | 4.0000 | 4.0000 |
| proposed_method | human_expert_1 | transition_quality | 69 | 3.3913 | 3.0000 | 3.0000 | 4.0000 |
| proposed_method | human_expert_1 | contingent_responsiveness | 69 | 3.8696 | 4.0000 | 4.0000 | 4.0000 |
| proposed_method | human_expert_2 | local_coherence | 69 | 4.0000 | 4.0000 | 4.0000 | 4.0000 |
| proposed_method | human_expert_2 | transition_quality | 69 | 3.7101 | 4.0000 | 3.0000 | 4.0000 |
| proposed_method | human_expert_2 | contingent_responsiveness | 69 | 3.9710 | 4.0000 | 4.0000 | 4.0000 |

## 3. 同 Case 配对比较 (Paired Comparisons)

- 请求 Bootstrap 重采样次数 (Requested Repeats): 10000

| 评价者 | 维度 | 方法 A | 方法 B | 配对数 | 均值差 (A-B) | 中位数差 | A较高 | 相同 | B较高 | 95% CI 低 | 95% CI 高 | 有效/请求重采样数 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| llm_expert_1 | local_coherence | hashimoto | llmrei-long | 69 | -0.7971 | -1.0000 | 3 | 24 | 42 | -1.0145 | -0.5942 | 10000 / 10000 |  |
| llm_expert_1 | local_coherence | hashimoto | sparkme | 69 | -0.3333 | 0.0000 | 11 | 30 | 28 | -0.5507 | -0.1301 | 10000 / 10000 |  |
| llm_expert_1 | local_coherence | hashimoto | proposed_method | 69 | -1.5507 | -1.0000 | 0 | 3 | 66 | -1.7391 | -1.3768 | 10000 / 10000 |  |
| llm_expert_1 | local_coherence | llmrei-long | sparkme | 69 | 0.4638 | 0.0000 | 30 | 34 | 5 | 0.2899 | 0.6522 | 10000 / 10000 |  |
| llm_expert_1 | local_coherence | llmrei-long | proposed_method | 69 | -0.7536 | -1.0000 | 3 | 16 | 50 | -0.8986 | -0.5942 | 10000 / 10000 |  |
| llm_expert_1 | local_coherence | sparkme | proposed_method | 69 | -1.2174 | -1.0000 | 0 | 6 | 63 | -1.3623 | -1.0725 | 10000 / 10000 |  |
| llm_expert_1 | transition_quality | hashimoto | llmrei-long | 69 | -1.0290 | -1.0000 | 4 | 9 | 56 | -1.2174 | -0.8406 | 10000 / 10000 |  |
| llm_expert_1 | transition_quality | hashimoto | sparkme | 69 | -0.9420 | -1.0000 | 2 | 19 | 48 | -1.1449 | -0.7391 | 10000 / 10000 |  |
| llm_expert_1 | transition_quality | hashimoto | proposed_method | 69 | -1.6377 | -2.0000 | 0 | 2 | 67 | -1.7971 | -1.4783 | 10000 / 10000 |  |
| llm_expert_1 | transition_quality | llmrei-long | sparkme | 69 | 0.0870 | 0.0000 | 17 | 41 | 11 | -0.0725 | 0.2464 | 10000 / 10000 |  |
| llm_expert_1 | transition_quality | llmrei-long | proposed_method | 69 | -0.6087 | -1.0000 | 1 | 33 | 35 | -0.7826 | -0.4348 | 10000 / 10000 |  |
| llm_expert_1 | transition_quality | sparkme | proposed_method | 69 | -0.6957 | -1.0000 | 2 | 28 | 39 | -0.8699 | -0.5214 | 10000 / 10000 |  |
| llm_expert_1 | contingent_responsiveness | hashimoto | llmrei-long | 69 | -0.8696 | -1.0000 | 3 | 23 | 43 | -1.0870 | -0.6522 | 10000 / 10000 |  |
| llm_expert_1 | contingent_responsiveness | hashimoto | sparkme | 69 | -0.2609 | 0.0000 | 14 | 27 | 28 | -0.4928 | -0.0290 | 10000 / 10000 |  |
| llm_expert_1 | contingent_responsiveness | hashimoto | proposed_method | 69 | -1.7246 | -2.0000 | 0 | 3 | 66 | -1.9275 | -1.5362 | 10000 / 10000 |  |
| llm_expert_1 | contingent_responsiveness | llmrei-long | sparkme | 69 | 0.6087 | 1.0000 | 39 | 28 | 2 | 0.4493 | 0.7681 | 10000 / 10000 |  |
| llm_expert_1 | contingent_responsiveness | llmrei-long | proposed_method | 69 | -0.8551 | -1.0000 | 0 | 16 | 53 | -0.9855 | -0.7246 | 10000 / 10000 |  |
| llm_expert_1 | contingent_responsiveness | sparkme | proposed_method | 69 | -1.4638 | -1.0000 | 0 | 1 | 68 | -1.6087 | -1.3188 | 10000 / 10000 |  |
| llm_expert_2 | local_coherence | hashimoto | llmrei-long | 69 | -0.7536 | -1.0000 | 3 | 26 | 40 | -0.9710 | -0.5507 | 10000 / 10000 |  |
| llm_expert_2 | local_coherence | hashimoto | sparkme | 69 | -0.2899 | 0.0000 | 11 | 32 | 26 | -0.4928 | -0.0870 | 10000 / 10000 |  |
| llm_expert_2 | local_coherence | hashimoto | proposed_method | 69 | -1.5362 | -1.0000 | 0 | 4 | 65 | -1.7246 | -1.3478 | 10000 / 10000 |  |
| llm_expert_2 | local_coherence | llmrei-long | sparkme | 69 | 0.4638 | 0.0000 | 32 | 32 | 5 | 0.2899 | 0.6377 | 10000 / 10000 |  |
| llm_expert_2 | local_coherence | llmrei-long | proposed_method | 69 | -0.7826 | -1.0000 | 1 | 18 | 50 | -0.9130 | -0.6377 | 10000 / 10000 |  |
| llm_expert_2 | local_coherence | sparkme | proposed_method | 69 | -1.2464 | -1.0000 | 0 | 6 | 63 | -1.3913 | -1.1014 | 10000 / 10000 |  |
| llm_expert_2 | transition_quality | hashimoto | llmrei-long | 69 | -1.1014 | -1.0000 | 2 | 8 | 59 | -1.2754 | -0.9275 | 10000 / 10000 |  |
| llm_expert_2 | transition_quality | hashimoto | sparkme | 69 | -0.9565 | -1.0000 | 2 | 19 | 48 | -1.1594 | -0.7536 | 10000 / 10000 |  |
| llm_expert_2 | transition_quality | hashimoto | proposed_method | 69 | -1.6377 | -2.0000 | 0 | 3 | 66 | -1.8116 | -1.4493 | 10000 / 10000 |  |
| llm_expert_2 | transition_quality | llmrei-long | sparkme | 69 | 0.1449 | 0.0000 | 19 | 41 | 9 | -0.0145 | 0.3043 | 10000 / 10000 |  |
| llm_expert_2 | transition_quality | llmrei-long | proposed_method | 69 | -0.5362 | 0.0000 | 1 | 35 | 33 | -0.6957 | -0.3768 | 10000 / 10000 |  |
| llm_expert_2 | transition_quality | sparkme | proposed_method | 69 | -0.6812 | -1.0000 | 3 | 24 | 42 | -0.8551 | -0.5072 | 10000 / 10000 |  |
| llm_expert_2 | contingent_responsiveness | hashimoto | llmrei-long | 69 | -0.8696 | -1.0000 | 2 | 24 | 43 | -1.0870 | -0.6667 | 10000 / 10000 |  |
| llm_expert_2 | contingent_responsiveness | hashimoto | sparkme | 69 | -0.2464 | 0.0000 | 15 | 25 | 29 | -0.4783 | -0.0290 | 10000 / 10000 |  |
| llm_expert_2 | contingent_responsiveness | hashimoto | proposed_method | 69 | -1.6667 | -2.0000 | 0 | 3 | 66 | -1.8551 | -1.4928 | 10000 / 10000 |  |
| llm_expert_2 | contingent_responsiveness | llmrei-long | sparkme | 69 | 0.6232 | 1.0000 | 40 | 27 | 2 | 0.4638 | 0.7826 | 10000 / 10000 |  |
| llm_expert_2 | contingent_responsiveness | llmrei-long | proposed_method | 69 | -0.7971 | -1.0000 | 1 | 15 | 53 | -0.9130 | -0.6667 | 10000 / 10000 |  |
| llm_expert_2 | contingent_responsiveness | sparkme | proposed_method | 69 | -1.4203 | -1.0000 | 0 | 4 | 65 | -1.5652 | -1.2609 | 10000 / 10000 |  |
| human_expert_1 | local_coherence | hashimoto | llmrei-long | 69 | -1.3478 | -1.0000 | 0 | 13 | 56 | -1.5652 | -1.1304 | 10000 / 10000 |  |
| human_expert_1 | local_coherence | hashimoto | sparkme | 69 | -0.3188 | 0.0000 | 12 | 28 | 29 | -0.5507 | -0.0870 | 10000 / 10000 |  |
| human_expert_1 | local_coherence | hashimoto | proposed_method | 69 | -1.6812 | -2.0000 | 0 | 4 | 65 | -1.8696 | -1.4928 | 10000 / 10000 |  |
| human_expert_1 | local_coherence | llmrei-long | sparkme | 69 | 1.0290 | 1.0000 | 53 | 15 | 1 | 0.8551 | 1.2029 | 10000 / 10000 |  |
| human_expert_1 | local_coherence | llmrei-long | proposed_method | 69 | -0.3333 | 0.0000 | 2 | 43 | 24 | -0.4638 | -0.2029 | 10000 / 10000 |  |
| human_expert_1 | local_coherence | sparkme | proposed_method | 69 | -1.3623 | -1.0000 | 0 | 2 | 67 | -1.5072 | -1.2319 | 10000 / 10000 |  |
| human_expert_1 | transition_quality | hashimoto | llmrei-long | 69 | -1.1884 | -1.0000 | 0 | 8 | 61 | -1.3478 | -1.0290 | 10000 / 10000 |  |
| human_expert_1 | transition_quality | hashimoto | sparkme | 69 | -1.2899 | -1.0000 | 0 | 9 | 60 | -1.4783 | -1.1014 | 10000 / 10000 |  |
| human_expert_1 | transition_quality | hashimoto | proposed_method | 69 | -1.5217 | -1.0000 | 0 | 3 | 66 | -1.7101 | -1.3333 | 10000 / 10000 |  |
| human_expert_1 | transition_quality | llmrei-long | sparkme | 69 | -0.1014 | 0.0000 | 8 | 45 | 16 | -0.2464 | 0.0435 | 10000 / 10000 |  |
| human_expert_1 | transition_quality | llmrei-long | proposed_method | 69 | -0.3333 | 0.0000 | 4 | 40 | 25 | -0.4783 | -0.1884 | 10000 / 10000 |  |
| human_expert_1 | transition_quality | sparkme | proposed_method | 69 | -0.2319 | 0.0000 | 6 | 44 | 19 | -0.3913 | -0.0870 | 10000 / 10000 |  |
| human_expert_1 | contingent_responsiveness | hashimoto | llmrei-long | 69 | -1.0870 | -1.0000 | 1 | 13 | 55 | -1.2754 | -0.9130 | 10000 / 10000 |  |
| human_expert_1 | contingent_responsiveness | hashimoto | sparkme | 69 | -0.3768 | 0.0000 | 12 | 26 | 31 | -0.5942 | -0.1594 | 10000 / 10000 |  |
| human_expert_1 | contingent_responsiveness | hashimoto | proposed_method | 69 | -1.7826 | -2.0000 | 0 | 2 | 67 | -1.9420 | -1.6087 | 10000 / 10000 |  |
| human_expert_1 | contingent_responsiveness | llmrei-long | sparkme | 69 | 0.7101 | 1.0000 | 37 | 32 | 0 | 0.5362 | 0.8986 | 10000 / 10000 |  |
| human_expert_1 | contingent_responsiveness | llmrei-long | proposed_method | 69 | -0.6957 | -1.0000 | 2 | 19 | 48 | -0.8261 | -0.5652 | 10000 / 10000 |  |
| human_expert_1 | contingent_responsiveness | sparkme | proposed_method | 69 | -1.4058 | -1.0000 | 0 | 5 | 64 | -1.5507 | -1.2464 | 10000 / 10000 |  |
| human_expert_2 | local_coherence | hashimoto | llmrei-long | 69 | -1.2029 | -1.0000 | 2 | 16 | 51 | -1.4348 | -0.9710 | 10000 / 10000 |  |
| human_expert_2 | local_coherence | hashimoto | sparkme | 69 | -0.3043 | 0.0000 | 10 | 34 | 25 | -0.5217 | -0.0870 | 10000 / 10000 |  |
| human_expert_2 | local_coherence | hashimoto | proposed_method | 69 | -1.6377 | -1.0000 | 0 | 1 | 68 | -1.8261 | -1.4638 | 10000 / 10000 |  |
| human_expert_2 | local_coherence | llmrei-long | sparkme | 69 | 0.8986 | 1.0000 | 49 | 18 | 2 | 0.7101 | 1.0870 | 10000 / 10000 |  |
| human_expert_2 | local_coherence | llmrei-long | proposed_method | 69 | -0.4348 | 0.0000 | 2 | 37 | 30 | -0.5797 | -0.2899 | 10000 / 10000 |  |
| human_expert_2 | local_coherence | sparkme | proposed_method | 69 | -1.3333 | -1.0000 | 0 | 2 | 67 | -1.4638 | -1.2029 | 10000 / 10000 |  |
| human_expert_2 | transition_quality | hashimoto | llmrei-long | 69 | -1.2174 | -1.0000 | 0 | 6 | 63 | -1.3623 | -1.0725 | 10000 / 10000 |  |
| human_expert_2 | transition_quality | hashimoto | sparkme | 69 | -1.2319 | -1.0000 | 0 | 10 | 59 | -1.4058 | -1.0580 | 10000 / 10000 |  |
| human_expert_2 | transition_quality | hashimoto | proposed_method | 69 | -1.9275 | -2.0000 | 0 | 0 | 69 | -2.1014 | -1.7678 | 10000 / 10000 |  |
| human_expert_2 | transition_quality | llmrei-long | sparkme | 69 | -0.0145 | 0.0000 | 10 | 49 | 10 | -0.1453 | 0.1159 | 10000 / 10000 |  |
| human_expert_2 | transition_quality | llmrei-long | proposed_method | 69 | -0.7101 | -1.0000 | 1 | 23 | 45 | -0.8551 | -0.5652 | 10000 / 10000 |  |
| human_expert_2 | transition_quality | sparkme | proposed_method | 69 | -0.6957 | -1.0000 | 3 | 23 | 43 | -0.8696 | -0.5217 | 10000 / 10000 |  |
| human_expert_2 | contingent_responsiveness | hashimoto | llmrei-long | 69 | -0.8841 | -1.0000 | 1 | 24 | 44 | -1.0870 | -0.6812 | 10000 / 10000 |  |
| human_expert_2 | contingent_responsiveness | hashimoto | sparkme | 69 | -0.4783 | 0.0000 | 9 | 26 | 34 | -0.6812 | -0.2609 | 10000 / 10000 |  |
| human_expert_2 | contingent_responsiveness | hashimoto | proposed_method | 69 | -1.8261 | -2.0000 | 0 | 1 | 68 | -2.0145 | -1.6377 | 10000 / 10000 |  |
| human_expert_2 | contingent_responsiveness | llmrei-long | sparkme | 69 | 0.4058 | 0.0000 | 27 | 40 | 2 | 0.2609 | 0.5507 | 10000 / 10000 |  |
| human_expert_2 | contingent_responsiveness | llmrei-long | proposed_method | 69 | -0.9420 | -1.0000 | 0 | 11 | 58 | -1.0580 | -0.8261 | 10000 / 10000 |  |
| human_expert_2 | contingent_responsiveness | sparkme | proposed_method | 69 | -1.3478 | -1.0000 | 0 | 3 | 66 | -1.4928 | -1.2029 | 10000 / 10000 |  |

## 4. 评价者一致性 (Ordinal Krippendorff's Alpha)

- 请求 Bootstrap 重采样次数 (Requested Repeats): 10000

### 评价者在可配对单位中的有效评分贡献数 (Rater Contributions in Pairable Units)

| 评价组 | 维度 | llm_expert_1 | llm_expert_2 | human_expert_1 | human_expert_2 |
| --- | --- | --- | --- | --- | --- |
| llm_pair | local_coherence | 276 | 276 | 0 | 0 |
| llm_pair | transition_quality | 276 | 276 | 0 | 0 |
| llm_pair | contingent_responsiveness | 276 | 276 | 0 | 0 |
| human_pair | local_coherence | 0 | 0 | 276 | 276 |
| human_pair | transition_quality | 0 | 0 | 276 | 276 |
| human_pair | contingent_responsiveness | 0 | 0 | 276 | 276 |
| all_four | local_coherence | 276 | 276 | 276 | 276 |
| all_four | transition_quality | 276 | 276 | 276 | 276 |
| all_four | contingent_responsiveness | 276 | 276 | 276 | 276 |

### 一致性统计表 (Agreement Table)

| 评价组 | 维度 | 有效单位数 | Case数 | 总评分数 | 2评价单位 | 3评价单位 | 4评价单位 | Ordinal α | 95% CI 低 | 95% CI 高 | 有效/请求重采样数 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| llm_pair | local_coherence | 276 | 69 | 552 | 276 | 0 | 0 | 0.9479 | 0.9208 | 0.9706 | 10000 / 10000 |  |
| llm_pair | transition_quality | 276 | 69 | 552 | 276 | 0 | 0 | 0.9446 | 0.9129 | 0.9714 | 10000 / 10000 |  |
| llm_pair | contingent_responsiveness | 276 | 69 | 552 | 276 | 0 | 0 | 0.9565 | 0.9338 | 0.9763 | 10000 / 10000 |  |
| human_pair | local_coherence | 276 | 69 | 552 | 276 | 0 | 0 | 0.9146 | 0.8770 | 0.9461 | 10000 / 10000 |  |
| human_pair | transition_quality | 276 | 69 | 552 | 276 | 0 | 0 | 0.8116 | 0.7646 | 0.8554 | 10000 / 10000 |  |
| human_pair | contingent_responsiveness | 276 | 69 | 552 | 276 | 0 | 0 | 0.8746 | 0.8412 | 0.9047 | 10000 / 10000 |  |
| all_four | local_coherence | 276 | 69 | 1104 | 0 | 0 | 276 | 0.8523 | 0.8179 | 0.8825 | 10000 / 10000 |  |
| all_four | transition_quality | 276 | 69 | 1104 | 0 | 0 | 276 | 0.8165 | 0.7779 | 0.8482 | 10000 / 10000 |  |
| all_four | contingent_responsiveness | 276 | 69 | 1104 | 0 | 0 | 276 | 0.8908 | 0.8632 | 0.9156 | 10000 / 10000 |  |

## 5. 回查索引与产物路径

- 原始输入清单: `E:\PycharmProjects\FSE\evolution\rq2\artifacts\input_inventory.csv`
- 评分表目录: `E:\PycharmProjects\FSE\evolution\rq2\artifacts\ratings`
- 详细评分回查: `E:\PycharmProjects\FSE\evolution\rq2\artifacts\cases/<case_id>/<method_id>/`
