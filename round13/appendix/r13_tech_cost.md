# R13 / 技術構成・コスト試算：世界の賃貸・売買物件マップ＋室内写真サービス

**調査日：2026-08-29**（本文中の全URLの確認日は同日）
**担当：技術構成・コスト試算エージェント**
**対象：日本在住ソロエンジニア（元Cisco SE・Webエンジニア）が、世界中の賃貸・売買物件をマップ表示し室内写真を閲覧できるサービスを構築する場合の技術的実現可能性と実額コスト**

---

## 0. 結論サマリー（先に読む3行）

1. **技術は全部解ける。月1万円以下で10万物件・月3万セッションは実際に回る。** 地図・画像・DB・AIすべてに、2026年時点でソロが払える価格の解が存在する。100万物件でも月5〜8万円に収まる。
2. **金が溶けるのは「マネージド地図API」と「翻訳API」の2箇所だけ。** Google Maps は月300万セッションで**$20,930/月**、Mapbox は**$9,150/月**。翻訳を Google Translate API で10万件×10言語やると**$16,000（約255万円）**。どちらも**セルフホスト（Protomaps/PMTiles）とLLM翻訳（Gemini Flash-Lite で $85）**に置き換えると**100〜200分の1**になる。ここを間違えなければコストは問題にならない。
3. **致命的リスクは技術ではなく「データ」と「規約」。** Rightmove / ImmobilienScout24 の公式APIは**物件を"登録する"ためのAPI**であって"取得する"APIではない。Google Geocoding の緯度経度は**30日しかキャッシュできない**（物件DBに永続保存不可）。Cloudflare は**画像の偏った大量配信を無料CDNで行うことを禁じている**（R2/Images等の有料サービス必須）。この3つは設計を根本から変える。

> ### 【重要・調査上の制約の開示】
> 本セッションのegressプロキシが、**一次情報である公式価格ページの大半を403でブロック**した。具体的にブロックされたホスト：`docs.mapbox.com` / `www.mapbox.com` / `developers.google.com` / `mapsplatform.google.com` / `www.maptiler.com` / `protomaps.com` / `docs.protomaps.com` / `openfreemap.org` / `developers.cloudflare.com` / `cloudinary.com` / `imgproxy.net` / `supabase.com` / `neon.tech` / `fly.io` / `www.hetzner.com` / `typesense.org` / `www.meilisearch.com` / `www.elastic.co` / `aws.amazon.com` / `openai.com` / `www.deepl.com` / `stadiamaps.com` / `locationiq.com` / `opencagedata.com` / `web.archive.org` ほか。
>
> したがって**本レポートの価格の大半は、検索エンジン経由の要約および二次情報（価格比較サイト・ベンダー中立ブログ）による裏取り**である。各項目に出典URLと確認日を付し、**一次ソース原文を直接確認できていないものは［二次確認］と明記**した。Claude API の価格のみ、本セッション内の `claude-api` スキル（キャッシュ日 2026-06-24）という一次相当ソースで確認できている。
>
> **実運用の意思決定前に、各ベンダーの公式価格ページを自分の目で再確認すること。** 特に2026年は後述の通りハード価格が乱高下しており、価格改定頻度が異常に高い。

**為替前提**：1 USD = **159.55 JPY**（2026-08-28時点。出典 <https://tradingeconomics.com/japan/currency>、確認日 2026-08-29）。EUR/JPY は本セッションで検証できなかったため **1 EUR ≈ 1.17 USD ≈ 187 JPY** を仮定値として使用する［仮定・未検証］。

---

## 1. トラフィック・データ量モデル（全試算の共通前提）

実額を出すには前提を固定する必要がある。以下を全表で共通に使う。

| 記号 | 物件数 | 写真枚数（20枚/物件） | セッション/月 | 想定フェーズ |
|---|---|---|---|---|
| **S** | 1万件 | 20万枚 | 3万 | MVP・1カ国 |
| **M** | 10万件 | 200万枚 | 30万 | 数カ国・初期成長 |
| **L** | 100万件 | 2,000万枚 | 300万 | 主要国カバー |
| **XL** | 1,000万件 | 2億枚 | — | 地図描画手法の検討のみ |

**1セッションあたりの消費（保守的に多めに見積もる）**

| 項目 | 量 | 根拠 |
|---|---|---|
| 地図ベースマップのベクタータイル | 150タイル × 50KB = **7.5MB** | パン・ズームを含む地図中心のUX。1タイル10〜100KB |
| 検索結果サムネイル | 40枚 × 20KB(WebP 300px) = **0.8MB** | |
| 物件詳細の写真 | 10枚 × 220KB(WebP 1600px) = **2.2MB** | 3物件を開いて数枚ずつ見る |
| **画像合計** | **3.0MB/セッション** | |

**月次転送量**

| 規模 | 画像転送 | 地図タイル転送 | 画像リクエスト数 | 地図タイルリクエスト数 |
|---|---|---|---|---|
| S | 90 GB | 225 GB | 150万 | 450万 |
| M | 900 GB | 2.25 TB | 1,500万 | 4,500万 |
| L | 9 TB | 22.5 TB | 1億5,000万 | 4億5,000万 |

**画像ストレージ（派生2サイズのみ保持：サムネ20KB＋詳細220KB = 240KB/枚。オリジナルは保持しない）**

| 規模 | ストレージ |
|---|---|
| S | 48 GB |
| M | 480 GB |
| L | 4.8 TB |

---

## 2. 【レイヤー1】地図基盤

### 2-1. 選択肢比較表（2026年8月時点の料金）

| 選択肢 | 無料枠 | 超過料金 | S(3万)月額 | M(30万)月額 | L(300万)月額 | ソロ適性 | 出典（確認日 2026-08-29） |
|---|---|---|---|---|---|---|---|
| **Google Maps Dynamic Maps** | SKU毎 10,000イベント/月（2025年3月に全体$200クレジット廃止） | $7 / 1,000 map loads | **$140** | **$2,030** | **$20,930** | ✗ | <https://www.woosmap.com/blog/google-maps-api-pricing-breakdown>［二次確認］<br><https://mapatlas.eu/blog/google-maps-api-pricing-2026>［二次確認］ |
| **Google サブスク** | Starter $100/50k, Essentials $275/100k, Pro $1,200/250k events | 超過は従量 | $100 | $1,200+ | 要見積 | ✗ | 同上［二次確認］ |
| **Mapbox Map Loads for Web** | 50,000 map loads/月 | $5/1k（〜20万）、$3/1k（20万超） | **$0** | **$1,050** | **$9,150** | △（Sのみ） | <https://www.woosmap.com/blog/mapbox-pricing>［二次確認］<br><https://help.stockist.co/article/104-how-mapboxs-free-tier-works>［二次確認］ |
| **MapTiler Cloud Flex** | Free: 10万タイルreq + 5,000セッション + 100MBホスティング | Flex €25/月〜、追加セッション $2/1,000、追加リクエスト $0.10/1,000 | **~$79** | **~$619** | Unlimited $295 推奨 | △ | <https://www.maptiler.com/cloud/pricing/>［二次確認］<br><https://saaspartout.com/marketplace/maptiler/>［二次確認］ |
| **Protomaps ホスト版API** | 非商用 100万タイルreq/月まで無料 | **商用は $14/月〜**（GitHub Sponsors経由） | $14 | $14〜 | 要確認 | ◎ | <https://protomaps.com/api>［二次確認］<br><https://apio.sh/apis/protomaps>［二次確認］ |
| **OpenFreeMap 公開インスタンス** | **完全無料・無制限・APIキー不要・登録不要** | — | **$0** | **$0** | **$0** | ◎ ただしSLA無 | <https://openfreemap.org/>（確認日 2026-08-29）<br><https://github.com/hyperknot/openfreemap>（同） |
| **Protomaps PMTiles セルフホスト（R2）** | — | R2ストレージ+Class B ops のみ、**egress $0** | **~$7** | **~$17** | **~$152** | ◎ **推奨** | 下記2-3参照 |
| **Planetiler で自前ビルド + 自前nginx** | — | サーバ代のみ | サーバに含む | サーバに含む | 帯域が厳しい | ○ | 下記2-4参照 |

**判定：Google Maps と Mapbox は、この用途では検討に値しない。** 地図が主UIのサービスは1セッション=1 map load であり、月30万セッション（＝1日1万セッション、決して大きくない）で Mapbox $1,050 / Google $2,030 が確定する。これは「月数万円まで」という制約を1桁超える。

### 2-2. Protomaps / PMTiles セルフホストの実額

**プラネットPMTilesのサイズ：約100〜130GB**（zoom 0-15）。Protomaps は毎日フルプラネットをビルドして配布している。
出典：<https://docs.protomaps.com/basemaps/downloads>［二次確認］、<https://blog.pinballmap.com/2024/11/05/protomaps-tile-hosting/>（確認日 2026-08-29）、<https://github.com/koala73/worldmonitor/issues/1044>（同）

**Cloudflare R2 の2026年料金**（出典：<https://developers.cloudflare.com/r2/pricing>［二次確認、検索経由］、<https://mecanik.dev/en/posts/cloudflare-r2-pricing-explained-real-costs-vs-s3-and-backblaze/>（確認日 2026-08-29）、<https://egresscost.com/cloudflare/>（同））

| 項目 | 単価 | 無料枠（毎月） |
|---|---|---|
| Standard ストレージ | **$0.015 / GB / 月** | 10 GB |
| Class A（書込系）操作 | **$4.50 / 100万** | 100万 |
| Class B（読取系）操作 | **$0.36 / 100万** | 1,000万 |
| **Egress（下り転送）** | **$0（全ボリューム無料）** | 無制限 |
| Infrequent Access | $0.01/GB、Class A $9.00/M、Class B $0.90/M、取り出し $0.01/GB | 無料枠なし |

**Cloudflare Workers（PMTilesの範囲リクエストをキャッシュ効率化するため推奨）**
$5/月に**1,000万リクエスト + 3,000万CPUミリ秒**込み。超過は**$0.30/100万リクエスト**、CPU $0.02/100万ms。**egress課金なし**。
出典：<https://developers.cloudflare.com/workers/platform/pricing/>［二次確認］、<https://www.budgetforge.dev/tools/cloudflare-workers-pricing-2026>（確認日 2026-08-29）

**実額（Cloudflare CDN前段でタイルキャッシュヒット率90%と仮定）**

| 規模 | タイルreq/月 | R2ストレージ | R2 Class B | Worker | **月額合計** |
|---|---|---|---|---|---|
| S | 450万 | $1.80（120GB） | $0（45万→無料枠内） | $5 | **$6.80 ≈ ¥1,085** |
| M | 4,500万 | $1.80 | $0（450万→無料枠内） | $5 + $10.50 | **$17.30 ≈ ¥2,760** |
| L | 4億5,000万 | $1.80 | $12.60（4,500万→3,500万課金） | $5 + $132 | **$151.40 ≈ ¥24,156** |

> **L規模での節約テク**：Worker のリクエスト課金($132)が地図コストの大半を占める。MapLibre の `pmtiles://` プロトコルは**クライアントから直接HTTP Rangeリクエスト**を投げられるので、R2 のカスタムドメインを直接叩かせれば Worker を経由せず **$0** にできる（キャッシュ効率はやや落ちる）。この1手で L規模の地図代が **$151 → $19** になる。

### 2-3. OpenFreeMap 公開インスタンスという「ゼロ円の裏技」

