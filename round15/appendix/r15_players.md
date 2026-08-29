# R15: 「自分で計測してデータを作り、公開して収益を得る」サービスの実例調査

調査日: 2026-08-29 / 全URL確認日: 2026-08-29
調査者注記: 本セッションではWebFetchが組織のegressポリシーで全ホスト403となったため、**一次ソース（企業ブログ・IR等）の直接取得ができず、検索エンジン経由の要約に依拠している箇所がある**。数値の確度は【確】＝複数ソースまたは公式で確認 / 【推】＝第三者推定値（Owler/CBInsights/getlatka等の推定は実額と乖離しうる） / 【仮】＝本レポートの推論 として明示する。

---

## 0. 結論サマリー（先に読む用）

1. **「自前計測 × 広告のみ」でソロが食えている実例は、ほぼ存在しない。** 唯一に近いのがPhoronix（Michael Larabel、ほぼ1人）だが、本人が「広告業界の状況と読者のアドブロックで運営は年々困難」と公言し、サブスク（Phoronix Premium）と寄付を併用している。
2. **「自前計測 × アフィリエイト」は成立実例がある**（camelcamelcamel、PCPartPicker、RTINGS）。ただし**全て10人前後〜70人規模まで育ってから安定**しており、camelcamelcamelはインフラだけで月$11,000かかる。ソロで到達した例は確認できなかった。
3. **ソロで最も再現性が高いのは「自前計測 × B2Bサブスク/API販売」。** BuiltWith（実質1人で年商$14M+）、Have I Been Pwned（実質1人）、Numbeo（1〜3人、広告＋API）、Shodan（$1.9M ARR推定）。
4. **依頼主の方針（初期収益＝広告/アフィリ）は、実例上は最も薄い道。** ただし**Numbeo型（広告＋APIサブスクの併走、1〜3人、月230万訪問）**が唯一の現実的な折衷モデル。
5. **2026年、消費者向け計測サイトの検索流入は実際に死んだ。** RTINGS（月800万オーガニック訪問）が2026年3月31日にAIスクレイピングと検索流入減を理由にハードペイウォール化。Wirecutterは2025年5→8月でGoogle可視性60%超喪失。AnandTechは2024年8月に27年で閉鎖。

---

## 1. 実例マトリクス

### A. 個人・少人数が計測データを公開して収益化した例

