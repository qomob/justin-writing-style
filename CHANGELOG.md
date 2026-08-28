# Changelog

本文件遵循 semver-light：patch = 修复措辞/补充说明；minor = 新增步骤/场景/检查项；major = 架构重构/流程重写。

## 1.2.0 — 2026-08-28

审计来源：SkillForge v5.26.0 Audit-Only（评分 95/100，GO with Caveats）。本次修复全部 Caveat 与生产化建议项。

### 修复
- **规则 7 与 R7 对齐**（消除 Critical 级跨文件矛盾）：明喻允许用于"物"或"动作"，不许用于情绪。原根文档仅写"物"，会误杀 worked-example 中"像个护士在给别人量脉搏"类合法动作明喻。
- **Step 2 结构模式计数修正**："六个" → "七个（P1-P7，其中 P7 可选）"，与 references/structure-patterns.md 实际定义一致。

### 新增
- `scripts/style_lint.py`：可计数规则机械校验器（R1 段落句数 / R2 引号与对话动词修饰 / R4 抒情词 / R5 模糊量词 / R7 明喻配额 / R12 禁用收尾句式），Step 5 自检的半独立验证通道。
- `evals/evals.json`：3 触发 + 3 反触发 + 1 机械合规用例。
- `README.md`、`LICENSE`（MIT）。
- SKILL.md 增加硬规则同步维护提示（规则 4↔E1、规则 7↔明喻配额、规则 12↔P4 交叉引用登记）。
- description 增加不适用文体排斥声明："不处理营销文案/说理文/学术写作"（AP-10 误触发加固）。

## 1.1.0 — 基线

- Skill Compiler 2.3.1（full 模式，trae 平台）编译初始版本。
- 来源：用户提供的单篇中文叙事长文 PDF（15 页），按风格分析用途编译；包内不含原文摘录。
