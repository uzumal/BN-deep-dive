# R13 競合・差別化調査：グローバル物件マップ×「新しい導線」

**調査日: 2026-08-29**（本文中の全URLの確認日は特記なき限り 2026-08-29）
**依頼主前提**: 日本在住ソロエンジニア／日英可／元Cisco SE・Webエンジニア／フォロワー0・広告予算0
**スコープ**: 「世界中の賃貸・売買物件を1つのマップで見られ、物件を押すと室内写真が見られる」サービスの競合と、まだ空いている体験（導線）

---

## 0. 調査手法の限界（先に開示）

- 本セッションでは **egress proxy により WebFetch が全ドメインで遮断**された（properstar.com, nomads.com, globalpropertyguide.com, en.wikipedia.org, ja.sekaiproperty.com など全て `EGRESS_BLOCKED`）。したがって **一次ソースの画面を直接確認できていない**。全事実は検索エンジン経由の要約と、複数クエリでの突き合わせによる。
- そのため各事実に **確度ラベル**を付す：
  - `[高]` = 複数の独立系ソース、または当事者自身の公式ページの記述が検索結果に現れたもの
  - `[中]` = 単一の二次ソース（業界メディア／レビューサイト）
  - `[低]` = 推定を含む／数値がソース間で食い違う
- **「空白」の主張には、必ず敵対的検索のクエリと結果を併記**した。ヒットしなかったことは「存在しない」証明ではなく「検索到達性が低い」に過ぎない点も明記する。

---

## 1. 既存プレイヤーのマトリクス

### 1-A. グローバル横断ポータル（売買中心）

| サービス | カバー | 掲載件数 | マップUI | 室内写真 | 収益モデル | 運営規模 |
|---|---|---|---|---|---|---|
| **Properstar**（旧ListGlobally） | 60〜100カ国（ソース間で差） `[低]` | 300万件+ `[中]` | あり。地図上の**フリーハンド描画検索**を実装。2026年に**AI検索**を投入 `[中]` | あり（エージェント配信フィード由来） | 買い手は無料。**エージェント課金＋70以上のポータルへのシンジケーション（25言語自動翻訳）** `[中]` | **Properstar SA（スイス・ローザンヌ）、従業員73名** `[中]`。2009年創業 |
| **JamesEdition** | 120〜140カ国（ソース間で差） `[低]` | 20万〜77万件（ソース間で大きく食い違う） `[低]` | あり（ラグジュアリー特化） | あり | プレミアム掲載料・広告・B2Bエージェンシー契約 `[中]` | **JamesEdition B.V.（アムステルダム）、従業員35〜51名程度、Verdane Group が買収** `[中]` |
| **Green-Acres** | 22〜56カ国（欧州セカンドホーム中心＋イスラエル・UAE） `[低]` | 28.8万〜40万件 `[低]` | あり | あり | **2022年にリード課金→サブスク移行。€99/月〜（掲載数連動）。売買手数料ゼロ。約2万エージェント** `[中]` | 企業（仏 Realist 系） |
| **Kyero** | スペイン・ポルトガル・フランス・イタリア | 50万〜70万件（うちスペイン40万） `[低]` | あり | あり | **フリーミアム。基本掲載無料＋"Kyero Prime" 有料枠（€3〜6/物件/月、25枠€450/3ヶ月 等）。約5,000エージェント** `[中]` | 企業（Portal47 Ltd）。**2024年12月にidealistaが買収発表 → 2025年9月24日にidealistaが撤回**（スペインCNMC・ポルトガルAdCの競争法審査が第2フェーズ入りしたため）。**Kyeroは独立を維持** `[高]` |
| **thinkSPAIN** | スペイン特化（オーディエンスは国際） | 25万件+ | あり | あり | 掲載パッケージ課金。約2,000広告主、月5万件の問い合わせ、12言語 `[中]` | 企業（2003年〜） |
| **Rightmove Overseas** | 50〜90カ国（ソース間で差）。実質は西欧＋地中海 `[低]` | 約20万件 `[低]` | 英国本体ほどのマップ品質ではない `[低]` | あり | **個人売主 £130/月、エージェントはコアメンバーシップ £1,150〜1,295/月（2020-21年数値）。売買手数料なし** `[中]` | 上場企業。※本体は2026年4月に**£15億の集団訴訟**（市場支配的地位濫用・「不当な」手数料）を提起されている `[中]` |
| **Realtor.com International** | News Corp/REA Group の "Global Property Network"、**56カ国・300万件超、12サイト、月2億訪問** `[中]` | 300万件+ | サイト横断のネットワーク（統一マップではない） | あり | ポータル横断広告／リード | 大企業（News Corp） |
| **Juwai / Juwai IQI** | **91カ国・年間600万件**、アジア（特に中華圏）バイヤー向け `[中]` | 600万件/年 | あり | あり | **広告課金（Juwai.com）＋自社仲介（IQI Global）のハイブリッド** `[中]` | アジア最大級のプロップテック企業 |
| **Tranio / Realting / HomesGoFast** | Tranio 9万件超、HomesGoFast 50カ国超 | 中規模 | 簡易 | あり | Tranioは**ブローカー寄り（仲介手数料）**、HomesGoFastは掲載型 `[中]` | 中小企業 |
| **Global Listings / Global Properties / Landelity** | 50カ国前後を標榜 | 不明 | Landelityは「全世界マップ＋区画境界」を標榜 `[低]` | あり | 掲載・無料掲載 | 小規模 `[低]` |
| **セカイプロパティ（日本語）** | カンボジア・フィリピン・マレーシア・タイ・ベトナム・ドバイ・米国・ハワイ等 | 不明 | あり `[低]` | あり | **投資向け送客・仲介** `[低]` | 企業（日本） |

### 1-B. 賃貸・中長期滞在（実質的にグローバル賃貸マップの競合）

