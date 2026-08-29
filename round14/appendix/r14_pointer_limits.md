# R14 / ポインタ型アーキテクチャの限界検証

**調査日：2026-08-29**（本文中の全URLの確認日は同日。個別に異なる場合のみ明記）
**担当：ポインタ型アーキテクチャ限界検証エージェント**
**対象：日本在住ソロエンジニアが「運用コストをほぼゼロに保つ地図サービス」を作る場合に、実際にどこで破綻するか**
**為替前提：1 USD = 159.55 JPY**（R13 と共通。出典 <https://tradingeconomics.com/japan/currency>、R13 取得日 2026-08-28）

---

## 0. 結論サマリー（先に読む5行）

1. **ホスティングは本当にゼロ円になる。Cloudflare Pages の静的アセットはリクエストも帯域も無制限で無料（一次確認）。破綻するのはホスティングではない。**
2. **破綻するのは YouTube のクォータ。** search.list は1回100ユニット、無料枠は1日10,000ユニット。**地理探索（location+locationRadius、半径上限1,000km）で全球を1回スイープするだけで15,000〜30,000ユニット＝1.5〜3日分を消費する。「世界中のライブを自動発見して常時更新する」は構造的に不可能。** 無料枠で成立するのは「既知の数百〜2,000本を5〜15分間隔で生死確認する」までで、これが worldwatcher.live が "hundreds" に留まる理由。
3. **Twitch は逆に完全に足りる。** 同時配信約9.3〜9.7万chを Get Streams（100件/ページ、800 req/分）で**約1.2分で全件列挙**できる。ポインタ型ライブ配信マップの主軸は YouTube ではなく Twitch にならざるを得ない。ただし Twitch は**位置情報を持たない**。
4. **収益化は規約で塞がれている。** YouTube Developer Terms は「YouTube API Data を含むページでの広告販売」を、"YouTube API Data を取り除いても広告を正当化できる独立した価値"が同ページにない限り禁止し、「埋め込みプレーヤでの視聴への課金」を明示的に禁止する（一次相当・原文引用あり）。さらに **Non-Authorized Data は30日を超えて保持できない**＝「時系列を貯めて堀にする」戦略が規約で封じられている。
5. **不動産×ポインタ型は成立しない。** 画像をやめても月額は S規模で**月90円**、L規模で**月$102（約1.6万円）**しか下がらない。残るコストは全部「データを持つコスト」で、ポインタ型はそこに一切効かない。しかも中核価値（押すと室内写真）を外部に投げることになり、入口の問題（在庫データをどう取るか）は1ミリも解決しない。

---

## 【重要・調査上の制約の開示】

本セッションの egress プロキシは、curl による直接アクセスを全面的に拒否し（example.com ですら CONNECT 403）、WebFetch も多くのホストをブロックした。**ブロックされた主要ホスト**：

`developers.google.com`（YouTube ToS/Developer Policies/クォータ表の一次ソース）、`lucent.earth`、`dev.twitch.tv`、`legal.twitch.com`、`www.twitch.tv`、`vercel.com`、`docs.github.com`、`developers.cloudflare.com`、`api.radio-browser.info`、`www.zillow.com`、`en.wikipedia.org`、`googlemapsmania.blogspot.com`、`huggingface.co`、`youtubehelp.fandom.com`、`labs.polsys.net`、`studiosupport.liveu.tv`、`elfsight.com`、`www.getphyllo.com`、`outlierkit.com`、`www.socialcrawl.dev`、`news.ycombinator.com`、`curia.europa.eu`、`www.courts.go.jp`

**到達できたホスト**：`github.com` / `raw.githubusercontent.com` / GitHub Code Search API、および WebSearch（検索エンジン経由の要約）。

したがって本レポートの一次ソースは以下の2経路に限られる：

- **経路A（一次相当）**：`OpenTermsArchive/pga-snapshots` リポジトリに保存された **YouTube Developer Terms の HTML スナップショット原文**（commit `35bb781e26d377cbce290c9b1a47fe1b71ba8f92`、パス `YouTube/Developer Terms.html`）。GitHub Code Search で原文断片を逐語取得した。**本レポートで「原文引用」と記したものはすべてこの経路で取得した実テキストである。** ただしスナップショット取得日はアーカイブ側の管理下にあり本セッションでは特定できていない。
- **経路B（一次）**：`raw.githubusercontent.com/cloudflare/cloudflare-docs/production/...` に置かれた **Cloudflare 公式ドキュメントのソース Markdown**（Workers pricing / Workers limits / Pages limits / Pages Functions pricing / R2 pricing）。

**それ以外はすべて［二次確認］**（検索エンジンの要約経由）である。実運用の意思決定前に、各ベンダーの公式ページを自分の目で再確認すること。

---

# 1. 検証1：lucent.earth 型は本当に月 $0〜20 で回るのか

## 1-1. YouTube Data API のクォータ：数字で詰める

### 確定している数値

| 項目 | 値 | 出典 |
|---|---|---|
| デフォルト日次クォータ | **10,000 ユニット/日/プロジェクト**、リセットは太平洋時間の深夜 | ［二次確認］<https://www.socialcrawl.dev/blog/youtube-data-api-2026>、コード内定数として <https://github.com/antonmarklundcom/yt/blob/main/src/lib/youtube/quota.ts>（"daily reset (midnight America/Los_Angeles)"） |
| `search.list` | **100 ユニット** | ［独立3ソースで一致］<https://github.com/superdesigndev/treg/blob/main/scripts/catalog_ingest.py>（`YT_QUOTA = {"youtube.search.list": 100, ...}`）、<https://github.com/ksjpswaroop/Cutroom/blob/main/server/youtube-quota.ts>（`"search.list": 100`）、<https://github.com/HailBahafi/InfluenceRadar>（"``search.list`` burned through in 100 calls"） |
| `videos.list` | **1 ユニット** | 同上（`"videos.list": 1`） |
| `playlistItems.list` / `channels.list` | **1 ユニット** | 同上 |
| `captions.list` | **50 ユニット** | 同上 |
| `videos.list` の `id` パラメータ | **最大50件のカンマ区切り**。51件以上は即エラー | ［二次確認］<https://www.technetexperts.com/youtube-api-videos-list-id-limit/> |
| `search.list` の1ページ | **最大50件**。ページ送りごとに再度100ユニット | ［二次確認］<https://developers.google.com/youtube/v3/docs/search/list>（検索経由） |
| 地理検索 `location` + `locationRadius` | 両方必須。**半径は1,000kmを超えられない**。`type=video` 必須 | ［二次確認］<https://googleapis.dev/java/google-api-services-youtube/v3-rev20241010-2.0.0/com/google/api/services/youtube/YouTube.Search.List.html>（"The API does not support locationRadius parameter values larger than 1000 kilometers"） |

> **注意**：一部の二次情報（unbrowse.ai 等）が「video detail request は3〜5ユニット」と書いているが、これは v3 が2019年に廃止した「part別課金」時代の記述と思われる。**独立した3つの実装コードがいずれも `videos.list = 1` としており、こちらを採る。**

### (A) 「発見」の数学 ― ここで確実に破綻する

- 1日に打てる `search.list` は **10,000 ÷ 100 = 100回**。
- 1回50件なので、**全クォータを発見だけに使い切って理論最大5,000件/日**。更新には1ユニットも残らない。
- 地理探索で全球を覆う場合：
  - 半径1,000kmの円1つの面積 = π × 1,000² ≈ **314万 km²**
  - 地球の陸地面積 ≈ **1億4,900万 km²**
  - 重なりゼロの理想値で **47円**。実際は緯度による歪み・海域除外の粗さ・重複を見込んで **150〜300円**が必要。
  - → **全球1スイープ = 150〜300 calls = 15,000〜30,000 ユニット = 1.5〜3日分のクォータ**
- **結論：1日1回の全球スイープすら物理的にできない。** しかも各円で50件を超えれば追加ページごとにさらに100ユニット。
- 加えて、ライブ配信の寿命は数時間である。**1日1回でも遅すぎるのに、その1回すら打てない。**

### (B) 「更新」の数学 ― ここだけは無料枠で回る

`videos.list`（50件/1ユニット）で追跡中N本の生死・視聴者数を間隔T分で確認する場合：

消費ユニット/日 = ⌈N/50⌉ × (1440/T)

| 追跡本数 N | 更新間隔 T | 消費ユニット/日 | 残りで打てる search.list |
|---|---|---|---|
| 300 | 1分 | 8,640 | 13回 |
| 500 | 2分 | 7,200 | 28回 |
| **1,000** | **5分** | **5,760** | **42回** |
| 2,000 | 5分 | 11,520 | **超過（不可）** |
| 2,000 | 10分 | 5,760 | 42回 |
| 5,000 | 15分 | 9,600 | 4回 |
| 10,000 | 30分 | 9,600 | 4回 |
| 20,000 | 60分 | 9,600 | 4回 |

**判定：無料クォータ10,000/日で成立するのは「既知の数百〜2,000本を5〜15分間隔で生死確認する」運用まで。**
それ以上は、更新頻度を犠牲にするか、本数を犠牲にするかの二択になる。

**この数字が現実のサービス設計をそのまま説明している。** World Watcher は「hundreds of YouTube live streams across every continent」と自称している（［二次確認］<https://worldwatcher.live/>、検索経由）。これは能力の限界ではなく、**クォータが許す設計上限そのもの**である。

## 1-2. クォータ増枠申請の実際

**規約原文（一次相当、OpenTermsArchive スナップショット）**：

> "If your API Client reaches the quota limit for a service, you can apply for a quota extension by completing an **API Compliance Audit** where you must specify the use case for which you need the extension."

**実際の運用（［二次確認］）**：

| 事実 | 出典（確認日 2026-08-29） |
|---|---|
| 申請には **YouTube API Services - Audit and Quota Extension Form** の提出と、Google による手動審査が必要 | <https://www.getphyllo.com/post/is-the-youtube-api-free-in-2026-quota-limits-costs-when-to-pay> |
| **待ち時間は数週間〜数カ月**。公開コミュニティスレッドに **5カ月**の遅延事例 | 同上 |
| **スクレイパー / 一括データ収集 / 競合分析の用途は頻繁に却下される** | 同上、<https://www.socialcrawl.dev/blog/youtube-data-api-2026> |
| 却下の典型理由：用途が曖昧、公開プライバシーポリシーがない、スクレイピングに見える自動化、一括ダウンロードツールに見える | 同上 |
| **承認されても要求より低い枠になることがある**。定義された期限を持つ異議申立て手段は存在しない | 同上 |
| 増枠自体は**無料**（ユニット単位の課金は存在しない） | 同上 |
| 「1分あたりのユーザー毎クエリ数」は変更できず、**変えられるのは日次クォータのみ** | 同上 |

**「世界中のライブ配信を地図にマップする」という用途は、Google の目からは「一括データ収集」に極めて近い。** 却下リスクは実務上高いと見るべきである。

**さらに、規約原文（一次相当）に「休眠でクォータを失う」条項がある**：

> "YouTube reserves the right to disable or curtail your access to, or use of, specific YouTube API Services **if your API Project has been inactive for 90 consecutive days**. For example, YouTube could revoke your API Credentials, or reduce (or eliminate) your API Project's quotas..."

→ **一度取った増枠は、90日使わなければ剥奪されうる。** ソロの「作って放置」運用と相性が悪い。

## 1-3. 実際の運用者は何をしているのか（5パターン）

| # | 手法 | クォータ | 規約 | 実例・評価 |
|---|---|---|---|---|
| 1 | **キュレーション済みID表 + `videos.list`** | 500本を2分間隔で 7,200 units/日 | ◎ 完全適法 | worldwatcher.live 型。**本命。** ただし「発見」を人力で担う＝キュレーションが労働として残る |
| 2 | **チャンネルRSS（`feeds/videos.xml`）** | **クォータ消費ゼロ・APIキー不要** | ○（公開フィード） | ［二次確認］<https://philippdubach.com/posts/degoogling-cost-me-my-youtube-feed-so-i-made-my-own/>、<https://deepwiki.com/DIYgod/RSSHub/6.3-youtube-integration>。新着検知には使えるが**ライブ中かどうかは分からない**ので `videos.list` との併用が必要 |
| 3 | **クォータ増枠申請（API Compliance Audit）** | 承認されれば拡大 | ◎ | 数週間〜数カ月、却下率不明、この用途は却下されやすい |
| 4 | **InnerTube / youtubei.js / yt-dlp** | **無制限（非公式内部API）** | **✗ 規約違反** | ［二次確認］<https://dev.to/0012303/youtube-has-a-hidden-api-that-needs-no-api-key-here-is-how-to-use-it-2n9e>。ToS の "will not exceed or circumvent use or quota restrictions" に真正面から抵触。**アカウント停止・IPブロック・法的リスク。ソロが事業として乗せる基盤ではない** |
| 5 | **ユーザー投稿型** | 発見コストをユーザーに転嫁 | ◎ | LiveMap（Google Play）は「explore global YouTube live streams on a map **or add their own**」と明記［二次確認］<https://play.google.com/store/apps/details?id=com.worldyoutubelive>。**後述する"堀"の話とも直結する最重要パターン** |