| # | サービス | 何をどう計測 | 収益モデル | 規模 | 運営人数 | 初期集客 | 計測コスト | 現状 |
|---|---|---|---|---|---|---|---|---|
| A1 | **securityheaders.com**（Scott Helme） | 自前プローブ。指定URLにHTTPリクエストしセキュリティヘッダを採点 | サイト自体は無料。スポンサー収入のみ。本業収益は別サービス | 2015/2開始→2016/2に25万スキャン→2023/7に**2.5億スキャン**【確】 | ソロ | **HNフロントページ掲載**が25万スキャンの起点【確】 | 極小（HTTPリクエストのみ、製品購入不要） | **2023年6月Probelyが買収**。Scottは同社Strategic Advisorに。スキャンは無料継続【確】 |
| A2 | **Report URI**（同上） | 自前収集。ブラウザから送られるCSP/CT違反レポートを受信・集計 | B2B SaaSサブスク（**広告ではない**） | 課金ユーザー比率**1.98%**（2024/10時点、98.02%が無料）【確】。収益額は非公開 | Crunchbase上1-10人。Scott＋Michal Špaček等【確】 | securityheadersからの導線 | サーバー費が主。**2015〜2017年は自腹、耐えられず2017年後半に有料化**【確】 | 継続。2022/11に初値上げ、2024年に9段階→4段階に簡素化 |
| A3 | **Shodan**（John Matherly） | 自前スキャン。インターネット全体のポートスキャン＋バナー収集 | Membership一括**$49（生涯）**、Corporate **$1,099/月**、Enterprise個別【確】 | 推定ARR **$1.9M**、評価額$5.6M【推：getlatka 2025】 | 約17人（2026、4大陸）【推】 | 2009年公開。セキュリティ研究者コミュニティ | スキャンインフラ費 | 継続・独立 |
| A4 | **Artificial Analysis** | 自前計測。各社APIを継続的に叩き品質・速度・レイテンシ・価格を測定 | フリーミアム。公開リーダーボードは無料、プレミアムサブスク＋商用API＋エンタープライズデータ販売【確】。**広告ゼロ** | 250以上のモデルを比較。従業員約50人【推：Crunchbase系】 | 2023年は共同創業者2名（シドニーの地下室）→現在は法人 | **Latent Spaceポッドキャスト出演**で開発者に浸透【確】。2024年1月公開 | API課金（推論コスト）＝実費のみ | 継続。AI Grant（Nat Friedman / Daniel Gross）からシード調達 |
| A5 | **aistupidlevel.info** | 自前計測。140以上のコーディング/デバッグ課題を22モデル×7プロバイダに継続実行。CUSUM＋Page-Hinkley変化点検知で劣化を数時間内に検出【確】 | **スマートAPIルーター**（統一APIキーで最適モデルに自動ルーティング、フェイルオーバー/コスト最適化）で換金【確】 | 収益規模は非公開 | 運営はStudio Platforms（ルーマニア）【確】 | OSS＋技術メディア掲載（Gizmochina 2025/9等） | API課金が実費（各モデルを繰り返し叩く＝**継続課金が重い**） | 継続 |
| A6 | **cloudping.co / cloudping.info** | cloudping.coはAWS全リージョン間レイテンシをサーバーレスで常時計測（Matt Adorjan）。cloudping.infoはブラウザからのHTTP ping | **収益化情報が確認できない＝実質非収益** | — | ソロ | AWSコミュニティ | サーバーレスで極小 | 継続。**「レイテンシ計測サイトは広告で成立していない」という負の実例** |
| A7 | **Keepa** | 自前クロール。約60億商品の価格・ランキング履歴を追跡 | Keepa Pro **€29/月**、API **€49〜€53,500/月**【確】。**広告ではなくサブスク＋API** | Chrome拡張**400万+ユーザー**【確】。「500万+のセラー/ショッパー」自称 | Keepa GmbH（独Kemnath）、CEO Marius Johann、株主2名【確】。従業員数非公開＝少数【仮】 | **ブラウザ拡張が配布チャネル**。流入の**72.87%が直接**＝検索非依存【確】 | クロール＋ストレージ（60億商品の時系列） | 継続・堅調 |
| A8 | **camelcamelcamel** ★最重要 | Amazon Product Advertising API経由で価格履歴を追跡【確】 | **Amazonアフィリエイト100%**。サブスクなし【確】 | **月428万訪問**（2026/5）【推：Similarweb】。流入は直接48.1%＞オーガニック検索 | **10人未満**、リモートファースト【確】。2008年はDaniel Green個人プロジェクト（開発4ヶ月）【確】 | 2008/4公開。（初期集客の一次記録は本調査で未確認） | **月$11,000の維持費**（2019年時点、Cosmic Shovel）【確】 | 継続。2026年にWalmart版「Camelmart」に拡張。VCなしでオーガニックに黒字【確】 |
| A9 | **Numbeo** ★広告成立例 | クラウドソース（ユーザー投稿）＋独自インデックス算出 | **広告 ＋ APIサブスク ＋ データライセンス**【確、創業者自身の説明】 | **月230万訪問**（2026/5）、オーガニック検索64.88%【推：Similarweb】 | **1〜3人**【推：ZoomInfo/CBInsights】。元Googleエンジニア Mladen Adamović が2009/4に個人で開始【確】 | 検索流入（都市名×生活費の長尾キーワード） | ほぼゼロ（ユーザーが投稿する） | 継続 |
| A10 | **Have I Been Pwned**（Troy Hunt） | 自前計測ではなく漏洩データの収集・正規化・公開 | 企業向けAPIキー課金＋スポンサー（1Password等）。政府機関は無料【確】 | 収益非公開。「六桁収入」との報道【推】 | **実質1人**（後に妻Charlotteが運営担当として参加）【確】 | 2013年開始。セキュリティ報道・Firefox/1Password統合 | データ処理・ホスティング | 継続。2019年Project Svalbardで売却を試みたが中止し独立継続【確】 |
| A11 | **downforeveryoneorjustme.com** ★広告のみの現実 | 外形監視（指定サイトへHTTPリクエスト） | **広告のみ** | **月220万訪問**（US #5396）、流入の**80.98%がオーガニック検索**【推：Similarweb】。2018年時点で**月約$1,000グロス、AWS費用差引後はかなり少ない**【確：HN投稿 news.ycombinator.com/item?id=17795553】 | 小（Alex Payne作成→2010年Bweebが買収）【確】 | 検索流入 | AWS費 | 継続 |
| A12 | **isitdownrightnow.com** | 外形監視 | **広告のみ**（GumGum / AppNexus / OpenX / AdSense）【確：SimilarTech技術検出】 | **月52万訪問**（2026/3）、オーガニック85.7%【推：Similarweb】 | 不明（小規模） | 検索流入 | サーバー費 | 継続 |
| A13 | **Phoronix**（Michael Larabel）★ソロ×自前計測×広告の唯一格 | **自分でハードウェアを回してLinuxベンチマークを実測**。Phoronix Test Suite（OSS）＋OpenBenchmarking.org | **広告 ＋ Phoronix Premium（サブスク：広告非表示＋追加ベンチマークデータ）＋ 寄付（PayPal/Stripe）**【確】 | **年間2.5億ヒット超**【確】。週35本以上の記事 | **ほぼソロ**（記事の大半が本人バイライン）【確】。2004年開始、19年以上 | Linux/OSSコミュニティ、19年の蓄積 | ハードウェア入手（メーカー貸出＋自費）＋電力＋時間 | 継続。ただし**「アドブロック率の高さと広告市況で運営が年々困難」と本人が公言**【確】 |
| A14 | **BuiltWith**（Gary Brewer）★ソロ最強 | **自前クローラで全ウェブをスキャン**し技術スタックを判定 | **B2Bサブスク $295 / $595 / $995/月**、有料顧客**約3,000社**【確】 | **年商$14M+**（近年$22.6M/年との推定も）【推】。**月間200万PVのみ**（全てオーガニック） | **実質0〜1人**【確：複数ソース】 | ①**ReadWriteWebに独占ネタを提供 ②Diggで1位** ③その後**AboutUsが全レコードにBuiltWithリンクを設置してトラフィック10倍**【確】 | クロール＋ストレージ。**会社員をしながら毎晩4年間**開発【確】 | 継続。オーストラリア最高収益性のオンライン企業の一つと評される |
| A15 | **Flightradar24** ★趣味計測→最大成功 | **自宅屋根のADS-B受信機**で開始→2009年に一般開放→**5万台超のクラウドソース受信機網（世界最大）**【確】 | **広告 ＋ サブスク ＋ B2Bデータ販売**【確】 | **売上SEK 4.2億（約€37M）、利益SEK 2.18億（約€19M）**【確】 | 2006年にスウェーデン人**2名の趣味**として開始（Mikael Robertsson / Olov Lindberg）【確】 | **2010年アイスランド火山噴火**。報道各社が欠航の可視化に使いバイラル化【確】 | 受信機は**ユーザー負担に外部化** | 継続。PE案件化 |
| A16 | **PCPartPicker** | 各小売業者のパーツ価格を継続収集＋互換性判定 | **PPC＋PPS（アフィリエイト）**、Amazonアソシエイト参加【確】 | 年商**$6.6M**【推】、38カ国対応 | **13人**【推】。2011年 Philip Carmichael が作成【確】 | PC自作コミュニティ（Reddit等） | クロール＋正規化 | 継続 |

### B. 消費者向け計測メディアの収益