| サービス | カバー | 件数 | 収益モデル | 規模 |
|---|---|---|---|---|
| **Rentola** | **36カ国**（各国ローカルドメイン） `[中]` | **100万件超**、**2,400サイトからのアグリゲーション** `[中]` | **借主課金サブスク（€1トライアル→月額、£35報告あり）**。Trustpilot 1.9〜2.2 と評判は極めて悪く、解約困難の告発多数 `[中]` | Reva Media ApS（デンマーク） |
| **HousingAnywhere** | 125都市超。2024年にKamernet統合後、Amsterdam/Berlin/Paris に集中 `[中]` | Rent Index は25都市・11カ国・35,399件ベース `[高]` | 借主手数料＋家主向けツール | 企業 |
| **Spotahome** | 欧州80都市超 | — | **借主のブッキング手数料（家賃約25%相当の一時金）＋家主サービス料** `[中]` | 企業 |
| **Blueground** | **32都市・17カ国**（50都市超の記述もあり） `[低]` | — | **マスターリース運営＋7%コミッション** `[中]` | 累計 $302M 調達 `[中]` |
| **Flatio** | **17カ国・60都市・17,000件超** `[中]` | 17,000+ | **掲載無料。家主手数料 5%（個室）／7.5%（一棟）**。全リースがビザ用の住所証明になる（ポルトガルD8等） `[中]` | 中小企業（チェコ） |
| **Anyplace / TripOffice / Nomad Stays** | TripOffice は **100カ国超・20万件**（デスクと椅子を保証） `[中]` | — | 予約手数料／アフィリエイト | 小〜中規模 |
| **Airbnb（長期）** | 全世界 | — | **28泊以上の予約が総宿泊夜数の17%（2025年Q4）**。2022年の21%からは低下。長期滞在予約者の55%が仕事・学業目的（2024年） `[中]` | 巨大企業 |
| **Nestpick** | 200都市超の家具付き比較 | — | 送客 | **2023年5月にBluegroundが買収** `[中]` |

### 1-C. データ層（物件を持たない）

| サービス | カバー | 物件リンク | 収益 |
|---|---|---|---|
| **Numbeo** | 12,859都市・989万価格・88.6万投稿者 `[中]` | **なし**（家賃指数のみ）。地図あり | **APIライセンス $50〜500/月、COL estimator $260/月** `[中]` |
| **Global Property Guide** | 80〜87カ国、38指標、400地点超の中央値家賃 `[中]` | **なし** | データ・広告 |
| **Nomad List / nomads.com** | 1,000〜2,000都市、10万データポイント `[中]` | **なし**（"Airbnb price vs rent price" は指標として持つが実物件へのリンクは確認できず） `[低]` | **$149買い切り／月$8〜30サブスク** `[中]` |
| **WhereNext** | 95カ国・380都市 | **なし。公式に「実際の賃貸物件は idealista / Inmuebles24 / DDProperty / 99.co で見よ」と外部ポータルへ誘導している** `[高]` | 無料＋不明 |
| **LivingCost / ExpatsList / Where Can I Live** | 9,294都市197カ国／250都市／315都市96カ国 | **なし** | 広告・アフィリエイト |

---

## 2. 構造的な結論：「世界の物件を1つのマップ」自体はもう空白ではない

**判定：❌ 埋まっている。** 敵対的検索の結果、以下がすでに存在する：

- Properstar：60〜100カ国／300万件／地図描画検索／AI検索（2026年投入）／73名体制
- JamesEdition：120〜140カ国／地図
- Rentola：36カ国／100万件超／2,400サイトからのアグリゲーション
- Juwai：91カ国／年600万件
- Realtor.com International：56カ国／300万件超のネットワーク
- Green-Acres：22〜56カ国

検索クエリ（英）: `"world map" real estate listings all countries single map browse properties globally without selecting country` / `Properstar map search worldwide zoom out global map price filter` / `Rentola rental portal countries coverage listings aggregator international`
検索クエリ（日）: `世界の物件 地図 海外不動産 マップ 検索 サービス 日本語 移住` / `海外 賃貸 物件 横断検索 世界 日本語 サイト 個人 移住 探す 比較`

→ **「マップ＋室内写真」という基本形は差別化にならない。**

### そしてソロには「供給の壁」がある（最重要）

これが今回いちばん重い発見。

1. **主要ポータルのAPIは"出稿用"であって"検索用"ではない。**
   Rightmove（Real Time Data Feed／Commercial Listings API）、Zoopla、idealista はいずれも**エージェント／ソフトウェアベンダー向けのパートナーAPIのみ**を提供し、公開検索APIは存在しない。これらは「掲載管理のためのAPIであり、オープンな検索用ではない」と明示的に整理されている。 `[中]`
   - https://www.scrapingbee.com/blog/best-real-estate-apis-for-developers/ （確認日 2026-08-29）
   - https://www.realtyapi.io/blog/best-property-data-api （確認日 2026-08-29）

2. **スクレイピングはToS違反かつ技術的に困難。**
   idealista の一般条件は「reproduce / scrape / monitor / deep-link を商用目的で行うことを許諾しない」と明記。技術的にも **DataDome WAF＋地域制限＋CAPTCHA** で「最も防御の固いサイトのひとつ」と評されている。 `[中]`
   - https://www.idealista.pt/apoioutilizador/artigos/aviso-legal-e-condicoes-gerais/?lang=en （確認日 2026-08-29）
   - https://scrapfly.io/blog/posts/how-to-scrape-idealista （確認日 2026-08-29）

3. **唯一の現実的な合法ルート＝エージェント側が自発的に出す XML フィードを受ける。**
   **Kyero XML** は国際不動産エージェント間で「事実上の業界標準になりつつある」（BLM と並ぶ）フォーマットで、公開仕様がある。Property Hive（WordPress）等のサードパーティも取り込み対応済み。XML2U のようなサービスが月$16程度でフィードを持たないエージェントの代わりにフィードを生成し、「好きなだけポータルに出す」構造がすでにある。
   - https://help.kyero.com/estate-agents/xml-import-specification （確認日 2026-08-29）
   - https://wp-property-hive.com/kyero-xml-added-list-supported-import-formats/ （確認日 2026-08-29）
   - https://estateagentfeeds.com/ （確認日 2026-08-29）
   → **つまり「トラフィックさえ作れれば、在庫は無料で流し込める」。逆に言えばトラフィックが先で、在庫は後。**