**やってはいけないこと（規約原文で確認）**：複数の GCP プロジェクトに分散して枠を稼ぐ「シャーディング」。Developer Policies は **1 API Client につき API Project は厳密に1つ**と定め、これに反すると**正規のものを含む全プロジェクトが停止される**（［二次確認］<https://developers.google.com/youtube/terms/developer-policies-guide>、検索経由。<https://github.com/ThioJoe/YT-Spammer-Purge/discussions/937> にコミュニティでの議論あり）。

## 1-4. 他の候補API：レート制限と「世界地図を常時更新する」用途への適合

| API | 認証 | レート制限 | 全球1スイープの所要 | 位置情報 | ポインタ型適合 |
|---|---|---|---|---|---|
| **YouTube Data v3** | APIキー | 10,000 units/日 | **1.5〜3日**（不可能） | ✗（`location` は動画側の任意メタデータで、付いている動画はごく少数） | **✗ 発見に使えない** |
| **Twitch Helix** | App Access Token（client credentials） | **トークンバケット 800ポイント/分**、1リクエスト=1ポイント（デフォルト） | 同時配信 **9.33万〜9.72万ch**（2026）÷ 100件/ページ = **972 req → 約1.2分** | ✗（title/tag/RealtimeIRL から推定するしかない） | **◎ 発見も更新も余裕** |
| **Kick Public API v1** | OAuth 2.1 (PKCE)、トークン1時間 | **公開情報なし・不透明**。`GET https://api.kick.com/public/v1/livestreams` | 不明 | ✗ | △ 動くが不確実 |
| **Radio Browser** | **不要** | **明示的な上限なし。2〜3 req/秒が推奨**。descriptive User-Agent（`AppName/1.2`）を送ることが求められる。**CORS対応でブラウザから直接叩ける** | 45,000局。全カタログのダウンロード・自前ミラーも許可 | **◎ 局に国・州・緯度経度が付いている** | **◎ ポインタ型の理想形** |

**Twitch の余裕を数字で**：5分間隔で全ch更新 = 972 req × 288回 = **279,936 req/日 = 平均194 req/分**。制限800 req/分の **24%** しか使わない。

**Twitch 出典**（いずれも［二次確認］、確認日 2026-08-29）：
- レート制限：<https://dev.twitch.tv/docs/api/guide>（"token-bucket algorithm... default limit is approximately 800 requests per minute"）、<https://discuss.dev.twitch.com/t/helix-api-rate-limits/24854>
- ページング：Get Streams はデフォルト20件・**最大100件**、`pagination.cursor` を `after` に渡す
- 同時配信ch数：<https://twitchtracker.com/statistics>、<https://www.demandsage.com/twitch-users/>（2026年 平均同時配信ch **93,300〜97,200**）

**Radio Browser 出典**（［二次確認］、確認日 2026-08-29）：<https://api.radio-browser.info/>、<https://docs.radio-browser.info/>、<https://github.com/AnowHosting/radio-browser-api-documentation>、<https://github.com/api-evangelist/radio-browser>
サーバ発見は `all.api.radio-browser.info` の DNS ラウンドロビン、または `_api._tcp.radio-browser.info` の SRV レコード。失敗時は次のサーバへリトライする作法。

**この表が示す構造的事実：**

> **「発見（discovery）」を無料で許すAPIと、許さないAPIがある。Twitch と Radio Browser は許す。YouTube は許さない。ポインタ型サービスの成否は、この一点でほぼ決まる。**

lucent.earth が Twitch / YouTube / Kick を並べているのは網羅性のためだろうが、**技術的には Twitch が主・YouTube が従にならざるを得ない。**

## 1-5. 静的ホスティングの無料枠と、地図サービスがそれを超える条件

### 一次確認（Cloudflare 公式ドキュメントのソース Markdown）

**Cloudflare Pages**（<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/pages/platform/limits.mdx>、確認日 2026-08-29）

| 項目 | Free | Pro | Business |
|---|---|---|---|
| ビルド回数 | **500 / 月** | 5,000 | 20,000 |
| サイトあたりファイル数 | **20,000** | 100,000 | 100,000 |
| 単一アセット最大サイズ | **25 MiB** | 同 | 同 |
| プロジェクト数 | **100 / アカウント** | 同 | 同 |
| カスタムドメイン/プロジェクト | 100 | 250 | 500 |
| ビルド時間上限 | 20分 | 同 | 同 |
| 帯域・リクエスト | **記載なし＝制限なし** | — | — |

**Cloudflare Pages Functions 課金**（<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/pages/functions/pricing.mdx>、同日）

> - Free: **100,000 daily requests shared with Workers**（"you could use 50,000 Functions requests and 50,000 Workers requests to use your full 100,000 daily request usage"）
> - リセットは **midnight UTC**
> - **静的アセットは完全に無料・無制限で、クォータにカウントされない**

**Cloudflare Workers 課金**（<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/workers/platform/pricing.mdx>、同日）

| | Free | Paid |
|---|---|---|
| リクエスト | **100,000 / 日** | **$5/月**に1,000万/月込み、超過 **$0.30 / 100万** |
| CPU時間 | 10ms / 呼び出し | 3,000万 CPU-ms 込み、超過 **$0.02 / 100万 CPU-ms** |
| 実行時間（duration） | 課金なし | 課金・上限なし |
| **静的アセットへのリクエスト** | **無料・無制限** | **無料・無制限** |
| データ転送（egress）／帯域 | 追加課金なし | **追加課金なし** |

**Cloudflare Workers 制限**（<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/workers/platform/limits.mdx>、同日）

| | Free | Paid |
|---|---|---|
| リクエスト/日 | **100,000** | 無制限 |
| サブリクエスト | **50 / リクエスト** | 10,000（拡張で1,000万） |
| メモリ | 128 MB / isolate | 同 |
| **Cron Triggers / アカウント** | **5** | 250 |
| Worker数 / アカウント | 100 | 500 |
| 環境変数 | 64（各5KB） | 128 |
| スクリプトサイズ（圧縮後） | 3 MB | 10 MB |
| 起動時間 | 1秒 | 同 |

超過時：**Error 1027**。ルートの fail mode 設定により「Worker をバイパス（fail open）」か「1027 エラーページを返す（fail closed）」（［二次確認］<https://community.cloudflare.com/t/error-1027-when-i-load-my-worker-but-i-dont-see-how-it-has-exceeded-the-100-000-request-limit/331056>）。エラー文言は "This website has been temporarily rate limited. You cannot access this site because the owner has reached their plan limits."

**Cloudflare R2**（<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/r2/pricing.mdx>、同日）

| | 単価 | 無料枠/月 |
|---|---|---|
| Standard ストレージ | $0.015 / GB-月 | **10 GB-月** |
| Class A（書込系） | $4.50 / 100万 | **100万** |
| Class B（読取系） | $0.36 / 100万 | **1,000万** |
| **Egress** | **無料** | 無制限 |

※「Cloudflare は使用量を次の課金単位に切り上げる」（1.1GB → 2GB-月として課金）と明記されている。

### 他社（［二次確認］）

| プラットフォーム | 無料枠 | 超過時の挙動 | 出典（確認日 2026-08-29） |
|---|---|---|---|
| **GitHub Pages** | 帯域 **100GB/月（ソフト）**、公開サイト **1GB以下**、ビルド **10回/時（ソフト）** | 自動遮断はしない。「サイトを配信できないことがある」＋ GitHub Support から CDN 導入・移行を勧めるメール | <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits>（検索経由）、<https://github.com/orgs/community/discussions/22155>、<https://supadrop.host/blog/github-pages-limits/> |
| **Vercel Hobby** | 帯域 100GB/月、Function実行 10万/月、実行時間10秒 | **超過課金の仕組みが存在しない＝30日ローリング窓がリセットされるまでデプロイが一時停止** | <https://flexprice.io/blog/vercel-pricing-breakdown>、<https://temps.sh/blog/vercel-pricing-complete-guide-2026> |
| **Vercel Pro** | $20/開発者/月 | 従量課金。実例：**HN一面で24h・5万訪問 → 帯域超過 $1,141**／クローラが8.4TB取得 → $1,477（うち帯域$1,267）／DDoS → **$23,000** | <https://deploybase.app/blog/vercel-bill-shock-1100-bandwidth-costs-alternatives-2026>、<https://usagebox.com/articles/vercel-23000-dollar-bill-usage-based-platform-bill-shock-2026>、<https://bex.co/blog/2026/07/31/vercel-bandwidth-bill-shock> |
| **Netlify Free** | **2026-04-14 に帯域のクレジット単価が倍化。300クレジット/月・20クレジット/GB → 実質 約15GB/月** | **ハード300クレジットキャップ。課金されず停止する** | <https://temps.sh/compare/vs-netlify>、<https://flexprice.io/blog/complete-guide-to-netlify-pricing-and-plans>、<https://costbench.com/software/developer-tools/netlify-dev/free-plan/> |
| **Netlify 超過単価** | — | **$55 / 追加100GB（≒$0.55/GB）**。Pro はクレジット枯渇時に1,500クレジット$10（≒75GB）で自動チャージ | 同上 |
| **GitHub Actions** | **パブリックリポジトリは標準ランナー無制限・無料**。プライベートは Free プランで 2,000分/月 + 500MB | 新規Freeアカウントは支出上限$0がデフォルトなので、私有リポジトリは**停止するだけで課金されない** | <https://docs.github.com/billing/managing-billing-for-github-actions/about-billing-for-github-actions>（検索経由）、<https://github.com/orgs/community/discussions/26054>、<https://cicdcalculator.com/github-actions-free-tier> |

### 地図サービスが無料枠を超える条件

**ポインタ型（＝画像も動画も持たない）1セッションの転送量モデル：**

| 内訳 | 初回訪問 | 再訪（キャッシュ後） |
|---|---|---|
| HTML + JS バンドル（MapLibre / three.js） | 300 KB | 0 |
| 地球テクスチャ（3Dグローブ方式・単一画像） | 2,000 KB | 0 |
| データJSON（数千ピンの座標＋メタ、gzip後） | 200 KB | 200 KB |
| ベースマップのベクタータイル（2D地図方式を採る場合） | 3,000〜7,500 KB | 大部分キャッシュ |
| **合計（3Dグローブ方式）** | **約2.5 MB** | **約0.2 MB** |
| **合計（2D地図方式）** | **約5.5〜10 MB** | **約0.5 MB** |

**無料枠を超える訪問者数（初回訪問のみで計算＝最悪ケース）**

| プラットフォーム | 上限 | 3Dグローブ方式（2.5MB） | 2D地図方式（8MB） |
|---|---|---|---|
| Cloudflare Pages（静的のみ） | **なし** | **無制限** | **無制限** |
| GitHub Pages | 100GB/月（ソフト） | 約 **40,000 人/月** | 約 **12,500 人/月** |
| Vercel Hobby | 100GB/月 | 約 **40,000 人/月**で停止 | 約 **12,500 人/月**で停止 |
| Netlify Free（2026-04以降） | 約15GB/月 | 約 **6,000 人/月**で停止 | 約 **1,900 人/月**で停止 |

**→ Netlify Free は2026年4月の変更で、地図サービスには事実上使えなくなった。** GitHub Pages と Vercel Hobby も「月4万人」で頭打ち。**Cloudflare Pages だけが構造的に無制限。**

**ただし Functions / Workers を1つでも挟むと、10万req/日の壁が立つ。** ポインタ型で「$0を維持する」最重要の設計判断は、**Worker を一切使わず、静的アセットだけで完結させること**である。

## 1-6. バズった日のコスト