| # | サービス | 何をどう計測 | 収益モデル | 規模 | 運営人数 | 初期集客 | 計測コスト | 現状 |
|---|---|---|---|---|---|---|---|---|
| B1 | **RTINGS** ★実測メディア最重要 | **全製品を自費購入して自社ラボで実測**。累計**4,845製品**【確】 | **アフィリエイト ＋ 会員（$10/月 or $45/年）**。**ディスプレイ広告なし**【確】 | **月800万+オーガニック訪問**【確】。年商**$6.3M〜$7.3M**【推】 | **約70人**【推】。2011年 Cédric Demers が地下室で開始【確】 | 当初はレビュー集約サイト（ガジェット版Rotten Tomatoes）→2010年代半ばに自前実測へピボット【確】。検索流入で拡大 | **直近1年で618製品に$714,000**（施設・工具・人件費は別）【確】 | **2026年3月31日、全テスト結果を会員限定のハードペイウォールへ移行**。理由は**AIスクレイピングと検索流入の急減、アフィリエイト経済の悪化**。「アフィリエイトは高額商品を勧める動機を生むので、直接会員課金が唯一持続可能」と説明【確】 |
| B2 | **Consumer Reports** | **全製品を匿名で小売購入**して実測。広告を一切取らない【確】 | **会員費が収益の70%**【確】 | 収益 **$2.38億（2024-25）→ $2.67億（2025）**、費用$2.45億【確】。会員**459万人**（2025/5末、前年比約5%減）【確】 | 大組織（1936年設立の非営利） | 90年の歴史・報道 | **テストに年約$3,300万**【確】 | 継続。会員モデルが減トラフィック下で収益を守っている |
| B3 | **Wirecutter** | 年間数千製品をテスト | **アフィリエイト**（2024年から広告も追加）【確】 | **月1,500万訪問**【確】。NYTのaffiliate/licensing/other は2025Q2で$70.5M（+5.8% YoY）【確、ただしWirecutter単独ではない】 | 編集部**160〜180人**（2019年の約80人から倍増）【確】 | 2011年創業→2016年NYT買収 | 製品購入＋人件費 | 継続。ただし**2025年5月→8月でGoogle可視性を60%超喪失**【確】 |
| B4 | **DXOMARK** | 16ラボ・100人超のエンジニアでスマホのカメラ/画面/音/電池を実測【確】 | **B2Bコンサル＋チューニング受託＋ラボ機材（Analyzer）販売**。**公開サイトは非収益化**【確】 | 年商**$7.8M**【推】 | 100人超 | 2003年DxO Labsの部門→2008年公開スコアボード→2017年9月スピンアウト【確】 | ラボ設備＋エンジニア | 継続。「スコアを売っているのでは」という利益相反批判が継続的にある |
| B5 | **Ookla（Speedtest / Downdetector）** ★データ販売最大事例 | **ユーザー端末が計測装置**。月**2.5億超**の消費者起点テスト【確】 | **データライセンス＋サブスク分析**。無料消費者ツールを収集エンジンとしてB2B事業を賄う【確】 | Ziff Davisのconnectivity部門で**2025年売上$231M**（全社の約16%）【確】 | 大組織 | 2006年創業、Speedtestの圧倒的シェア | ユーザー端末に外部化 | **2026年、Accentureが$1.2Bで買収**【確】（$1.9Bとする報道もあり数値は割れている） |
| B6 | **AnandTech**（負の実例） | ハードウェアを実測 | 広告 | — | 1997年 Anand Lal Shimpi が個人で創業→Future PLC傘下 | — | — | **2024年8月30日、27年で閉鎖**。「文字のテックジャーナリズムの市場はもう戻らない」【確】。**2024年時点で検索エンジンは流入の8倍を自分で抱え込む**【確】 |

### C. 価格の定点観測

| # | サービス | 計測方法 | 収益 | 備考 |
|---|---|---|---|---|
| C1 | Keepa / camelcamelcamel | 上記A7/A8参照 | サブスク＋API / アフィリエイト | **自前で価格履歴を作っている**唯一のクラス |
| C2 | **Idealo / PriceRunner** | **小売業者が提供するフィード/API**（CSV等）を集約。**自前計測ではない**【確】 | **CPC $0.10〜$1.50 / CPA 5〜20%**【確】 | Idealoは2022年に**1,100人**【推】。参入には小売との契約が要る＝ソロ不可 |
| C3 | **価格.com（カカクコム）** | **掲載店舗からの掲載データ**。自前計測ではない | 掲載店舗からクリック数・販売実績に応じた**手数料収入**＋広告【確】 | FY26/3通期売上予想**920億円**（+17.3%）。価格.com＋食べログで全社売上の8割強【確】 |
| C4 | **モノレート（日本）★最重要の負の実例** | Amazonの価格・ランキング推移を追跡（旧Amashow） | 無料公開＋（せどり層向け）広告等 | **約10年運営後、2020年6月30日に閉鎖**。理由は**Amazonから「規約違反」と通告されたため**【確】。運営はインバイス（吉村氏）。**プラットフォーム依存の計測は規約一本で死ぬ** |
| C5 | **地域別価格差・値上げ追跡（shrinkflation系）** | The Shrink List（17万+ユーザー）、ShrinkWatch（Reddit r/shrinkflation 18万+人発）、Shrinkflation App。いずれも**コミュニティ投稿ベース**【確】 | **収益実績が確認できない** | 2025〜2026年に複数登場したが、**換金に成功した例は本調査では確認できず**。ニーズはあるが収益化は未証明【仮】 |

---

## 2. ソロで成立した例の共通条件

ソロ/2人で成立した例＝**BuiltWith、Have I Been Pwned、Numbeo、Phoronix、Flightradar24（初期）、securityheaders、camelcamelcamel（初期）**。これらに共通するのは次の7点。

### 条件1: 「誰も持っていない時系列データ」を持っている（スナップショットではなく履歴）
- BuiltWith＝技術採用の推移、Keepa/camel＝価格履歴、Phoronix＝カーネルバージョン別の性能推移、HIBP＝漏洩の蓄積。
- **単発の測定結果は誰でも再現できるので価値がない。「何年分あるか」が堀になる。**
- これはソロに極めて有利な条件でもある。堀が「時間」なので、資本でも人数でも買えない。