---

## 3. 「まだ誰もやっていない導線」候補リスト（敵対的検索の証拠つき）

判定記号：❌=埋まっている／△=部分的に埋まっている（誰がやっているか明記）／⭕=空白の可能性（証拠と限界を明記）

---

### ❌ 3-1. 自然言語での物件検索（"a quiet 2BR near a park under €1500"）
**判定：埋まっている。**
- **Properstar が 2026年に「AIで強化された検索」を発表済み**（"Meet Properstar Search, now supercharged with AI"）。
  https://agent.properstar.com/en/meet-properstar-search-now-supercharged-with-ai （確認日 2026-08-29）
- 米国側では **Zillow が2025年後半に ChatGPT 内アプリを初投入、Redfin が追随、Realtor.com が2026年3月に投入**。
  https://www.realestatenews.com/2026/03/30/realtor-com-the-latest-portal-to-launch-search-app-in-chatgpt （確認日 2026-08-29）
- ベンダー側も NLP 物件検索を製品化済（Serviceform, Ascendix, RoofAI 等）。
  https://www.serviceform.com/blog/ai-property-search-real-estate-guide/ （確認日 2026-08-29）
- 敵対的クエリ: `natural language AI property search "quiet 2 bedroom near park" semantic real estate search engine 2026`

### ❌ 3-2. isochrone（等時間圏）で通勤時間から物件を逆引き
**判定：埋まっている（少なくとも英国では標準）。**
- **Zoopla と Foxtons が TravelTime の Isochrone を本番導入**。公共交通・自転車・自動車を選べ、最大5つの通勤先を重ねられる。
  https://traveltime.com/case-study/isochrone-map-example-case-study-foxtons （確認日 2026-08-29）
- 無料の isochrone ジェネレータも多数（RadiusMapper, Mappr, Geoapify, Google Isochrones API）。
- 敵対的クエリ: `isochrone commute time property search map travel time real estate tool`
- **補足**: 通勤は都市内の概念なので「グローバル横断」の文脈では差別化価値が薄い。

### ❌ 3-3. 価格履歴・掲載期間の可視化
**判定：主要市場では埋まっている。**
- 米国：Zillow の price history は標準。
- スペイン：**idealista は掲載主の提示価格履歴を追跡し、自動査定との乖離（+10%／-10%）を表示**。第三者Chrome拡張（Precios Inmuebles Plus）も存在。idealista自身が「7日未満で成約13%（2026年Q1）」等の在庫日数統計を出している。
  https://www.idealista.com/tools/centrodeayuda/en/articulos/prospecting-map/ （確認日 2026-08-29）
  https://chromewebstore.google.com/detail/precios-inmuebles-plus/occnbidehejacmbkflojjiijidjifbjh （確認日 2026-08-29）
- 敵対的クエリ: `idealista price history price drop tracking listing "days on market" Europe portals compared Zillow price history`
- **残る隙間**：非主要市場（東欧・中南米・東南アジア）の価格履歴は薄い可能性。ただしこれは「導線」ではなく「データ取得」の問題で、供給の壁（§2）に直撃する。

### ❌ 3-4. 世界→日本のakiya（空き家）導線
**判定：完全に飽和。ここは避けるべき。**
- 既存：**AkiyaMart**（2025年に約150件の外国人購入を処理、定額 US$5,000）、**Akiya Japan**（100万円未満28,800件超、1,000万円未満87,600件超・2026年4月時点）、**AkiyaHub**、**All Akiyas**、**Old Houses Japan**、**Koryoya**、**Akiya Banks**、**HelloAkiya**、**MailMate**、そして **Cheap Houses Japan**。
  https://www.businesstraveller.com/insights/japan-akiya-boom-buying-abandoned-homes/ （確認日 2026-08-29）
  https://www.akiyajapan.com/articles/global-search-japanese-property-surges-2026 （確認日 2026-08-29）
- 需要自体は伸びている（英国+57%、カナダ+62%、米国+38% YoY／2026年Q1）が、**供給者（サイト）側がすでに10社以上いる**。
- 敵対的クエリ: `foreigners buying property in Japan 2025 2026 surge English language akiya platform startups competition`

### ❌ 3-5. AIによる室内写真の分析・バーチャルステージング・リフォーム後イメージ
**判定：埋まっている（レッドオーシャン）。**
- REimagineHome、RoomStage AI、AIHomeDesign、Imagen AI 等が2026年時点で製品化済み。「アルゴリズムが部屋のレイアウトを即座に理解し家具を配置」というレベルまで到達。
  https://www.reimaginehome.ai/blogs/ai-essential-interior-design-2026 （確認日 2026-08-29）
- 敵対的クエリ: `AI analyze listing interior photos natural light room layout renovation visualization real estate startup 2026`

### △ 3-6. ゴールデンビザ／投資移住の要件と物件の重ね合わせ
**判定：部分的に埋まっている。だが「ソロが勝てる形」の実例がある。**
- **Nomad Gate（Thomas K. Running の個人〜小規模運営）が「ポルトガル・ゴールデンビザ物件検索」を実装済み**：住所を入れると高密度／低密度地域か、内陸地域かを判定し、地図上で全ポルトガルの密度・内陸ステータスを表示する。
  https://nomadgate.com/portugal/golden-visa-search/ （確認日 2026-08-29）
- UAE：Property Kumbh が AED 2M 以上でフィルタできる。
- **空いている部分**：これは**1国×1制度でしか実装されていない**。ギリシャ（2026年に閾値変更）、スペイン（廃止）、UAE、マルタ、タイ等を**横断して「閾値以上の実物件」を1つの地図に載せた例は検索では見つからなかった**。
- 敵対的クエリ: `golden visa property search platform map investment threshold listings filter`
- **リスク**：ゴールデンビザ制度は政治的に不安定（ポルトガル改定、スペイン廃止）。仕様が毎年壊れる。