### HN 一面のトラフィック実測（［二次確認］、確認日 2026-08-29）

| 指標 | 値 | 出典 |
|---|---|---|
| 一面20時間の典型 | **15,000 uniques / 18,000 PV** | <https://blog.royalsloth.eu/posts/how-much-traffic-comes-from-the-front-page-of-hackernews/> |
| 別の記録 | 最初の20時間で **85,000 requests / 43,000 uniques** | <https://harrisonbroadbent.com/blog/hacker-news-traffic-spike-anatomy/> |
| 経験則 | **50 uniques/分 ≈ 3,000/時 ≈ 72,000/日** | <https://marcotm.com/articles/stats-of-being-on-the-hacker-news-front-page/> |
| 記録された帯域スパイク | **233 GB**（推定3万 uniques） | <https://www.vincentschmalbach.com/analyzing-a-year-of-hacker-news-traffic/> |
| 変動幅 | 3,500 〜 160,000+ PV | <https://luke.hsiao.dev/blog/2023-hn-traffic/> |

### バズ日の実額（3Dグローブ方式・初回訪問2.5MB、uniques 43,000 を想定 → 約107GB）

| ホスティング | バズ日のコスト | 挙動 |
|---|---|---|
| **Cloudflare Pages（静的のみ）** | **$0** | 無傷 |
| **Cloudflare Workers Free を挟んだ場合** | $0 | **10万req/日で Error 1027**。43,000人が平均3リクエスト打てば12.9万req → **昼過ぎに落ちる** |
| GitHub Pages | $0 | 100GB ソフト上限をわずかに超過 → 警告メール |
| Vercel Hobby | $0 | **100GBで停止**。バズの最中にサイトが消える |
| Vercel Pro | 実例ベースで **$300〜1,141** | 課金される（前掲の "50,000 visitors in 24 hours → $1,141" が最も近い実例） |
| Netlify Free | $0 | **6,000人（バズ開始から約2時間）で停止** |
| Netlify Pro | 107GB ≒ $59（$0.55/GB） | 自動チャージ |

### **しかし、本当に死ぬのは帯域ではなくAPIクォータである**

もしクライアント（ブラウザ）から直接 YouTube Data API を叩く設計にしていた場合：

- 訪問者1人が地図を開くたび `videos.list`（50ID）を1回 = **1ユニット**
- 43,000 uniques × 1 = **43,000ユニット = 無料枠10,000の 4.3倍**
- → **その日の朝10,000人目でクォータが尽き、以降の全ユーザーが空の地図を見る**
- `search.list` を1回でも打つ設計なら **100人で死ぬ**

**さらに、クライアントから叩く時点で API キーがブラウザに露出しており、第三者に無断使用されればバズを待たずに枯れる。**（Twitch の App Access Token も同様に、client credentials フローはクライアント側に置けない。）

> ### **ポインタ型のバズ耐性の結論**
> **「APIをクライアントから叩かない。cron で焼いた静的JSONだけを配る。」**
> これを守れば、バズ日のコストは帯域だけの問題になり、**Cloudflare Pages なら $0**。
> 守らなければ、**ホスティングが無傷でもサービスは死ぬ。**

---

# 2. 検証2：埋め込みの規約リスク

## 2-1. YouTube ― 原文で確認した条項

以下は **OpenTermsArchive/pga-snapshots の `YouTube/Developer Terms.html`（commit 35bb781）から GitHub Code Search で逐語取得した原文**である（一次相当）。

### (a) 広告・収益化

> "**sell advertising, sponsorships, or promotions on any page or screen that contains YouTube API Data unless other data, content, or material not obtained from YouTube appears on the same page and offers enough independent value to justify such sales if the YouTube API Data were removed.**"

> "**sell advertising, sponsorships, or promotions that are placed on or within YouTube audiovisual content or the YouTube player without YouTube's prior written approval;**"

### (b) 課金・ゲーティング

> "**API Clients must not charge users to watch content in an embedded YouTube player.**"

> "**API Clients must not otherwise gate access to a video by requiring a user to take an action other than clicking the play button to view or continue playing YouTube audiovisual content.** For example, API Clients must not require a user to subscribe to a channel or like a video to continue watching YouTube audiovisual content."

### (c) データ保存 ― **30日ルール**

> "**API Clients may temporarily store limited amounts of Non-Authorized Data for as long as is necessary for the purposes of the API Client but not longer than 30 calendar days.** As in section (III.E.4.c) immediately above, this means that after 30 calendar days, the API Client must either delete or refresh the stored data."

（併せて Authorized Data 側）
> "API Clients may store all other types of Authorized Data not identified in section (III.E.4.b) for as long as is necessary for the purposes of the specific consent granted by an active user and **for no longer than 30 calendar days. After 30 calendar days, the API Client must either delete or refresh the stored data.**"

**Non-Authorized Data = APIキーで取得できる公開データ（動画メタデータ、チャンネル情報、ライブ状態など）。つまり「YouTubeのライブ配信情報を31日以上保持すること自体が規約違反」である。**

### (d) 休眠によるクォータ剥奪

> "YouTube reserves the right to disable or curtail your access to, or use of, specific YouTube API Services **if your API Project has been inactive for 90 consecutive days.** For example, YouTube could revoke your API Credentials, or reduce (or eliminate) your API Project's quotas for specific YouTube API Services."

### (e) 機能制限の禁止

> "An API Client should not limit or reduce the functionality of a YouTube feature unless that limitation is a core aspect... of the API Client itself and that YouTube feature is not required by the RMF ('Permitted Feature Limitation')."

### 二次確認どまりの条項（developers.google.com がブロックされたため）

| 条項 | 内容 | 出典（確認日 2026-08-29） |
|---|---|---|
| 埋め込みプレーヤの最小サイズ | **ビューポート 200px × 200px 以上**。コントロールを表示する場合はそれを完全に表示できる大きさが必要。16:9 なら **480×270px 以上を推奨** | <https://developers.google.com/youtube/terms/required-minimum-functionality>（検索経由） |
| 自動再生 | プレーヤが**画面内で50%超可視になるまで自動再生を開始してはならない** | 同上 |
| **同時自動再生** | **1ページ／1画面に、自動再生するYouTubeプレーヤは1つまで** | 同上 |
| Referer 必須 | 埋め込みプレーヤを使う API Client は **HTTP Referer ヘッダで身元を示さねばならない**。欠けていると再生がブロックされエラー画面になる | <https://support.google.com/youtube/answer/171780> ほか（検索経由） |
| Attribution | YouTube が提供する帰属表示（埋め込みプレーヤ内のものを含む）を直接・間接に妨害・隠蔽してはならない | <https://developers.google.com/youtube/terms/developer-policies>（検索経由） |
| 1 API Client = 1 API Project | 複数アプリ／複数GCPプロジェクトで人為的にクォータを増やす「シャーディング」は禁止。違反すると**正規のものを含む全プロジェクトが停止** | <https://developers.google.com/youtube/terms/developer-policies-guide>（検索経由） |
| derived metrics 例外 | 監査済み開発者がアナリティクス用途でクォータ拡張申請を通じて明示許可を得た場合のみ、統計データを30日超保存できる（**2026-06-01以降**の運用） | <https://developers.google.com/youtube/terms/derived-metrics-policy>（検索経由） |

### 「地図UIに大量のプレーヤーを並べる行為」の判定

| 行為 | 判定 | 根拠 |
|---|---|---|
| 地図上のピンをクリックすると1つのプレーヤが開く | **○ 適法** | 標準的な埋め込み利用 |
| サムネイル代わりに小さな iframe を大量に敷き詰める | **△〜✗** | **各プレーヤは200×200px以上が必要**。地図上に多数並べるとこれを割りやすい |
| 複数プレーヤを同時に自動再生（"live wall" UI） | **✗ 明確に違反** | 「1ページに自動再生するプレーヤは1つまで」 |
| プレーヤの上にオーバーレイを重ねる／帰属表示を隠す | **✗** | attribution 妨害の禁止 |
| ピンをクリックする前に「フォローしろ」「登録しろ」を挟む | **✗** | ゲーティング禁止条項の原文に直接該当 |
| **自サイトに広告を置く** | **✗ 原則違反。例外の立証責任は自分側** | 「YouTube API Data を取り除いても広告を正当化できる独立した価値」が同じページに必要 |
| **サブスクで有料化する** | **✗ 明確に違反** | "must not charge users to watch content in an embedded YouTube player" |

> ### **収益化に関する冷徹な結論**
> **「YouTubeのライブ配信を地図に並べたサービス」は、YouTube API Data を取り除いたら地図に何も残らない。** したがって "offers enough independent value to justify such sales if the YouTube API Data were removed" の要件を満たすのは、構造上きわめて難しい。
> **広告 → 原則アウト。サブスク → 明確にアウト。**
> 逃げ道は「自前の独立したデータ・コンテンツを同じページに載せ、それが単独で広告を正当化すると主張できる設計にする」ことだが、**その判断権はYouTube側にあり、こちらに異議申立ての期限付き手段はない。**
> これは lucent.earth 型ビジネスの最大の構造的欠陥である。**コストがゼロでも、収入もゼロに縛られる。**

## 2-2. Twitch

| 項目 | 内容 | 出典（確認日 2026-08-29、いずれも［二次確認］：`dev.twitch.tv` と `legal.twitch.com` はブロック） |
|---|---|---|
| **`parent` パラメータ必須** | 埋め込みを設置するドメインを申告する。`https://player.twitch.tv/?channel=xxx&parent=example.org`。**指定がないと再生エラーが出て、ユーザーは「Twitchで見る」へ誘導される** | <https://dev.twitch.tv/docs/embed/video-and-clips/>（検索経由）、<https://discuss.dev.twitch.com/t/embed-api-parent-parameter-not-working-for-specific-domain/26671> |
| **HTTPS必須** | 「Twitch埋め込みを使うドメインは SSL 証明書を使わねばならない」 | 同上 |
| 複数ドメイン | JS埋め込みは配列 `parent: ["a.example.com","b.example.com"]`、iframe は `&parent=` を複数連結 | 同上 |
| **広告ネットワーク禁止** | "You must not transmit embeddable experiences to or through any advertising network or other advertising-related service." | <https://legal.twitch.com/legal/developer-agreement/>（検索経由、2024-12-04版 DSA） |
| **有償の埋め込み禁止** | "You must not create or implement embeddable experiences in exchange for any compensation (monetary or non-monetary, directly or indirectly) from a content provider on a site or service that the content provider does not own or operate." | 同上 |
| **Twitch Data の商用利用禁止** | Twitch Data（エンドユーザーやそのブラウザ/アプリ活動について収集したデータ、そこから導かれた知見を含む）は、Twitch の事前書面許可なしに販売・ライセンス・収益化・配布・第三者への提供をしてはならない | 同上 |

**判定**：
- **`parent` 必須は運用上の地雷。** ドメインを変えたり、プレビュー環境やカスタムドメインを増やすたびに、埋め込みが**サイレントに壊れる**（Twitch側でエラー画面が出る）。マルチテナントやユーザー独自ドメインを想定するサービスでは致命的。
- 自サイトに広告を置くこと自体は Twitch が直接禁じてはいない（YouTube とは異なる）。ただし **Twitch Data の収益化禁止**が広く書かれているため、「Twitchから取った配信メタデータを主要素材にしたサイトで広告を売る」はグレー。**書面許可なしで踏み込む領域ではない。**

## 2-3. X-Frame-Options / CSP frame-ancestors ― 埋め込み型が壊れる場所

| 事実 | 内容 | 出典（確認日 2026-08-29、［二次確認］） |
|---|---|---|
| 2つのヘッダ | `X-Frame-Options`（2008年、DENY / SAMEORIGIN のみ）と `Content-Security-Policy: frame-ancestors`（オリジンのリスト・ワイルドカード可）。**両方あれば CSP を持つブラウザは frame-ancestors を優先し XFO を無視する** | <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors>、<https://content-security-policy.com/frame-ancestors/> |
| 壊れ方 | ブラウザが iframe の読み込みを**ブロック**する。エラーは DevTools コンソールに "Refused to display / Refused to load ... because it does not appear in the frame-ancestors directive" と出るだけ | 同上 |
| 現在のベストプラクティス | XFO の送信はもはや推奨されず、CSP frame-ancestors を使うべきとされている | <https://www.invicti.com/blog/web-security/missing-x-frame-options-header> |

**ポインタ型サービスにとっての意味：**

