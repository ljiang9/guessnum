"""guessnum 猜数字游戏：猜 1-100（可调范围），给"太大了/太小了"提示。

纯标准库，无依赖。最佳成绩存在 ~/.config/guessnum.json。
"""
import argparse
import json
import math
import os
import secrets
import sys

VERSION = "0.1.0"
DEFAULT_LOW, DEFAULT_HIGH = 1, 100


def default_score_file():
    cfg = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(cfg, "guessnum.json")


def load_scores(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_scores(path, scores):
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except OSError as e:
        print(f"警告：成绩保存失败：{e}", file=sys.stderr)


def parse_range(text):
    parts = text.split("-")
    if len(parts) != 2:
        raise ValueError("范围格式应为 低-高，例如 1-100")
    try:
        low, high = int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ValueError("范围两端必须是整数")
    if low >= high:
        raise ValueError("范围下限必须小于上限")
    return low, high


def hint(guess, target):
    if guess < target:
        return "太小了"
    if guess > target:
        return "太大了"
    return "猜中"


def auto_solve(low, high, target):
    """二分法自动求解，返回猜测次数（用于演示最优策略）。"""
    lo, hi = low, high
    tries = 0
    while lo <= hi:
        tries += 1
        mid = (lo + hi) // 2
        if mid == target:
            return tries
        if mid < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return tries  # 理论上不会到这里


def play_interactive(low, high, target, score_file):
    print(f"我想了一个 {low} 到 {high} 之间的整数，猜猜看！（输入 q 退出）")
    tries = 0
    while True:
        try:
            raw = input(f"第 {tries + 1} 次，请输入你的猜测：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n已退出。")
            return 1
        if raw.lower() in ("q", "quit", "exit", "退出"):
            print(f"答案是 {target}，下次再来！")
            return 1
        try:
            guess = int(raw)
        except ValueError:
            print("请输入一个整数（或 q 退出）。")
            continue
        if guess < low or guess > high:
            print(f"超出范围，请输入 {low} 到 {high} 之间的数。")
            continue
        tries += 1
        h = hint(guess, target)
        if h == "猜中":
            print(f"🎉 猜中了！答案就是 {target}，共用了 {tries} 次。")
            key = f"{low}-{high}"
            scores = load_scores(score_file)
            best = scores.get(key)
            if best is None or tries < best:
                scores[key] = tries
                save_scores(score_file, scores)
                print(f"🏆 新纪录！{low}-{high} 范围最佳成绩：{tries} 次。")
            else:
                print(f"该范围最佳成绩：{best} 次。")
            return 0
        print(f"{h}，再试试！")


def main(argv=None):
    p = argparse.ArgumentParser(prog="guessnum", description="猜数字游戏：猜 1-100，给大小提示。")
    p.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    p.add_argument("--range", dest="range", default="1-100", help="猜测范围，格式 低-高（默认 1-100）")
    p.add_argument("--target", type=int, default=None, help="固定答案（仅用于测试/演示）")
    p.add_argument("--auto", action="store_true", help="二分法自动求解演示（非交互）")
    p.add_argument("--score-file", default=None, help="成绩文件路径（默认 ~/.config/guessnum.json）")
    args = p.parse_args(argv)

    try:
        low, high = parse_range(args.range)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    score_file = args.score_file or default_score_file()

    if args.target is not None:
        if args.target < low or args.target > high:
            print(f"error: --target {args.target} 不在范围 {low}-{high} 内", file=sys.stderr)
            return 2
        target = args.target
    else:
        target = secrets.randbelow(high - low + 1) + low

    if args.auto:
        tries = auto_solve(low, high, target)
        bound = math.ceil(math.log2(high - low + 1))
        print(f"答案：{target}（范围 {low}-{high}）")
        print(f"二分法用了 {tries} 次猜中（理论上限 {bound} 次）。")
        return 0

    return play_interactive(low, high, target, score_file)


if __name__ == "__main__":
    sys.exit(main())
