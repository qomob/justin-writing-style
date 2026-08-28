#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""justin-writing-style 机械风格校验器。

对生成的正文做可计数规则的自动检测（十二条硬规则中的机械化子集）：

  R1   段落句数 <= 3（本风格"行即段"，按非空行计）
  R2a  对话无引号（检测 " " 「 」 『 』）
  R2b  对话动词只许"说/问"（检测 修饰语+地+说/问、笑着说、叹了口气说 等）
  R4   抒情词黑名单（情绪名词 + 心理动词直述）；评价性形容词报 WARN
  R5   模糊量词（很多/好几天/几千块 等）
  R7   明喻配额 <= 3（启发式计数 仿佛/宛如/如同/好比/好像/像）
  R12  禁用收尾句式（"后来我才明白"）

不可机械化规则（成语 / 形容词堆砌 / 载情物件 / 反高潮结构等）仍由 LLM 自检
（SKILL.md Step 5）。本脚本只做它真能判断的事。

用法:
    python3 scripts/style_lint.py <正文文件>
    python3 scripts/style_lint.py -          # 从 stdin 读取

行为:
    - 若文本含 "**风格自检**" 分隔标记，只校验其前的正文部分
    - 跳过标题行(#)、分隔线(---)、表格行(|)、加粗行(**)
退出码:
    0 = 无 violation   1 = 存在 violation   2 = 用法错误
"""

import re
import sys

# ---------- 规则配置 ----------

QUOTE_RE = re.compile(r'[“”"「」『』]')

MODIFIED_VERB_RE = re.compile(
    r'[一-龥a-zA-Z]{1,3}地(?:说|问)'
    r'|(?:笑|叹|哭|喊|吼|骂)(?:着|了|了口气|了口气)?(?:说|问)'
    r'|(?:冷冷|轻声|低声|淡淡|平静)(?:地)?(?:说|问)'
)

# R4 硬违规：情绪名词 + 心理动词直述
EMOTION_HARD = [
    '难过', '悲伤', '心痛', '幸福', '孤独', '绝望', '心碎',
    '我感到', '我感觉', '我的内心', '内心深处', '感到一阵',
]

# R4 软告警：评价性形容词（评价性使用才违规，机械无法判语境，报 WARN）
EMOTION_WARN = ['痛苦的', '温柔的', '残忍的']

FUZZY_QUANTIFIERS = [
    '很多', '许多', '无数', '好几天', '好几个', '好几个月', '好几年',
    '好几百', '好几十', '几千块', '几万块', '几十万', '几百万', '几千万',
]

SIMILE_RE = re.compile(r'仿佛|宛如|如同|好比|好像|(?<![不好])像(?!样)')

BANNED_ENDINGS = ['后来我才明白']

SENTENCE_END_RE = re.compile(r'[。！？]')

SKIP_LINE_RE = re.compile(r'^(#|\s*---+\s*$|\||\*\*)')


def lint(text: str) -> tuple[list, list]:
    """返回 (violations, warnings)，每项为 (rule, line_no, message)。"""
    violations, warnings = [], []

    # 只校验自检表之前的正文
    body = text.split('**风格自检**')[0]

    simile_hits = []
    for no, raw in enumerate(body.splitlines(), start=1):
        line = raw.strip()
        if not line or SKIP_LINE_RE.match(line):
            continue

        # R1 段落（行）句数 <= 3
        n_sent = len(SENTENCE_END_RE.findall(line))
        if n_sent >= 4:
            violations.append(('R1', no, f'单行 {n_sent} 句，超过 3 句上限，须拆分'))

        # R2a 引号对话
        for _ in QUOTE_RE.finditer(line):
            violations.append(('R2', no, '对话使用引号（本风格对话不加引号）'))
            break

        # R2b 修饰对话动词
        m = MODIFIED_VERB_RE.search(line)
        if m:
            violations.append(('R2', no, f'对话动词带修饰：「{m.group()}」，只许"说/问"'))

        # R4 抒情词
        for w in EMOTION_HARD:
            if w in line:
                violations.append(('R4', no, f'抒情词/心理直述：「{w}」，转译为动作或物件'))
        for w in EMOTION_WARN:
            if w in line:
                warnings.append(('R4', no, f'评价性形容词（需人工判断语境）：「{w}」'))

        # R5 模糊量词
        for w in FUZZY_QUANTIFIERS:
            if w in line:
                violations.append(('R5', no, f'模糊量词：「{w}」，改为精确数字'))

        # R7 明喻计数
        for m in SIMILE_RE.finditer(line):
            simile_hits.append((no, line[max(0, m.start() - 4):m.end() + 6]))

        # R12 禁用收尾句式
        for w in BANNED_ENDINGS:
            if w in line:
                violations.append(('R12', no, f'禁用收尾句式：「{w}」'))

    if len(simile_hits) > 3:
        detail = '；'.join(f'L{no}…{frag}…' for no, frag in simile_hits)
        violations.append(('R7', simile_hits[0][0],
                           f'明喻 {len(simile_hits)} 处，超过 ≤3 配额：{detail}'))

    return violations, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2

    path = sys.argv[1]
    if path == '-':
        text = sys.stdin.read()
    else:
        try:
            with open(path, encoding='utf-8') as f:
                text = f.read()
        except OSError as e:
            print(f'读取失败: {e}', file=sys.stderr)
            return 2

    violations, warnings = lint(text)

    print('== justin-writing-style 机械校验 ==')
    if not violations and not warnings:
        print('PASS：可计数规则全部通过（其余规则由 LLM 自检）')
        return 0

    for rule, no, msg in violations:
        print(f'FAIL [{rule}] L{no}: {msg}')
    for rule, no, msg in warnings:
        print(f'WARN [{rule}] L{no}: {msg}')
    print(f'-- {len(violations)} violation / {len(warnings)} warning')
    return 1 if violations else 0


if __name__ == '__main__':
    sys.exit(main())