### 条件2: 計測の限界費用がほぼゼロ（ソフトウェアだけで測れる領域）
- 成立例は全て**製品を買わずに測れる領域**を選んでいる：HTTPヘッダ（securityheaders）、ポートスキャン（Shodan）、ウェブクロール（BuiltWith / Keepa / camel）、公開API（Artificial Analysis / aistupidlevel）、ユーザー投稿（Numbeo）。
- **例外はPhoronixとRTINGSだけで、Phoronixはメーカー貸出に依存し、RTINGSは年$714,000を払える規模まで育ってからしか実測を始めていない**（初期は他社レビューの集約サイトだった）。
- → **「自分で製品を買って測る」は、ソロの初期戦略としては成立例がゼロに近い。**

### 条件3: 検索に依存しない配布チャネルを自前で持っている
- Keepa＝Chrome拡張400万ユーザー、**直接流入72.87%**。
- camelcamelcamel＝**直接流入48.1%**、メールが3位（価格アラート通知）。
- Flightradar24＝アプリ＋受信機ネットワーク。
- Ookla＝アプリ。
- **これが2026年に生き残っている側とそうでない側を分けている最大の変数**（isitdownrightnow はオーガニック85.7%、downforeveryone は80.98%＝検索一本足で、収益も薄い）。

### 条件4: 購入意図または業務意図に直結している
- 価格追跡（買う直前）、技術スタック調査（営業リスト作成＝B2B予算）、漏洩チェック（コンプラ予算）。
- **意図が薄いデータ（レイテンシ、可用性）は広告単価もアフィリ転換も低く、cloudping系は収益化されていない。**

### 条件5: 数年の無収入期間を本業・自腹で耐えている
- BuiltWith＝会社員をしながら**毎晩4年間**。
- Report URI＝**2015〜2017年は自腹**、耐えられなくなって2017年後半に有料化。
- camelcamelcamel＝2008年公開、収益化に長期を要した。
- Flightradar24＝2006年趣味開始→2010年にブレイク（**4年**）。
- → **「1年で食う」を目標にした成立例は一件も見つからなかった。**

### 条件6: 単発の大規模露出を最低1回は掴んでいる（フォロワーゼロからの離陸点）
- securityheaders＝**Hacker Newsフロントページ**（これが25万スキャンの起点）。
- BuiltWith＝**ReadWriteWebへの独占ネタ提供 ＋ Diggで1位**、その後AboutUsの全レコードへのリンク設置で**トラフィック10倍**。
- Flightradar24＝**2010年アイスランド火山噴火**の報道需要。
- Artificial Analysis＝**Latent Spaceポッドキャスト**。
- → **共通するのは「フォロワーではなく、既存の大きな配管に一度乗る」こと。** BuiltWithのAboutUs提携が最も示唆的で、これは広報ではなく**他サービスへの組み込み（埋め込み/被リンク）**である。

### 条件7: プラットフォーム依存を持つ場合、規約リスクで死にうる
- **モノレート＝約10年運営後、Amazonの規約違反通告一本で2020年6月30日に閉鎖。**
- camelcamelcamel は公式のProduct Advertising APIを使っているため生き残っている。
- → **スクレイピング前提の設計は、事業ではなく時限爆弾。公式APIか、プラットフォームを持たない対象（インターネット全体、公開エンドポイント）を選ぶこと。**

---

## 3. 広告/アフィリで食うのに必要なトラフィック実数と、その獲得経路

### 3-1. 日本語・広告（ディスプレイ）の実数

**実データ（日本のソロ個人開発、最も参照価値が高い）:**
- **オプチャグラフ（openchat-review.me）**: LINEオープンチャットの統計を可視化するソロ開発サービス。**月6〜8万PVで月2万円前後**。内訳はリワード広告（オファーウォール）33%、ページ内広告38%、全画面広告20%。
  → **実効RPM 約250〜330円**
  → さらに重要な観察：**2025年6月にPVが3倍（19万PV）に急増したが収益はほぼ横ばい**。「エンゲージのないPVは収益に貢献しない」。
  - https://qiita.com/pikachu0203/items/8241585e0b3114891615 （確認日 2026-08-29）

**日本のRPM相場**: 雑記/トレンド系で**200〜300円**（複数ブログ運営者ソース、確認日 2026-08-29）。ガジェット・レビュー系は金融・美容より低単価。

**必要PV（日本語・広告のみ）:**

| 目標月収 | RPM 200円 | RPM 250円 | RPM 300円 |
|---|---|---|---|
| **月10万円** | 50万PV | 40万PV | 33万PV |
| **月50万円** | 250万PV | 200万PV | 167万PV |

**裏付けとなる実例（英語圏だが構造は同じ）:**
- **downforeveryoneorjustme**: 現在**月220万訪問**、しかし2018年時点の実績は**月$1,000グロス（AWS差引後はかなり少ない）**。
  → 計測ユーティリティ系サイトは **①1訪問=1PVで直帰 ②滞在数秒 ③広告在庫が薄い** ため、RPMがブログ相場を大きく下回る。**200万訪問クラスでも月15万円前後**という現実。
  - https://news.ycombinator.com/item?id=17795553 （確認日 2026-08-29）

→ **【結論】計測ユーティリティ型サイトで広告のみだと、日本語で月50万円には実質200〜400万PVが要る。ソロの新規参入で現実的な水準ではない。**

### 3-2. アフィリエイトの実数

**ベンチマーク（2026年）:**
- **EPC（1クリックあたり収益）**: 全プログラム平均 **$0.45〜$1.50**。**Amazon全体では$0.15〜$0.50/クリック**、高単価ニッチのレビューコンテンツで$0.80〜$2.00。EC系平均$0.65。
- **CVR**: EC系プログラムで **1〜3%**。高意図ニッチ（SaaS/金融）で4〜8%。
- コンテンツ型アフィリはクーポン型の**2.4倍**の転換率。
- Amazonアソシエイト日本: **2024年8月7日に1商品あたり1,000円の紹介料上限が撤廃**（高額商品で有利化）。
  - https://affiliate.amazon.co.jp/help/node/topic/GJ2QX3RTJ9ELJMPP （確認日 2026-08-29）

**必要トラフィック（アフィリエイト）:**