- **登録不要・ユーザーDB無し・APIキー無し・Cookie無し・map view数もリクエスト数も無制限で完全無料**
- MapLibre 使用時は帰属表示（attribution）が自動付与される
- 公開インスタンスは **Hetzner の2台**で稼働、運営費は**寄付で賄われている**
- セルフホストも可能：**事前ビルド済みタイルのダウンロードなら Ubuntu + 300GB SSD + 4GB RAM**で足りる（タイルサーバは動かさず、Btrfsパーティションイメージ＋3億個のハードリンクを最適化nginx設定で直接配信するという設計）。**自前ビルドなら 500GB ディスク + 64GB RAM**が必要。

出典：<https://openfreemap.org/>（確認日 2026-08-29）、<https://github.com/hyperknot/openfreemap>（同）、<https://openfreemap.org/quick_start/>（同）、<https://simonwillison.net/2024/Sep/28/openfreemap/>（同）

**評価**：MVP〜S規模では**これ一択でいい**。ただし寄付ベース・SLA無しなので、収益が立った時点でセルフホスト（R2 + PMTiles）に移行する前提で設計を組む。MapLibre のスタイルURLを差し替えるだけなので移行コストはほぼゼロ。

### 2-4. 自前ビルドする場合（Planetiler）

- **プラネット全体を約2時間でビルド**（ハイエンドデスクトップ/サーバの場合）
- 推奨RAM **64GB**、CPUコアは多いほど良い（Core i9 / Ryzen 9 / AWS c7gd.8xlarge 相当）
- ストレージ **1TB以上のNVMe SSD**（ネットワークストレージ不可、インスタンスストア必須）
出典：<https://github.com/onthegomap/planetiler/blob/main/PLANET.md>（確認日 2026-08-29）、<https://github.com/onthegomap/planetiler>（同）、<https://docs.protomaps.com/basemaps/build>［二次確認］

**評価**：ソロ運用では**やらなくていい**。Protomaps が毎日ビルドしたPMTilesを落としてくれば済む。自前スタイルが要るなら Planetiler ではなくスタイルJSONだけ書き換える。ビルドが必要になるのは「独自レイヤをベースマップに焼き込む」時だけで、それはMVPの範囲外。

### 2-5. 【最重要】数万〜数千万件のマーカーをどう描くか

これがこのサービスの技術的核心。規模ごとに手法が変わる。

| 物件数 | 推奨手法 | 実装 | 実現性 | コスト増 |
|---|---|---|---|---|
| **〜1万件** | クライアントサイド clustering | 全件GeoJSON（~2MB）を1回配信し `supercluster` でブラウザ内クラスタリング | ◎ 数時間で実装 | $0 |
| **〜10万件** | ① bbox+フィルタでAPI問い合わせ→GeoJSON<br>② または ST_AsMVT オンザフライ | PostGIS の GiST インデックス。z12タイル1枚のクエリで10〜50ms | ◎ | $0（DBのCPUのみ） |
| **〜100万件** | **ST_AsMVT オンザフライ + Cloudflareキャッシュ**、低ズームは **H3集計テーブル** | z<10 は H3 res 4-6 の事前集計マテビューで「件数」だけ返す。z≥10 は個票をMVTで | ○ 設計が要る | $0〜$30/月（キャッシュ） |
| **〜1,000万件** | **必須：事前集計 + フィルタ次元の制限** | tippecanoe で PMTiles を定期生成（`--cluster-distant-points=512` で**毎秒100万点**処理）。フィルタは MapLibre の `filter` 式でクライアント側処理できる4〜6属性に限定 | △ ここから本格的なエンジニアリング | $30〜$150/月 |

**ライブラリの実測値（出典付き）**

- **supercluster**：**600万点をブラウザにロードして60fpsでスムーズに閲覧可能**。Mapbox GL JS のクラスタリングを駆動しているライブラリ本体。Node.js でサーバサイドクラスタリングし、結果をベクタータイルに変換することも可能。
  出典：<https://blog.mapbox.com/clustering-millions-of-points-on-a-map-with-supercluster-272046ec5c97>（確認日 2026-08-29）、<https://github.com/mapbox/supercluster>（同）
- **tippecanoe**：数百万フィーチャを処理し、ズームレベル別に賢く簡略化。`--cluster-distant-points=512` で**毎秒100万点**。92%のサイズ削減 → 4G/5Gで6倍高速ロード。z0-10 のタイルをPMTilesで配信し MapLibre で描画すれば**5年前のノートPCでも60fps**。
  出典：<https://github.com/felt/tippecanoe>（確認日 2026-08-29）、<https://johal.in/tippecanoe-vector-tiles-python-geojson-optimize-2025/>（同）、<https://docs.protomaps.com/pmtiles/create>［二次確認］
- **deck.gl**：ScatterplotLayer は大量点を問題なく扱えるが、**クラスタリング機能は組み込みではない**（長年のオープンissue）。supercluster と組み合わせる必要がある。
  出典：<https://github.com/visgl/deck.gl/issues/3055>（確認日 2026-08-29）、<https://github.com/tkhrmeme/deckgl_supercluster>（同）

**【設計上の落とし穴：フィルタ付きタイルのキャッシュ爆発】**

事前生成タイル（PMTiles）は**任意のフィルタ条件を反映できない**。「価格500-800万・2LDK以上・築10年以内・ペット可」のような組合せは無限にあり、(z,x,y,filter-hash) をキーにキャッシュすると**キャッシュキーが爆発してヒット率がゼロになる**。実務的な解は3つ：

1. **属性をタイルに焼き込んでクライアント側でフィルタ**：価格・寝室数・種別など4〜6個の数値/列挙型属性をタイルのプロパティに入れ、MapLibre の `filter` 式で表示制御。タイルは1種類だけキャッシュすればいい。**これが本命。** 制約：属性が増えるとタイルサイズが膨らむ、テキスト検索は不可。
2. **ST_AsMVT オンザフライ**：WHERE句付きでタイルを都度生成。キャッシュはヒットしないがDBのCPUで殴る。100万件・z≥12 なら実用速度。z<12 は集計テーブルに逃がす。
3. **ハイブリッド（推奨）**：z<11 は「H3セル別の件数ヒートマップ」（フィルタ適用済みの集計をDBで計算、軽い）、z≥11 は「個票のMVT」（表示範囲が狭いので行数が少なく、フィルタ付きでも高速）。ユーザーの体感は「広域＝密度、拡大＝個別ピン」で自然。

---

## 3. 【レイヤー2】画像：ホットリンク vs キャッシュ配信

### 3-1. 選択肢比較表

| 選択肢 | ストレージ | 配信 | 変換 | S月額 | M月額 | L月額 | 出典（確認日 2026-08-29） |
|---|---|---|---|---|---|---|---|
| **ホットリンク（元サーバ直参照）** | $0 | $0 | $0 | **$0** | **$0** | **$0** | — |
| **R2 + Cloudflare CDN + 自前imgproxy** | $0.015/GB/月 | **$0（egress無料）** | サーバCPUのみ | **~$1** | **~$10** | **~$97** | <https://developers.cloudflare.com/r2/pricing>［二次確認］ |
| **Bunny.net Storage + Volume CDN** | $0.01/GB/月/リージョン | Volume $0.005/GB（〜500TB）、Standard $0.01/GB(北米欧)〜$0.06/GB(アジア) | Optimizer $9.50/月 | **~$10** | **~$19** | **~$103** | <https://bunny.net/pricing/>（確認日 2026-08-29）、<https://bunny.net/pricing/storage/>（同） |
| **Cloudflare Images（フルマネージド）** | **$5 / 10万枚保存 / 月** | **$1 / 10万枚配信 / 月** | **$0.50 / 1,000ユニーク変換**（無料5,000/月） | **~$25** | **~$250** | **~$2,500** | <https://developers.cloudflare.com/images/pricing>［二次確認］、<https://theimagecdn.com/docs/cloudflare-images-pricing>（確認日 2026-08-29） |
| **Cloudflare Image Transformations（R2等の外部ソースを変換のみ）** | 別途 | 別途 | $0.50/1,000ユニーク変換 | 初回20万枚×2 = **$200一括** | 初回400万変換 = **$2,000一括** | 初回4,000万 = **$20,000一括** | 同上 |
| **Cloudinary** | クレジット制（1クレジット = 1GB保存 or 1GB帯域 or 1,000変換） | 同左 | 同左 | Free 25クレジット→**Plus $99/月**必要 | 約1,400クレジット必要 → **Advanced $249では不足、要見積** | 約14,000クレジット → **エンタープライズ** | <https://theimagecdn.com/docs/cloudinary-pricing>（確認日 2026-08-29）、<https://www.buildmvpfast.com/tools/api-pricing-estimator/cloudinary>（同） |
| **imgproxy セルフホスト** | 別途 | 別途 | **サーバ代のみ**。4コアVPS 1台でキャッシュ済み変換**500+ req/s** | サーバに含む | サーバに含む | サーバに含む | <https://www.pistack.xyz/posts/self-hosted-image-optimization-imgproxy-thumbor-sharp-2026/>（確認日 2026-08-29）、<https://railway.com/deploy/img-proxy>（同） |

**Cloudinary 価格の詳細**：Free 25クレジット/月、**Plus $99/月（225クレジット）**、**Advanced $249/月（600クレジット）**。実効単価は Plus で約$0.40/クレジット、Advanced で約$0.37。**Free/Plus/Advanced は超過課金をせず、警告のうえ最終的にアカウントを停止する**（＝バーストで死ぬ）。
出典：<https://theimagecdn.com/docs/cloudinary-pricing>（確認日 2026-08-29）、<https://costbench.com/software/digital-asset-management/cloudinary/free-plan/>（同）

### 3-2. 【決定的な設計判断】変換はCloudflareにやらせるな、取り込み時に自前で焼け

上表の **「Cloudflare Image Transformations」の行が最も重要**。

- 200万枚 × 2サイズ = **400万ユニーク変換 = $2,000（約32万円）**
- 同じことを **取り込みパイプラインで imgproxy / sharp を回して事前生成**すれば、**VPSのCPU時間だけ（実質$0）**

**したがって推奨は「取り込み時に派生サイズを2〜3種類生成 → R2にPUT → Cloudflare CDNで配信」**。オンザフライ変換は要らない。物件写真はユーザー生成コンテンツではなくバッチ取り込みなので、事前生成が完全に成立する。

R2への書き込み（Class A）コストも忘れずに：
- S: 40万オブジェクト → 無料枠100万以内 → **$0**
- M: 400万オブジェクト → 300万課金 × $4.50/100万 = **$13.50（一度きり）**
- L: 4,000万オブジェクト → 3,900万 × $4.50/100万 = **$175.50（一度きり）**

### 3-3. ホットリンク vs キャッシュ配信：正面比較