1. **障害がサイレントである。** ユーザーには「空白の枠」しか見えず、監視も難しい。地図上のピンの一部が黙って壊れる。
2. **YouTube / Twitch / Kick は専用の埋め込み用ドメイン（`youtube-nocookie.com`、`player.twitch.tv`、`player.kick.com`）を用意しているので現状は壊れない。** ただしこれは相手の善意による提供であって、こちらとの契約ではない。**Facebook/Instagram は2020年に実際に一方的に壊した**（後述）。
3. **個別コンテンツ単位でも壊れる。** YouTube には `status.embeddable` があり、権利者は埋め込みを個別に無効化できる。無効な動画は **エラー101 / 150**（"The owner of the requested video does not allow it to be played in embedded players"）になる。音楽系・スポーツ系・一部の公式配信で日常的に発生する。**「地図上のピンの一定割合が常に壊れている」ことを前提に設計する必要がある。**（出典：<https://developers.google.com/youtube/iframe_api_reference>、検索経由）
4. **一般の商用サイト（不動産ポータル、ECサイト等）はほぼ確実に frame-ancestors / XFO を設定している。** → **「他サイトのページをiframeで見せる」型のサービスは、埋め込み専用ドメインを提供しているプラットフォーム以外では最初から成立しない。**

## 2-4. ホットリンク（他サイトの画像URLを直接表示）

### 技術リスク

| 事実 | 内容 | 出典（確認日 2026-08-29） |
|---|---|---|
| Referer ベースの遮断は**今も完全に機能する** | Chrome は2020年以降デフォルトを `strict-origin-when-cross-origin` にしたが、これは**クロスオリジンでも「オリジン」は送り続ける**（パスとクエリだけが落ちる）。ホットリンク保護はオリジン単位の判定なので**影響を受けない** | ［二次確認］<https://developer.chrome.com/blog/referrer-policy-new-chrome-default/>、<https://chromestatus.com/feature/6251880185331712>、<https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy> |
| 遮断は相手側の設定1つで起きる | Cloudflare の Hotlink Protection をはじめ、主要CDNは1クリックで有効化できる機能を持つ | ［二次確認］ |
| 画像の差し替え | 「無断転載禁止」バナーへの差し替えは今も一般的な運用 | ［二次確認］ |
| **LCP崩壊** | 元画像は 300KB〜2MB の JPEG。サムネイル欄に40枚並べれば初回表示が数十秒（R13 §3-3 で検証済み） | R13 レポート |
| **画像の消滅** | 元サーバが消せば即座に404。物件が成約して消えたとき、**画像だけ先に壊れる** | R13 レポート |

### 法的位置づけ

#### 米国 ― server test（第9巡回区のみ）

**Perfect 10, Inc. v. Amazon.com, Inc., 508 F.3d 1146 (9th Cir. 2007)**（判決 2007-05-16）
- 自サーバに複製を置いて表示すれば **public display 権の侵害**。
- **インラインリンク（埋め込み）で第三者サーバ上の画像を表示するだけなら、画像は自分のコンピュータのメモリに固定されていないので「display」に当たらない＝侵害ではない。**
- 第9巡回区は **Hunley v. Instagram, LLC** で server test を再確認。
- **ただし、第9巡回区外の複数の連邦地裁が、埋め込みSNS投稿やニュース記事の事案でこれを否定または疑問視している。**
- 出典（［二次確認］、確認日 2026-08-29）：<https://en.wikipedia.org/wiki/Server_test>、<https://www.copyright.gov/fair-use/summaries/perfect10-amazon-9thcir2007.pdf>、<https://www.crowell.com/en/insights/client-alerts/will-the-supreme-court-address-whether-the-ninth-circuits-server-test-comports-with-the-display-right-accorded-copyright-owners>

→ **「米国ではホットリンクは合法」は不正確。「第9巡回区では合法、他は不確実」が正しい。**

#### EU ― 技術的防止措置の有無で決まる

**CJEU C-392/19, VG Bild-Kunst v Stiftung Preußischer Kulturbesitz（2021-03-09判決）**
- 判旨：権利者の許諾を得て自由にアクセスできるサイト上にある著作物を、**権利者が採用または（ライセンス条件として）課したフレーミング防止措置を回避して**、第三者サイトにフレーミングで埋め込む行為は、指令2001/29/EC 第3条(1)の「公衆への伝達」に当たる。
- **本件で初めて、権利者が自ら技術的措置を実装するのではなく、ライセンシーに実装を義務づける契約によって「当初の公衆」を限定できることが認められた。**
- 系譜：Svensson（C-466/12）、BestWater（C-348/13）、GS Media（C-160/15）→ **防止措置がなければリンク／フレーミングは原則適法**、あれば侵害。
- 出典（［二次確認］、確認日 2026-08-29）：<https://ipcuria.eu/case?reference=C-392%2F19>、<https://www.fieldfisher.com/en/services/intellectual-property/intellectual-property-blog/cjeu-clarifies-circumstances-in-which-embedding-co>、<https://www.medialaws.eu/the-cjeus-take-on-unauthorized-framing-of-online-content-only-if-technologically-precluded-then-prohibited/>

→ **EUは「相手が技術的措置を入れた瞬間に違法化する」。ホットリンク保護の導入は、遮断であると同時に**法的な地雷の設置**でもある。**

#### 日本 ― リンクは原則適法、だが2つの例外が刺さる

**原則**：リンクを張る行為自体は、著作権法上の「複製」にも「公衆送信（送信可能化）」にも当たらず、原則として著作権侵害ではない。
出典（［二次確認］、確認日 2026-08-29）：<https://www.kottolaw.com/column/001653.html>、<https://topcourt-law.com/intellectual-property/reachsite-copyright>

**例外1：リーチサイト規制（2020年改正、2020-10-01施行）**
- 著作権法 **113条2〜4項**、119条、120条の2 を改正。
- 侵害コンテンツへのリンク情報の提供、およびリーチサイトの運営を、著作権侵害と**みなす**（差止・損害賠償の対象）。刑事罰もある。
- **リンク情報は直リンクのURLに限られない。**「侵害コンテンツを含むページのURL」や「そのURLを含むページのURL」など、**現実的に侵害コンテンツへのアクセスを容易にする情報**を広く含む。
- 出典（［二次確認］）：<https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/r02_hokaisei/>（文化庁）、<https://www.businesslawyers.jp/articles/815>、<https://www.jstage.jst.go.jp/article/jshuppan/51/0/51_161/_pdf/-char/ja>、<https://www.jcea.info/2020houkaisei/2020leechsite.html>

→ **ポインタ型サービスは定義上「リンクを集約したサイト」である。リンク先に侵害コンテンツが混じった瞬間、リーチサイト規制の射程に入る。** ライブ配信マップなら「無断転載の海賊配信」が、不動産なら「無断転載の物件写真」が該当しうる。**「自分は元コンテンツを持っていないから安全」は、日本法では成り立たない。**

**例外2：リツイート事件・最判令和2年7月21日（最三小判）**
- 写真家がウェブに掲載した写真が無断でツイート・リツイートされた事案。
- **リツイートによる自動トリミングで、元画像に表示されていた著作者名の部分が表示されなくなった**結果、**氏名表示権（著作者人格権）の侵害**が認められた。
- リツイートした者はプロバイダ責任制限法4条1項の「発信者」に当たるとして、発信者情報開示が認められた。
- 出典（［二次確認］、確認日 2026-08-29）：<https://storialaw.jp/blog/7281>、<https://www.kottolaw.com/column/200728.html>、<https://gvalaw.jp/blog/k20200924-2/>、<https://svjmwb01.hakuoh.ac.jp/logos/files/21170331石月遥香「リツイート事件（最三小判令和2年7月21日）における問題点」.pdf>

→ **日本では「複製も公衆送信もしていない」でも、著作者人格権で刺される。** そして **「地図のサムネイル枠に合わせて他サイトの画像を自動クロップする」のは、まさにリツイート事件と同じ構図である。** ホットリンク＋自動トリミングは、日本で最も危険な組み合わせ。

### ホットリンクの総合判定

| 観点 | 判定 |
|---|---|
| **節約額** | R13 の実測で **S規模 月$0.57（約90円）／M規模 月$21（約3,400円）／L規模 月$102（約1.6万円）** |
| **技術リスク** | 相手の設定1つで即遮断。referrer policy の変化は防御にならない |
| **UXリスク** | LCP崩壊、画像404、リサイズ・WebP化不可 |
| **法的リスク（米）** | 第9巡回区では server test で保護。**他の巡回区は不確実** |
| **法的リスク（EU）** | 相手が技術的措置を入れたら **公衆送信侵害** |
| **法的リスク（日）** | リンク集約はリーチサイト規制の射程。**自動トリミングで著作者名が消えれば氏名表示権侵害（最判令2.7.21）** |
| **結論** | **月90円〜1.6万円のために引き受けるリスクとしては、明白に割に合わない。** R13 の結論（キャッシュ配信一択）を、法的観点からも支持する |

---

# 3. 検証3：前回調査（不動産）をポインタ型に作り替えたらコストはどうなるか

## 3-1. 前提（R13 の実額）

R13 §7-3、L規模（100万件 / 2,000万枚 / 月300万セッション）、R2直Range版：**月 $340.13 ≈ ¥54,266**

| 項目 | キャッシュ配信 | 分類 |
|---|---|---|
| DBサーバ（Hetzner AX41-NVMe） | $49.49 | データを持つコスト |
| アプリサーバ（CAX31） | $24.56 | データを持つコスト |
| 検索サーバ（CAX31） | $24.56 | データを持つコスト |
| **画像処理サーバ（CAX21）** | **$12.27** | **画像コスト** |
| **画像ストレージ（R2 4.8TB）** | **$71.85** | **画像コスト** |
| **画像 R2 ops** | **$18.00** | **画像コスト** |
| 地図（PMTiles、R2直Range） | $14.40 | データを持つコスト |
| ジオコーディング（LocationIQ） | $49.00 | データを持つコスト |
| AI（月次） | $46.00 | 一部が画像コスト |
| バックアップ・監視・ログ | $30.00 | データを持つコスト |
| **合計** | **$340.13** | |

## 3-2. (a) 画像を一切ホストせず、リンクアウトのみにした場合

**消える費目**：画像処理サーバ $12.27 + 画像ストレージ $71.85 + 画像R2 ops $18.00 = **$102.12**
**追加で消える費目**：画像を持たないので画像AI解析ができない。R13 の AI $46 は「解析＋翻訳＋embedding」なので、解析分を保守的に半分と見て **−$23**

| 規模 | キャッシュ配信 | **リンクアウトのみ** | 削減額 | 削減率 |
|---|---|---|---|---|
| **S（1万件 / 月3万セッション）** | $22.64（¥3,612） | **$22.07（¥3,521）** | **$0.57（¥91）** | **2.5%** |
| **M（10万件 / 月30万セッション）** | $132.18（¥21,090） | **$105.86（¥16,890）**※AI解析分−$5 | $26.32（¥4,200） | 20% |
| **L（100万件 / 月300万セッション）** | $340.13（¥54,266） | **$215.01（¥34,305）** | $125.12（¥19,963） | **37%** |

**残る $215 の内訳（L規模）**：DB $49.49 / アプリ $24.56 / 検索 $24.56 / 地図 $14.40 / ジオコーディング $49.00 / AI $23.00 / 運用 $30.00

> **すべて「データを持つコスト」であり、ポインタ型はここに一切効かない。**

## 3-3. (b) 画像をホットリンクした場合

**月額はリンクアウトのみと完全に同一**（$22.07 / $110.86 / $238.01。R13 のホットリンク列と一致）。
画像をホストしない以上、**コスト面での差はゼロ**。差は「表示されるかどうか」というUXと、§2-4 で見た遮断・法的リスクだけ。

**したがって「ホットリンクを選ぶ理由は、コストではなくUXしかない」。そしてそのUX（LCP崩壊・404）は、R13 の検証でホットリンク側が明確に劣る。**

**遮断リスクの具体像**：
- 遮断は**相手のCDN設定1つ**で、こちらに予告なく起きる。
- 日本のポータル（SUUMO / HOME'S / at home）が現にホットリンク保護をかけているかは、**本セッションでは検証できなかった**（egressブロック）。**しかし、かけていないと仮定して設計するのは無謀である。**
- 遮断された時、**地図上の全物件のサムネイルが同時に壊れる。** ポインタ型は「一気に全滅する」性質を持つ。