| 目標月収 | 必要アフィリクリック数 | 必要セッション数（CTR 2%） | 必要セッション数（CTR 5%） | 必要セッション数（CTR 15%※価格追跡型） |
|---|---|---|---|---|
| **月10万円**（≒$650、EPC $0.30想定） | 約2,200 | 11万 | 4.4万 | **1.5万** |
| **月50万円**（≒$3,300、EPC $0.30想定） | 約11,000 | 55万 | 22万 | **7.3万** |

**★最重要の含意**: 価格追跡サイトは**訪問者の目的が「買うタイミングの判断」そのもの**なので、CTRが一般ブログ（2〜5%）より桁違いに高い。camelcamelcamel が月428万訪問で**月$11,000のインフラ費を賄いつつ10人未満を養えている**ことから、**アフィリエイト収益は年間数億円規模と推定される【仮】**。

→ **【結論】広告よりアフィリエイトのほうが、同じPVで一桁良い。ただし「買う直前の人が来る」設計が絶対条件。可用性チェックやレイテンシ計測にはこの性質がない。**

### 3-3. 獲得経路（2026年に実際に生きている導線）

**死んでいる経路（確認済み事実）:**
- **ゼロクリック検索が既定**: SparkToro 2026分析で**Google検索の60%がクリックゼロで終わる**。
- **AI Overview対象キーワードで首位ページのCTRが58%減**（Ahrefs）。
- **2026年3月コアアップデートでアフィリエイトサイトの71%が順位下落**。
- 「best X for Y」型クエリはAI Overviewが直接答えるため、**中尾レビューサイトは検索段階で仕事を失った**。
- 情報系クエリ依存サイトはオーガニックセッション**20〜40%減**。

**生きている経路（実例つき）:**

| 経路 | 実力値 | 実例 |
|---|---|---|
| **① ブラウザ拡張 / アプリという配布チャネル** | Keepa: 拡張400万ユーザー、**直接流入72.87%**で検索非依存 | Keepa, camelcamelcamel, Ookla, Flightradar24 |
| **② 他サービスへの組み込み・埋め込み** | BuiltWith: AboutUsが全レコードにリンク設置で**トラフィック10倍** | BuiltWith（最も再現性が高い戦術） |
| **③ Hacker News / Reddit / X の技術コミュニティ** | HNフロントページで**24時間に1万〜3万訪問** | securityheaders（25万スキャンの起点）, PCPartPicker |
| **④ 報道フック（イベント駆動）** | 火山噴火・大規模障害など「今その数字が要る」瞬間 | Flightradar24（2010年火山）, Downdetector |
| **⑤ メール・通知（自前リスト）** | camelcamelcamel は流入3位がメール（価格アラート） | camelcamelcamel。**依頼主の「将来の通知課金」構想と一致する** |
| **⑥ ポッドキャスト/ニュースレターへの露出** | 開発者層に一気に浸透 | Artificial Analysis（Latent Space） |
| **⑦ LLM引用（新規経路）** | **CVRが桁違いに高い**: ChatGPT 15.9%、Perplexity 10.5%、Claude 5.0%、Gemini 3.0% vs Googleオーガニック1.76%。ただし**ボリュームは小さい**（AI流入の92.4%がChatGPT）。earned media経由コンテンツはAI引用が**325%多い** | Artificial Analysis型（一次データ保有者は引用先になりやすい） |

---

## 4. 最終的な問いへの回答

### Q1: 「自分で計測して公開し、広告・アフィリで食う」はソロで成立するのか

**A: 広告のみでは、ほぼ成立しない。アフィリエイトなら成立実例はあるが、いずれもソロを卒業してから安定している。**

事実ベースの整理：
- **広告のみ**で自前計測サイトが食えている例＝Phoronix（ほぼソロ、年2.5億ヒット）が唯一格だが、本人が広告だけでは苦しいと公言しサブスク＋寄付を併用。isitdownrightnow（月52万訪問）や downforeveryoneorjustme（月220万訪問で2018年に月$1,000）は「食える」水準にない。
- **アフィリエイト**では camelcamelcamel（10人未満）、PCPartPicker（13人）、RTINGS（70人）が成立。**ただし全て10人以上、または月400万訪問クラス。ソロで到達した記録は見つからなかった。**
- **ソロで実際に食えているのは全てB2B課金**: BuiltWith（1人・$14M+）、HIBP（実質1人）、Numbeo（1〜3人、広告＋API）、Shodan（$1.9M ARR）。

**依頼主の方針への直接の含意:**
「広告/アフィリを初期収益に置く」は、実例上は最も薄い道。**ただしNumbeoが唯一の反例として重要**：1〜3人・月230万訪問で、**広告 ＋ APIサブスク ＋ データライセンスを併走**させている。つまり「広告か、B2Bか」ではなく**「広告で薄く回しながら、同じデータをAPIで売る」**が、ソロが取れる唯一の現実的な形。

**さらに、依頼主の想定する「通知課金は将来」という順序は、実例と逆である可能性がある。** camelcamelcamelは価格アラート（＝通知）がメール流入を生み、それがアフィリの導線になっている。Keepaは拡張＝通知チャネルが直接流入72.87%を生んでいる。**通知は換金手段である前に、検索非依存の配布チャネルとして最初から必要**【仮】。

### Q2: 成立した実例の共通条件

上記「2.」の7条件。要約すると：
**時系列データ（時間が堀）× 限界費用ゼロの計測領域 × 検索以外の配布チャネル × 購入/業務意図への直結 × 数年の忍耐 × 一度の大規模露出 × プラットフォーム非依存**

### Q3: 必要トラフィック実数

- **広告のみ・日本語**: 月10万円＝**33〜50万PV**、月50万円＝**167〜250万PV**。計測ユーティリティ系は直帰率とPV/セッションが低いため、**実際はこの1.5〜2倍要る**【仮、downforeveryone の実績から逆算】。
- **アフィリエイト・購入意図直結**: 月10万円＝**1.5万〜11万セッション**、月50万円＝**7.3万〜55万セッション**（CTRに強く依存）。
- **広告よりアフィリが一桁効率が良い。ただし対象が「買う直前の判断」でなければこの効率は出ない。**