| 観点 | ホットリンク | キャッシュ配信（R2+CF） |
|---|---|---|
| **月額コスト（M規模）** | **$0** | **~$10** |
| **月額コスト（L規模）** | **$0** | **~$97** |
| **遮断リスク** | **高**。Refererベースのhotlink protectionで一発停止。CDN前段だとオリジンが見るRefererはCDNのIPになるためCDN層でブロックされる | 無し |
| **表示速度（LCP）** | **致命的**。元画像は300KB〜2MB のJPEG。40枚のサムネイル欄に2MB画像を並べると初回表示が数十秒 | サムネ20KB / 詳細220KB のWebP/AVIF。LCP 1秒台 |
| **リサイズ・WebP化** | 不可（元サーバのURLをそのまま使うだけ） | 自由 |
| **AI解析** | **結局ダウンロードが必要**。「配信はしないが解析はする」なら取り込み時に落とすことになり、ホットリンクの利点が半減 | 取り込み時にすでに手元にある |
| **画像消失** | 元サーバが消したら即座に壊れる。物件が成約して消えた時に**画像だけ先に404**になる | 自分の保持ポリシーで制御 |
| **規約適合** | **ソースによって真逆**。MLSのボードによっては「公式ウォーターマーク維持のため画像のローカルコピーを作るな＝ホットリンクしろ」と要求、別のボードは「画像のキャッシュを制限する」。**ソースごとに条件分岐が必要**（出典：<https://mlsimport.com/mlsimport-premium-hosting-cdn-luxury-sites/>、<https://mlsimport.com/mlsimport-photo-quality-gallery-display/>、いずれも確認日 2026-08-29） | 同左（許可されるソースのみキャッシュ） |
| **Cloudflare ToS** | 影響なし | **旧Section 2.8は自己サービス規約から削除されたが、Service-Specific Terms に残存**。Enterprise以外は**画像等の大容量ファイルを配信するには Developer Platform / Images / Stream 等の有料サービスの使用が必須**で、無しでCDNを使って「不均衡な割合の画像・音声・大容量ファイル」を配信するとCloudflareはCDNアクセスを制限・停止する権利を留保。**→ R2 を使う構成なら適合**（出典：<https://blog.cloudflare.com/updated-tos>、<https://developers.cloudflare.com/fundamentals/reference/policies-compliances/delivering-videos-with-cloudflare/>、いずれも確認日 2026-08-29［二次確認］） |

**判定：ホットリンクの節約額は M規模で月$10（約1,600円）、L規模で月$97（約1万5,000円）。**
**この金額のために、遮断リスク・LCP崩壊・画像404 を丸ごと引き受けるのは割に合わない。** 特にLCPは「室内写真を見せる」というサービスの中核価値そのものを壊す。**キャッシュ配信一択。**

ただし**規約でキャッシュが禁じられているソースだけホットリンク**という**ソース別ハイブリッド**は必要になる。設計として `image_policy: 'cache' | 'hotlink'` をソースマスタに持たせておくこと。

---

## 4. 【レイヤー3】データ取り込み

### 4-1. 各国フィードの現実（ここが本当の壁）

| 地域/ポータル | 提供形態 | 第三者が"取得"できるか | 費用 | 出典（確認日 2026-08-29） |
|---|---|---|---|---|
| **米国 MLS Grid** | RESO Web API、単一のMaster Data License Agreement | **要交渉**。公開価格表なし、データ消費者×参加MLS毎に個別見積 | 非公開（support@mlsgrid.com） | <https://www.mlsgrid.com/faq>［二次確認］、<https://docs.mlsgrid.com/>［二次確認］ |
| **米国 Bridge Interactive（Zillow）** | RESO Web API | 要審査 | **MLS単位フィードで月$500〜** | <https://www.realtyapi.io/blog/best-property-data-api>（確認日 2026-08-29） |
| **米国 Trestle（CoreLogic）** | 300+ MLSを単一RESO APIに集約 | 要審査 | エンタープライズ価格 | 同上 |
| **米国 Spark API（FBS）** | RESO Web API | 要審査 | **アクセスするMLSごとに月$50** | <https://sparkplatform.com/docs/overview/faq>（確認日 2026-08-29） |
| **米国 OneKey MLS（MLS Grid経由）** | RESO Web API | ベンダー登録要 | **フィード月$250 + ライセンス毎月$20** | <https://support.onekeymls.com/hc/en-us/articles/27251536794644-Data-Delivery-Resources>（確認日 2026-08-29） |
| **英国 Rightmove** | **公開APIは無い**。api-docs.rightmove.co.uk は**登録済み不動産業者が自社物件を登録・更新・削除するためのAPI** | **✗ 不可**。個別物件データのAPI販売はしていない。Data Services部門は集計マーケット分析のみをエンタープライズ契約で提供 | — | <https://api-docs.rightmove.co.uk/docs/property-feed-api-product/1/overview>（確認日 2026-08-29）、<https://scrapfly.io/blog/posts/how-to-scrape-rightmove>（同） |
| **独 ImmobilienScout24** | 「物件の作成・管理、掲載パフォーマンス分析、検索」用API | **主に出稿者向け**。第三者による全件取得の道は開いていない | — | <https://api.immobilienscout24.de/main/api-products/>（確認日 2026-08-29） |
| **西 idealista** | Search API あり。**申請制**（プロジェクト内容を伝えてAPIキー取得） | **△ 申請次第**。南欧のポータル/投資家ダッシュボード/市場分析向けと明記 | 非公開 | <https://developers.idealista.com/access-request>（確認日 2026-08-29、egressブロックのため検索経由）、<https://www.scrapingbee.com/blog/best-real-estate-apis-for-developers/>（同） |
| **日本 SUUMO/HOME'S/at home** | — | **✗**（R11で検証済み。ToS違反） | — | R11レポート参照 |
| **日本 REINS** | 宅建業者限定 | **✗** | — | R11レポート参照 |

**この表が示す構造的事実：**

> **主要国のポータルAPIは「物件を載せる側」のためのAPIであって、「物件を集める側」のためのAPIではない。**

Rightmove と ImmobilienScout24 の API は Create/Update/Delete が主機能である。これは偶然ではなく、ポータルのビジネスモデル（掲載課金＋自社トラフィック独占）から必然的にそうなっている。**第三者に全件フィードを渡すことは自社の存在意義を削る行為**なので、構造的に開かれない。

**米国だけが例外**で、それは NAR/MLS という「共同データベースを業界で共有する」制度があるからだ。ただしそこも **①宅建業者/認定ベンダーであること ②MLS毎に契約 ③月$50〜$500/MLS** という壁がある。米国には約500〜600のMLSがあるので、「全米カバー」は Trestle/MLS Grid のような集約業者と契約する以外になく、それはエンタープライズ価格。

**技術的結論**：取り込みパイプラインの設計自体は難しくない（後述）。**難しいのは入口の契約であり、それはエンジニアリングでは解けない。**

### 4-2. 正規化パイプラインの設計（データが取れた前提での話）

```
[ソースアダプタ層]  RESO Web API / RETS / XML feed / JSON API / CSV
        ↓ ソースごとに1ファイル、共通インタフェースに正規化
[raw_listings]     ソース原文をJSONBで無加工保存（再処理可能性の担保）
        ↓
[正規化]           単位換算(sqft↔m²)、通貨、列挙値マッピング、
                   住所パース(libpostal)、多言語フィールド分離
        ↓
[ジオコーディング]  フィード内のlat/lonを優先。無い場合のみ外部API
        ↓
[重複排除]         下記4-4
        ↓
[listings]         正規化済みマスタ（PostGIS geometry + JSONB属性）
        ↓
[派生]             画像DL→リサイズ→R2 / AI解析 / embedding / 翻訳
        ↓
[インデックス]      検索インデックス、ベクタータイル、H3集計
```

**差分更新の設計**
- RESO Web API は OData の `$filter=ModificationTimestamp gt <last_sync>` で差分取得できる。これが標準にある唯一の恩恵。
- **削除検知が最大の落とし穴**。多くのフィードは「消えたこと」をイベントで教えない。対策は2つ併用：
  1. `StandardStatus` / `MlsStatus` フィールドの変化を追う（Active → Closed / Withdrawn）
  2. **定期フルリコンサイル**（週1で全ID一覧だけを取得し、手元にあってフィードに無いものを `disappeared_at` でマーク → 7日猶予後に非表示）
- 「成約済みなのに載っている」は不動産サービスで最も信頼を壊す欠陥なので、**削除検知は機能ではなく品質の核**として扱う。

### 4-3. ジオコーディング：精度と費用と【規約の罠】

| 選択肢 | 無料枠 | 料金 | 永続保存 | 必要リソース | ソロ適性 | 出典（確認日 2026-08-29） |
|---|---|---|---|---|---|---|
| **フィード内蔵 lat/lon** | — | **$0** | 可（ソース規約次第） | — | ◎ **第一選択** | RESO標準に Latitude/Longitude あり |
| **Google Geocoding** | SKU毎10,000/月 | $5/1,000（Essentials） | **✗ 緯度経度は最大30日しかキャッシュ不可、以降は削除義務。永続保存は place_id のみ** | — | **✗ 失格** | <https://developers.google.com/maps/documentation/geocoding/policies>［二次確認］、<https://www.lunar.dev/flows/google-maps-api>（確認日 2026-08-29） |
| **Mapbox Geocoding** | 100,000/月 | temporary $0.75/1,000。permanent は別料金（高い） | permanentプラン契約なら可 | — | △ | <https://www.woosmap.com/blog/mapbox-pricing>［二次確認］ |
| **LocationIQ** | 5,000/日（"Search by LocationIQ" バックリンク条件） | **$49/月で10,000/日（月30万件、実効 $0.16/1,000）** | 可 | — | **◎ 推奨** | <https://www.bitoff.org/geocoding-apis-comparison/>（確認日 2026-08-29）、<https://scrap.io/free-geocoding-api-comparison-2026>（同） |
| **OpenCage** | 2,500/日（月約7.5万） | 約$0.35/1,000 | 可 | — | ○ | 同上 |
| **Geoapify** | 無料枠でバッチジオコーディングも可（数少ない） | クレジット制 | 可 | — | ○ | 同上 |
| **Nominatim セルフホスト（プラネット）** | — | サーバ代のみ | 可 | **RAM 128GB強く推奨（64GB未満はOOM報告不可）、ディスク1TB+、NVMe必須、インポート2.5日（SSDなら4-5日）、PostgreSQL 13+ / PostGIS 3.2+** | **✗ 予算外** | <https://nominatim.org/release-docs/latest/admin/Installation/>（確認日 2026-08-29） |
| **Nominatim セルフホスト（国別extract）** | — | サーバ代のみ | 可 | 日本単独なら 8〜32GB RAM で可 | ○ **国を絞るなら現実的** | 同上（extract運用は一般的手法） |
| **Photon セルフホスト** | — | サーバ代のみ | 可 | **RAM 64GB推奨**、プラネットDB約95GB（年10%増）。圧縮インデックスはdbモードで約60GB、jsonlモードで約26GB。**更新時はDBの2倍の空き容量が必要** | **✗ 予算外**（プラネット） | <https://github.com/komoot/photon>（確認日 2026-08-29）、<https://chibigeo.com/docs/photon/self-hosting-photon/>（同） |

**【致命的な規約リスク】Google Geocoding の緯度経度は30日でキャッシュ削除義務がある。**
> "Customer can temporarily cache latitude (lat) and longitude (lng) values from the Geocoding API for up to 30 consecutive calendar days, after which Customer must delete the cached latitude and longitude values."

物件DBは**緯度経度を永続保持することが存在意義**である。したがって **Google Geocoding はこの用途では規約上使えない**。無料枠が10,000/月あるからといって手を出すと、後で全データを作り直す羽目になる。

**推奨**：
1. まずフィード内蔵の lat/lon を使う（RESO なら大半が入っている）→ **費用$0、7〜9割カバー**
2. 欠損分だけ **LocationIQ $49/月**（月30万件）でバッチ処理
3. 国を絞れるなら **国別extractのNominatim** を Hetzner の1台に同居（追加$0）

10万物件で欠損率20%なら2万件 → LocationIQ の無料枠（5,000/日 = 月15万件）でも初回バッチが4日で終わる。**実質$0も可能。**

### 4-4. 重複排除（同一物件が複数ポータルに載る問題）

