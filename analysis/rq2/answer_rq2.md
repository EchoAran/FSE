# RQ2：从研究问题组织证据

叙事链路 §7.2 和 §7.6 的问题是：不同方法能否保持连贯的访谈流程，并根据受访者表达合理推进？RQ2 在全文中承担访谈过程质量的验证，与 RQ1 的信息产出和 RQ3 的下游支持价值衔接。

## 正文所需证据

| 论证环节 | 必要证据 | 位置 |
| --- | --- | --- |
| 评分是否具有一致性 | 全部四位评价者的 ordinal α 及其 95% CI | 评价协议或结果开头的一句话 |
| 四种方法的流程质量如何 | 三个维度的四评价者平均评分及其 CI | 现有三面板均值图 |
| 本文方法相对 baseline 的改善幅度 | 九项 Case 配对均值差及其 95% CI | 三个 baseline × 三个维度的紧凑表 |
| 跨 Case 的优势方向是否稳定 | 九项双侧精确符号检验，统一 Holm 校正 | 正文一句话；精确结果保留在 CSV |
| 如何回答 RQ2 | 连贯性、回答承接和主题转换的结果解释 | Answer to RQ2 |

一致性评价承担测量依据的角色。主文报告 all-four 结果已经覆盖正式使用的评价者集合：Local Coherence 为 0.852 [0.818, 0.882]，Transition Quality 为 0.817 [0.778, 0.848]，Contingent Responsiveness 为 0.891 [0.863, 0.916]。全部三组评价者的精确结果保留于 `agreement.csv`。

主图回答绝对表现，主表回答提升幅度。正式表名说明数值为本文方法相对 baseline 的配对均值提升及其 95% CI；表内只保留列名和数据。胜／平／负数量和九个极小 p 值保留在 `tables/paired_sign_tests.csv`，避免将分析明细铺满正文。

显著性可以写为：九项配对比较的均值差区间均高于零；九项双侧精确符号检验经统一 Holm 校正后均有 p < 0.001。两项证据分别报告：区间描述均值提升的不确定性，符号检验判断非平局 Case 中的胜负倾向；这些 CI 仍为逐项区间。

## 结果解释

本文方法的 Local Coherence、Transition Quality 和 Contingent Responsiveness 均值分别为 3.93、3.50 和 3.89，在三个维度中均最高。LLMREI-long 在三个维度中都是均值最高的 baseline；相对它，本文方法分别高出 0.58、0.55 和 0.82 分。三个 baseline 的完整改善幅度及其区间由主表提供。

最直接的结论是：在本研究评估的访谈中，本文方法在维持问题联系、组织主题转换和承接受访者回答方面均优于所比较的方法。Transition Quality 的均值低于另外两项，表明主题转换仍是本文方法相对薄弱的环节。这种解释同时交代优势和改善空间，而不把所有结果压缩成“整体显著更好”。

## Answer to RQ2

在本研究的 69 个 Case 中，本文方法在局部连贯性、主题转换质量和回答承接能力上均取得最高平均评分，并相对三个 baseline 呈现正向的配对均值提升。其中，相对均值最高的 baseline LLMREI-long，三个维度分别提升 0.58、0.55 和 0.82 分。这些结果支持本文方法能够维持更连贯的访谈流程，并更充分地利用受访者表达推进后续提问；主题转换仍是相对薄弱的环节。

Across the 69 evaluated Cases, our method achieved the highest mean ratings for Local Coherence, Transition Quality, and Contingent Responsiveness, with positive paired mean gains over all three baselines. Compared with LLMREI-long, the highest-scoring baseline in each dimension, the gains were 0.58, 0.55, and 0.82 points, respectively. These results support more coherent interview flow and more responsive progression based on stakeholder answers, while topic transitions remain the comparatively weaker aspect of our method.

## 分析文件

- `rq2_mean_scores.png/.svg/.pdf`：主图。
- `tables/table1_summary.png/.svg/.pdf/.md/.tex`：主表。
- `tables/table1_summary.csv`：九项改善幅度、CI 和精确 p 值。
- `tables/paired_sign_tests.csv`：完整检验及胜／平／负数量。
- `agreement.csv`：评价者一致性及其置信区间。
