# 何年ぶり記録簿（仮）MVP — 全国1枚カード

定義②「観測史上1位の記録が更新され、かつ前記録がT年以上前」を判定し、
OGPサイズ(1200×630)のシェアカードを生成する最小パイプライン。

## 構成
- `pipeline.py` — rank_update CSV → 定義②フィルタ(閾値30年・日最高気温のみ) → 最上位イベントを `out/event.json` に出力
- `card.html` — カードテンプレート（Noto Sans CJK / 1200×630 / 固定ライト）
- `render_card.py` — event.json + card.html → `out/card.png`（Playwright + Chromium）
- `sample_rank_update.csv` — 想定スキーマのサンプル（実データ取得不可環境用）

## 実データで動かす手順（要・ネット到達環境）
1. 気象庁「観測史上1位の値 更新状況」のCSV（rank_update）を取得
2. **実CSVのヘッダを確認し、`pipeline.py` 冒頭の `COLUMN_MAP` をそのヘッダ名に合わせる**（ここだけが未確定の前提）
3. `python3 pipeline.py rank_update.csv && python3 render_card.py`

## 設計上の決定（2026-08-31確定）
- 全国1枚/日のみ。町別ページ・記念証・OGP自動化はこの範囲に含めない
- 統計切断の扱いはJMAのrank_update側の記録判定に委譲（JMAが正）
  → 町別ページ・記念証の段階で初めて自前の在庫表（代表地点・継続年数・切断）が必要になる
- 文言は定義②に固定:「◯◯年間破られなかった記録が、今日更新されました」
- 未来形の文言は使わない（気象業務法ガードレール）

## 依存
`apt install fonts-noto-cjk` / `pip install playwright`（Chromiumは既存のものをexecutable_pathで検出）