**ツール**
- **libpostal**：OpenStreetMapの**10億件以上**の住所レコードで学習された住所パース/正規化ライブラリ。`postal_normalize()` / `postal_parse()` を公開。v1.1 で**コンポーネント単位の重複排除、近似重複ハッシュ、名前のファジー重複排除**を導入。住所全体の文字列比較より、**住所要素レベルでの意味的比較**の方が圧倒的に精度が高い。
- **lieu**：libpostal の国際住所正規化を使い、**場所/POI・住所・street の重複排除**を行うPythonライブラリ。まさにこの用途向け。

出典：<https://senzing.com/what-is-libpostal/>（確認日 2026-08-29）、<https://github.com/openvenues/libpostal>（同）、<https://github.com/openvenues/lieu>（同）、<https://www.crunchydata.com/blog/quick-and-dirty-address-matching-with-libpostal>（同）

**現実的な多段マッチング設計**
1. **一意キー一致**：MLS番号 / 物件ID が同一 → 確定同一
2. **住所正規化ハッシュ**：libpostal で正規化 → `(country, city, street, house_number, unit)` のハッシュ一致 → ほぼ確定
3. **地理+属性ブロッキング**：50m以内 かつ 面積±5% かつ 部屋数一致 → 候補
4. **画像パーセプチュアルハッシュ（pHash）**：**これが実は最強**。同じ物件は同じ写真を使い回すため、写真のpHash一致は住所より信頼できる。5枚中2枚が近似一致なら同一と判定
5. **残りは信頼度スコア付きで人手レビューキューへ**

**精度の現実**：libpostal + 地理ブロッキングで **80〜90%**。残り10〜20%（同一建物の別部屋、同一部屋の別業者掲載、古い重複）はヒューリスティックの積み重ねになる。**ここを外すと地図上に同じ物件が3個並び、サービスが壊れて見える。** MVPでは「同一建物内は住所+階+間取りで束ねる」「画像pHashを必ず入れる」の2つを最初から実装すべき。

### 4-5. 多言語対応（機械翻訳）のコスト試算

**前提**：物件説明1件800文字、10言語へ展開、10万物件。

| 方式 | 単価 | 10万物件×10言語の初回コスト | 出典（確認日 2026-08-29） |
|---|---|---|---|
| **Google Cloud Translation v3** | **$20 / 100万文字**（最初の50万文字/月は無料） | 8億文字 = **$16,000 ≈ ¥255万** | <https://cloud.google.com/translate/pricing>［二次確認］、<https://www.buildmvpfast.com/api-costs/translation>（確認日 2026-08-29） |
| **Google TextTranslation LLM モデル** | $10/100万入力 + $10/100万出力 | 約 **$16,000** | 同上 |
| **DeepL API Pro（レガシー）** | $5.49/月 + **$25 / 100万文字**。※**2026年7月以降 API Free / API Pro は新規購入不可**、新規は Developer / Growth プランへ誘導 | 8億文字 = **$20,000 ≈ ¥319万** | <https://www.eesel.ai/blog/deepl-pricing>（確認日 2026-08-29）、<https://langbly.com/blog/deepl-api-pricing-guide/>（同） |
| **DeepL Growth** | $26/月に1,200万文字/年（≒月100万）、超過 $27.50/100万文字 | 実質同上 | 同上 |
| **LLM翻訳：Gemini 2.5 Flash-Lite（Batch）** | **$0.05/M入力・$0.20/M出力**（通常$0.10/$0.40の50%オフ） | 300M入力+350M出力 = **$85 ≈ ¥13,600** | <https://benchlm.ai/google/api-pricing>（確認日 2026-08-29）、<https://crazyrouter.com/en/blog/gemini-2-5-flash-lite-pricing>（同） |
| **LLM翻訳：GPT-5.4 Nano（Batch）** | $0.20/$1.25 の50%オフ = $0.10/$0.625 | **$249 ≈ ¥39,700** | <https://benchlm.ai/openai/api-pricing>（確認日 2026-08-29） |
| **LLM翻訳：Claude Haiku 4.5（Batch）** | $1/$5 の50%オフ = $0.50/$2.50 | **$1,025 ≈ ¥163,500** | `claude-api` スキル価格表（キャッシュ日 2026-06-24） |
| **LLM翻訳：Claude Sonnet 5（Batch）** | $2/$10 の50%オフ = $1/$5 | **$2,050 ≈ ¥327,000** | 同上 |

**発見：LLM翻訳は専用翻訳APIより 100〜190倍安い。**
Google Translate $16,000 vs Gemini Flash-Lite $85。品質は不動産説明文（定型的・短い・専門用語限定）なら実用上十分で、むしろ「日本語→英語で不動産用語を適切に置換する」という指示が効くぶんLLMの方が良い場合もある。

**さらに95%削減する設計**：**全件事前翻訳をしない。** 閲覧された物件×言語の組合せだけをオンデマンドで翻訳し、DBにキャッシュする。10万物件のうち実際に詳細ページが開かれるのは月数%であり、言語も英語＋現地語に偏る。実測ベースだが **初回$85 → 月$5〜20** の水準になる。検索結果一覧に必要な短いフィールド（物件名・種別・エリア）だけ事前翻訳しておけばUXは損なわれない。

> **注意**：**Gemini 2.5 Flash-Lite は 2026年10月16日に提供終了予定**（出典：<https://www.cloudzero.com/blog/gemini-pricing/>、確認日 2026-08-29）。最安モデルに設計を固定しないこと。プロバイダ抽象化レイヤを1枚入れ、モデルIDを設定で差し替えられるようにしておく。

---

## 5. 【レイヤー4】DB / 検索

### 5-1. エンジン比較

| エンジン | 地理検索 | 属性フィルタ/ファセット | 全文検索 | CJK対応 | 1本で賄えるか | ソロ適性 |
|---|---|---|---|---|---|---|
| **PostgreSQL + PostGIS + pg_trgm/tsvector + pgvector** | ◎ 最も成熟した実績あるOSS空間DB | ○（ファセット集計は工夫が要る。window関数やParadeDB系拡張で改善可） | △〜○（ネイティブFTSは弱い。pg_search 拡張なら**10M行でネイティブFTSの20〜1000倍、Elasticsearch同等以上**） | △（日本語は pg_bigm 等が必要） | **○ 実質1本で行ける** | **◎** |
| **Elasticsearch / OpenSearch** | ○ geo_point/geo_shape | ◎ 最強 | ◎ | ◎ | ◎ | **△** 運用負荷とコストが重い |
| **Meilisearch** | ○ | ○ | ◎ | **◎ charabia による中/日/韓の専用セグメンテーション。100+言語の自動言語検出** | △（地理は補助的） | **◎** |
| **Typesense** | ○ | ○ | ◎ | **✗ 弱い**。中国語/日本語は文字レベルのトークナイズ回避策になり、辞書ベースのセグメンテーションより品質が劣る。フィールド毎に明示的なlocale設定が必要 | △ | ○（ただしCJK案件では選ばない） |

出典：<https://www.paradedb.com/blog/faceting>（確認日 2026-08-29）、<https://neon.com/blog/postgres-full-text-search-vs-elasticsearch>（同）、<https://www.meilisearch.com/docs/capabilities/indexing/advanced/tokenization>［二次確認］、<https://www.meilisearch.com/comparisons/meilisearch-vs-typesense>（確認日 2026-08-29）、<https://apiscout.dev/guides/meilisearch-vs-typesense-api-2026>（同）、<https://github.com/perrygeo/spatial-search-showdown>（同）

**pgvector のスケール限界**：**1,000万ベクトル以下なら pgvector の方がエンドツーエンドで高速・安価・運用が単純**。それを超えると専用ベクタDB（Pinecone/Weaviate/pgvectorscale）を検討。10万〜100万物件なら余裕で範囲内。純ベクタ検索単独では精度62%程度で頭打ちだが、**pg_trgm + tsvector を Reciprocal Rank Fusion で組み合わせると84%+に上がる**。
出典：<https://www.instaclustr.com/education/vector-database/pgvector-performance-benchmark-results-and-5-ways-to-boost-performance/>（確認日 2026-08-29）、<https://callsphere.ai/blog/vw7h-pg-trgm-pgvector-hybrid-retrieval-2026>（同）

**推奨構成**：
- **PostgreSQL + PostGIS + pgvector を「真実の источник」**（地理・属性・ベクタ・タイル生成）
- **Meilisearch を「多言語全文検索の前段」**（CJK対応が Typesense より明確に優れる）
- 2つを同じサーバに同居させる。100万件までこれで足りる。

### 5-2. マネージド/セルフホストの実額（2026年8月）

| 選択肢 | 構成 | S(1万件) | M(10万件) | L(100万件) | 出典（確認日 2026-08-29） |
|---|---|---|---|---|---|
| **Supabase** | Free / Pro $25（$10コンピュートクレジット込、DB 8GB、ストレージ100GB、帯域100GB）。Micro→Small +$5、Medium +$50、Large +$100 | **$0**（Free） | **$30**（Pro + Small） | **$85〜**（Pro + Medium + ストレージ超過） | <https://makerkit.dev/blog/saas/supabase-pricing>（同）、<https://flexprice.io/blog/supabase-pricing-breakdown>（同） |
| **Neon** | Launch $0.106/CU-h、Scale $0.222/CU-h（1CU = 1vCPU+4GB）、ストレージ $0.35/GB-月。**2025年12月以降月額最低料金なし**、scale-to-zero | **~$5** | **~$30** | **~$90**（1CU常時 = $76 + ストレージ） | <https://www.prisma.io/blog/prisma-postgres-vs-neon-pricing-2026>（同）、<https://selfhost.dev/blog/neon-pricing-cost-of-serverless-postgres/>（同） |
| **Fly.io** | shared-cpu-1x/1GB ≈ $5.70/月、256MB ≈ $2.02/月。ボリューム $0.15/GB/月。転送 $0.02/GB(北米欧)〜$0.12/GB(アフリカ/インド)。**新規アカウントは無料枠なしの完全従量** | ~$10 | ~$40 | ~$150 | <https://deployhandbook.com/pricing/fly-io>（同）、<https://kuberns.com/blogs/flyio-pricing/>（同） |
| **Hetzner Cloud CAX21**（ARM 4vCPU/8GB/80GB） | €10.49/月 ≈ **$12.27** | ◎ | ◎ | △ | <https://costgoat.com/pricing/hetzner>（同）、<https://sparecores.com/server/hcloud/cax21>（同） |
| **Hetzner Cloud CAX31**（ARM 8vCPU/16GB/160GB） | €20.99/月 ≈ **$24.56** | ◎ | ◎ | ○（ギリギリ） | 同上 |
| **Hetzner AX41-NVMe**（専用サーバ） | **€42.30/月** ≈ $49.49（2026年4月時点で€36.70→改定） | — | ◎ | ◎ | <https://kuberns.com/blogs/hetzner-dedicated-server/>（同）、<https://klymentiev.com/blog/cheap-dedicated-server-2026>（同） |
| **Hetzner AX102** | **€122.30/月** ≈ $143。※**セットアップ費が€79→€269に値上げ** | — | — | ◎ | 同上 |
| **Meilisearch Cloud** | 月$30〜のシンプルな階層。HA/Enterpriseは要商談 | $30 | $30〜 | 要見積 | <https://www.buildmvpfast.com/api-costs/search>（同） |
| **Typesense Cloud** | 0.5GB 約$7/月〜、上位は$29.99/月〜。0.5GB〜1024GBの構成を公開 | $7 | ~$50 | ~$200+ | <https://toolradar.com/tools/typesense/pricing>（同）、<https://www.buildmvpfast.com/api-costs/search>（同） |
| **Elastic Cloud / OpenSearch マネージド** | 最小構成でも$95〜 | ✗ | ✗ | △ | — |

