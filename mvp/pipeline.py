#!/usr/bin/env python3
"""定義②判定パイプライン: 気象庁 rank_update CSV → 最上位イベントJSON

定義②: 観測史上1位の記録が更新され、かつ「これまでの記録」が T 年以上前のもの。
カード文言: 「◯◯年間破られなかった記録が、今日更新されました」

【重要な前提】この環境からJMAへ到達できないため、COLUMN_MAP は想定スキーマ。
実物の rank_update CSV のヘッダに合わせて COLUMN_MAP だけ直せば動く設計。
"""
import csv, json, re, sys
from pathlib import Path

THRESHOLD_YEARS = 30          # 全国1枚カードの閾値（定義②のT）
TARGET_ELEMENTS = {"日最高気温"}  # 初版は日最高気温のみ

# 実CSVのヘッダ名に合わせてここだけ修正する
COLUMN_MAP = {
    "pref":       "都道府県",
    "station":    "地点",
    "element":    "要素",
    "new_value":  "更新値",
    "new_date":   "起日",        # 新記録の日付
    "old_value":  "これまでの記録",
    "old_date":   "これまでの起日",  # 旧記録の日付
}

def parse_year(s: str):
    m = re.search(r"(\d{4})", s or "")
    return int(m.group(1)) if m else None

def load_events(path: str):
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                el = row[COLUMN_MAP["element"]].strip()
                if el not in TARGET_ELEMENTS:
                    continue
                ny, oy = parse_year(row[COLUMN_MAP["new_date"]]), parse_year(row[COLUMN_MAP["old_date"]])
                if ny is None or oy is None:
                    continue
                years = ny - oy
                if years < THRESHOLD_YEARS:
                    continue
                yield {
                    "pref": row[COLUMN_MAP["pref"]].strip(),
                    "station": row[COLUMN_MAP["station"]].strip(),
                    "element": el,
                    "new_value": row[COLUMN_MAP["new_value"]].strip(),
                    "new_date": row[COLUMN_MAP["new_date"]].strip(),
                    "old_value": row[COLUMN_MAP["old_value"]].strip(),
                    "old_date": row[COLUMN_MAP["old_date"]].strip(),
                    "years_stood": years,
                }
            except KeyError as e:
                sys.exit(f"列が見つかりません: {e} — COLUMN_MAP を実CSVのヘッダに合わせてください")

def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "sample_rank_update.csv"
    events = sorted(load_events(src), key=lambda e: -e["years_stood"])
    if not events:
        print(json.dumps({"event": None, "note": f"閾値{THRESHOLD_YEARS}年を超えるイベントなし"}, ensure_ascii=False))
        return
    top = events[0]
    Path("out").mkdir(exist_ok=True)
    Path("out/event.json").write_text(json.dumps(top, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"qualifying events: {len(events)}; top: {top['pref']} {top['station']} {top['years_stood']}年 → out/event.json")

if __name__ == "__main__":
    main()