## 3-4. (c) 「押すと室内写真が見られる」を自分でホストせずに満たす方法は存在するか

| # | 手法 | 成立するか | 理由 |
|---|---|---|---|
| 1 | **リンクアウト**（元ポータルの物件ページを開く） | **△ 技術的には成立するが、規約で制限される場合がある** | **Zillow の Terms of Use は、不動産・融資の専門家/機関が所有または運営する不動産関連サイト以外の第三者サイトから Zillow へのリンクを提供・掲載・許可することを禁じている**［二次確認］<https://www.zillow.com/corporate/terms-of-use/>（検索経由、確認日 2026-08-29）。**リンクアウトそのものが規約違反になりうる。** かつ体験としては「地図で探して、写真は別サイト」となり連続性が切れる |
| 2 | **元サイトのOGP画像1枚を使う** | **✗** | `og:image` を得るには物件ページを**サーバ側で取得する＝スクレイピング**が必要。Zillow ToU は "automated queries, including screen and database scraping, spiders, robots, crawlers" を明示的に禁止［二次確認］。SUUMO / HOME'S も同様（R11 で検証済み）。**入口で違反。** さらに得た `og:image` の表示自体がホットリンクであり、§2-4 のリスクを全部背負う |
| 3 | **oEmbed** | **✗ 存在しない** | oEmbed 公式レジストリは375プロバイダ（<https://oembed.com/>、確認日 2026-08-29）。**GitHub Code Search で `iamcal/oembed` リポジトリ内を `zillow OR rightmove OR suumo OR realtor OR immobilienscout` で検索した結果、ヒット0件**（一次相当・本セッション実施）。不動産ポータルで oEmbed を実装しているものは確認できない |
| 4 | **iframe 埋め込み** | **✗** | 商用サイトは通常 `frame-ancestors` / `X-Frame-Options` を設定している。**Zillow ToU はフレーミングも制限している**［二次確認］。埋め込み専用ドメインを提供している不動産ポータルは確認できない |
| 5 | **正式提携／アフィリエイト** | **△ ただしそれは「ポインタ型」ではない** | LIFULL HOME'S は felmat 等の ASP 経由でアフィリエイト案件が存在する（クローズド型・審査あり）［二次確認］<https://media-analytics.jp/affisearch/promotions/lifull-homes>、<https://sekaweb.com/asp-homes/>（確認日 2026-08-29）。提携すれば画像利用の許諾が付く可能性はあるが、**それは「提携型」であり、審査と契約が入口になる。ポインタ型の"誰にも許可を取らずに始められる"という利点が消える** |
| 6 | **逆ポータル型（掲載者が自分で投稿）** | **○ 成立するが、画像は自分でホストする** | 権利処理が自分側で完結し、法的に最も安全。ただし**それはポインタ型ではない。** そして R13 の実額では画像ホスト代は **S規模で月$0.57**。**そもそも解決すべき問題ではない** |

**→ 「自分でホストせずに室内写真を見せる」方法は、実質的に存在しない。**

## 3-5. 結論：不動産×ポインタ型は成立するのか

# **成立しない。**

理由は3つ。すべて独立に致命的である。

### 理由1：経済的に無意味

- 削減額は **S規模で月90円、M規模で月4,200円、L規模で月2万円**。
- **S規模（1万件）では削減率2.5%。誤差である。**
- L規模でも「月5.4万円が3.4万円になる」だけで、事業の成否を左右しない。
- **ポインタ型が解決すると期待した費用は、このドメインで最大の費用ではなかった。** R13 が示した通り、このドメインの金食い虫は「マネージド地図API」と「翻訳API」であり、それはセルフホストとLLM翻訳で既に潰してある。画像は3番目以下の項目である。

### 理由2：中核価値を外部に投げることになる

- 「押すと室内写真が見られる」は、このサービスの存在理由そのものである。
- ポインタ型はそれを「押すと他社サイトに飛ぶ」に変える。**それは地図付きリンク集であって、サービスではない。**
- ホットリンクで見せようとすれば、LCP崩壊（元画像300KB〜2MBを40枚）と画像404（成約済み物件の画像が先に消える）で、体験が壊れる。R13 の検証と一致する。

### 理由3：入口の問題を1ミリも解決しない

- 地図にピンを置くには、**住所・価格・座標**が必要である。それを取得する手段の壁は、画像をどう扱うかとは**完全に独立**している。
- R13 が確認した通り：Rightmove と ImmobilienScout24 の API は「物件を**登録する**側」のためのAPIであって取得用ではない。日本のポータルは ToS 違反。米国MLSは宅建業者/認定ベンダー要件＋**MLS毎に月$50〜$500**。
- **ポインタ型はこの壁の前で何もしない。** 画像を捨てても、データを取る許可は1ミリも得られない。

### **唯一成立する変種：公的オープンデータだけを使うポインタ型**

**国土交通省「不動産情報ライブラリ」**（2024-04-01 運用開始）
- 不動産取引価格情報、地価公示・都道府県地価調査の鑑定評価書情報、国土数値情報等を**公開APIとして無料提供**。
- **API利用申請制**。フォームから申請 → 審査結果は**5営業日を目安**にメールでAPIキー送付。
- 出典（［二次確認］、確認日 2026-08-29）：<https://www.reinfolib.mlit.go.jp/help/apiManual/>、<https://www.reinfolib.mlit.go.jp/api/request/>、<https://www.reinfolib.mlit.go.jp/help/termsOfUse/>、<https://api-catalog.e-gov.go.jp/info/ja/apicatalog/view/69>（e-Gov APIカタログ）

- これは**物件在庫ではなく市況データ**なので「押すと室内写真」は成立しない。
- しかし **規約もコストもクリーンで、後述する「ポインタ型の唯一の堀＝時系列蓄積」とも相性がよい**（公的データには YouTube のような30日保存制限がない）。
- **不動産で"ポインタ型かつ持続可能"を成立させたいなら、これしかない。** ただしそれは「物件マップ」ではなく「地価・取引価格マップ」であり、別のサービスである。

---

# 4. 検証4：ポインタ型の構造的な弱点

## 4-1. 資産が蓄積しない問題 ― ポインタ型でも堀は作れるか

### まず、規約が堀を禁じている場合がある

**§2-1(c) で原文確認した通り、YouTube は Non-Authorized Data（＝APIキーで取れる公開メタデータ）を30日を超えて保持することを禁じている。**

> "API Clients may temporarily store limited amounts of Non-Authorized Data for as long as is necessary for the purposes of the API Client but **not longer than 30 calendar days**... after 30 calendar days, the API Client must either delete or refresh the stored data."

**→ 「2026年3月にここでライブがあった」というスナップショットを、YouTube API Data のまま蓄積することは規約違反である。**
**→ 過去12ラウンドの結論だった「時系列・実測が堀」という戦略が、YouTube というドメインでは規約で明示的に封じられている。**

唯一の例外は **derived metrics ポリシー**：監査済み開発者が、アナリティクス用途で、クォータ拡張申請を通じて明示的に許可を得た場合のみ、統計データを30日超保存できる（2026-06-01以降の運用）［二次確認］<https://developers.google.com/youtube/terms/derived-metrics-policy>（検索経由、確認日 2026-08-29）。**ソロが最初から取れる道ではない。**

### では、ポインタ型で作れる堀は何か（4種類）

| # | 資産 | 30日ルールの対象か | 強度 | 実例 |
|---|---|---|---|---|
| 1 | **キュレーション（何を載せるか・どこに置くかの人手の選定）** | **対象外**（自分の判断の産物） | **中〜強**。模倣にはコストがかかるが、模倣は可能 | worldwatcher.live が "hundreds" に絞っているのは能力の限界ではなく、これが資産だから |
| 2 | **メタデータの正規化・同一性の紐付け**（このTwitchch＝このYouTubech＝この場所） | **対象外**（元APIに存在しない、自分が作った情報） | **強**。JustWatch の堀の本体 | JustWatch（後述） |
| 3 | **自分の観測ログ**（自分のクローラが時刻Tに何を見たか） | **境界が曖昧・要注意**。中身がYouTube API Data そのものなら対象。**IDと時刻と自分が推定した座標だけ**にすれば安全側 | **強**（時系列は原理的に模倣不能） | camelcamelcamel / Keepa 型。**ただしYouTubeでは規約が阻む** |
| 4 | **ユーザーの行動と投稿**（どのピンが押されたか、ユーザーによる位置補正・チャンネル追加） | **完全に対象外**。自分の資産 | **最強**。ネットワーク効果を持つ | LiveMap（"explore global YouTube live streams on a map **or add their own**"）［二次確認］<https://play.google.com/store/apps/details?id=com.worldyoutubelive> |

### 実証事例1：Streams Charts IRL Map（2026）― 資本を持つ側が同じ結論に到達している

- Streams Charts（商用ストリーミング・アナリティクス企業）が **IRL Map** を投入。
- 設計：**「チャンネルの配信履歴を、インタラクティブな3Dグローブ上の旅程に変換する」**。国別統計、視聴者数データ、共有可能な公開リンク付き。Twitch / YouTube / Kick のチャンネルを検索し、**配信タイトルを解析して配信国を推定する**。
- 出典（［二次確認］、確認日 2026-08-29）：<https://streamscharts.com/tools/irl-map>、<https://streamscharts.com/news/streams-charts-launches-interactive-travel-map>、<https://www.netinfluencer.com/streams-charts-launches-irl-map-an-interactive-tool-for-tracking-streamers-travel-history/>

> **重要：彼らは「今どこで配信中か」（＝lucent.earth のフロー型）ではなく、「履歴と統計」（＝ストック型）を製品にしている。**
> **資本とデータ基盤を持つ側が、独立に「ポインタ型の価値は履歴側にある」という結論に到達している。** これは戦略の正しさの傍証であると同時に、**その戦略の空間に既に競合がいる**ことを意味する。

### 実証事例2：Radio Garden ― 純粋なポインタ型が10年間無収益で走った記録

| 年 | 出来事 |
|---|---|
| 2013-2016 | Netherlands Institute for Sound and Vision、Transnational Radio Knowledge Platform、欧州5大学が開発。**EU出資の研究プロジェクト Transnational Radio Encounters (TRE) の成果物**として生まれた |
| 2016-12 | 公開 |
| 2017 | Webby Award（Media Streaming）受賞 |
| 2019 | **独立した会社に移行** |
| 2021-02 | コロナ禍で **1,500万ユーザー（通常比+750%）** |
| 2023 | iOS/Android アプリに **プレミアム階層**を導入（広告なし、スリープタイマー等、**年約$25**） |
| 2025-02-13 | "Balloon Ride" モード追加 |
| 現在 | 稼働中。**外部資金調達は一度もない** |

出典（［二次確認］、確認日 2026-08-29）：<https://en.wikipedia.org/wiki/Radio_Garden>（検索経由）、<https://www.crunchbase.com/organization/radio-garden>、<https://studiomoniker.com/projects/radio-garden>、<https://docubase.mit.edu/project/radio-garden>

> **教訓：純粋なポインタ型（Radio Browser 的な公開カタログを地図に載せただけ）は、EU研究資金という「誰かが払ったコスト」の上でしか成立しなかった。**
> **公開から収益化まで7年。堀は「世界中の局のキュレーション＋地図UI＋ブランド」であって、データではない。**
> **そして最終的な収益源は「広告を消す権利」＝ユーザーへの課金だった。YouTubeを使うサービスは、この手が規約で塞がれている。**

### 実証事例3：JustWatch ― ポインタ型が資産化した唯一の実証パターン

- **収益は3本立て**：
  1. 自社プラットフォームの収益化（**アフィリエイト手数料 + フリーミアム + バナー広告**）
  2. **「どこで観られるか」データとインサイトのライセンス**（多数のパートナー・クライアントへ）
  3. そのデータを使った **予告編広告キャンペーンの運用**（YouTube / Facebook / Instagram / TikTok 上で、Universal / Paramount / Sony / Disney / Prime Video 等のために）
- 規模：46カ国、数百の配信サービス。
- 出典（［二次確認］、確認日 2026-08-29）：<https://www.justwatch.com/us/JustWatch-Streaming-API>、<https://tmbroadcast.com/index.php/justwatch-finding-way-streaming/>、<https://www.crunchbase.com/organization/justwatch>