### 5-3. 【2026年の重大な逆風】ハードウェア価格の高騰

> **Hetzner は2026年6月15日に大幅値上げを実施した。**
> - **CCX（専用vCPU）とCPX（AMD共有vCPU）が113〜175%上昇**。CCX13 は €15.99 → **€42.99（+169%）**、CCX63 は €374.49 → €853.49
> - ARM系（CAX）とIntel共有系は**約30%上昇**
> - 専用サーバ（AX）は比較的小幅。AX41-NVMe は €35.60 → €36.70（2026年4月）→ €42.30
> - 専用サーバは2026年6月15日付で全モデルを標準化・リネーム（-1/-2/-3 型番）し再価格設定
>
> 出典：<https://northflank.com/blog/hetzner-cloud-server-price-increases>（確認日 2026-08-29）、<https://byteiota.com/hetzner-june-2026-price-shock/>（同）、<https://privatedevops.com/news/hetzner-june-2026-cloud-price-increase-what-to-do>（同）、<https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/>［二次確認］
>
> **原因**：AI企業がメモリ生産能力の大半を消費していることによる**RAM/SSDの世界的供給不足**。Netcup も18.5%値上げ、OVHcloud も価格改定を発表。Contabo は**ハードウェア調達難で一部製品の提供を停止**。
> 出典：<https://netcupvoucher.com/blog/netcup-vs-hetzner-after-rampocalypse-2026>（確認日 2026-08-29）、<https://danubedata.ro/blog/contabo-alternatives-reliability-2026>（同）

**設計への含意**：
1. **ARM（CAX / Ampere）を選べ。** 値上げ幅が最小（約30%）で、コスト/vCPU が最良。PostgreSQL・Meilisearch・imgproxy・Node/Go アプリはすべて ARM で問題なく動く。
2. **メモリを最小化する設計にする。** Nominatim プラネット（128GB）や Photon プラネット（64GB）が予算外になった主因はこれ。
3. **代替先を確保**：Netcup 入門VPS **128GB NVMe が約€5.91/月**（ISO 27001、ドイツ管轄GDPR）、Contabo 最安 **€4.5/月で 4vCPU/6GB/100GB NVMe/32TB転送**、UpCloud €5/月〜。
   出典：<https://sliplane.io/blog/top-5-cheap-vps-providers>（確認日 2026-08-29）、<https://danubedata.ro/blog/ovh-vs-hetzner-vs-danubedata-comparison-2026>（同）

---

## 6. 【レイヤー5】AI機能のコスト（10万物件規模）

### 6-1. モデル別・単価表（2026年8月）

| モデル | 入力 $/1M | 出力 $/1M | Batch（50%オフ） | 画像トークン化 | 出典（確認日 2026-08-29） |
|---|---|---|---|---|---|
| **Claude Opus 5** (`claude-opus-5`) | $5.00 | $25.00 | $2.50 / $12.50 | 長辺2,576pxまで、最大約4,784トークン/枚。約 (W×H)/750、または28×28ピクセル1パッチ=1トークン | `claude-api`スキル価格表（キャッシュ日 2026-06-24）＋ `shared/model-migration.md`, `shared/cost-optimization.md` |
| **Claude Sonnet 5** (`claude-sonnet-5`) | $2.00 | $10.00 | $1.00 / $5.00 | 同上（高解像度対応） | 同上 |
| **Claude Haiku 4.5** (`claude-haiku-4-5`) | $1.00 | $5.00 | $0.50 / $2.50 | 長辺1,568pxまで | 同上 |
| **Claude Fable 5** (`claude-fable-5`) | $10.00 | $50.00 | $5.00 / $25.00 | 上限なし | 同上 |
| **Gemini 2.5 Flash-Lite** | $0.10 | $0.40 | **$0.05 / $0.20** | **テキスト・画像・動画すべて同単価**。384px以下=258トークン、超過は768×768タイル毎に258トークン | <https://benchlm.ai/google/api-pricing>、<https://ai.google.dev/gemini-api/docs/tokens>（いずれも確認日 2026-08-29） |
| **GPT-5.4 Nano** | $0.20 | $1.25 | $0.10 / $0.625 | — | <https://benchlm.ai/openai/api-pricing>（同） |
| **GPT-5.4 Mini** | $0.75 | $4.50 | $0.375 / $2.25 | — | 同上 |
| **GPT-5.1** | $1.25 | $10.00 | $0.625 / $5.00 | — | 同上 |
| **voyage-3.5-lite（埋め込み）** | $0.02 | — | — | — | <https://futureagi.com/llm-cost-calculator/voyage-ai/voyage-3-5-lite/>（同） |
| **OpenAI text-embedding-3-small** | $0.02 | — | Batch $0.01 | — | <https://embeddingcost.com/openai>（同） |

> **重要な設計指針**：`shared/cost-optimization.md` より —「画像とPDFはフル解像度で投げず、タスクに必要な解像度まで事前に縮小せよ。ビジョン入力はピクセル面積でトークン化されるため、コストは情報量ではなく解像度に比例する。**1280×720 が安全なデフォルトで、1枚あたり約1,200トークンに抑えられる**」

### 6-2. 【試算1】室内写真のAI分析（部屋種別判定・設備検出・魅力度スコア）

**設計**：1物件につき代表8枚を**1リクエストにまとめて**投げ、構造化出力（JSON）で返させる。画像は1024×768に縮小。
- 入力：8枚 × 約1,050トークン + プロンプト400 = **約8,800トークン/物件**
- 出力：構造化JSON **約300トークン/物件**
- 10万物件 = 入力 8.8億トークン / 出力 3,000万トークン
- **Batch API（50%オフ）を必ず使う**（不動産の初回一括解析はレイテンシ非依存）

| モデル | 初回10万物件（Batch） | 円換算 | 月次更新（新規/変更5% = 5,000件） |
|---|---|---|---|
| **Gemini 2.5 Flash-Lite** | **$49** | **¥7,800** | **$2.5 ≈ ¥400** |
| **GPT-5.4 Nano** | **$105** | ¥16,750 | $5.3 ≈ ¥850 |
| **Claude Haiku 4.5** | **$515** | ¥82,150 | $26 ≈ ¥4,150 |
| **Claude Sonnet 5** | **$1,030** | ¥164,300 | $52 ≈ ¥8,300 |
| **Claude Opus 5** | **$2,575** | ¥410,800 | $129 ≈ ¥20,580 |

**現実的な運用**：「部屋種別（LDK/寝室/浴室/キッチン/外観）」「設備検出（エアコン/システムキッチン/浴室乾燥）」程度なら **Gemini Flash-Lite / GPT Nano クラスで十分**。「魅力度スコア」「リフォーム提案」など判断が要る部分だけ **Sonnet 5 / Opus 5** に回す2段構え（カスケード）が合理的。ただし `shared/cost-optimization.md` の指摘通り、**カスケードはモデル毎にキャッシュ名前空間が分かれてキャッシュ再利用を失う**点に注意。まず「最上位モデルを低effortで回す」方を先に計測すべき。

### 6-3. 【試算2】自然言語検索（embedding + ベクタ検索）

- 物件説明 約600トークン × 10万件 = **6,000万トークン**
- voyage-3.5-lite / text-embedding-3-small @ $0.02/M = **$1.20（一度きり）≈ ¥190**
- クエリ側：月10万検索 × 20トークン = 200万トークン = **$0.04/月**
- ベクタ保存：10万 × 1,024次元 × 4byte = **400MB**（512次元なら200MB）。pgvector HNSW で16GB RAM のマシンに余裕で載る

**→ ほぼ無視できるコスト。** 自然言語検索は「やらない理由がない」機能。

### 6-4. 【試算3】物件説明の多言語生成

4-5節の通り。**Gemini Flash-Lite Batch で10万件×10言語 = $85**。オンデマンド翻訳＋キャッシュにすれば **月$5〜20**。

### 6-5. AI機能の合計（10万物件）

| 項目 | 初回（Gemini Flash-Lite） | 初回（Claude Haiku 4.5） | 月次 |
|---|---|---|---|
| 画像解析 | $49 | $515 | $2.5〜$26 |
| 多言語生成（全件事前） | $85 | $1,025 | — |
| 多言語生成（オンデマンド） | ≈$0 | ≈$0 | $5〜$20 |
| Embedding | $1.2 | $1.2 | $0.04 |
| **合計（オンデマンド翻訳方式）** | **$50 ≈ ¥8,000** | **$516 ≈ ¥82,300** | **$8〜$46 ≈ ¥1,300〜7,300** |

**結論：AIは、正しく設計すれば全コストの中で最も小さい項目になる。** 初回1万円弱、月次数千円。これは「AI機能を出し惜しみする理由がない」ことを意味する。逆に、Opus 5 で全画像を非Batchで処理すると初回82万円になり、設計の差が80倍の差になる。

---

## 7. 月額コスト総合試算（3規模 × ホットリンク/キャッシュ）

**共通の構成前提**：Cloudflare Pages（フロント、無料）、Hetzner ARM（アプリ+PostGIS+Meilisearch+imgproxy）、Protomaps PMTiles on R2（地図）、R2+Cloudflare CDN（画像）、Gemini Flash-Lite Batch（AI）。

### 7-1. S規模：1万件 / 20万枚 / 月3万セッション

| 項目 | キャッシュ配信 | ホットリンク |
|---|---|---|
| サーバ（Hetzner CAX21 €10.49） | $12.27 | $12.27 |
| 画像ストレージ（R2 48GB） | $0.57 | $0 |
| 画像 egress | $0（R2無料） | $0 |
| 画像 R2 ops | $0（無料枠内） | $0 |
| 地図（PMTiles on R2 + Worker） | $6.80 | $6.80 |
| ジオコーディング | $0（フィード内蔵＋LocationIQ無料枠） | $0 |
| AI（月次） | $1 | $1 |
| ドメイン・DNS・監視 | $2 | $2 |
| **月額合計** | **$22.64 ≈ ¥3,612** | **$22.07 ≈ ¥3,521** |

**→ S規模では画像方式の差は月$0.6（約90円）。ホットリンクを選ぶ意味は皆無。**
※OpenFreeMap 公開インスタンスを使えば地図の$6.80も消え、**月$16 ≈ ¥2,550** になる。

### 7-2. M規模：10万件 / 200万枚 / 月30万セッション

| 項目 | キャッシュ配信 | ホットリンク |
|---|---|---|
| サーバ（CAX31 €20.99 + CAX21 €10.49） | $36.83 | $24.56（CAX31のみ、画像処理不要） |
| 画像ストレージ（R2 480GB） | $7.05 | $0 |
| 画像 egress | $0 | $0 |
| 画像 R2 ops（Class B、CFキャッシュ後） | $2.00 | $0 |
| 地図（PMTiles + Worker） | $17.30 | $17.30 |
| ジオコーディング（LocationIQ） | $49.00 | $49.00 |
| AI（月次：解析+翻訳+embedding） | $12.00 | $12.00 |
| バックアップ・監視・ドメイン | $8.00 | $8.00 |
| **月額合計** | **$132.18 ≈ ¥21,090** | **$110.86 ≈ ¥17,687** |
| **（LocationIQ不要な月）** | **$83.18 ≈ ¥13,271** | **$61.86 ≈ ¥9,870** |

**→ 差は月$21（約3,400円）。**
**→ 「月5〜10万円」の予算枠に対して、10万物件でも半分以下で収まる。**

### 7-3. L規模：100万件 / 2,000万枚 / 月300万セッション