### △ 3-7. 「外国人が買えるか／借りられるか」の物件単位判定
**判定：国別ガイドは大量に存在するが、物件単位の判定は見つからず。ただし証拠は弱い。**
- **存在するもの**：米国議会図書館の39法域比較レポート（地図・図表つき）、International Living、janushermes、realting 等の国別ガイド。サウジアラビアは **REGA が国籍ベースの自動適格判定を持つ政府ポータル "Saudi Properties" を開設**（＝国レベルの公式実装はある）。
  https://tile.loc.gov/storage-services/service/ll/llglrd/2023555905/2023555905.pdf （確認日 2026-08-29）
  https://www.businesslink.sa/en/saudi-property-ownership-portal-for-foreigners-2026-guide （確認日 2026-08-29）
- **見つからなかったもの**：一般の国際ポータル上で「あなたのパスポート／在留資格でこの物件は取得可能か」を**listing単位でバッジ表示**する実装。
- 敵対的クエリ: `property portal filter "foreigners can buy" eligibility nationality restriction listing level feature` / `foreign ownership property restrictions by country interactive map can foreigners buy`
- **限界の明示**：ポータル内部の細かなUI機能は検索に載りにくい。Properstar / JamesEdition の実画面を確認できていない（proxy遮断）ため、**「存在しない」とは断定できない**。⭕ではなく△に留める。
- **法的リスク**：これは実質的に法務助言。誤判定の責任が重い。「参考情報」枠で出すしかない。

### ⭕（最有力）3-8. 「都市選び層」と「物件層」が接続されていない
**判定：これがいちばん確度の高い空白。**

証拠（＝分断されている側の自白）：
- **WhereNext（95カ国380都市）は自ら「実際の賃貸物件は idealista / Inmuebles24 / DDProperty / 99.co を見て、WhereNext の中央値家賃と突き合わせよ」と外部誘導している。** つまり自分たちは物件を持たないと公言している。
  https://getwherenext.com/tools/city-cost-compare （確認日 2026-08-29）
  https://getwherenext.com/blog/free-numbeo-alternative-cost-of-living （確認日 2026-08-29）
- **Nomad List / nomads.com** は 1,000〜2,000都市の生活費・ネット速度・気候データを持つが、**実物件のリンクは確認できず**。指標として "Airbnb price vs rent price" は持つ。
  https://nomads.com/ （確認日 2026-08-29 ※本文は proxy 遮断のため検索結果経由）
- **Numbeo**：家賃指数の世界地図はあるが物件なし。
  https://www.numbeo.com/cost-of-living/gmaps.jsp?indexToShow=getRentIndex （確認日 2026-08-29）
- **Global Property Guide**：85カ国38指標の世界地図。物件なし。
  https://www.globalpropertyguide.com/world-map （確認日 2026-08-29）
- 逆方向（物件側）：Properstar も Rentola も Kyero も、**気候・ビザ・時差・ネット速度・治安といった生活データを検索軸として持っていない**（検索結果に現れる機能記述は寝室数・バスルーム・バルコニー・プール・エネルギークラス・ペット可など従来型フィルタのみ）。
- 敵対的クエリ:
  - `"compare cities" tool that also shows real apartment listings relocation product city ranking plus rentals`
  - `"where can I afford to live" world map rent budget reverse search tool global`
  - `Nomad List nomads.com housing section apartments listings link Airbnb integration feature`
  - `reddit expat "where should I move" tool combining rent listings visa cost of living missing wish existed`
  - `digital nomad visa map platform combined with rental listings apartments booking integration`
- 該当する具体形：
  - 「**月15万円の予算・気温18〜28℃・ネット100Mbps以上・日本と時差4時間以内・ビザ180日以上**」→ 世界地図に条件を満たす都市がハイライト → **そのまま実在物件と室内写真に着地する**
  - 「**東京の家賃12万円は、リスボンでは◯◯、チェンマイでは◯◯**」型の変換UIから、実物件へ
- **競合が来る方向**：Flatio は「全リースがビザの住所証明になる」を打ち出しており、**ノマド文脈と物件を繋げる動きは既に始まっている**（17カ国17,000件と規模は小さい）。TripOffice は「デスクと椅子を保証」で100カ国20万件。**つまり"ノマド属性×物件"は部分的に始まっている。空いているのは"都市選定の意思決定データ（ビザ・税・時差・気候）×実物件"の接続部分。**
- **最大の障壁**：§2 の供給の壁。全世界の実物件在庫を持てないと着地点がない。→ **現実解は「着地は既存ポータルへのディープリンク／アフィリエイト、自前在庫はKyero XMLで来た分だけ」**。

### ⭕ 3-9. グローバル版「Zillow surfing」＝物件を眺めるエンタメ導線
**判定：グローバル横断のプロダクトとしては見つからなかった。ただし近接する成功例が複数あり、部分的に埋まりつつある。**

証拠：
- **Zillow Gone Wild**：クロスプラットフォーム計 430万フォロワー（Instagram 190万、X 61.9万）、HGTVで番組化。**ただし米国物件限定。**
  https://www.washingtonpost.com/home/2024/04/29/wild-rise-zillow-gone-wild/ （確認日 2026-08-29）
  https://en.wikipedia.org/wiki/Zillow_Gone_Wild （確認日 2026-08-29 ※検索結果経由）
- **Cheap Old Houses**：Instagram 200万フォロワー。**"Cheap Old Houses Abroad" という国際版の派生アカウントを既に持っている**（フランス・スペイン・ノルウェー等）。→ **ここは部分的に埋まっている。**
  https://www.forbes.com/sites/juliabrenner/2020/08/23/get-to-know-cheap-old-houses-the-property-listing-instagram-account-with-over-1-million-followers/ （確認日 2026-08-29）
- **1eurohouses.com**：イタリアの1ユーロ住宅を**インタラクティブ地図**で集約。CNN・NYT・Guardian・BBC が報じるレベルまでバイラル化。2026年時点で70以上の自治体が制度実施。**小規模運営で世界的注目を取った実例。**
  https://1eurohouses.com/1-euro-houses-map/ （確認日 2026-08-29）
  https://www.idealista.it/en/news/property-for-sale-in-italy/2026/01/23/315095-map-of-1-euro-houses-in-italy-2026 （確認日 2026-08-29）