> **堀は「正規化された可用性データ」そのもので、それをB2Bに売っている。**
> **ただしこれは「元プラットフォームが嫌がらないデータ」（作品がどこで配信中か＝配信者にとって送客になる情報）だから成立している。**
> **元プラットフォームが嫌がるデータ（例：競合分析、視聴者数の時系列）を貯めようとした瞬間、規約と技術の両方で殺される。** これが YouTube の30日ルールの正体である。

### 実証事例4：camelcamelcamel / Keepa ― 時系列を堀にした型と、その限界

- CamelCamelCamel は Amazon の **Product Advertising API (PA-API)** を使って価格追跡・値下げ通知を提供。
- PA-API は **アカウントあたり約1リクエスト/秒**の厳しいレート制限があり、**数百万商品を妥当な鮮度で追跡するのは困難**。承認制でもある。
- Amazon はスクレイピングを積極的に検知・ブロックする。
- 出典（［二次確認］、確認日 2026-08-29）：<https://dev.to/agenthustler/amazon-product-api-pa-api-in-2026-restrictions-alternatives-and-web-scraping-4l35>、<https://www.systemdesignhandbook.com/guides/design-camelcamelcamel/>

> **「元APIのデータを時系列で貯める」は、ポインタ型が堀を持つ唯一の形である。**
> **そして、それができるかどうかはドメインごとに規約で決まっている。** Amazon は（レート制限は厳しいが）保持期間の制限を課していないので camelcamelcamel が成立した。**YouTube は明示的に30日で切っているので、同じ型が作れない。**

### **4-1 のまとめ**

> **ポインタ型でも堀は作れる。ただし作れる場所は「元APIの外側」に限られ、その具体は4つしかない：**
> **① キュレーション ② 同一性の紐付け・正規化 ③ 自分の観測記録（規約が許す場合のみ） ④ ユーザーの投稿と行動**
>
> **そして最も強いのは④である。** ユーザーが「このピンの位置が違う」「このチャンネルを追加して」と投稿した情報は、規約の対象外で、模倣不能で、増えるほど価値が上がる。
> **lucent.earth 型で唯一の持続可能な設計は、「APIから自動で集める」ではなく「ユーザーに集めさせる」である。** これは同時に、§1-1 で見た YouTube のクォータ問題への唯一の構造的な解でもある（発見コストをユーザーに転嫁する）。

## 4-2. プラットフォーム依存リスク ― 実例の年表

| 時期 | 出来事 | 影響 | 出典（確認日 2026-08-29） |
|---|---|---|---|
| **2020-10-24** | **Facebook / Instagram が認証不要の oEmbed を廃止**。トークンベースのアクセスへ移行を強制（移行期限は 2020-10-23 10AM PDT） | **世界中の数百万サイトの埋め込みが一斉に壊れた**。WordPress はコアから FB/IG を信頼済み oEmbed プロバイダとして削除し、何年分もの投稿の埋め込みが URL 表示に戻った | ［二次確認］<https://developers.facebook.com/blog/post/2020/10/14/required-migration-token-based-access-user-picture-oEmbed-endpoints/>、<https://make.wordpress.org/core/2020/09/22/facebook-and-instagram-embeds-to-be-deprecated-october-24th/>、<https://wptavern.com/upcoming-api-change-will-break-facebook-and-instagram-oembed-links-across-the-web-beginning-october-24> |
| **2022-11-28** | **Heroku が無料 dyno / 無料 Postgres / 無料 Key-Value を全廃**。理由として不正利用対策を挙げた | 無料PaaSの基準点が消滅 | ［二次確認］<https://help.heroku.com/RSBRUH58/removal-of-heroku-free-product-plans-faq>、<https://redmonk.com/kholterhoff/2022/12/01/the-end-of-herokus-free-tier/> |
| **2023-02** | **Twitter が無料APIを終了。予告は7日間。** Essential / Elevated（月数十万〜数百万ツイート）を廃止し Basic **$100/月**へ | 学術研究・OSS・個人プロジェクトが一斉に停止 | ［二次確認］<https://www.newtarget.com/web-insights-blog/twitter-api/>、<https://www.bitoff.org/twitter-api-new-plans/> |
| **2023-06-08 / 06-30** | **Reddit が $0.02 / 1,000 API calls を導入。** Apollo は年**$2,000万**と試算され 2023-06-30 に終了。RIF、Sync、BaconReader も終了 | サードパーティクライアントのエコシステムが消滅 | ［二次確認］<https://techcrunch.com/2023/06/08/popular-third-party-reddit-app-apollo-is-shutting-down-as-a-result-of-reddits-new-api-pricing/>、<https://9to5mac.com/2023/05/31/reddit-may-force-apollo-and-third-party-clients-to-shut-down/> |
| **2023-07-03 / 08-01** | **Railway が無料プランを廃止**（クリプトマイナー・torrent bot による濫用が理由）。30日$5トライアル＋月$1最低課金へ | Heroku 後の避難先が1つ消えた | ［二次確認］<https://blog.railway.com/p/pricing-and-plans-migration-guide-2023>、<https://www.saaspricepulse.com/blog/railway-pricing-history> |
| **2025-03** | **Google Maps Platform が全体$200クレジットを廃止**、SKU別無料枠へ移行 | R13 の試算で月$2,030〜$20,930の差を生んだ | R13 レポート |
| **2026-04-14** | **Netlify が帯域のクレジット単価を倍化。** 無料枠は 300クレジット/月・20クレジット/GB = 実質約15GB/月 | **無料の静的ホスティングとして事実上使えなくなった** | ［二次確認］<https://temps.sh/compare/vs-netlify> |
| **2026-06-01** | YouTube の derived metrics / データ保存の追加ポリシーが運用開始 | 30日超保存が「監査済み＋申請済み」限定であることが明確化 | ［二次確認］<https://developers.google.com/youtube/terms/derived-metrics-policy>（検索経由） |
| **2026-10-16（予定）** | Gemini 2.5 Flash-Lite 提供終了 | R13 で最安と判定したモデルが消える | R13 レポート |

### この年表の読み方

1. **頻度**：2020年から2026年までの6年間で、大規模な条件変更が **少なくとも9回**。**平均して年1.5回、どこかの依存先が条件を変えている。**
2. **予告期間**：Twitter は **7日**。Facebook/Instagram は約2ヶ月。**「十分な予告がある」という前提は成り立たない。**
3. **理由の共通性**：「不正利用・濫用」（Heroku、Railway）と「AIの学習データ収奪への対抗」（Twitter、Reddit）。**どちらも、こちらの善良さとは無関係に発生する。**
4. **最重要**：**Facebook/Instagram の 2020-10-24 は、「埋め込みは無料で永続する」という業界の前提が実際に一度崩壊した日である。** ポインタ型のすべての前提はこの日に反証されている。

> ### **ポインタ型の脆弱性の本質**
> **在庫を持たないので、変化を吸収する緩衝材がない。**
> 自社にデータを持つサービスは、APIが止まっても手元のデータで何ヶ月か走れる。ポインタ型は、**元APIが止まった瞬間にサービスが空になる。**
> しかも YouTube の30日ルールは、**その緩衝材を持つことを規約で禁じている。**
> これは「作らないほうがいい」という意味ではなく、**「元プラットフォームの気分が変われば即座に終わる前提で、そこに投じる労力の総量を決めろ」**という意味である。

## 4-3. lucent.earth 自体の現状

> **【取得不可の明示】lucent.earth はegressポリシーによりブロックされ、本セッションでは直接確認できなかった。** GitHub 上にそれらしいリポジトリも見つからず、**作者・技術スタック・収益化の有無・寄付の受付・稼働状況の一次確認はいずれもできていない。**

**二次情報で確認できたこと（すべて［二次確認］、確認日 2026-08-29）：**

| 項目 | 内容 | 出典 |
|---|---|---|
| 存在 | ドメインは生きており、検索エンジンに `https://lucent.earth/` が索引されている | 検索結果 |
| 実体 | **「Twitch、YouTube、Kick のストリームを発見できる3Dグローブ」** | <https://googlemapsmania.blogspot.com/2026/03/the-irl-streaming-map.html>（"The IRL Streaming Map"） |
| **稼働確認の最新時点** | **2026年3月**（Google Maps Mania がレビュー記事を掲載） | 同上 |
| レビューの論調 | **コンセプトは評価するが、コンテンツの質に否定的。** 「表面上は本当にわくわくするアイデアだが、残念ながらライブ配信者は例外なく退屈な人ばかり」「Kick は、夜中に見知らぬ人に絡む退屈な男たちのためのプラットフォームらしい」。例外としてフィンランドのアイスフィッシング配信を挙げている | 同上 |
| 収益化 | **確認できず** | — |
| 作者の発言 | **確認できず**（GitHub・SNSともに該当なし） | — |
| 競合 | **Streams Charts が2026年に IRL Map を投入**（履歴・統計側から） | <https://streamscharts.com/tools/irl-map> |
| 類似サービス | World Watcher（<https://worldwatcher.live/>、YouTubeライブカム "hundreds" を地図化）、LiveMap（Google Play、ユーザー投稿型）、Radio Garden（ラジオ、2016-） | 各URL |

**この情報から言えること：**

1. **2026年3月時点で稼働していた。** 8月時点の稼働は未確認。
2. **レビューが指摘している問題は、コストでも技術でもなく「中身がつまらない」である。** これはポインタ型の本質的な弱点を突いている。**自分でコンテンツを作らないサービスは、他人のコンテンツの質を選べない。** キュレーションでしか改善できず、キュレーションは労働である。
3. **収益化の痕跡が外部から見えない。** §2-1 で見た通り、YouTube を含む構成では広告もサブスクも規約で塞がれている。**「収益化していない」のが最も自然な推測である。**
4. **資本を持つ競合（Streams Charts）が同じ空間に入り、しかも「履歴」というより堅い側から入っている。**

---

# 5. 【出力2】ポインタ型で本当にコストゼロに近い構成

## 5-1. 推奨構成（月 $1〜5 = ¥160〜800）

```
┌─ 収集（cron） ───────────────────────────────────────┐
│ GitHub Actions（パブリックリポジトリ＝標準ランナー分数 無制限・無料）  │
│                                                                 │
│  ├ Twitch Helix: App Access Token → Get Streams 全件列挙          │
│  │    97,200ch ÷ 100/page = 972 req、800 req/分 → 約1.2分で完了     │
│  │    → 位置は title / tag / RealtimeIRL 連携から推定              │
│  ├ Radio Browser: キー不要・CORS可・2〜3 req/s・UA必須             │
│  │    45,000局。緯度経度が最初から付いている                        │
│  ├ Kick: api.kick.com/public/v1/livestreams（OAuth 2.1）          │
│  └ YouTube: 【キュレーション済みID表のみ】videos.list（50件/1unit）  │
│       1,000本 × 5分間隔 = 5,760 units/日（残4,240 = search 42回）   │
│                                                                 │
│  ↓ 正規化・座標付与・重複排除 → data.json（gzip後 100〜300KB）      │
│  ↓ リポジトリにコミット                                            │
└──────────────────────────────────────────────┘
                          ↓ 自動デプロイ
┌─ 配信 ────────────────────────────────────────────┐
│ Cloudflare Pages（静的アセットは リクエスト・帯域とも 無制限・無料）  │
│                                                                 │
│  ├ 3Dグローブ: three.js + 単一の地球テクスチャ（自前アセット）        │
│  │   （2D地図が要る場合のみ OpenFreeMap 公開インスタンス $0／SLA無）  │
│  ├ data.json: 同じ Pages から配信                                 │
│  └ 【Worker / Pages Functions は一切使わない】                     │
└──────────────────────────────────────────────┘
                          ↓
┌─ 再生 ────────────────────────────────────────────┐
│ YouTube / Twitch(parent必須・HTTPS必須) / Kick の iframe          │
│  → 動画の帯域はすべて相手持ち = $0                                 │
└──────────────────────────────────────────────┘
```

## 5-2. 月額内訳

| 項目 | 月額 | 根拠 |
|---|---|---|
| Cloudflare Pages（静的のみ） | **$0** | 静的アセットのリクエスト・帯域は無制限で無料（一次確認） |
| GitHub Actions（publicリポジトリ） | **$0** | 標準ランナーは無制限・無料 |
| Twitch Helix API | **$0** | 800 req/分の24%しか使わない |
| Radio Browser API | **$0** | 無料・キー不要 |
| Kick Public API | **$0** | 無料（制限は不透明） |
| YouTube Data API | **$0** | 無料クォータ 10,000 units/日の範囲内 |
| OpenFreeMap（2D地図が要る場合） | **$0** | 寄付ベース・SLA無し |
| ドメイン `.com` | **$1.0〜1.3**（年$12〜15） | |
| （`.earth` の場合） | $2.5〜5.0（年$30〜60） | |
| **合計** | **$1〜5（¥160〜800）** | |

