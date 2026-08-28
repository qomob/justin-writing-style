# justin-writing-style（孙的写作风格）

第一人称克制白描叙事生成器：把任意题材（情感 / 金钱 / 权力 / 失去 / 创业 / 家族）编译成"零抒情、精确数字、物件载情、反高潮收尾"的长篇叙事文。

风格内核：海明威冰山理论 × 中文互联网克制白描。

> 适用：回忆录、叙事长文、风格克隆写作。
> 不适用：营销文案 / 说理文 / 议论文 / 学术写作 / 欢乐轻快主题。

![justin-writing-style](./justin-writing-style.png)

## 安装

将本目录放入宿主平台的 skills 路径，例如 Trae：

```
<project>/.trae/skills/justin-writing-style/
```

无第三方依赖；`scripts/style_lint.py` 仅需 Python 3 标准库。

## 使用

对模型说出触发意图即可，例如：

- "用克制白描风格写一篇第一人称回忆录，题材：我和发小的二十年"
- "模仿 Justin 那种冰山理论的写法写个故事，不要抒情"

skill 内部按五步执行：题材摄取 → 结构设计（七个模式 P1-P7）→ 系统配置（载情物件 / 精确数字 / 顺从性重复句）→ 分节生成 → 12 项硬规则风格自检，输出正文 + 自检表。

### 机械校验（可选）

对生成的正文文件运行 lint，自动检测可计数规则（引号对话、对话动词修饰、抒情词、段落句数、明喻配额、模糊量词、禁用收尾句式）：

```
python3 scripts/style_lint.py <正文文件>     # 文件入参
python3 scripts/style_lint.py - < draft.txt  # stdin
```

退出码：`0` 通过，`1` 存在违规（逐条列出规则号与行号），`2` 用法错误。机器可判项以 lint 为准，成语 / 形容词堆砌 / 反高潮结构等语义规则仍由 LLM 自检。

## 目录结构

```
justin-writing-style/
├── SKILL.md                      # 根文档：流程路由 + 十二条硬规则速查
├── references/
│   ├── style-rules.md            # R1-R12 完整句法/词汇规则（Step 4 加载）
│   ├── structure-patterns.md     # P1-P7 结构模式 + 分节大纲方法（Step 1/2 加载）
│   ├── emotion-engineering.md    # E1-E7 情感转译技术（Step 3 加载）
│   └── worked-example.md         # 语感对照示范样本（Step 5 加载）
├── scripts/
│   └── style_lint.py             # 可计数规则机械校验器
├── evals/
│   └── evals.json                # 3 触发 + 3 反触发 + 1 合规用例
├── CHANGELOG.md
├── LICENSE                       # MIT
└── README.md
```

各 reference 均按需懒加载（见 SKILL.md 各 Step 的 📍 标记），不会全量读入。

## 维护约定

- 修改十二条硬规则时，须同步 `references/style-rules.md`（R1-R12）与 SKILL.md 速查表，并全库检索交叉引用（规则 4↔E1 转译表、规则 7↔明喻配额、规则 12↔P4）。
- 版本号遵循 semver-light，变更记录于 `CHANGELOG.md`。
- 部署后每 90 天用 `evals/evals.json` 的触发/反触发用例复验一次路由命中率，命中率下降即回炉。

## 诚实边界

- 规则提取自单一叙事长文样本，存在单样本过拟合风险。
- references 中示范片段均为按规则自创的风格示意，非任何原文摘录。
- 用本 skill 生成涉及真实人物的文本时，应附带虚构声明。

## 许可

[MIT](./LICENSE)