### Q4: 計測コストがトラフィックに先行する問題をどう乗り越えたか

実例から抽出した6つの解:

1. **本業・自腹で耐える** — BuiltWith（会社員をしながら毎晩4年）、Report URI（2015〜2017年は自腹、耐えられず有料化）、Flightradar24（趣味として4年）。**最も一般的な解であり、事実上これが標準経路。**
2. **計測コストがゼロに近い領域を選ぶ** — HTTPヘッダ、ポートスキャン、公開API、ウェブクロール。**製品を買わなくても測れるものを選ぶことで問題自体を消す。これが最も賢い解。**
3. **計測装置を外部化する** — Flightradar24（ユーザーの受信機5万台）、Ookla（ユーザー端末で月2.5億テスト）、Numbeo（ユーザー投稿）。**設備投資をユーザーに肩代わりさせる。**
4. **スポンサーを先に取る** — securityheaders は2020年9月からProbelyがスポンサー、2023年6月に同社が買収。**無料計測サイトは「広告枠」ではなく「スポンサー枠」として売れる。**
5. **公式APIを使う** — camelcamelcamel は Amazon Product Advertising API。**ただしモノレートはこれを外れて規約違反で死んだ。**
6. **実測は後から始める** — **RTINGSは当初レビュー集約サイトで、自前実測は2010年代半ばのピボット。** 年$714,000を払える規模になってから製品購入を始めた。**「最初から買って測る」を選んだ例が見つからない**のは決定的な示唆。

### Q5: 2026年、新規参入がトラフィックを得る経路はあるか

**A: 検索は主経路として使えない。だが4つの経路が実例つきで生きている。**

**まず、検索が死んだことの確認（事実）:**
- RTINGS（月800万オーガニック訪問）が2026年3月31日にハードペイウォール化。理由は**AIスクレイピングと検索流入の急減、アフィリエイト経済の悪化**。「アフィリエイトは高額商品を勧める動機を生むので、直接会員課金が唯一持続可能」。
- Wirecutterが2025年5月→8月でGoogle可視性60%超喪失。
- AnandTechが2024年8月に27年で閉鎖。
- ゼロクリック60%、AI Overview対象KWで首位CTR58%減、2026年3月コアアップデートでアフィリサイトの71%が下落。
- **消費者向け実測メディアの「検索×アフィリエイト」モデルは、2026年に業界最強のプレイヤー（RTINGS）が自ら放棄した。新規参入がこの道を選ぶ理由は無い。**

**生きている経路（優先順）:**

1. **ブラウザ拡張／アプリ**（最強）— Keepa は拡張400万ユーザーで直接流入72.87%。**検索アルゴリズムの外側に自分の配管を持つ唯一の方法。** 依頼主の「通知」構想はここに直結する。
2. **他サービスへの組み込み・埋め込み**（最も再現性が高い戦術）— BuiltWithのAboutUs提携でトラフィック10倍。**自分のデータを他人のページに置いてもらう。** 埋め込みウィジェット、バッジ、無料API、READMEバッジ等。
3. **技術コミュニティでの単発バイラル**（離陸専用）— HNフロントページで24時間1万〜3万訪問。securityheadersの離陸点。**フォロワーゼロでも乗れる唯一の大配管。ただし1回きりで、これだけでは持続しない。**
4. **報道フック（イベント駆動）** — Flightradar24（火山）、Downdetector（障害）。**「今この数字が要る」瞬間に唯一の情報源であること。** これは計測サービスの構造的な強みで、依頼主の領域でも設計できる可能性がある。
5. **LLM引用（新規・小さいが質が高い）** — ChatGPT経由CVR 15.9% vs Googleオーガニック1.76%。**一次データの唯一の保有者はAIに引用されやすい**（Artificial Analysisはこの位置を取った）。ただしボリュームは小さく、**引用されても流入は薄い**ので、これ単体を収益基盤にはできない【仮】。

**新規参入への総合判断【仮・本レポートの推論】:**
2026年に消費者向け計測サイトを新規に立てて**広告で食うのは、実例上ほぼ不可能**。取りうる形は次のいずれか：
- **(a) Numbeo型**: 限界費用ゼロの計測 ＋ 検索の長尾 ＋ 広告 ＋ APIサブスク併走。1〜3人規模。
- **(b) Keepa/camel型**: 拡張機能・通知を最初から配布チャネルとして作り、購入意図に直結する計測（価格）でアフィリ換金。**ただしプラットフォーム規約リスク（モノレートの死）が常につきまとう。**
- **(c) BuiltWith/HIBP型**: 広告を捨て、最初からB2B課金。ソロで最も収益効率が高い（BuiltWithは月200万PVで年商$14M＝トラフィックではなく単価で成立）。
- **(d) 撤退判断**: 「自分で製品を買って実測して広告/アフィリ」は、RTINGSが2026年に自ら放棄したモデル。**ソロが今から入る道ではない。**

---

## 5. 出典一覧（全て確認日 2026-08-29）