## 5-3. 更新頻度を上げたい場合の変種（月 $0〜5）

Cloudflare Pages のビルドは **月500回**＝**約90分間隔が上限**。1分更新が要るなら：

```
Cloudflare Worker（Cron Trigger、無料枠5個/アカウント）
  → 収集して data.json を R2 に PUT（Class A 無料枠 100万/月 → 1分毎でも43,200/月で余裕）
  ↓
ブラウザは R2 のカスタムドメインを【直接】読む
  → Class B 無料枠 10万/月... ではなく 1,000万/月。
    月300万セッション × 1 fetch = 300万 → 無料枠内
  → Worker を経由しないので Workers の 10万req/日 に当たらない
```

**追加コスト $0。** これが1分更新を維持しつつ無料枠に収まる唯一の設計。

**やってはいけない代替**：Cloudflare KV は無料枠が **書込 1,000/日**。1分更新（1,440/日）で超える。R2 か Git コミットにすること。

## 5-4. この構成を壊す設計ミス（守るべき6つの線）

1. **APIをクライアント（ブラウザ）から叩かない。** 叩いた瞬間、YouTube の10,000 units/日は訪問者1万人で枯れ、HNバズ（1日1.5〜4.3万人）で確実に死ぬ。`search.list` なら **100人**で死ぬ。加えてAPIキーがブラウザに露出する。
2. **Worker / Pages Functions を1つも挟まない。** 挟むと 10万req/日の壁が立ち、Error 1027 でサイトが落ちる。静的アセットのみなら無制限。
3. **Cloudflare Pages のビルドは月500回**（≒90分間隔）。それより速い更新が要るなら Worker cron + R2 直配信へ。
4. **KV に高頻度で書かない**（無料枠 書込1,000/日）。
5. **Cron Triggers は無料5個/アカウント。**
6. **YouTube 由来データは30日以内に削除または更新する。** 蓄積したい情報は「自分が推定した座標」「自分の観測時刻」「ユーザーの投稿」など、**元APIの外側の情報だけ**に切り分ける。

---

# 6. 【出力3】ポインタ型が破綻する条件のリスト

## A. クォータ・レート制限で破綻する

| # | 条件 | 破綻の具体 |
|---|---|---|
| A1 | **元APIの「発見」コストが高い + 発見が主要機能** | YouTube `search.list` = 100 units、無料枠10,000/日。**全球1スイープで1.5〜3日分。設計時点で破綻している** |
| A2 | **追跡対象数がクォータ上限を超える** | YouTube: **約1,000〜2,000本 / 5〜15分間隔が上限**。それ以上は鮮度か本数を捨てるしかない |
| A3 | **クライアントから直接APIを叩く設計** | **バズで即死**。1万人（videos.list）／100人（search.list）が上限 |
| A4 | **複数プロジェクトでシャーディング** | 規約違反。**正規のものを含む全プロジェクトが停止** |
| A5 | **90日アクセスがない** | YouTube はクォータを削減・剥奪できる。休眠プロジェクトの再開は保証されない |
| A6 | 元APIが位置情報を持たない | Twitch も Kick も持たない。推定（title解析・RealtimeIRL連携）に頼ると精度が事業の質になる |

## B. 規約で破綻する

| # | 条件 | 破綻の具体 |
|---|---|---|
| B1 | **収益化した瞬間に規約に触れる** | YouTube：「API Data を取り除いても広告を正当化できる独立した価値」が同ページに必要（原文確認）。**ストリーム発見マップは構造上これを満たしにくい** |
| B2 | **有料化が明示的に禁止** | "API Clients must not charge users to watch content in an embedded YouTube player."（原文確認） |
| B3 | **ゲーティングが明示的に禁止** | 再生ボタン以外の行動を要求してはならない（原文確認）。会員登録の壁を挟めない |
| B4 | **元データの永続保存が禁止** | YouTube: Non-Authorized Data **30日**（原文確認）。**時系列の堀が作れない** |
| B5 | **埋め込みに前提条件がある** | Twitch: `parent` 必須・HTTPS必須。ドメインを増減するたびサイレントに壊れる |
| B6 | **埋め込みの流通・対価が禁止** | Twitch DSA: 広告ネットワークへの流通禁止、対価を得た埋め込み禁止 |
| B7 | **リンクアウトすら制限される** | Zillow ToU: 不動産事業者が所有・運営する不動産関連サイト以外からのリンクを禁止［二次確認］ |
| B8 | **日本：リーチサイト規制** | 侵害コンテンツへのリンク集約は著作権侵害とみなされる（著113条2〜4項、2020-10-01施行）。**「元データを持っていないから安全」は成立しない** |
| B9 | **日本：氏名表示権** | インラインリンク＋自動トリミングで著作者名が消えると侵害（最判令2.7.21）。**地図のサムネイル枠に合わせた自動クロップが該当する** |
| B10 | **EU：技術的措置の回避** | 権利者のフレーミング防止措置を回避すれば公衆送信侵害（CJEU C-392/19） |
| B11 | **米国：server test は全国法ではない** | 第9巡回区外の地裁で否定・疑問視例あり |
| B12 | 埋め込みプレーヤの物理制約 | 最小 200×200px、自動再生は1ページ1つまで、attribution を隠してはならない。**"live wall" UI は作れない** |

## C. 技術で破綻する

| # | 条件 | 破綻の具体 |
|---|---|---|
| C1 | **相手が `frame-ancestors` / `X-Frame-Options` を入れる** | **サイレントに空白化**。DevTools にしかエラーが出ない |
| C2 | **個別コンテンツの `embeddable=false`** | YouTube エラー101/150。**ピンの一定割合が常に壊れている状態が定常** |
| C3 | **ホットリンク保護（Referer）** | Chrome のデフォルト referrer policy でもオリジンは送られるので**今も完全に効く**。相手の設定1つで全サムネイルが同時に壊れる |
| C4 | 元URL・ID体系の変更 | リンク切れが自動では直らない。検知の仕組みが別途必要 |
| C5 | 元サーバの画像削除 | 物件が成約・配信が終了すると**画像だけ先に404** |

## D. ホスティングで破綻する

| # | プラットフォーム | 破綻する条件 |
|---|---|---|
| D1 | **Netlify Free** | 2026-04-14変更で実質約15GB/月 → **3Dグローブ方式で約6,000人／2D地図方式で約1,900人**で停止。HNバズ開始から約2時間 |
| D2 | **Vercel Hobby** | 100GB/月 → 約40,000人で**デプロイ一時停止**。バズの最中に消える |
| D3 | **Vercel Pro** | 従量課金。実例で**$1,141（HN 5万訪問/24h）／$1,477（クローラ8.4TB）／$23,000（DDoS）** |
| D4 | **GitHub Pages** | 帯域100GB/月（ソフト）、サイト1GB、ビルド10回/時。約40,000人で警告メール |
| D5 | **Cloudflare Workers Free** | 10万req/日 → **Error 1027** |
| D6 | **Cloudflare Pages Free** | ビルド500回/月（≒90分間隔が上限）、20,000ファイル/サイト、1ファイル25MiB |
| D7 | **Cloudflare KV Free** | **書込 1,000/日** → 1分更新（1,440/日）で超過 |
| D8 | **Cron Triggers Free** | **5個/アカウント** |

## E. 事業構造で破綻する

| # | 条件 | 実例 |
|---|---|---|
| E1 | **プラットフォームが有料化する** | Twitter（2023-02、予告**7日**）、Reddit（2023、Apollo は年$2,000万相当で終了） |
| E2 | **埋め込みの前提が一方的に変わる** | **Facebook/Instagram oEmbed（2020-10-24）。世界中の数百万サイトの埋め込みが一斉に壊れた** |
| E3 | **無料ホスティングが有料化する** | Heroku（2022-11、濫用対策）、Railway（2023-08、クリプトマイナー）、**Netlify（2026-04、帯域単価倍化）** |
| E4 | **無料枠の定義が変わる** | Google Maps Platform $200クレジット廃止（2025-03） |
| E5 | **最安モデル・サービスが終了する** | Gemini 2.5 Flash-Lite（2026-10-16 提供終了予定） |
| E6 | **資本を持つ競合が同じ地図を出す** | Streams Charts IRL Map（2026） |
| E7 | **コンテンツの質を自分で選べない** | lucent.earth のレビュー：「アイデアは面白いが配信者が退屈」。**自分でコンテンツを作らないサービスは、他人のコンテンツの質を選べない** |
| E8 | **蓄積資産がないため、依存先が消えると事業価値がゼロになる** | 在庫がないので緩衝材がない。**YouTube の30日ルールは緩衝材を持つこと自体を禁じている** |

## F. 「破綻しない条件」（＝設計の必要十分条件）

上のA〜Eをすべて回避する構成は、次の6条件を満たすものに限られる：

1. **発見（discovery）を無料で許すAPIだけを主軸にする**（Twitch、Radio Browser、公的オープンデータ）。YouTube は「確認」専用に降格させる。
2. **APIをクライアントから叩かず、cron で焼いた静的JSONだけを配る。**
3. **Worker / Functions を挟まず、静的アセットだけで完結させる**（Cloudflare Pages）。
4. **収益化を、元プラットフォームの規約が許す形に限定する**（YouTube を含むなら広告・課金は原則不可。アフィリエイト、B2Bデータライセンス、独立した価値を持つ自社コンテンツの併設）。
5. **蓄積する情報を「元APIの外側」に限定する**（キュレーション、同一性紐付け、自分の推定座標と観測時刻、ユーザー投稿）。
6. **発見コストをユーザーに転嫁する**（ユーザー投稿型）。これがクォータ問題と堀の問題を同時に解く唯一の設計。

---

# 7. 【出力4】不動産×ポインタ型の可否判定

## 判定：**不成立**

| 評価軸 | 判定 | 根拠 |
|---|---|---|
| **コスト削減効果** | **✗ ほぼ無意味** | S規模 月**$0.57（¥91、削減率2.5%）**／M規模 月$26（¥4,200）／L規模 月$125（¥19,963、削減率37%）。**期待した費用がこのドメインの主要費用ではなかった** |
| **中核価値の維持** | **✗ 破壊する** | 「押すと室内写真が見られる」がサービスの存在理由。リンクアウトはそれを他社に投げる。ホットリンクはLCP崩壊と画像404で壊す |
| **画像を自前ホストせず写真を見せる手段** | **✗ 実質存在しない** | リンクアウト（Zillow ToU が制限）／OGP（スクレイピングが必要＝入口で違反）／oEmbed（**不動産ポータルの登録は0件、GitHub Code Search で確認**）／iframe（frame-ancestors で不可）／提携（それは提携型であってポインタ型ではない） |
| **入口（データ取得）の問題** | **✗ 1ミリも解決しない** | Rightmove / ImmobilienScout24 の API は「登録する側」用。日本のポータルは ToS 違反。米国MLSは月$50〜$500/MLS。**画像を捨てても許可は得られない** |
| **法的リスク** | **✗ むしろ増える** | 日本：リーチサイト規制の射程 + 自動クロップによる氏名表示権侵害（最判令2.7.21）／EU：技術的措置回避で公衆送信侵害／米国：server test は第9巡回区限定 |

## 唯一成立する変種

**公的オープンデータだけを使う「地価・取引価格マップ」**

- **国土交通省 不動産情報ライブラリ API**（2024-04-01運用開始、申請制・審査5営業日目安・**無料**）
  <https://www.reinfolib.mlit.go.jp/help/apiManual/> / <https://www.reinfolib.mlit.go.jp/api/request/> / <https://www.reinfolib.mlit.go.jp/help/termsOfUse/>（確認日 2026-08-29）
- 規約もコストもクリーン。**YouTube のような30日保存制限がないので、時系列を貯めて堀にできる**（過去12ラウンドの結論と整合する）。
- **ただしこれは「物件在庫マップ」ではなく「市況マップ」であり、「押すと室内写真」は成立しない。別のサービスである。**