| 項目 | キャッシュ配信 | ホットリンク |
|---|---|---|
| DBサーバ（AX41-NVMe €42.30） | $49.49 | $49.49 |
| アプリサーバ（CAX31 €20.99） | $24.56 | $24.56 |
| 検索サーバ（CAX31 €20.99） | $24.56 | $24.56 |
| 画像処理サーバ（CAX21 €10.49） | $12.27 | $0 |
| 画像ストレージ（R2 4.8TB） | $71.85 | $0 |
| 画像 egress | $0 | $0 |
| 画像 R2 ops | $18.00 | $0 |
| 地図（PMTiles + Worker） | $151.40 | $151.40 |
| **地図（Workerを外しR2直Range配信に変更した場合）** | **$14.40** | **$14.40** |
| ジオコーディング（LocationIQ） | $49.00 | $49.00 |
| AI（月次：10万件相当の変更分） | $46.00 | $46.00 |
| バックアップ・監視・ログ | $30.00 | $30.00 |
| **月額合計（Worker版）** | **$477.13 ≈ ¥76,122** | **$375.01 ≈ ¥59,832** |
| **月額合計（R2直Range版）** | **$340.13 ≈ ¥54,266** | **$238.01 ≈ ¥37,973** |

**→ 100万物件・月300万セッションでも「月5〜8万円」に収まる。**
**→ 差（キャッシュ vs ホットリンク）は月$102（約1万6,000円）。**

**同じ L規模を Google Maps / Mapbox / Cloudinary で組んだ場合の対比：**

| 構成 | 月額 | 円換算 |
|---|---|---|
| **推奨構成（セルフホスト地図 + R2）** | **$340** | **¥54,266** |
| 地図を Mapbox に置換 | $340 - $14 + $9,150 = **$9,476** | ¥1,511,900 |
| 地図を Google Maps に置換 | $340 - $14 + $20,930 = **$21,256** | ¥3,391,395 |
| さらに画像を Cloudinary に置換 | **$26,000+** | ¥4,148,000+ |

**この62倍の差が、本レポートで最も金額的にインパクトのある発見である。**

---

## 8. 推奨アーキテクチャ2案

### 8-1. 【案A】最小構成 — 月1万円以内 / 上限 約10〜30万物件

```
┌─ フロント ───────────────────────────────┐
│ Cloudflare Pages（無料）                             │
│ MapLibre GL JS + supercluster（〜1万件はクライアント側）│
└──────────────────────────────────────────┘
              ↓                          ↓
┌─ 地図タイル ──────────┐  ┌─ 画像 ─────────────┐
│ OpenFreeMap 公開インスタンス │  │ Cloudflare R2（48GB, $0.57）│
│  → $0（SLA無し、寄付ベース）  │  │  + Cloudflare CDN（egress $0）│
│ ※収益化後に PMTiles on R2 へ  │  │ 派生2サイズは取り込み時に   │
│   （$1.80/月）移行            │  │ imgproxy で事前生成         │
└──────────────────────┘  └────────────────────┘
              ↓
┌─ アプリ + DB + 検索 ─ Hetzner CAX21 (ARM 4vCPU/8GB) €10.49/月 ─┐
│  ・Node/Go アプリ（API + ST_AsMVT タイル生成）                    │
│  ・PostgreSQL 16 + PostGIS + pgvector + pg_trgm                  │
│  ・Meilisearch（多言語全文検索、CJK対応）                          │
│  ・imgproxy（取り込み時の派生生成）                                │
│  ・取り込みバッチ（cron）                                          │
└────────────────────────────────────────────────┘
              ↓
┌─ 外部 ────────────────────────────────────┐
│ LocationIQ 無料枠（5,000/日） / フィード内蔵 lat-lon         │
│ Gemini Flash-Lite Batch（画像解析 + オンデマンド翻訳）        │
└────────────────────────────────────────────┘
```

**月額内訳**

| 項目 | 月額 |
|---|---|
| Hetzner CAX21 | $12.27（¥1,957） |
| R2 ストレージ 48GB | $0.57（¥91） |
| 地図（OpenFreeMap） | $0 |
| ジオコーディング（無料枠） | $0 |
| AI（Gemini Flash-Lite 月次） | $1〜3（¥160〜479） |
| ドメイン・バックアップ | $3（¥479） |
| **合計** | **$17〜19 ≈ ¥2,700〜3,000** |

**扱える上限（実測ベースの見積）**
- **物件数：10万件が快適、30万件が実用上限**（8GB RAM で PostGIS + Meilisearch を同居させた場合。Meilisearch のインデックスがRAMを食うので、30万件超では CAX31 に上げる）
- **セッション：月5〜10万**（4vCPU で ST_AsMVT オンザフライ + API を捌く限界）
- **写真：60万枚（144GB、$2.16/月）まではストレージ的に無問題**

**この案の弱点**
- OpenFreeMap 公開インスタンスに依存（SLA無し）→ 収益化前提の許容リスク。移行はスタイルURL差し替えのみ
- 単一障害点（サーバ1台）→ バックアップは R2 に pg_dump を毎日投げる（$0.1/月）
- LocationIQ 無料枠はバックリンク表示が条件

### 8-2. 【案B】成長構成 — 月5〜8万円 / 上限 約100〜300万物件

```
┌─ フロント ───────────────────────────────────┐
│ Cloudflare Pages + Workers（$5/月）                       │
│ MapLibre GL JS（ベクタータイル駆動、クライアント側フィルタ）   │
└──────────────────────────────────────────────┘
      ↓                    ↓                      ↓
┌─ ベースマップ ──┐ ┌─ 物件タイル ────┐ ┌─ 画像 ──────────┐
│ Protomaps PMTiles│ │ z<11: H3集計マテビュー│ │ R2 4.8TB ($71.85)  │
│ on R2 (120GB)    │ │ z≥11: ST_AsMVT      │ │ + Cloudflare CDN   │
│ R2直Rangeで配信  │ │  → CF Cache API     │ │ egress $0          │
│ $14.40/月        │ │ 変更時のみ tippecanoe │ │ 派生3サイズ事前生成 │
└─────────────┘ └────────────────┘ └───────────────┘
      ↓
┌─ DB: Hetzner AX41-NVMe 専用サーバ €42.30 ─────────────┐
│ PostgreSQL + PostGIS + pgvector（100万件 + 100万ベクタ）     │
│ H3 集計マテビュー、パーティショニング（国別）                 │
│ レプリカ（読み取り）を CAX31 に1台                            │
└─────────────────────────────────────────────┘
┌─ アプリ: CAX31 €20.99 ──┐ ┌─ 検索: CAX31 €20.99 ──┐
│ API + タイル生成 + 取り込み  │ │ Meilisearch（多言語）      │
│ imgproxy（別プロセス）       │ │ 100万件インデックス        │
└──────────────────┘ └─────────────────┘
┌─ 外部 ────────────────────────────────────┐
│ LocationIQ $49/月（月30万ジオコード）                        │
│ Gemini Flash-Lite Batch（画像解析）+ オンデマンドLLM翻訳      │
│ Grafana Cloud 無料枠 / Better Stack（監視）                   │
└────────────────────────────────────────────┘
```

**月額内訳**

| 項目 | 月額 |
|---|---|
| Hetzner AX41-NVMe（DB） | $49.49（¥7,896） |
| Hetzner CAX31 ×2（アプリ・検索） | $49.12（¥7,837） |
| Hetzner CAX21（画像処理・バッチ） | $12.27（¥1,957） |
| R2 ストレージ（画像4.8TB + PMTiles 120GB） | $73.65（¥11,751） |
| R2 操作（Class A/B） | $18（¥2,872） |
| Cloudflare Workers | $5（¥798） |
| LocationIQ | $49（¥7,818） |
| AI（画像解析 + 翻訳 + embedding、月次） | $46（¥7,339） |
| 監視・バックアップ・ドメイン | $30（¥4,787） |
| **合計** | **$332.53 ≈ ¥53,050** |

**扱える上限**
- **物件数：100万件が快適、300万件が実用上限**（AX41 のRAM/ディスクとMeilisearchのインデックスサイズが律速。300万超は国別シャーディングが必要）
- **セッション：月300〜500万**
- **写真：2,000万枚（4.8TB）。5,000万枚（12TB, $180/月）まで線形に伸ばせる**

**1,000万物件を目指す場合の追加変更**（月10〜15万円）
- DB を国別に水平分割（AX41 を3〜4台、€169/月）
- 個票タイルの ST_AsMVT オンザフライを断念し、**tippecanoe による事前生成PMTiles + クライアント側フィルタ4属性**に切り替え
- z<12 は完全に H3 集計のみ（個票は返さない）
- Meilisearch を国別インデックスに分割
- 画像 20万GB(200TB)級になるので R2 は $3,000/月 → **Infrequent Access ($0.01/GB) と併用**、または古い物件の画像を削除するライフサイクル

---

## 9. MVP開発工数の見積

**スコープ**：1カ国・1万件・マップ表示＋写真ギャラリー＋検索/フィルタ。認証・保存機能は最小限。

| # | タスク | 素の工数 | AI支援後 | AI支援の効き | 備考 |
|---|---|---|---|---|---|
| 1 | データ取り込みパイプライン（1ソースのアダプタ、パース、正規化、スケジューラ） | 60h | **48h** | 20% | フィード固有の癖はAIが知らない。ここは自分で泥をかぶる |
| 2 | DBスキーマ設計 + PostGIS + インデックス設計 | 25h | **15h** | 40% | 定型的、AIが強い |
| 3 | 重複排除（libpostal + 地理ブロッキング + 画像pHash） | 40h | **32h** | 20% | ロジックの調整が本質で、コード量ではない |
| 4 | 削除検知・差分更新・フルリコンサイル | 25h | **18h** | 28% | |
| 5 | 画像パイプライン（DL、リサイズ、WebP、R2アップロード、再試行） | 35h | **21h** | 40% | 定型的 |
| 6 | 地図基盤（OpenFreeMap統合、ST_AsMVT、クラスタリング、H3集計） | 45h | **34h** | 25% | 性能チューニングはAIが当てにくい |
| 7 | 検索/フィルタAPI（PostGIS + Meilisearch連携、ファセット） | 30h | **20h** | 33% | |
| 8 | フロントエンド（地図UI、フィルタパネル、一覧、詳細、ギャラリー、レスポンシブ） | 80h | **48h** | **40%** | AI支援が最も効く領域 |
| 9 | i18n（2言語、翻訳キャッシュ、言語別ルーティング） | 20h | **13h** | 35% | |
| 10 | AI解析の組み込み（Batch API、構造化出力、リトライ、コスト監視） | 25h | **16h** | 36% | |
| 11 | デプロイ・CI・監視・バックアップ | 25h | **18h** | 28% | |
| 12 | 法務対応（帰属表示、出典表記、規約、プライバシーポリシー、ソース別画像ポリシー） | 15h | **12h** | 20% | |
| 13 | デバッグ・手戻り・性能調整バッファ（上記の30%） | 128h | **90h** | — | ここを削るとMVPが出ない |
| | **合計** | **553h** | **385h** | **平均30%削減** | |

**週20時間での所要**

| ケース | 工数 | 週数 | 実時間 |
|---|---|---|---|
| AI支援なし | 553h | **28週** | **約6.5ヶ月** |
| **AI支援あり（現実的な中央値）** | **385h** | **19週** | **約4.5ヶ月** |
| AI支援あり・楽観（既知フィード・1ソースのみ・重複排除を後回し） | 280h | **14週** | **約3.3ヶ月** |
| AI支援あり・悲観（フィードの癖が強い・規約対応が長引く） | 500h | **25週** | **約5.8ヶ月** |