### A. 個人・少人数の計測公開
- Scott Helme「Celebrating 250,000,000 scans on Security Headers!」 https://scotthelme.co.uk/celebrating-250-000-000-scans-on-security-headers/ ※本セッションでは直接取得不可（egress 403）、検索経由で内容確認
- Scott Helme「Security Headers is joining Probely!」 https://scotthelme.co.uk/security-headers-is-joining-probely/
- David Strom「Scott Helme and Probely join forces on SecurityHeaders.com」 https://strom.wordpress.com/2023/06/28/scott-helme-and-probely-join-forces-on-securityheaders-com/
- Scott Helme「Report URI: Simplifying pricing and changes to free accounts」 https://scotthelme.co.uk/report-uri-simplifying-pricing-and-changes-to-free-accounts/
- Scott Helme「New pricing for Report URI」 https://scotthelme.co.uk/new-pricing-for-report-uri/
- Crunchbase: Report-uri.io https://www.crunchbase.com/organization/report-uri-io
- Shodan Book / Platform https://book.shodan.io/getting-started/platform/
- Shodan Pricing（TrustRadius） https://www.trustradius.com/products/shodan/pricing
- getlatka: Shodan Revenue 2025 https://getlatka.com/companies/shodan.io 【推定値】
- Artificial Analysis https://artificialanalysis.ai/
- Grokipedia: Artificial Analysis https://grokipedia.com/page/artificial-analysis
- PitchBook: Artificial Analysis https://pitchbook.com/profiles/company/680302-90
- AIStupidLevel https://aistupidlevel.info/
- Gizmochina「Open-source tool now measures the 'stupidity level' of AI models in real time」 https://www.gizmochina.com/2025/09/18/open-source-tool-now-measures-the-stupidity-level-of-ai-models-in-real-time/
- CloudPing.co About https://www.cloudping.co/about
- GitHub: mda590/cloudping.co https://github.com/mda590/cloudping.co
- Keepa Chrome Web Store https://chromewebstore.google.com/detail/keepa-amazon-price-tracke/neebplgakaahbhdphmkckjjcegoiijjo
- Keepa Pricing 2026（RevenueGeeks） https://revenuegeeks.com/keepa-pricing/
- Similarweb: keepa.com https://www.similarweb.com/website/keepa.com/ 【推定値】
- camelcamelcamel About https://camelcamelcamel.com/about
- Software Engineering Daily「CamelCamelCamel: Amazon Price Tracker with Daniel Green」（2019/5/24） https://softwareengineeringdaily.com/2019/05/24/camelcamelcamel-amazon-price-tracker-with-daniel-green/ ／ 文字起こしPDF https://softwareengineeringdaily.com/wp-content/uploads/2019/05/SED837-CamelCamelCamel.pdf ※直接取得不可
- Similarweb: camelcamelcamel.com https://www.similarweb.com/website/camelcamelcamel.com/ 【推定値】
- Grokipedia: Camelcamelcamel https://grokipedia.com/page/Camelcamelcamel
- Numbeo Cost of Living API https://www.numbeo.com/api/cost-of-living-api
- Similarweb: numbeo.com https://www.similarweb.com/website/numbeo.com/ 【推定値】
- TechCrunch「How Have I Been Pwned became the keeper of the internet's biggest data breaches」 https://techcrunch.com/2020/07/03/have-i-been-pwned/
- Troy Hunt「Project Svalbard, Have I Been Pwned and its Ongoing Independence」 https://www.troyhunt.com/project-svalbard-have-i-been-pwned-and-its-ongoing-independence/
- HIBP About https://haveibeenpwned.com/About
- Hacker News「Down For Everyone Or Just Me ... Makes ~$1,000 ...」 https://news.ycombinator.com/item?id=17795553 ★広告のみ計測サイトの実収益
- Similarweb: downforeveryoneorjustme.com https://www.similarweb.com/website/downforeveryoneorjustme.com/ 【推定値】
- Similarweb: isitdownrightnow.com https://www.similarweb.com/website/isitdownrightnow.com/ 【推定値】
- SimilarTech: isitdownrightnow.com 技術検出 https://www.similartech.com/websites/isitdownrightnow.com
- Phoronix / Michael Larabel https://www.phoronix.com/michaellarabel
- 「Phoronix at 19: The Linux Benchmark Standard Behind AWS」 https://aiforautomation.io/news/2026-04-28-phoronix-19-years-linux-hardware-michael-larabel
- Startup Daily「BuiltWith is perhaps one of Australia's most profitable online companies and has zero staff」 https://www.startupdaily.net/advice/builtwith-is-perhaps-one-of-australias-most-profitable-online-companies-and-has-zero-staff/
- Colin Keeley「The Story of BuiltWith: 1 Employee, $14m+ ARR」 https://www.colinkeeley.com/blog/the-story-of-builtwith-1-employee-14m-arr
- Starter Story「How Gary Brewer Stumbled Into A $14M Idea Profiling Websites」 https://www.starterstory.com/stories/builtwith-technology-lookup-breakdown
- Flightradar24 About https://www.flightradar24.com/about/
- Dealroom「Flightradar24's PE Deal & Founders' Story」 https://app.dealroom.co/news/note/flightradar24-s-pe-deal-founders-story
- PCPartPicker Disclosure https://pcpartpicker.com/disclosure/
- 「How does PCPartPicker make money?」 https://pcpartpicker.com/forums/topic/16195-how-does-pcpartpicker-make-money

### B. 消費者向け計測メディア
- RTINGS About Us https://www.rtings.com/company/about-us ※直接取得不可
- RTINGS「Revamping Our Membership Program」 https://www.rtings.com/company/revamping-our-membership-program
- Niche Pursuits「How RTings Attracts 8+ Million Organic Visitors Per Month And Profits Without Ads」 https://www.nichepursuits.com/rtings-success-story/ ★$714,000 / 618製品
- Back2Gaming「RTINGS Locks Full Test Results Behind a Paywall to Combat AI Scraping」 https://www.back2gaming.com/news/rtings-locks-full-test-results-behind-a-paywall-to-combat-ai-scraping/
- Fast Company「RTings: How a group of Canadians write the best TV reviews on the web」 https://www.fastcompany.com/90986256/rtings-tv-reviews-cedric-demers
- Consumer Reports Annual Report 2025 Financials https://www.consumerreports.org/annual-report/2025/financials/
- Consumer Reports Annual Report 2024 Financials https://www.consumerreports.org/annual-report/2024/financials/
- What's New in Publishing「Consumer Reports' Membership Model Shields Revenue as Traffic Declines」 https://whatsnewinpublishing.substack.com/p/consumer-reports-membership-model
- Forbes「Wirecutter's Path To $1 Billion In Commerce, One Product Review At A Time」（2025/10/7） https://www.forbes.com/sites/andymeek/2025/10/07/wirecutters-path-to-1-billion-in-commerce-one-product-review-at-a-time/
- A Media Operator「New York Times Digital Ad Revenue Growth Accelerates」 https://www.amediaoperator.com/news/new-york-times-q2-2025-earnings-digital-ad-revenue/
- DXOMARK Corporate（Smartphone） https://corp.dxomark.com/smartphone/
- Grokipedia: DxOMark https://grokipedia.com/page/DxOMark
- TNW「Accenture buys Speedtest and Downdetector in $1.2B deal」 https://thenextweb.com/news/accenture-buys-speedtest-and-downdetector-in-1-2b-deal
- Kunal Ganglani「Why GTCR Paid $1.3B for Ookla's Network Data」 https://www.kunalganglani.com/blog/gtcr-ookla-speedtest-billion-dollar-network-intelligence-play
- Slashdot「AnandTech Shuts Down After 27-Year Run」 https://news.slashdot.org/story/24/08/30/1235233/anandtech-shuts-down-after-27-year-run
- The Silicon Underground「Anandtech shut down abruptly, August 30, 2024」 https://dfarq.homeip.net/anandtech-shut-down-abruptly-august-30-2024/