## 補足：不動産で本当に効いた費用削減はどこにあったか（R13 との整合）

| 施策 | 削減額（L規模） |
|---|---|
| **地図を Google Maps → セルフホスト PMTiles** | $20,930 → $14.40（**1,450分の1**） |
| **翻訳を Google Translate → Gemini Flash-Lite Batch** | $16,000 → $85（**188分の1**、初回一括） |
| **画像変換を Cloudflare on-the-fly → 取り込み時に事前生成** | $20,000 → 実質$0（初回一括） |
| **画像をやめてポインタ型にする** | $340 → $215（**1.6分の1**） |

> **ポインタ型は、このドメインで4番目に効く施策であり、しかも唯一「サービスの中核価値を犠牲にする」施策である。**
> **順番として、上の3つを先にやるべきであり、それをやった後にはポインタ型を採る理由が残らない。**

---

# 8. 全体総括

## 8-1. 「月$0〜20で回る」は本当か

**回る。ただし、回るのは「ホスティング」だけである。**

- Cloudflare Pages の静的アセットは、**リクエストも帯域も無制限で無料**（Cloudflare公式ドキュメント原文で確認）。HNバズで10万人来ても$0。
- GitHub Actions のパブリックリポジトリは**分数無制限**。cron 収集も$0。
- 動画の帯域は全部プラットフォーム持ち。
- **月$1〜5（ドメイン代のみ）が現実的な下限。**

**回らないのは：**
- **YouTube の「発見」**。全球スイープに1.5〜3日分のクォータが要る。**構造的に不可能。**
- **収益化**。YouTube の規約で広告も課金も原則封じられている。**コストがゼロでも、収入もゼロに縛られる。**
- **資産の蓄積**。Non-Authorized Data の30日ルールが、時系列という唯一の堀を禁じている。

## 8-2. 楽観を禁じた場合の結論

**lucent.earth 型は「作れる」が「事業にはならない」。**

- 作るコスト：月$1〜5。**これは事実。**
- しかし、YouTube を含む構成では **広告もサブスクも規約違反**。アフィリエイトも配信プラットフォームには存在しない。
- 蓄積できる資産は「キュレーション」「同一性の紐付け」「ユーザー投稿」の3つに限られ、いずれも**労働集約的**である。
- コンテンツの質を自分で選べない（lucent.earth のレビューが実証している）。
- 資本を持つ競合（Streams Charts）が、より堅い側（履歴・統計）から既に参入している。
- Radio Garden は**EU研究資金の上で7年走り、最後にアプリ課金で収益化した**。純粋なポインタ型が自力で立った実例は、本調査では見つからなかった。
- JustWatch は成功しているが、それは **B2Bデータライセンスと広告運用**という別事業に転換したからであり、**「元プラットフォームが送客として歓迎するデータ」だから許されている。**

**不動産×ポインタ型は「作れるが作る意味がない」。**
削減額がS規模で月90円である以上、これは技術判断ですらない。

## 8-3. この検証が示す、より一般的な設計原則

> **ポインタ型の成否は、「元プラットフォームが、あなたのサービスを送客とみなすか、収奪とみなすか」で決まる。**
>
> - **送客とみなされる**（JustWatch の「どこで観られるか」、アフィリエイト経由の不動産リンク、Radio Browser の局カタログ）→ APIも埋め込みも寛容、堀を作れる。
> - **収奪とみなされる**（YouTube の全球ライブ発見、Amazon の価格時系列、Twitter/Reddit のデータ取得）→ **クォータ・規約・保存期限のすべてで締められる。**
>
> **そして、この判定を下すのはこちらではない。**
> **ポインタ型を選ぶということは、この判定権を他人に渡すということである。**

---

## 付録：出典一覧（すべて確認日 2026-08-29）

### 一次相当（原文を本セッションで逐語取得）

- YouTube Developer Terms 原文：`OpenTermsArchive/pga-snapshots` リポジトリ、`YouTube/Developer Terms.html`、commit `35bb781e26d377cbce290c9b1a47fe1b71ba8f92`。GitHub Code Search API 経由で断片取得。<https://github.com/OpenTermsArchive/pga-snapshots>
- Cloudflare Workers 課金：<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/workers/platform/pricing.mdx>
- Cloudflare Workers 制限：<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/workers/platform/limits.mdx>
- Cloudflare Pages 制限：<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/pages/platform/limits.mdx>
- Cloudflare Pages Functions 課金：<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/pages/functions/pricing.mdx>
- Cloudflare R2 課金：<https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/r2/pricing.mdx>
- YouTube API クォータ単価（実装コード3件で相互確認）：<https://github.com/superdesigndev/treg>、<https://github.com/ksjpswaroop/Cutroom>、<https://github.com/antonmarklundcom/yt>
- oEmbed レジストリに不動産ポータルが存在しないこと：`iamcal/oembed` を GitHub Code Search で検索、ヒット0件

### 二次確認（検索エンジン経由）

YouTube: <https://developers.google.com/youtube/terms/developer-policies> / <https://developers.google.com/youtube/terms/required-minimum-functionality> / <https://developers.google.com/youtube/terms/developer-policies-guide> / <https://developers.google.com/youtube/terms/derived-metrics-policy> / <https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits> / <https://www.getphyllo.com/post/is-the-youtube-api-free-in-2026-quota-limits-costs-when-to-pay> / <https://www.socialcrawl.dev/blog/youtube-data-api-2026> / <https://outlierkit.com/resources/youtube-api-quota/> / <https://www.technetexperts.com/youtube-api-videos-list-id-limit/>

Twitch: <https://dev.twitch.tv/docs/api/guide> / <https://dev.twitch.tv/docs/embed/video-and-clips/> / <https://legal.twitch.com/legal/developer-agreement/> / <https://discuss.dev.twitch.com/t/helix-api-rate-limits/24854> / <https://twitchtracker.com/statistics> / <https://www.demandsage.com/twitch-users/>

Kick: <https://repostit.io/kick-api-guide/> / <https://www.netrows.com/blog/best-kick-streaming-data-apis-2026>

Radio Browser: <https://api.radio-browser.info/> / <https://docs.radio-browser.info/> / <https://github.com/AnowHosting/radio-browser-api-documentation> / <https://github.com/api-evangelist/radio-browser>

ホスティング: <https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits> / <https://github.com/orgs/community/discussions/22155> / <https://flexprice.io/blog/vercel-pricing-breakdown> / <https://deploybase.app/blog/vercel-bill-shock-1100-bandwidth-costs-alternatives-2026> / <https://usagebox.com/articles/vercel-23000-dollar-bill-usage-based-platform-bill-shock-2026> / <https://bex.co/blog/2026/07/31/vercel-bandwidth-bill-shock> / <https://temps.sh/compare/vs-netlify> / <https://flexprice.io/blog/complete-guide-to-netlify-pricing-and-plans> / <https://cicdcalculator.com/github-actions-free-tier> / <https://community.cloudflare.com/t/error-1027-when-i-load-my-worker-but-i-dont-see-how-it-has-exceeded-the-100-000-request-limit/331056> / <https://blog.cloudflare.com/updated-tos>

HNトラフィック: <https://blog.royalsloth.eu/posts/how-much-traffic-comes-from-the-front-page-of-hackernews/> / <https://harrisonbroadbent.com/blog/hacker-news-traffic-spike-anatomy/> / <https://marcotm.com/articles/stats-of-being-on-the-hacker-news-front-page/> / <https://www.vincentschmalbach.com/analyzing-a-year-of-hacker-news-traffic/> / <https://luke.hsiao.dev/blog/2023-hn-traffic/>

埋め込み・ヘッダ: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors> / <https://content-security-policy.com/frame-ancestors/> / <https://www.invicti.com/blog/web-security/missing-x-frame-options-header> / <https://developer.chrome.com/blog/referrer-policy-new-chrome-default/> / <https://chromestatus.com/feature/6251880185331712>

法: <https://en.wikipedia.org/wiki/Server_test> / <https://www.copyright.gov/fair-use/summaries/perfect10-amazon-9thcir2007.pdf> / <https://www.crowell.com/en/insights/client-alerts/will-the-supreme-court-address-whether-the-ninth-circuits-server-test-comports-with-the-display-right-accorded-copyright-owners> / <https://ipcuria.eu/case?reference=C-392%2F19> / <https://www.fieldfisher.com/en/services/intellectual-property/intellectual-property-blog/cjeu-clarifies-circumstances-in-which-embedding-co> / <https://www.medialaws.eu/the-cjeus-take-on-unauthorized-framing-of-online-content-only-if-technologically-precluded-then-prohibited/> / <https://www.bunka.go.jp/seisaku/chosakuken/hokaisei/r02_hokaisei/> / <https://www.businesslawyers.jp/articles/815> / <https://www.jstage.jst.go.jp/article/jshuppan/51/0/51_161/_pdf/-char/ja> / <https://www.jcea.info/2020houkaisei/2020leechsite.html> / <https://www.kottolaw.com/column/001653.html> / <https://storialaw.jp/blog/7281> / <https://www.kottolaw.com/column/200728.html> / <https://gvalaw.jp/blog/k20200924-2/>

プラットフォーム依存の実例: <https://developers.facebook.com/blog/post/2020/10/14/required-migration-token-based-access-user-picture-oEmbed-endpoints/> / <https://make.wordpress.org/core/2020/09/22/facebook-and-instagram-embeds-to-be-deprecated-october-24th/> / <https://wptavern.com/upcoming-api-change-will-break-facebook-and-instagram-oembed-links-across-the-web-beginning-october-24> / <https://help.heroku.com/RSBRUH58/removal-of-heroku-free-product-plans-faq> / <https://redmonk.com/kholterhoff/2022/12/01/the-end-of-herokus-free-tier/> / <https://www.newtarget.com/web-insights-blog/twitter-api/> / <https://techcrunch.com/2023/06/08/popular-third-party-reddit-app-apollo-is-shutting-down-as-a-result-of-reddits-new-api-pricing/> / <https://blog.railway.com/p/pricing-and-plans-migration-guide-2023>

事例研究: <https://googlemapsmania.blogspot.com/2026/03/the-irl-streaming-map.html> / <https://streamscharts.com/tools/irl-map> / <https://www.netinfluencer.com/streams-charts-launches-irl-map-an-interactive-tool-for-tracking-streamers-travel-history/> / <https://worldwatcher.live/> / <https://play.google.com/store/apps/details?id=com.worldyoutubelive> / <https://en.wikipedia.org/wiki/Radio_Garden> / <https://www.crunchbase.com/organization/radio-garden> / <https://studiomoniker.com/projects/radio-garden> / <https://www.justwatch.com/us/JustWatch-Streaming-API> / <https://tmbroadcast.com/index.php/justwatch-finding-way-streaming/> / <https://dev.to/agenthustler/amazon-product-api-pa-api-in-2026-restrictions-alternatives-and-web-scraping-4l35> / <https://www.systemdesignhandbook.com/guides/design-camelcamelcamel/> / <https://rtirl.com/>

不動産: <https://www.zillow.com/corporate/terms-of-use/> / <https://www.reinfolib.mlit.go.jp/help/apiManual/> / <https://www.reinfolib.mlit.go.jp/api/request/> / <https://www.reinfolib.mlit.go.jp/help/termsOfUse/> / <https://api-catalog.e-gov.go.jp/info/ja/apicatalog/view/69> / <https://media-analytics.jp/affisearch/promotions/lifull-homes> / <https://sekaweb.com/asp-homes/> / <https://oembed.com/>

### 取得できなかったもの（明示）

- **lucent.earth 本体**（egressブロック）。稼働状況は2026年3月の第三者レビューまでしか確認できていない。作者・収益化・技術スタックは**不明**。
- **developers.google.com の一次ページ全般**（YouTube ToS 本文、Developer Policies、クォータ表、RMF）。OpenTermsArchive スナップショットと検索経由で代替した。
- **dev.twitch.tv / legal.twitch.com の一次ページ**。Twitch の記述はすべて［二次確認］。
- **api.radio-browser.info の一次ドキュメント**。
- **www.zillow.com の Terms of Use 原文**。Zillow に関する記述はすべて［二次確認］であり、**リンクアウト制限の条項は原文で確認できていない。実務判断の前に必ず原文を読むこと。**
- **日本の不動産ポータル（SUUMO / HOME'S / at home）のホットリンク保護の有無・frame-ancestors 設定の有無**。技術的検証は本セッションでは不可能だった。