- **物件ファン**（日本）：「不動産エンターテインメントサイト」を名乗る。**日本国内限定。**
  https://suumo.jp/journal/2018/03/02/150071/ （確認日 2026-08-29）
- **「ルーレット／ランダム表示」**：業界ブログで「なぜ不動産検索サイトにルーレット機能がないのか」という記事が2010年代からあるが、**実装された主要プロダクトは見つからなかった。**
  https://theamericangenius.com/housing/editorials/real-estate-roulette/ （確認日 2026-08-29）
- 敵対的クエリ: `"Zillow surfing" global version random international properties browse for fun` / `"random" house listing generator website property roulette surf random real estate worldwide` / `random property viewer world "just listed" live feed real estate map global fun site` / `物件 眺める 世界 ランダム 海外 家 写真 見る サイト エンタメ 間取り`
- **限界の明示**：SNSアカウント形態のものは検索で捕捉しづらい。「Cheap Old Houses Abroad」が既に存在する以上、**"完全な空白"とは言えない。空いているのは「地図＋横断＋ランダム性」を持ったWebプロダクト形態。**
- **フォロワー0・広告予算0という制約に対しては、この方向がいちばん相性が良い**（Zillow Gone Wild も Cheap Old Houses も 1eurohouses もゼロから始まっている）。

### ⭕ 3-10. 越境AIエージェント／MCPサーバとしての「世界の物件」
**判定：米国は埋まったが、クロスボーダーは空いている可能性。**
- 埋まっている側：Zillow（2025年後半）、Redfin、Realtor.com（2026年3月）が ChatGPT アプリを提供。Cotality（旧CoreLogic）が 2026年3月31日に MCP サーバを公開。Homesage.ai が2026年7月に1.55億件の米国物件レコード＋33ツールのMCPを公開。Repliers、Rechat（2026年8月）も。**すべて米国／MLS中心。**
  https://www.inman.com/2026/08/03/rechat-mcp-server-ai/ （確認日 2026-08-29）
  https://www.cotality.com/platforms/mcp-server （確認日 2026-08-29）
  https://chatforest.com/guides/mcp-real-estate/ （確認日 2026-08-29）
- 見つからなかったもの：**「複数国横断で、ビザ・税・生活費・物件を同時に引ける」MCPサーバやChatGPTアプリ**。Apify上に「4プラットフォーム統合」のものはあるが実質米系。
- 敵対的クエリ: `international cross-border property search ChatGPT app MCP server global listings multi-country AI`
- **限界**：MCPは2025-2026年に爆発的に増えており、個人公開のものは検索到達性が非常に低い。**「空いている」と断定するには証拠不足。「主要プレイヤーは不在」までしか言えない。**

### ❌ 3-11. 新着物件の即時通知（スピード勝負）
**判定：埋まっている＋既にニッチ事業者がいる。**
- Rightmove の Instant Property Alerts は新規ユーザーの57%が選択、**1日70万件超**の通知を送っている。idealista も即時メールアラートあり。
  https://www.rightmove.co.uk/news/articles/uncategorized/rightmove-users-find-it-first-with-instant-property-alerts/ （確認日 2026-08-29）
- 残る隙間として「ポータルの通知は15〜60分遅れる」と主張して**その差分だけで商売している事業者（Dwellio）が既にいる**。GitHubにも `RightmoveInstantAlert` のようなOSSがある。
  https://dwellio.co.uk/blog/instant-rightmove-alerts （確認日 2026-08-29）
  https://github.com/p-hather/RightmoveInstantAlert （確認日 2026-08-29）
- 敵対的クエリ: `idealista Rightmove new listing alert instant notification competitive advantage speed renters first mover`
- **かつ**、これはスクレイピング前提であり §2 のToS/WAF問題に真正面からぶつかる。

### ❌ 3-12. 日照シミュレーション
**判定：日本国内では既に無料で存在。**
- **国交省 PLATEAU の3D都市モデル（全国240都市）を使い、ブラウザで登録不要に日影を確認できる無料サービスが既にある**（shadow.datagen-pro.com）。ホームズ君・日当り君等の専門ソフトも。
  https://shadow.datagen-pro.com/hikage-simulation/ （確認日 2026-08-29）
  https://www.homeskun.com/products/homeshiatari/ （確認日 2026-08-29）
- 敵対的クエリ: `日照シミュレーション 物件 サービス 不動産 日当たり 3D 検索`
- グローバル版は3Dビル形状データがない国が大半で、そもそも作れない。

### △ 3-13. 日本語で「世界の賃貸／売買」を移住視点で横断
**判定：日本語圏では薄い。ただし市場が小さい。**
- 既存：**セカイプロパティ**（東南アジア＋ドバイ＋米国、**投資目的**）、**海外CHINTAI**（エイブル海外ネットワーク、**駐在・赴任の日系物件**）、**エイブル海外**（16海外拠点）。
  https://ja.sekaiproperty.com/ （確認日 2026-08-29）
  https://kaigai.chintai.net/ （確認日 2026-08-29）
- **空いている部分**：「投資」でも「駐在」でもなく、**個人の移住・ノマド視点で日本語で世界の実物件を横断する**導線は見当たらない。
- 敵対的クエリ: `海外 賃貸 物件 横断検索 世界 日本語 サイト 個人 移住 探す 比較` / `世界の物件 地図 海外不動産 マップ 検索 サービス 日本語 移住`
- **致命的な弱点**：日本語のみの市場規模。かつ日本人の海外移住人口は小さい。**依頼主が日英可であることを活かすなら、日本語は入口にしても収益源にはしにくい。**

---

## 4. 収益モデルの実在確認と、個人が取れるモデルの序列

### 4-A. 実在確認された数値

**(1) リード課金（CPL）**
- 海外不動産セクターの CPL は **$1.82〜$25**。英語圏キャンペーン（ドバイ・ギリシャ）で **$2.48〜$4.34**、ロシア語圏（トルコ・北キプロス）で **$7.05〜$17.49**。SQL（営業が処理する適格リード）の適正価格は **$30〜$60**。
  https://profydigital.com/cost-per-lead-real-estate-ads-2026 （確認日 2026-08-29）