**AI支援の効き方の内訳（実感ベースの分解）**
- **よく効く（35〜45%削減）**：フロントエンドのコンポーネント、CRUD API、スキーマ定義、画像処理の定型コード、テストコード、i18n の配線
- **そこそこ効く（20〜30%削減）**：デプロイ設定、CI、外部API連携のボイラープレート、SQL
- **ほとんど効かない（0〜15%）**：フィード固有データの癖の発見と対処、重複排除のしきい値調整、地図タイルの性能チューニング、規約解釈、「なぜ遅いか」の切り分け

**重要な但し書き**
> **上記はすべて「データが合法的に取得できている」前提のエンジニアリング工数である。**
> データ調達（MLS/ポータルとの契約交渉、宅建業者要件のクリア、審査）は**エンジニアリング工数ではなくカレンダー時間**であり、米国MLSなら数ヶ月、欧州ポータルなら「そもそも開かない可能性が高い」。**MVPの真のクリティカルパスはコードではなく契約。**
>
> R11の検証結果と合わせると、日本市場は SUUMO/HOME'S のスクレイピングが ToS違反で、REINS は宅建業者限定。**日本を1カ国目にする場合、合法的なデータソースが存在しない。** 1カ国目は米国（MLS Grid / Spark API $50/MLS）か、申請次第で開く可能性のあるスペイン（idealista）が現実的。

---

## 10. 技術的な致命的リスク（重大度順）

### 🔴 R1. データソースが構造的に開かれていない（最重大・技術では解けない）
- Rightmove、ImmobilienScout24 の公式APIは**物件を登録・更新・削除する側**のAPIであり、第三者が全件を取得する経路ではない。Rightmove は「個別物件データのAPIアクセスを販売していない」と明記される
- 米国MLSは制度的に開いているが **①宅建業者/認定ベンダー要件 ②MLS単位契約 ③月$50〜$500/MLS**。全米は約500〜600MLS
- **影響**：サービスの前提が成立しない。**技術検討より先にここを解くこと**
- 出典：<https://api-docs.rightmove.co.uk/docs/property-feed-api-product/1/overview>、<https://api.immobilienscout24.de/main/api-products/>、<https://scrapfly.io/blog/posts/how-to-scrape-rightmove>（いずれも確認日 2026-08-29）

### 🔴 R2. Google Geocoding の緯度経度は30日でキャッシュ削除義務がある
- 「最大30暦日まで一時キャッシュ可、以降は削除しなければならない」。永続保存できるのは place_id のみ
- **影響**：物件DBの中核である座標を保持できない。無料枠に釣られて使うと後で全データ再構築
- **対策**：フィード内蔵座標を第一に、欠損分は LocationIQ / OpenCage / セルフホストNominatim（国別extract）
- 出典：<https://developers.google.com/maps/documentation/geocoding/policies>［二次確認］、<https://www.lunar.dev/flows/google-maps-api>（確認日 2026-08-29）

### 🔴 R3. 画像ホットリンクは3方向から壊れる
1. **遮断**：Refererベースの hotlink protection。CDN経由だとオリジンが見るRefererがCDNのIPになるため、CDN層でのブロックになる
2. **表示速度**：元画像は300KB〜2MB。サムネイル欄に40枚並べるとLCPが崩壊し、「室内写真を見せる」という中核価値が消える
3. **404**：元サーバが物件削除時に画像を先に消すと、こちらの一覧が穴だらけになる
- **さらに厄介**：MLSのボードによって規約が**真逆**（「ローカルコピーを作るな＝ホットリンクしろ」vs「キャッシュを制限する」）。ソース別に `image_policy` を持つ設計が必須
- 出典：<https://mlsimport.com/mlsimport-premium-hosting-cdn-luxury-sites/>、<https://mlsimport.com/mlsimport-photo-quality-gallery-display/>、<https://meshworld.in/blog/web-dev/security/prevent-image-hotlinking/>（いずれも確認日 2026-08-29）

### 🔴 R4. Cloudflare は無料CDNでの偏った画像大量配信を禁じている
- 旧 Section 2.8（非HTMLコンテンツ禁止）は自己サービス規約から削除されたが、**Service-Specific Terms に実質的な制限が残存**
- 「Enterprise以外の顧客は、動画やその他の大容量ファイルをCDN経由で配信するには Developer Platform / Images / Stream 等の**有料サービスを使わなければならない**。それなしにCDNで動画や**不均衡な割合の画像・音声・大容量ファイル**を配信した場合、Cloudflareはアクセスを無効化または制限する権利を留保する」
- **影響**：「VPSに画像を置いて Cloudflare 無料プランで配信」は規約違反リスク。**R2 を使う構成なら適合する**（本レポートの推奨構成はこれ）
- 出典：<https://blog.cloudflare.com/updated-tos>、<https://developers.cloudflare.com/fundamentals/reference/policies-compliances/delivering-videos-with-cloudflare/>（いずれも確認日 2026-08-29［二次確認］）

### 🟠 R5. 多言語検索は「翻訳」だけでは解けない（言語横断マッチング問題）
- **CJKセグメンテーション**：Typesense は中国語/日本語で文字レベルのトークナイズ回避策になり、辞書ベースより品質が劣る。Meilisearch は charabia による専用パイプラインで CJK を自動処理し、100+言語の自動言語検出を持つ → **Typesense を選ぶとCJK市場で詰む**
- **言語横断（cross-lingual）**：「日本語で検索して英語の物件説明にヒットさせる」は BM25 系エンジンでは原理的に不可能。解は2つ ①全物件説明を全対象言語に翻訳して各言語インデックスを持つ（インデックスがN倍に膨らむ）②多言語埋め込みモデルでベクタ検索（精度は落ちるがインデックスは1本）
- **推奨**：構造化属性（価格・面積・部屋数・エリア）は言語非依存なので**フィルタで解く**。自由文検索は「検索言語と同じ言語の翻訳済みフィールド」に限定し、UIで「英語の説明も検索する」トグルを出す。全言語横断を無理に自動化しない
- 出典：<https://www.meilisearch.com/comparisons/meilisearch-vs-typesense>、<https://apiscout.dev/guides/meilisearch-vs-typesense-api-2026>、<https://www.meilisearch.com/blog/searching-across-multiple-languages>（いずれも確認日 2026-08-29）

### 🟠 R6. フィルタ付きベクタータイルのキャッシュキー爆発
- (z,x,y) × 任意フィルタ組合せ = 無限。キャッシュヒット率がゼロになりDBが焼ける
- **対策**：①クライアント側フィルタ可能な4〜6属性に制限してタイルは1種類だけ ②z<11 は H3集計、z≥11 は個票 ③タイルの TTL を短く（5〜15分）してCache APIで吸収
- **これを設計初期に決めないと、100万件でリライトになる**

### 🟠 R7. 重複排除の残り10〜20%
- libpostal + 地理ブロッキングで80〜90%。残りは「同一建物の別部屋」「同一部屋の別業者掲載」「古い重複」
- **地図上に同じ物件が3個並ぶと、サービス全体が壊れて見える**（信頼の一発破壊）
- **対策**：画像pHash を最初から入れる（同じ物件は同じ写真を使い回すため、住所より信頼できる）。信頼度スコア付きで人手レビューキューを持つ
- 出典：<https://github.com/openvenues/lieu>、<https://senzing.com/what-is-libpostal/>（いずれも確認日 2026-08-29）

### 🟠 R8. 削除検知の欠落 = 成約済み物件の掲載
- 多くのフィードは削除イベントを送らない
- **対策**：`StandardStatus` 追跡 + **週1のフルリコンサイル**（全ID一覧を取得し差集合を `disappeared_at` でマーク、7日猶予後に非表示）
- 「問い合わせたら成約済みでした」が続くとユーザーもリード先の業者も離れる

### 🟡 R9. 2026年のハードウェア価格高騰（進行中）
- Hetzner CCX/CPX が **2026年6月15日に113〜175%値上げ**。ARM/Intel共有系も約30%。Netcup +18.5%、Contabo は一部製品を調達難で停止
- 原因は AI企業によるRAM/SSD需要でメモリが世界的に不足
- **対策**：**ARM（CAX / Ampere）を選ぶ**（値上げ幅が最小）、メモリを最小化する設計、Netcup/OVH/UpCloud を代替として確保
- **さらなる値上げを前提に予算を20〜30%積む**
- 出典：<https://northflank.com/blog/hetzner-cloud-server-price-increases>、<https://byteiota.com/hetzner-june-2026-price-shock/>、<https://netcupvoucher.com/blog/netcup-vs-hetzner-after-rampocalypse-2026>（いずれも確認日 2026-08-29）

### 🟡 R10. 無料/寄付ベース依存の脆さ
- **OpenFreeMap 公開インスタンス**：完全無料・無制限だが Hetzner 2台上で寄付運営、SLA無し
- **Protomaps ホスト版**：無料は**非商用のみ**、100万タイルreq/月まで。商用は $14/月〜（GitHub Sponsors）
- **LocationIQ 無料枠**：バックリンク表示が条件
- **対策**：いずれも「収益が立つまでの踏み台」と割り切り、移行パスを事前に確認しておく（OpenFreeMap → PMTiles on R2 はスタイルURL差し替えのみ）
- 出典：<https://openfreemap.org/>、<https://protomaps.com/api>［二次確認］、<https://www.bitoff.org/geocoding-apis-comparison/>（いずれも確認日 2026-08-29）

### 🟡 R11. 最安AIモデルの提供終了
- **Gemini 2.5 Flash-Lite は 2026年10月16日に提供終了予定**。本レポートの最安試算（画像解析$49、翻訳$85）はこのモデル前提
- **対策**：プロバイダ抽象化レイヤを1枚入れ、モデルIDを環境変数で差し替え可能に。Batch API のインタフェース差（Anthropic/OpenAI/Google）を吸収するアダプタを最初から書く
- 出典：<https://www.cloudzero.com/blog/gemini-pricing/>（確認日 2026-08-29）

### 🟡 R12. OSM データの帰属義務（ODbL）
- MapLibre は帰属を自動付与するが、**自前でスタイルを組んだりタイルを加工した場合は自分で表示責任を負う**
- ジオコーディング結果を OSM 由来（Nominatim/Photon/LocationIQ）で得た場合も帰属が必要
- ODbL の share-alike は「派生データベース」の扱いが論点になり得る。物件DBに OSM 由来の座標を混ぜる設計は、法務的に一度整理しておくべき

### 🟢 R13. 単一障害点とバックアップ
- 案A（サーバ1台）は SPOF。**pg_dump を毎日 R2 に投げる（$0.1/月）** だけで復旧可能性が確保できる
- R2 は Cloudflare の障害と運命共同体。画像は「元URLが残っていれば再取得できる」設計にしておく（`source_image_url` を必ず保持）

---

## 11. 実行順序の推奨（技術判断のチェックリスト）

1. **【最優先・技術ではない】1カ国分の合法データソースを確定させる。** これが解けるまでコードを1行も書かない。米国 Spark API（$50/MLS）が最も入口が狭くない
2. データソースが確定したら、そのフィードの**実データを100件だけ手で眺める**。正規化設計はここからしか出てこない
3. **Meilisearch を選ぶ（Typesense を選ばない）**。CJK対応で決定的な差がある
4. **地図は最初から MapLibre + OpenFreeMap**。Mapbox/Google に触らない。移行コストが後で払えなくなる
5. **画像は取り込み時に派生生成 → R2**。オンザフライ変換に手を出さない（$2,000の差）
6. **AI は Batch API を必ず使い、画像は1280×720に縮小**。この2つで80%コストが変わる
7. **翻訳はオンデマンド + キャッシュ**。全件事前翻訳をしない
8. **重複排除に画像pHashを最初から入れる**。後付けが最も高くつく箇所
9. **フィルタ可能属性を4〜6個に固定してタイルに焼き込む**。設計を後から変えられない箇所
10. ARM（Hetzner CAX）を選び、代替ホスティング先を1つ確保しておく

