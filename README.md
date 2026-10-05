# guessnum 猜数字

终端猜数字小游戏：电脑想一个整数，你来猜，给"太大了 / 太小了"提示。

纯 Python 标准库（argparse / secrets / json），无依赖，离线可玩。

## 快速开始

```bash
python3 -m guessnum                 # 默认猜 1-100
python3 -m guessnum --range 1-1000  # 更大范围
python3 -m guessnum --auto          # 看二分法自动求解演示
```

## 玩法

- 输入整数猜测，程序提示"太小了 / 太大了"，直到猜中。
- 输入 `q` 随时退出；`Ctrl-C` / `Ctrl-D` 也安全退出。
- 猜中后显示用时次数；最佳成绩按范围存在 `~/.config/guessnum.json`（`--score-file` 可覆盖）。

## 参数

| 参数 | 说明 |
|---|---|
| `--range 1-1000` | 猜测范围（默认 `1-100`） |
| `--target 42` | 固定答案，仅用于测试/演示 |
| `--auto` | 非交互：二分法自动求解并报告次数 |
| `--score-file PATH` | 成绩文件路径 |

## 设计取舍

- 答案用 `secrets.randbelow` 生成（密码学安全随机），不是 `random`。
- `--auto` 证明可解性：1-100 范围内二分法最多 `ceil(log2(100)) = 7` 次必中。
- 成绩文件原子写入（tmp + `os.replace`），避免中断写坏。

## 已知局限

- 纯终端交互，无图形界面。
- 最佳成绩按范围字符串记（如 `1-100`），改范围另起记录。
- 输入校验只接受整数，小数/文字会提示重输。

## 许可证

MIT，Copyright (c) 2026 ljiang9。