### C. 価格の定点観測
- idealo（Wikipedia） https://en.wikipedia.org/wiki/Idealo ※直接取得不可
- Track360「Comparison Shopping Engines (CSS) for Affiliate Programs」 https://track360.io/blog/comparison-shopping-engines-css-ecommerce-affiliate-2026
- カカクコム ビジネスモデル https://corporate.kakaku.com/ir/individual/businessmodel
- カカクコム FY26/3 Q2 決算説明資料（2025/11/5） https://www2.jpx.co.jp/disc/23710/140120251105587593.pdf
- モノレート お知らせ https://mnrate.com/announce
- Amazonセラーセントラル「モノレート閉鎖（6/30）のお知らせ」 https://sellercentral.amazon.co.jp/seller-forums/discussions/t/595cb88c53af8e8daa4d930d81957f04
- ERESA「モノレートがサービス終了！」 https://eresa.jp/column/monorate/
- The Shrink List https://theshrinklist.com/
- ShrinkWatch https://shrinkwatch.app/about

### D. 収益・トラフィック単価
- Qiita「個人開発WEBサービスのAdSense収益20ヶ月分を公開する - 月2万円の内訳と、効いた施策」 https://qiita.com/pikachu0203/items/8241585e0b3114891615 ★日本ソロ実データ
- Google AdSense ヘルプ「インプレッション収益（RPM）」 https://support.google.com/adsense/answer/190515?hl=ja
- 千愛「グーグルアドセンスのインプレッション収益とPVの目安」 https://affimama.com/adsense-profit-pv/
- ToolSignal「Display Ad RPM by Niche in 2026」 https://toolsignal.site/articles/blog-display-ad-rpm-by-niche-2026
- Newor Media「Best Ad Networks for Publishers in 2026: Ranked by RPM」 https://newormedia.com/blog/best-ad-networks-for-publishers-2026/
- DollarPocket「Affiliate Marketing Benchmarks 2026: CVR, EPC & Commission Rates」 https://www.dollarpocket.com/affiliate-marketing-benchmarks-2026/
- wecantrack「Affiliate Program Performance Statistics: 2026 Benchmarks」 https://wecantrack.com/insights/affiliate-program-performance-statistics/
- Amazonアソシエイト「紹介料上限の廃止のご案内」 https://affiliate.amazon.co.jp/help/node/topic/GJ2QX3RTJ9ELJMPP
- Amazonアソシエイト 紹介料率表 https://affiliate.amazon.co.jp/promotion/advertisingfeeschedule

### E. 2026年の検索・AI流入環境
- SeoProfy「Google AI Overviews: Statistics and Trends in 2026」 https://seoprofy.com/blog/google-ai-overviews/
- SEO-Kreativ「AI Overviews Traffic 2026: 58% CTR Drop and Google's Response」 https://www.seo-kreativ.de/en/blog/google-ai-overviews-updates-2026-en/
- AffiliateBay「Google's AI Overviews Are Cutting Affiliate Traffic」 https://affiliatebay.net/googles-ai-overviews-are-affiliate-traffic/
- Affiliyo「Is AI killing affiliate marketing? The 2026 data」 https://affiliyo.com/blog/is-ai-killing-affiliate-marketing-2026
- Indexly「The State of LLM Referral Traffic in 2026」 https://indexly.ai/blog/state-of-llm-referral-traffic/
- AuthorityTech「LLM Referral Traffic Converts 5-9x Higher Than Organic」 https://authoritytech.io/blog/llm-referral-traffic-conversion-optimization-2026
- Previsible「2026 AI Traffic Report: ChatGPT Wins 92% Share」 https://previsible.com/seo-strategy/ai-traffic-report-july-2026/
- Awesome Directories「How to Reach Hacker News Front Page: Data from 14 Launches & 10M+ Posts」 https://awesome-directories.com/blog/hacker-news-front-page-guide/

---

## 6. 調査の限界

1. **WebFetchが組織のegressポリシーで全ホスト403となり、一次ソース（scotthelme.co.uk、rtings.com、softwareengineeringdaily.com、Wikipedia等）の直接取得ができなかった。** 上記の【確】マークは検索エンジンの要約経由で複数ソースが一致したものだが、原文の細部（正確な日付・金額の桁）は再確認が望ましい。
2. **非上場企業の収益（Keepa、camelcamelcamel、RTINGS、Shodan、DXOMARK、BuiltWith、Numbeo）は全て第三者推定値**であり、実額との乖離が大きい可能性がある。特にOwler/ZoomInfo/CBInsights/getlatkaの推定は幅がある。
3. **Similarwebのトラフィック数値は推定**。特に「traffic value $570.4K」のような指標は広告収益ではなくSEO価値換算であり、収益と読み替えてはならない。
4. **camelcamelcamel・Keepaの初期集客の一次記録が取れなかった。** SED podcast の文字起こしPDFにDaniel Greenの証言があるはずだが、取得できていない。**依頼主にとって最重要の論点（フォロワーゼロからどう離陸したか）なので、後日この一次ソースを当たることを強く推奨する。**
5. **日本国内のソロ計測サービスの収益実例は、オプチャグラフの1件しか具体的な数字を確認できなかった。** 日本語圏の個人開発コミュニティ（Zenn、Qiita、個人開発者のポッドキャスト）にはさらに事例がある可能性が高い。