---

## 12. 出典一覧（全URL・確認日 2026-08-29）

### 地図
- Mapbox 価格（二次）: <https://www.woosmap.com/blog/mapbox-pricing> / <https://help.stockist.co/article/104-how-mapboxs-free-tier-works> / <https://www.buildmvpfast.com/api-costs/maps>
- Google Maps Platform 価格（二次）: <https://www.woosmap.com/blog/google-maps-api-pricing-breakdown> / <https://mapatlas.eu/blog/google-maps-api-pricing-2026> / <https://radar.com/blog/google-maps-api-cost> / <https://www.woosmap.com/blog/is-google-maps-api-free>
- Google Maps 公式（egressブロック、検索経由）: <https://developers.google.com/maps/billing-and-pricing/overview> / <https://developers.google.com/maps/billing-and-pricing/faq> / <https://mapsplatform.google.com/pricing/>
- MapTiler: <https://www.maptiler.com/cloud/pricing/> / <https://saaspartout.com/marketplace/maptiler/> / <https://frontdeskreview.com/software/maps-api/maptiler/>
- Protomaps: <https://protomaps.com/api> / <https://docs.protomaps.com/basemaps/downloads> / <https://docs.protomaps.com/deploy/cloudflare> / <https://docs.protomaps.com/pmtiles/create> / <https://apio.sh/apis/protomaps> / <https://blog.pinballmap.com/2024/11/05/protomaps-tile-hosting/> / <https://github.com/koala73/worldmonitor/issues/1044>
- OpenFreeMap: <https://openfreemap.org/> / <https://github.com/hyperknot/openfreemap> / <https://openfreemap.org/quick_start/> / <https://simonwillison.net/2024/Sep/28/openfreemap/>
- Planetiler: <https://github.com/onthegomap/planetiler/blob/main/PLANET.md> / <https://github.com/onthegomap/planetiler> / <https://docs.protomaps.com/basemaps/build>
- tippecanoe / supercluster / deck.gl: <https://github.com/felt/tippecanoe> / <https://github.com/mapbox/supercluster> / <https://blog.mapbox.com/clustering-millions-of-points-on-a-map-with-supercluster-272046ec5c97> / <https://github.com/visgl/deck.gl/issues/3055> / <https://johal.in/tippecanoe-vector-tiles-python-geojson-optimize-2025/> / <https://walker-data.com/posts/pmtiles-texas-blocks/>
- Stadia Maps: <https://stadiamaps.com/pricing/>

### 画像・CDN・ストレージ
- Cloudflare R2: <https://developers.cloudflare.com/r2/pricing> / <https://mecanik.dev/en/posts/cloudflare-r2-pricing-explained-real-costs-vs-s3-and-backblaze/> / <https://egresscost.com/cloudflare/> / <https://flarecalc.com/calculators/r2/>
- Cloudflare Images: <https://developers.cloudflare.com/images/pricing> / <https://theimagecdn.com/docs/cloudflare-images-pricing> / <https://leanopstech.com/blog/cloudflare-images-pricing-2026/>
- Cloudflare Workers: <https://developers.cloudflare.com/workers/platform/pricing/> / <https://www.budgetforge.dev/tools/cloudflare-workers-pricing-2026>
- Cloudflare ToS: <https://blog.cloudflare.com/updated-tos> / <https://developers.cloudflare.com/fundamentals/reference/policies-compliances/delivering-videos-with-cloudflare/> / <https://news.ycombinator.com/item?id=35961697>
- Cloudinary: <https://theimagecdn.com/docs/cloudinary-pricing> / <https://www.buildmvpfast.com/tools/api-pricing-estimator/cloudinary> / <https://costbench.com/software/digital-asset-management/cloudinary/free-plan/>
- Bunny.net: <https://bunny.net/pricing/> / <https://bunny.net/pricing/storage/> / <https://theimagecdn.com/docs/bunnycdn-pricing>
- imgproxy: <https://www.pistack.xyz/posts/self-hosted-image-optimization-imgproxy-thumbor-sharp-2026/> / <https://railway.com/deploy/img-proxy> / <https://modpagespeed.com/blog/economics-of-image-optimization/>
- ホットリンク/IDX画像: <https://mlsimport.com/mlsimport-premium-hosting-cdn-luxury-sites/> / <https://mlsimport.com/mlsimport-photo-quality-gallery-display/> / <https://meshworld.in/blog/web-dev/security/prevent-image-hotlinking/>

### データソース
- MLS Grid: <https://www.mlsgrid.com/> / <https://www.mlsgrid.com/faq> / <https://docs.mlsgrid.com/>
- Spark API: <https://sparkplatform.com/docs/overview/faq>
- OneKey MLS: <https://support.onekeymls.com/hc/en-us/articles/27251536794644-Data-Delivery-Resources>
- Bridge / Trestle / 各社比較: <https://www.realtyapi.io/blog/best-property-data-api> / <https://www.scrapingbee.com/blog/best-real-estate-apis-for-developers/>
- Rightmove: <https://api-docs.rightmove.co.uk/docs/property-feed-api-product/1/overview> / <https://scrapfly.io/blog/posts/how-to-scrape-rightmove>
- ImmobilienScout24: <https://api.immobilienscout24.de/main/api-products/>
- idealista: <https://developers.idealista.com/access-request>
- MLS導入コスト: <https://mlsimport.com/estimate-diy-mlsimport-total-cost-ownership/> / <https://mlsimport.com/extra-costs-beyond-mlsimport-plugin-fee/>

### ジオコーディング・住所正規化
- Google Geocoding ポリシー: <https://developers.google.com/maps/documentation/geocoding/policies> / <https://www.lunar.dev/flows/google-maps-api> / <https://developers.google.com/maps/documentation/geocoding/geocoding-strategies>
- 各社比較: <https://www.bitoff.org/geocoding-apis-comparison/> / <https://scrap.io/free-geocoding-api-comparison-2026> / <https://mapscaping.com/guide-to-geocoding-api-pricing/> / <https://csv2geo.com/blog/geocoding-api-pricing-compared-real-cost-2026>
- Nominatim: <https://nominatim.org/release-docs/latest/admin/Installation/>
- Photon: <https://github.com/komoot/photon> / <https://chibigeo.com/docs/photon/self-hosting-photon/> / <https://news.ycombinator.com/item?id=39399064>
- libpostal / lieu: <https://senzing.com/what-is-libpostal/> / <https://github.com/openvenues/libpostal> / <https://github.com/openvenues/lieu> / <https://www.crunchydata.com/blog/quick-and-dirty-address-matching-with-libpostal>

### DB・検索
- Supabase: <https://makerkit.dev/blog/saas/supabase-pricing> / <https://flexprice.io/blog/supabase-pricing-breakdown> / <https://www.jetadmin.io/blog/supabase-pricing-2026-guide-to-plans-limits-and-real-world-costs/>
- Neon: <https://www.prisma.io/blog/prisma-postgres-vs-neon-pricing-2026> / <https://selfhost.dev/blog/neon-pricing-cost-of-serverless-postgres/> / <https://makerkit.dev/pricing-calculator/neon>
- Fly.io: <https://deployhandbook.com/pricing/fly-io> / <https://kuberns.com/blogs/flyio-pricing/> / <https://northflank.com/blog/railway-vs-flyio>
- Hetzner: <https://costgoat.com/pricing/hetzner> / <https://sparecores.com/server/hcloud/cax21> / <https://kuberns.com/blogs/hetzner-dedicated-server/> / <https://klymentiev.com/blog/cheap-dedicated-server-2026> / <https://northflank.com/blog/hetzner-cloud-server-price-increases> / <https://byteiota.com/hetzner-june-2026-price-shock/> / <https://privatedevops.com/news/hetzner-june-2026-cloud-price-increase-what-to-do> / <https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/>
- 代替ホスティング: <https://netcupvoucher.com/blog/netcup-vs-hetzner-after-rampocalypse-2026> / <https://sliplane.io/blog/top-5-cheap-vps-providers> / <https://danubedata.ro/blog/ovh-vs-hetzner-vs-danubedata-comparison-2026> / <https://danubedata.ro/blog/contabo-alternatives-reliability-2026>
- Typesense / Meilisearch: <https://www.buildmvpfast.com/api-costs/search> / <https://toolradar.com/tools/typesense/pricing> / <https://www.meilisearch.com/comparisons/meilisearch-vs-typesense> / <https://apiscout.dev/guides/meilisearch-vs-typesense-api-2026> / <https://www.meilisearch.com/docs/capabilities/indexing/advanced/tokenization> / <https://www.meilisearch.com/blog/searching-across-multiple-languages> / <https://typesense.org/typesense-vs-meilisearch/>
- PostGIS / pgvector / 全文検索: <https://www.paradedb.com/blog/faceting> / <https://neon.com/blog/postgres-full-text-search-vs-elasticsearch> / <https://xata.io/blog/postgres-full-text-search-postgres-vs-elasticsearch> / <https://www.instaclustr.com/education/vector-database/pgvector-performance-benchmark-results-and-5-ways-to-boost-performance/> / <https://callsphere.ai/blog/vw7h-pg-trgm-pgvector-hybrid-retrieval-2026> / <https://github.com/perrygeo/spatial-search-showdown>
- Vercel: <https://makerkit.dev/blog/saas/vercel-cost> / <https://costbench.com/software/developer-tools/vercel/>

### AI・翻訳
- Claude 価格・ビジョン: `claude-api` スキル価格表（キャッシュ日 2026-06-24）、同スキル `shared/cost-optimization.md` / `shared/model-migration.md` / <https://platform.claude.com/docs/en/build-with-claude/vision>
- Gemini: <https://benchlm.ai/google/api-pricing> / <https://www.cloudzero.com/blog/gemini-pricing/> / <https://crazyrouter.com/en/blog/gemini-2-5-flash-lite-pricing> / <https://ai.google.dev/gemini-api/docs/tokens> / <https://ai.google.dev/gemini-api/docs/image-understanding>
- OpenAI: <https://benchlm.ai/openai/api-pricing> / <https://www.cloudzero.com/blog/openai-pricing/> / <https://embeddingcost.com/openai>
- Voyage AI: <https://futureagi.com/llm-cost-calculator/voyage-ai/voyage-3-5-lite/> / <https://www.buildmvpfast.com/blog/best-embedding-model-comparison-voyage-openai-cohere-2026>
- 翻訳API: <https://cloud.google.com/translate/pricing> / <https://www.buildmvpfast.com/api-costs/translation> / <https://www.eesel.ai/blog/deepl-pricing> / <https://langbly.com/blog/deepl-api-pricing-guide/> / <https://chatscontrol.com/blog/deepl-api-pricing-plans-limits-2026>

### 為替
- <https://tradingeconomics.com/japan/currency>（USD/JPY 159.5540、2026-08-28時点）

---

**作成：2026-08-29 / 技術構成・コスト試算エージェント**
**※価格は変動が激しい。特にHetzner等のホスティングは2026年に大幅改定が続いているため、意思決定前に各公式ページの再確認を強く推奨する。**