- グローバル全般では **$10〜$150/リード**。
  https://blog.rashfox.com/real-estate-lead-generation-cost-globally/ （確認日 2026-08-29）
- **Green-Acres は7〜8年リード課金でやったが、顧客の1/3が「代理店に再請求できない」と嫌い、2022年にサブスクへ移行**。→ **リード課金モデルは供給側から嫌われるという実証がある。**
  https://immoedge.com/green-acres-property-portal-review/ （確認日 2026-08-29）

**(2) 掲載課金（実在価格）**
| 事業者 | 価格 |
|---|---|
| Green-Acres | **€99/月〜**（掲載数連動サブスク、無制限コンタクト）。2022年導入、顧客の54%が移行 `[中]` |
| Kyero | 基本無料＋**Prime €3〜6/物件/月**（25枠€450/3ヶ月、50枠€600/3ヶ月、100枠€900/3ヶ月） `[中]` |
| Rightmove Overseas | **個人売主 £130/月**、エージェント **£1,150〜1,295/月**（2020-21年） `[中]` |
| Flatio | 掲載無料、**成約時に家主から 5%（個室）／7.5%（一棟）** `[中]` |
| Spotahome | **借主から家賃約25%相当の一時ブッキング料** `[中]` |
| Blueground | **予約ごとに 7% コミッション**、初期費用なし `[中]` |
| Rentola | **借主サブスク（€1トライアル→月額課金）** ※Trustpilot 1.9〜2.2、解約困難の告発多数 `[中]` |
| Numbeo | **API $50〜500/月、COL estimator $260/月** `[中]` |
| Nomad List | **$149買い切り／月$8〜30** `[中]` |

**(3) アフィリエイト**
- **SafetyWing（ノマド保険）**：**10%リカーリング×12ヶ月、30日クッキー、1人あたり約$50**（Nomad Insurance基本プランの場合）。
  https://safetywing.com/ambassador （確認日 2026-08-29）
  https://www.referly.so/affiliate-programs/safetywing （確認日 2026-08-29）
- **Remitly**：パートナープログラムあり（豪・墺・白・加・仏・独・愛・西・英・米等）。単価は非公開。
  https://www.remitly.com/gb/en/landing/affiliate-program （確認日 2026-08-29）
- **ゴールデンビザ助言**：弁護士費用が **€5,000〜€20,000/件**（ポルトガル）、政府・ファンド費用が別途約€30,000。**紹介料の余地は極めて大きいが、規制業種で個人が扱うリスクも大きい。** 具体的な紹介手数料の相場は公開情報として見つからなかった。
  https://vida-cap.com/blog/golden-visa-advisor-fees-2026 （確認日 2026-08-29）

**(4) メディア／ニュースレター課金 — ソロの実証例**
- **Cheap Houses Japan（Michael、カナダ人ソロ運営）**：日本の格安物件を毎週20件キュレーションするニュースレターを **$10/月**で販売し、**月$8,000（Starter Story 報告）**。Instagram → サイト → 有料ニュースレターの導線。
  https://www.starterstory.com/stories/cheap-houses-japan-breakdown （確認日 2026-08-29）
  https://cheaphousesjapan.com/chj-newsletter/ （確認日 2026-08-29）
- **1eurohouses.com**：地図＋制度キュレーションで CNN/NYT/Guardian/BBC の報道を獲得。
  https://1eurohouses.com/1-euro-houses-map/ （確認日 2026-08-29）
- **Nomad Gate**：個人〜小規模でポルトガル・ゴールデンビザの物件判定地図を提供。
  https://nomadgate.com/portugal/golden-visa-search/ （確認日 2026-08-29）

### 4-B. 「エージェントが自分から載せに来る」構造は作れるか

**作れる。ただしトラフィックが先。**
- **Kyero XML** が事実上の国際標準。**エージェントは既にこのフォーマットのフィードURLを持っている**（Kyero, Green-Acres, thinkSPAIN 等に出稿するために）。したがって受け側が「Kyero XML の URL を貼るだけ」にすれば、**エージェント側の追加コストはほぼゼロ**。
- Kyero が「基本掲載は無料、目立たせたいなら Prime」というフリーミアムで **5,000エージェント／70万物件**を集めた実績があり、これは個人でも模倣可能な唯一の構造。
- **ただし順序が逆にできない**：エージェントは「送客がある所」にしか出さない。Cheap Houses Japan も 1eurohouses も **メディア（Instagram／報道）が先、在庫が後**だった。

### 4-C. 個人が取れるモデルの序列（推奨順）

| 順位 | モデル | 理由 | 必要トラフィック規模 |
|---|---|---|---|
| **1** | **有料ニュースレター／キュレーション課金** | ソロでの実証例（$8K/月）が同じ日本文脈で存在。在庫の網羅性が不要（20件/週でいい）。編集の付加価値で勝てる。 | 数千フォロワー〜 |
| **2** | **アフィリエイト（保険・送金・ノマドサービス）** | SafetyWing 10%×12ヶ月（≒$50/人）等、単価と条件が公開されている。物件在庫ゼロでも成立。 | 月数万PV〜 |
| **3** | **データ／API販売** | Numbeo が $50〜500/月で実証。「世界のビザ×税×家賃×制度」の構造化データはまだ整備されていない。B2B（移住コンサル、HR、リロケーション会社）に売れる。 | トラフィック不要 |
| **4** | **フリーミアム掲載課金（Kyero型）** | 構造は模倣可能でXMLの標準もある。だがトラフィックが先。到達までが長い。 | 月数十万PV |
| **5** | **リード課金（CPL）** | CPL $2〜25 なので月$3,000稼ぐには **月120〜1,500リード**必要 ≒ CVR 2%なら月6千〜7.5万セッション。**かつ Green-Acres の実証どおり供給側に嫌われる。** | 月数万〜数十万セッション |
| **論外** | **借主サブスク（Rentola型）** | Trustpilot 1.9〜2.2、「€1トライアル→解約困難」の告発が多数。**個人が同じことをやれば信用が一撃で終わる。** | — |

---

## 5. 総括：どこに賭けるべきか

### 5-1. 潰れた前提
「世界の物件を1つのマップに載せ、押すと室内写真が出る」は **Properstar（60〜100カ国/300万件/73名）・Rentola（36カ国/100万件/2,400サイト集約）・JamesEdition・Juwai（91カ国）・Green-Acres・Realtor.com International** で既に実装済み。**この一次的な体験そのものには空白がない。** さらに個人には **在庫を持てない構造的な壁**（ポータルAPIは出稿専用、スクレイピングはToS違反＋DataDome）がある。

### 5-2. 生き残った空白（確度順）

1. **⭕⭕ 都市選定データ層 × 実物件層の接続**（§3-8）
   最も証拠が強い。**WhereNext が公式に「物件は外部ポータルで見よ」と書いている**、Nomad List / Numbeo / Global Property Guide が物件を持たない、逆に Properstar / Rentola / Kyero が生活データを検索軸に持たない、という**両側からの分断の証拠**がある。
   実装形：「予算＋気候＋時差＋ネット速度＋ビザ日数」→ 世界地図 → 実物件（自前在庫は Kyero XML、無ければ既存ポータルへのディープリンク／アフィリエイト）。
   注意：Flatio（ビザ用住所証明）と TripOffice（デスク保証100カ国20万件）が**物件側からこの方向に近づいている**。純粋な空白ではなく「先行者はいるが小さい」。

2. **⭕ グローバルの「眺め見」エンタメ導線**（§3-9）
   フォロワー0・広告予算0という制約に**唯一相性が良い**方向。Zillow Gone Wild（430万）、Cheap Old Houses（200万、既に "Abroad" 派生あり）、1eurohouses.com（報道獲得）という実証がある。
   注意：**Cheap Old Houses Abroad が既に存在するため「完全な空白」ではない**。差別化は「地図＋横断＋ランダム性を持つWebプロダクト」形態。

3. **△ ゴールデンビザ／制度 × 物件の多国横断**（§3-6）
   Nomad Gate がポルトガル1国で実装済み＝**ソロで成立する形の証明**。多国横断はまだ無い。ただし制度が政治的に不安定。

4. **△ 越境AIエージェント／MCP**（§3-10）
   米国はZillow/Redfin/Realtor.com/Cotality/Homesageで埋まったが、クロスボーダーは主要プレイヤー不在。**ただし検索到達性が低く「空いている」と断定する証拠が不足**。

5. **△ 日本語×移住視点の世界物件横断**（§3-13）
   セカイプロパティ（投資）・海外CHINTAI（駐在）しかなく隙間はあるが、**市場が小さい**。入口としてのみ。

### 5-3. 明確に避けるべき
- 世界→日本のakiya（§3-4、10社以上が既存）
- AI室内写真加工（§3-5、レッドオーシャン）
- 新着即時通知（§3-11、既存＋ToS違反リスク）
- 自然言語物件検索そのもの（§3-1、Properstarが2026年に実装済み）
- 借主サブスク課金（Rentola型、信用毀損）

### 5-4. 現実的な最初の一歩（供給の壁を回避する順序）
1. **在庫を持たずに始める**：データ層（ビザ・税・気候・時差・ネット速度・家賃中央値）＋既存ポータルへのディープリンクだけで「逆引き検索」を作る。物件は最初 Numbeo/GPG の中央値＋外部リンクで代替。
2. **エンタメ導線で流入を作る**：地図＋週次キュレーション（1eurohouses / Cheap Houses Japan の型）。SNS＋ニュースレター。
3. **トラフィックが出てから供給を開く**：「Kyero XML の URL を貼るだけ、掲載無料」でエージェントに開放。
4. **収益化の順序**：ニュースレター課金 → アフィリエイト → データ販売 → 掲載課金。リード課金は最後。

---

## 6. 参照URL一覧（全て確認日 2026-08-29）

**プレイヤー**
- https://www.properstar.com/what-is-properstar
- https://agent.properstar.com/en/meet-properstar-search-now-supercharged-with-ai
- https://agent.properstar.com/en/properstar-feature-announcement-drawing-on-maps
- https://www.listglobally.com/
- https://www.moneyhouse.ch/en/company/properstar-sa-6419284931
- https://www.jamesedition.com/real_estate
- https://www.jamesedition.com/professional_seller/real_estate
- https://pitchbook.com/profiles/company/61009-84
- https://www.green-acres.com/en/Observatory
- https://immoedge.com/green-acres-property-portal-review/
- https://support.green-acres.com/knowledge/quest-ce-que-la-tarification-%C3%A0-la-parution
- https://www.kyero.com/en/join
- https://www.kyero.com/en/join/market-insight/spain/kyero-next-chapter
- https://help.kyero.com/estate-agents/xml-import-specification
- https://help.kyero.com/estate-agents/kyero-xml-feed
- https://www.idealista.com/en/news/property-for-sale-in-spain/2024/12/05/821343-idealista-acquires-kyero
- https://www.idealista.com/en/news/property-for-sale-in-spain/2025/09/24/861275-idealista-withdraws-from-the-acquisition-of-kyero
- https://www.theolivepress.es/spain-news/2025/09/25/idealista-pulls-out-kyero-takeover/
- https://www.spanishpropertyinsight.com/2025/10/17/property-portal-merger-collapses-under-weight-of-government-meddling/
- https://www.rightmove.co.uk/overseas-property/advertise/estate-agent.html
- https://www.rightmove.co.uk/overseas-property.html
- https://esalesinternational.com/2026/05/20/how-to-advertise-with-rightmove-overseas-in-the-uk/
- https://scott-scott.com/1-5-billion-legal-action-filed-against-rightmove/
- https://www.prnewswire.com/news-releases/realtorcom-expands-international-reach-with-global-property-network-300305299.html
- https://list.juwai.com/
- https://www.juwai.asia/main/news/15892
- https://www.luxinmo.com/portals/thinkspain
- https://tranio.com/countries/
- https://homesgofast.com/countries/
- https://ja.sekaiproperty.com/search
- https://kaigai.chintai.net/
- https://www.able-nw.com/

**賃貸・中長期**
- https://rentola.com/about-us
- https://www.luntero.com/resource/platform/rentola
- https://www.trustpilot.com/review/rentola.com
- https://hotelub.fr/en/rentola-review-the-promise-of-a-single-click-the-trap-of-a-subscription-an-investigation-into-the-platform-that-divides/
- https://housinganywhere.com/rent-index-by-city
- https://www.onlinemarketplaces.com/articles/spotahome-vs-housing-anywhere-vs-uniplaces/
- https://www.theblueground.com/furnished-corporate-apartments
- https://www.cbinsights.com/company/blueground
- https://www.flatio.com/for-landlords
- https://www.flatio.com/help/article/2-how-much-does-it-cost-to-list-my-rental-property-on-flatio
- https://www.flatio.com/accommodation-for-digital-nomads
- https://www.nomadstays.com/
- https://www.luxurialifestyle.com/tripoffice-workation-digital-nomads-travel-ai-remote-work-and-trip-office/
- https://www.nestpick.com/
- https://sk.airbnb.com/e/monthly-discounts
- https://www.airbnb.com/help/article/2729

**データ層**
- https://www.numbeo.com/common/api.jsp
- https://www.numbeo.com/cost-of-living/gmaps.jsp?indexToShow=getRentIndex
- https://www.globalpropertyguide.com/world-map
- https://www.globalpropertyguide.com/rental-yields
- https://nomads.com/
- https://nomads.com/map/by/housing_price_in_usd
- https://getwherenext.com/tools/city-cost-compare
- https://getwherenext.com/blog/free-numbeo-alternative-cost-of-living
- https://livingcost.org/cost
- https://expatslist.org/tools/cost-of-living
- https://www.blog.brightcoding.dev/2026/08/27/where-can-i-live-with-my-salary-free-tool

**導線・敵対的検索の根拠**
- https://traveltime.com/case-study/isochrone-map-example-case-study-foxtons
- https://www.serviceform.com/blog/ai-property-search-real-estate-guide/
- https://www.realestatenews.com/2026/03/30/realtor-com-the-latest-portal-to-launch-search-app-in-chatgpt
- https://www.inman.com/2026/08/03/rechat-mcp-server-ai/
- https://www.cotality.com/platforms/mcp-server
- https://chatforest.com/guides/mcp-real-estate/
- https://nomadgate.com/portugal/golden-visa-search/
- https://tile.loc.gov/storage-services/service/ll/llglrd/2023555905/2023555905.pdf
- https://www.committee100.org/our-work/federal-and-state-bills-prohibiting-property-ownership-by-foreign-individuals-and-entities/
- https://internationalliving.com/global-property-ownership/
- https://www.businesslink.sa/en/saudi-property-ownership-portal-for-foreigners-2026-guide
- https://www.idealista.com/tools/centrodeayuda/en/articulos/prospecting-map/
- https://chromewebstore.google.com/detail/precios-inmuebles-plus/occnbidehejacmbkflojjiijidjifbjh
- https://www.rightmove.co.uk/news/articles/uncategorized/rightmove-users-find-it-first-with-instant-property-alerts/
- https://dwellio.co.uk/blog/instant-rightmove-alerts
- https://github.com/p-hather/RightmoveInstantAlert
- https://www.reimaginehome.ai/blogs/ai-essential-interior-design-2026
- https://shadow.datagen-pro.com/hikage-simulation/
- https://www.homeskun.com/products/homeshiatari/
- https://theamericangenius.com/housing/editorials/real-estate-roulette/
- https://suumo.jp/journal/2018/03/02/150071/

**エンタメ／ソロ実証例**
- https://www.washingtonpost.com/home/2024/04/29/wild-rise-zillow-gone-wild/
- https://www.marketingbrew.com/stories/2024/06/11/zillow-gone-wild-is-the-gift-that-keeps-on-giving-for-zillow
- https://www.forbes.com/sites/juliabrenner/2020/08/23/get-to-know-cheap-old-houses-the-property-listing-instagram-account-with-over-1-million-followers/
- https://1eurohouses.com/1-euro-houses-map/
- https://www.idealista.it/en/news/property-for-sale-in-italy/2026/01/23/315095-map-of-1-euro-houses-in-italy-2026
- https://www.starterstory.com/stories/cheap-houses-japan-breakdown
- https://cheaphousesjapan.com/chj-newsletter/

**日本akiya（飽和の証拠）**
- https://www.businesstraveller.com/insights/japan-akiya-boom-buying-abandoned-homes/
- https://www.akiyajapan.com/articles/global-search-japanese-property-surges-2026
- https://akiyahub.com/articles/akiya-japan-a-guide-for-foreign-buyers
- https://www.allakiyas.com/
- https://www.oldhousesjapan.com/
- https://www.akiyabanks.com/
- https://mailmate.jp/blog/akiya-banks-for-foreigners

**収益・供給側**
- https://profydigital.com/cost-per-lead-real-estate-ads-2026
- https://blog.rashfox.com/real-estate-lead-generation-cost-globally/
- https://safetywing.com/ambassador
- https://www.referly.so/affiliate-programs/safetywing
- https://www.remitly.com/gb/en/landing/affiliate-program
- https://vida-cap.com/blog/golden-visa-advisor-fees-2026
- https://www.scrapingbee.com/blog/best-real-estate-apis-for-developers/
- https://www.realtyapi.io/blog/best-property-data-api
- https://scrapfly.io/blog/posts/how-to-scrape-idealista
- https://www.idealista.pt/apoioutilizador/artigos/aviso-legal-e-condicoes-gerais/?lang=en
- https://estateagentfeeds.com/
- https://wp-property-hive.com/kyero-xml-added-list-supported-import-formats/
- https://www.agentiz.com/en/partnership/aggregation

**AI移住プランナー（隣接競合）**
- https://expatspark.ai/
- https://www.gullie.io/
- https://expatlife.ai/resources/moving
- https://relo.ai/
- https://www.expatfocus.com/articles/the-best-ai-tools-to-help-you-move-abroad-in-2026
