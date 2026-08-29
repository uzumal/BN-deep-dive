# R13 / 物件データ取得可能性・全世界調査

**調査日：2026-08-29（本文中の全URLの確認日は同日）**
**調査対象者の制約：日本在住ソロエンジニア／法人なし／宅地建物取引業免許なし／日英可／資金は個人規模**
**総合判定：写真付き物件リスティングを合法に表示できる経路は「ほぼ全滅」。生き残るのは3経路のみで、うち2つは「APIを叩く」のではなく「人に頼む」経路である。**

---

## 0. 調査上の制約（先に開示する）

本セッションの egress プロキシ（組織ポリシー）が、以下の**一次ソースへの直接アクセスを 403 で遮断**した。curl / WebFetch とも同様に遮断され、迂回は禁止事項のため行っていない。

遮断された主要ドメイン（=原文の逐条引用ができなかった先）：
`bridgeinteractive.com` / `mlsgrid.com` / `docs.mlsgrid.com` / `nar.realtor` / `rentcast.io` / `developers.rentcast.io` / `zillowgroup.com` / `crea.ca` / `developer.domain.com.au` / `developers.idealista.com` / `api.immobilienscout24.de` / `nestoria.co.uk` / `homedata.co.uk` / `help.repliers.com` / `web.archive.org` / 主要ポータルの `robots.txt` 全て

したがって本レポートは **検索エンジン経由の一次ソース要約＋二次資料** で構成されている。以下の表記を厳密に使い分ける：

- **【確】** = 複数経路で裏取り済み、または一次ソースの記述として引用可能
- **【単】** = 単一の二次ソースのみ。要自己確認
- **【推】** = 私の推論。証拠なし
- **【未】** = 調べたが確認できなかった（≠存在しない、だが痕跡がないことは弱い否定証拠）

**特に robots.txt の実態は一切確認できていない。** 「robots.txtでどうなっているか」を根拠にした判断は本レポートでは行っていない（そもそも robots.txt は法的許諾ではないので、判断根拠にしてはいけない）。

---

## 1. 結論サマリ（先に全部書く）

### 1-1. 構造的発見：ポータルのAPIは「全部逆向き」だった

調査で最も重要かつ、事前に想定していなかった発見はこれである。

**世界中の不動産ポータルは、ほぼ例外なく「API」を持っている。しかしそのAPIは全て、業者が物件を"アップロードする"ための入口（inbound）であって、第三者が物件を"取得する"ための出口（outbound）ではない。**

| ポータル | 「API」の実体 | 向き |
|---|---|---|
| Rightmove (英) | Real Time Datafeed / ADF、証明書認証 | agent → portal（**inbound**）【確】 |
| OnTheMarket (英) | Rightmove API準拠のReal Time Datafeed | agent → portal（**inbound**）【確】 |
| ImmoScout24 (独) | api.immobilienscout24.de、Exposé公開用 | agent → portal（**inbound**）【確】 |
| Immobiliare.it (伊) | REST-XML、IPホワイトリスト制 | partner → portal（**inbound**）【確】 |
| Kyero / Green-Acres / thinkSPAIN | XMLインポート仕様 | agent → portal（**inbound**）【確】 |
| HousingAnywhere | 公開APIドキュメントあり・無料 | partner → portal（**inbound**）【確】 |
| Domain (豪) Listings Management | 無料で開発者に開放 | agent → portal（**inbound**）【確】 |

`developers.〇〇.com` というURLを見て「公開APIがある」と読むのは全部誤読になる。**唯一の例外的な outbound API が豪 Domain の Agents & Listings と、西 Idealista の Search API である**（詳細は後述）。

### 1-2. 経路別の生存率

| 経路 | 個人可否 | 写真 | 判定 |
|---|---|---|---|
| 米国 MLS / IDX（RESO, Bridge, MLS Grid, Trestle, SimplyRETS） | **不可**（免許ブローカー必須） | 写真は取れるが表示権が来ない | **全滅** |
| 米英欧アジアの大手ポータル公式API | ほぼ不可（inbound専用 or 提携審査） | — | **ほぼ全滅** |
| 公開データAPI（RentCast, ATTOM, PropertyData, Homedata, URA, 不動産情報ライブラリ） | **可** | **写真なし** | **写真という要件で失格** |
| 非公式スクレイパー（RapidAPI / Apify / Datafiniti系） | 可 | 技術的には取れる | **法的に自殺行為**（後述の判例群） |
| エージェント直接フィード（Kyero XML等の業界標準） | **可** | **可（許諾を書面で取れる）** | **★最有力** |
| 豪 Domain API | **可（自己申請でキー発行）** | **可（imagesあり）** | **★次点。ただしApproved Purposeの壁** |
| 旅行/中期滞在アフィリエイト（Booking.com Demand API） | **可** | **可（imgタグでの利用を明文で許諾）** | **★合法性は最強。ただし「不動産」ではない** |
| 政府オープンデータの「募集中物件」 | 国により可 | 事実上なし | **補助的にしか使えない** |

### 1-3. 楽観を禁じるための一行

**「写真付き物件リスティングを、免許なしの個人が、APIを叩くだけで合法に取得する」方法は、地球上に事実上存在しない。**
存在するのは「エージェントに頼んで、書面で許諾をもらって、その人のサーバの画像を使わせてもらう」という、極めて泥臭い経路だけである。そしてそれは Kyero も Green-Acres も thinkSPAIN も Properstar も、実際に通ってきた道である。

---

## 2. 市場別 可否マトリクス

凡例：**個人可否** = 免許なし・法人なしの個人が申込めるか ／ **写真** = 物件写真の自社サイト表示が許諾されるか

### 2-A. 米国

| ソース | 個人可否 | 写真 | 費用 | 表示義務・再配布 | 個人の実例 |
|---|---|---|---|---|---|
| **RESO Web API / IDX（MLS直）** | **不可**。MLS参加資格は「有効な不動産ブローカー免許を持つ principal / partner / corporate officer / branch office manager」に限定【確】 | Media リソースに写真あり。ただし表示権はブローカーのIDX契約に紐づく | MLS会費＋feed料 | IDXルール（更新頻度・帰属・免責）はMLSごと | なし |
| **Bridge Interactive（Zillow Group）** | **不可**。MLS参加者、IDXベンダー、またはMLS提携済みテック企業に限定。Zillowデータチームの審査あり【確】 | MLSフィード次第 | **無料枠なし**【単】。「$500/月〜」の記述は scraper ベンダー（zillapi）由来で**要注意・未検証**【単】 | 各MLSと個別のデータライセンス契約が必要 | なし |
| **MLS Grid** | **不可**。Master Data License Agreement 署名＋**各発信元MLSの承認**が必要。非参加者用途は追加でMLS理事会承認が要る（例：Canopy MLS）【確】 | Media リソースあり。「Listing Data には text, photographs その他が含まれる」【確】 | 非公開。実例：OneKey MLS はベンダー $250/月＋ライセンス毎 $20/月【単】 | IDX / VOW / Back Office を1本の契約で規定 | なし |
| **Trestle（CoreLogic / Cotality）** | 申込フォーム自体は誰でも出せるが、**用途記述→各MLS承認**が必要【確】 | MLS次第 | $75/MLS/月（CRMLS事例）、IDXフィード $85/月、ブローカーフィード $25/月【単】 | MLSごと | なし |
| **SimplyRETS** | **不可（実質）**。「唯一の要件は、あなたが既にMLSからRETS/RESO Web API資格情報を持っていること」=前提が免許【確】 | 上流次第 | 接続あたり**初期$99**＋月額【確】。デモデータは無料 | 上流MLS準拠 | ラッパーのみ |
| **Zillow API** | **廃止**。公開ZWSID APIは **2021-09-30 で終了**、復活していない【確】 | — | — | — | — |
| **Zestimate API** | **公開されていない**【確】 | — | — | — | — |
| **Realtor.com / Move / ListHub** | **不可**。ListHubは「publisher site」として158サイトに配信するがブローカー起点の syndication。個人の申込口なし【確】 | — | — | — | なし |
| **Redfin Data Center** | **可（誰でもDL可）** | **写真なし。物件単位ですらない**（地域集計統計CSV/TSVのみ）。2026年5月に再構築【確】 | 無料 | — | 分析用途では多数 |
| **RentCast API** | **可（自己申請、カード不要の無料枠あり）**【確】 | **写真フィールドは確認できず【未】→ 実質「テキストのみ」と想定すべき**。公開ドキュメントが列挙する項目は attributes / status / listed price / days on market / listing contacts【確】 | Developer $0（50 req）／Foundation $74（1,000）／Growth $199（5,000）／Scale $449（25,000）【確】 | 「Terms of Use で明示的に禁止されていない用途は可」と標榜【確】。原文未確認 | 【未】 |
| **ATTOM Data** | **可（ATTOM Cloudで30日無料トライアル）**【確】 | **公開記録データ。物件募集写真は含まれないと考えるべき**【推】 | 非公開・要見積。Property Navigator は $499/年【確】 | 用途別ライセンス | 【未】 |
| **Estated** | 2020年に ATTOM が買収。**開発者ドキュメントは2026年中に廃止**、API管理はATTOM Developer Portalへ移管【確】 | 同上 | 移管中 | — | — |
| **Datafiniti** | 可（有料） | **利用規約が「property data 内の image URL にアクセスして得た画像の公開表示」を禁止**【確】。さらに「大幅な改変なしの再販・再配布・サブライセンス」も禁止【確】 | 非公開 | — | Zillow から「写真を含むコンテンツを組織的に収穫している」として**C&D を受けた**【確】 |
| **CoStar / Apartments.com** | **不可**。公開APIなし、利用規約が自動抽出を全面禁止、CFAAで提訴実績あり【確】 | — | — | — | — |
| **Zumper** | 公開APIなし【確】 | — | — | — | — |
| **RentSpree** | 【未】 | — | — | — | — |
| **HUD Home Store / HomePath / HomeSteps** | 誰でも閲覧可。**公式APIは見当たらない**【確】 | サイト上には写真あり。取得手段はスクレイピングのみ | 無料 | 各サイトのToU | Apifyのスクレイパーが存在＝公式経路がない証拠 |

> **米国の決定的な一行**：MLSのデータライセンスを持つベンダーであっても、**「自社のための、一般公開の物件閲覧サイト」を作ることは許されない**。ベンダーは「MLS会員のためのサイト」しか作れない【確・Repliers Help Center の要約】。これで米国は個人にとって完全に閉じる。

### 2-B. 英国

| ソース | 個人可否 | 写真 | 費用 | 備考 |
|---|---|---|---|---|
| **Rightmove** | **不可**。api-docs.rightmove.co.uk は**登録エージェントが自分の物件をCRUDするための** API。データフィードは Rightmove 発行の X509 証明書を持つ authorised party のみ【確】 | — | — | 窓口 adfsupport@rightmove.co.uk |
| **Zoopla** | **事実上死亡**。developers.zoopla.co.uk はドキュメントとエンドポイントが放置されたまま、キーは無効化・要個別再申請という状態が2018年から報告されている【確】 | — | — | 新規に賭ける対象ではない |
| **OnTheMarket** | **不可**。Real Time Datafeed は Rightmove API ベースの**エージェント向け（inbound）**【確】 | — | — | Network ID＋branch code をエージェントに発行 |
| **PropertyData** | **可（セルフサーブ、14日無料トライアル）**【確】 | **写真なし**（住所・価格・賃料・計画申請・所有権・制約などの分析データ）【確】 | **£28/月〜**、月次コミットなし【確】 | 分析レイヤとしては優秀 |
| **Homedata（HM Haus Group）** | **可（無料枠 100 calls/月、カード不要）**【確】 | **写真は確認できず【未】。データ出所（HM Land Registry / EPC / OS AddressBase / EA / ONS / Home.co.uk）から見て写真は無いと考えるべき**【推】 | 無料枠→**£49/月（2,000 calls）**【確】 | Home.co.uk 経由で1995年以降のリスティング履歴（DOM・価格変更・ステータス）を提供。「スクレイピングなし、OGLと商用契約でライセンス」と明言【確】 |
| **Nestoria / Mitula（LIFULL Connect）** | nestoria.co.uk/help/api は**依然として存在する**が、**稼働状況を本調査では確認できなかった（egress遮断）**【未】。Nestoria (UK) Limited は2022-04-26に解散済み【確】、ブランドは LIFULL Connect 傘下で継続【確】 | 【未】 | 【未】 | **かつて個人開発者に開かれた数少ないAPIだった。生きているなら価値は大きい。最優先で自分で叩いて確認すべき対象** |

### 2-C. 欧州大陸

| ソース | 個人可否 | 写真 | 費用 | 備考 |
|---|---|---|---|---|
| **Idealista（西・葡・伊）Search API** | **申請は誰でも出せる**。developers.idealista.com/access-request で氏名・メール・プロジェクト内容を申告 → **承認されれば**ドキュメントとキー/シークレットが届く【確】。承認基準は非公開・裁量【確】 | **thumbnail は返る**【単】。フル multimedia の可否は**未確認**【未】 | **開発用途は月100コール**【単・GitHub上の記述】。商用枠の料金は非公開 | 「vetted business partners限定で個人には開かれていない」という記述はスクレイパーベンダー由来で**未検証**【単】。**実際に申請して確かめる価値がある、欧州で唯一の outbound API** |
| **ImmoScout24（独）** | **不可**。パートナーAPIは不動産ソフトウェアベンダー向けで正式な提携契約が必要、新規個人登録は開いていない【確】。`channel=is24`（本体掲載）へのAPIアクセスは通常許可されない【確】 | — | — | inbound |
| **Immowelt（独）** | 公開APIなし。EstateSync等のサードパーティ経由が実態【確】 | — | — | inbound |
| **SeLoger / AVIV（仏）** | **不可**。「セルフサービスの公開APIは提供していない」。CaaS/ACP という提携製品と、Ubiflow等のゲートウェイ経由のみ【確】 | — | — | inbound |
| **Funda（蘭）** | **不可**。Partner API は**廃止され、現在は機能していない**【確】 | — | — | 代替はCRMベンダー経由 |
| **Immobiliare.it（伊）** | **不可**（データ取得側としては）。パートナーはサポートから認証情報を受け取り、**呼び出し元サーバのグローバルIPを事前申告**する必要がある＝厳格な提携制【確】 | — | Insights は有償B2B分析product【確】 | inbound |
| **Kyero（西・国際）** | 掲載側は誰でも（エージェントとして）。**取得側の公開APIはなし**【確】 | — | — | **Kyero XML は国際不動産の事実上の業界標準フォーマット**【確】。ここが後述の突破口 |
| **Green-Acres（56カ国・28.8万件）** | 同上。エージェント登録＋XML転送（Transferタブから申請）【確】 | — | エージェントはリード課金型【単】 | inbound |
| **thinkSPAIN** | 同上。多数の不動産ソフト企業とポータルからXMLフィードを受け入れる【確】 | — | — | inbound |
| **Properstar / ListGlobally** | **エージェント向け有料サブスク**（Global Agent Program）。**100以上のポータル・60以上の国に配信**【確】。無料枠でも24カ国26サイトに配信【確】 | — | 非公開 | **「受け取り側ポータル」としてこのネットワークに参加できるかは公開情報がない【未】が、構造上は交渉余地がある唯一の syndication ネットワーク** |
| **HousingAnywhere** | APIドキュメントは**完全公開・無料**、誰でもキー申請可と記載【確】。ただし**「現在、公開APIへの新規パートナーのオンボーディングは行っていない」**【確】 | — | 無料 | **かつ inbound**（パートナーが自分の在庫をJSONフィードで公開URLに置き、HAが日次でpullする） |
| **Spotahome / Blueground** | 公開API・開発者プログラムは**確認できず**【未】 | — | — | — |

### 2-D. 日本（R11の検証結果を再確認・補強）

| ソース | 個人可否 | 写真 | 備考 |
|---|---|---|---|
| **REINS（レインズ）** | **不可**。会員登録には**宅地建物取引業者であること**が必要。一般向けは REINS Market Information（成約価格統計・物件特定不可）のみ【確・R11】 | — | 議論の余地なし |
| **SUUMO** | **不可**。利用規約でコンテンツの複製・転載を原則禁止、商用スクレイピングは規約違反【確・R11、原文条項番号は未確認】 | — | — |
| **LIFULL HOME'S** | **物件データの外部提供APIは確認できず**【未】。公開されているのは「まちむすび 生成AI API」（街の評判データ）であって物件ではない【確】 | — | 企業間データ連携（RESTAR等）はあるが、それはBD案件 |
| **at home** | **不可**。ATBB は**加盟店専用**プラットフォーム【確】。API連携は不動産会社・システムベンダー向け【確】。「不動産データプロ」は事業者向け従量課金【確・R11】 | — | — |
| **ハトマークサイト／不動産ジャパン（全宅連・全日）** | 【未】だが、**業界団体の会員（＝宅建業者）向けであることは構造上ほぼ確実**【推】 | — | — |
| **楽待・健美家** | 公開APIの痕跡なし【未】 | — | 楽待アプリは自社内でハザード重畳を実装済み（R11） |
| **全国版空き家・空き地バンク** | **第三者向けAPIなし**【確】。LIFULL版と at home版があり、自治体↔at home のAPI連携は始まっている（今治市が全国初、2023年）【確】 | 自治体データには写真がある場合も | **自治体個別の空き家バンクをオープンデータ（CSV/CC）として公開しているケースの網羅は確認できなかった【未】。ただし国交省「Project LINKS」で空き家データのオープンデータ化が進行中**【単】 |
| **不動産情報ライブラリ（国交省）** | **可・無料・API公開**【確・R11】 | — | **ただし中身は取引価格・地価公示・防災・都市計画・周辺施設・学区であり「募集中物件」ではない**。33コンテンツ、2025年12月に防災5情報追加【確・R11】 |
| **アフィリエイト経由の物件フィード（A8.net / バリューコマース等）** | **不動産系の案件は存在するが、それは「資料請求」「一括査定」等のリードジェン広告であって、物件データフィードではない**【確】。**不動産の物件データフィードを提供しているASPは確認できなかった**【未＝ほぼ「無い」と読むべき】 | — | ECの商品データフィード（バリューコマースのMyLinkBox/商品DB等）と混同しないこと |

> **日本での最重要の法律的発見（事業設計に直結）**
> 宅建業法の「宅地」は**日本国内に所在するものと解され、海外物件は含まれない**（宅建業法は国内住宅政策の一環として制定され、国内法の効力は外国領土に原則及ばないため）。出典：深沢綜合法律事務所 高川佳子弁護士「国際的な不動産取引における宅建業法の適用関係」RETIO、2018-03-02、<https://www.retio.or.jp/wp-content/uploads/2024/11/houmu_17_002_02.pdf>（確認日 2026-08-29）【確】
> → **海外物件のみを扱う限り、宅建業免許は原則不要**。逆に言えば、日本国内物件に手を出した瞬間に媒介該当リスクが立ち上がる。この非対称性は、後述の「トップ3」の順位を決定づける。
> ※ ただし国交省自身が「海外支店・外国会社を免許制度上どう位置づけるかは今後の検討課題」としており、グレーは残る【確】。**報酬を受けて売買を仲介する形にするなら弁護士確認必須。**

### 2-E. カナダ／豪州／アジア／中東／中南米

| 国 | ソース | 個人可否 | 写真 | 備考 |
|---|---|---|---|---|
| **カナダ** | **CREA DDF®** | **不可**。**CREAの会員（REALTOR®）であり、有効なRETSアカウントを持つこと**が必要【確】。DDFは「listings を第三者サイトに配信したいREALTORとブローカーオーナーのためのマネージドサービス」と定義されている【確】 | 会員なら可 | Policy and Rules 2024年1月改訂版が一次ソース（原文は egress遮断で未読）【未】 |
| **豪州** | **Domain API** | **可。4社中唯一、APIキーをセルフサーブで発行する**【確】。GitHub / Google / メールでサインアップ→プロジェクト作成→即「Agencies and Listings」「Properties and Locations」にアクセス可【確】。**500 calls/day**【単】。Sandbox と Production の両ホストが公開されている【確】 | **可能性が高い**。residential search の応答は propertyDetails の **images コレクション**を持つ（media コレクションは Virtual Tour / Video 用と明記）【確】 | 料金は**非公開・案件ごとの見積**（AUD、GST別、業種と月間コール数でセグメント）【確】 | **契約上の壁**：API T&C は「**Approved Purpose に指定された場所・態様でのみ**データのサブセットを表示してよい。内容を改変してはならず、APIを出所として提示し、所定の帰属表示を含めること」と定める【確】。→ **キーは取れるが、一般消費者向けポータルとしての公開は Approved Purpose の承認事項**。また Domain 側は「あなたのビジネスと競合する製品を開発しうる」と明示的に留保している【確】 |
| **豪州** | REA / PropTrack、Pricefinder | **不可（実質）**。ドキュメントは公開だがアクセスはアカウントマネージャー経由のみ【確】 | — | — |
| **豪州** | Cotality（旧CoreLogic AU） | **不可**。ドキュメントもアクセスも契約の背後【確】 | — | — |
| **シンガポール** | **URA Data Service API（政府）** | **可・公式**【確】 | **写真なし**。私有不動産の**成約（caveat）・賃貸実績**データ【確】 | data.gov.sg / developer.tech.gov.sg |
| **シンガポール** | PropertyGuru / 99.co | **公式APIなし**。存在するのは Apify 等の非公式スクレイパーのみ【確】 | — | — |
| **韓国・台湾・香港・タイ** | Naver 부동산 / 직방 / 다방 / 591 / DDproperty | **公開APIは確認できず**【未＝痕跡なし】 | — | 各国政府の実取引価格オープンデータ（韓 국토부 실거래가、台 實價登錄）は存在するが、**募集中物件でも写真付きでもない**【推】 |
| **UAE** | Bayut / Property Finder | **公式の第三者向けAPIは確認できず**【未】。市場に出回る "BayutAPI" 等は**自ら「非公式であり Bayut.com とは無関係」と明記している**【確】 | — | 業者側は LeadSquared 等のコネクタで XML フィードを**push**する（inbound）【確】 |
| **ブラジル** | OLX / ZAP Imóveis / VivaReal（Grupo ZAP） | **公開開発者APIなし**【確】。ZAPとVivaRealは同一バックエンド【確】 | — | 存在するのは Apify / Parse.bot 等の非公式ラッパーのみ |

### 2-F. 横断：マーケットプレイス／公開データ

| 対象 | 評価 |
|---|---|
| **RapidAPI / Apify / ScrapingBee / Oxylabs / Zillapi / RealtyAPI / Parse.bot / HousingFeed 等** | **出所は全て無断スクレイピング。「合法性」は3重に破綻している。** ①元サイトの利用規約違反（契約責任）②データベース権（EU）③**物件写真の著作権が一切移転していない**。これらのベンダーは自分では写真の権利を持っていないので、あなたに使用許諾を与えられない。**「APIから返ってきたから使ってよい」は成立しない。** 実証：Zillow は Datafiniti に「写真を含むコンテンツの組織的な収穫」としてC&Dを送付【確】。CoStar は CREXi を著作権侵害で提訴し係争継続【確】。Datafiniti は自らの規約で **image URL 経由で得た画像の公開表示を禁止**している【確】＝**売り手自身が「写真は使うな」と言っている**。 |
| **Overture Maps / OpenStreetMap** | **物件リスティングは含まれない**【確】。Buildings（20億棟のフットプリント）、Addresses、Places、Divisions、Base のみ。募集中物件・価格・写真はない。 |
| **政府オープンデータの「募集中物件」** | **米国**：HUD Home Store（FHA差押）、Fannie Mae HomePath、Freddie Mac HomeSteps に写真付き募集中物件があるが、**公式APIはない**【確】。**日本**：空き家バンクが最も近いが第三者APIなし【確】。**シンガポール・韓国・台湾**：成約価格のみで募集中物件なし【確/推】。→ **「政府が募集中物件を写真付きAPIで出している国」は、本調査の範囲では見つからなかった。** |

---

## 3. 物件写真の著作権 ── ここが事業の生死を分ける

### 3-1. 権利者は誰か

**撮影者（またはそれを雇った不動産写真スタジオ）である。ポータルでも仲介業者でもない。** これは推測ではなく判例で確定している。

**VHT, Inc. v. Zillow Group（第9巡回区、2019年／差戻し後の再審2021年）**
- VHT は不動産ブローカー・エージェント・MLS に雇われて写真を撮影し、**「当該物件の売却に関連する使用」に限定したライセンス**で納品していた【確】
- Zillow はそれを Zillow Digs（住宅リフォームサイト）に流用 → **約$2M（再審で$1.927M）の損害賠償が確定**【確】
- 出典：<https://cdn.ca9.uscourts.gov/datastore/opinions/2019/03/15/17-35587.pdf>、<https://www.inman.com/2022/01/28/zillow-ordered-to-pay-vht-2m-as-listing-photo-saga-concludes/>（確認日 2026-08-29）

**CoStar Group v. Zillow（2025-07-30 提訴、ニューヨーク連邦地裁）**
- CoStar所有の写真**約47,000枚**の侵害を主張。**史上最大級の画像侵害訴訟**で、**損害賠償は$10億超になりうる**【確】
- 多くは Apartments.com 由来で、**CoStarのウォーターマークをトリミングして除去**していたと主張【確】
- 侵害写真は Zillow だけでなく、**syndication契約経由で Redfin と Realtor.com にも表示された**と主張【確】
- **2026年3月に修正訴状**、対象は約53,000枚に増加【確】
- Zillow は2025年9月に該当写真の撤去を開始【確】
- 出典：<https://www.costargroup.com/press-room/legal/litigation-zillow>、<https://www.realestatenews.com/2025/09/04/zillow-begins-pulling-photos-involved-in-copyright-lawsuit>、<https://www.realestatenews.com/2025/09/30/zillow-brazenly-continuing-copyright-violations-costar-claims>（確認日 2026-08-29）

> **含意**：Zillow ですら、写真の権利処理で二度負けている（VHT）／巨額訴訟に晒されている（CoStar）。**「大手がやっているから大丈夫」は完全に逆で、大手ですら安全ではない領域である。** 個人が同じことをすれば、統計的に見て賠償額は小さいが、事業は一撃で終わる。

### 3-2. ホットリンク（元サーバの画像を直接 `<img>` で表示）は許されるか

**答え：管轄によって割れており、「安全」とは絶対に言えない。**

- **米国・第9巡回区**：Perfect 10 v. Amazon 由来の**「server test」**が生きており、自分のサーバに保存していなければ公開展示権の直接侵害にならない【確】
- **米国・SDNY（ニューヨーク南部地区）**：**Goldman v. Breitbart（2018）で server test を明確に否定**。埋め込みツイート内の写真について、自社サーバに保存していなくても公開展示権侵害になりうるとした【確】。**Nicklen v. Sinclair Broadcast Group（2021）**でも再度否定【確】
- **第5巡回区**で係争中、判断が待たれている状態【確】
- **EU**：CJEU **Renckhoff（C-161/17）** — 他サイトにある写真を**自サイトに再掲載する行為は新たな許諾を要する**。**VG Bild-Kunst v. SPK（C-392/19）** — 権利者が技術的保護措置を講じている場合、それを回避したフレーミングは「公衆への伝達」に該当し侵害となる【確・要旨】
- **日本**：ホットリンク自体を直接扱った最高裁判例は本調査で確認できなかった【未】。ただし各ポータルの利用規約が禁じているため、**契約責任は確実に発生する**

**「許される」ことが文書で確認できた唯一の例**：Booking.com のアフィリエイト規約 ── **「ホテル画像のURLを保存し、HTMLのimgタグで使用すること。画像ファイル自体のダウンロードは許可されない」**【確】。
→ **これが「正しい許諾の形」の見本である。あなたが目指すべきは、どのソースについてもこの一文を書面で持っている状態。**

### 3-3. 実務上の結論

| 行為 | 判定 |
|---|---|
| ポータルからスクレイプした写真を自サーバに保存して表示 | **明確に侵害。やってはいけない** |
| ポータルの画像をホットリンクで表示 | **管轄次第で侵害。EUでは高確率で侵害。規約違反は確実** |
| RapidAPI/Apify のAPIが返す画像URLを表示 | **上と同じ。仲介業者が挟まっても権利は生まれない** |
| **エージェントから書面許諾を得て、エージェントのサーバの画像URLを表示** | **合法。これが唯一の安全解** |
| **Booking.com等、規約で明示的にimgタグ利用が許諾されたAPI** | **合法** |

---

## 4. スクレイピングの法的位置づけ（2026年8月時点）

### 4-1. 米国：「CFAAでは勝てる。契約と不法行為で負ける」

**hiQ Labs v. LinkedIn の全体像を、途中で切って読んではいけない。**

- 2022-04-18：第9巡回区が差止を再確認。**公開ウェブサイトに対して CFAA の "without authorization" は適用されない**とした【確】。ここまでが有名な部分。
- **2022-12-06：和解。hiQ に対し $500,000 の判決が登録され、hiQ は California コモンローの trespass to chattels（動産侵害）と misappropriation の責任を負い、LinkedIn のスクレイピングを事実上恒久的に禁じる差止に服した**【確】
- 出典：<https://www.privacyworld.blog/2022/12/linkedins-data-scraping-battle-with-hiq-labs-ends-with-proposed-judgment/>、<https://www.zwillgen.com/alternative-data/hiq-v-linkedin-wrapped-up-web-scraping-lessons-learned/>（確認日 2026-08-29）

**→ 「hiQが勝った＝スクレイピングは合法」は誤り。hiQは刑事的リスクを回避したが、民事で潰された。会社は消滅した。**

その後の展開：
- **Meta v. Bright Data（N.D. Cal.、2024-01-23）**：Bright Data 側の略式判決。**Metaの利用規約はログアウト状態での公開データ収集を禁じていない**（規約はログイン中のユーザーにのみ適用される）と判断【確】
- **X Corp. v. Bright Data（N.D. Cal.、2024-05-10）**：却下。公開データのコピーに基づく主張は**著作権法にプリエンプトされる**【確】
- **Google v. SerpApi（2025-12-19 提訴 → 2026-07-20 N.D. Cal. が却下）**：DMCA アンチサーカムベンション（SearchGuard）に基づく請求【確】
- **2026年前半**：YouTube クリエイターによる Snap 提訴、Meta に対する DMCA クラスアクション【確】

**含意**：「ログアウト状態での公開データ収集」は米国で徐々に守られつつある。**しかしこれは "データ" の話であって "写真" の話ではない。** 写真は著作権で保護されており、上記のどの判決もそれを覆していない。**むしろ X Corp. 判決の理屈（著作権によるプリエンプション）は、写真については著作権法がフルに効くことを意味する。**

### 4-2. EU：契約でスクレイピングを禁止できる（決定的）

**CJEU Ryanair v. PR Aviation（C-30/14、2015）**
- 対象データベースが**著作権でも sui generis データベース権でも保護されない**場合、**データベース指令は適用されず、所有者は契約条件によって利用を制限することが自由にできる**【確】
- 出典：<https://www.pinsentmasons.com/out-law/news/website-operators-can-prohibit-screen-scraping-of-unprotected-data-via-terms-and-conditions-says-eu-court-in-ryanair-case>（確認日 2026-08-29）

**→ EUでは二重の壁になる。**
1. ポータルのDBが「実質的投資」を伴うなら **sui generis データベース権**で保護される（不動産ポータルは典型的にこれに該当する【推】）
2. 仮に保護されなくても、**利用規約でスクレイピングを禁止でき、それは有効**

米国の hiQ / Bright Data ロジック（「公開データだから」）は **EUでは通用しない**。Idealista、ImmoScout24、Funda、Immobiliare.it、SeLoger を対象にした無断収集は、米国よりはっきり危険である。

### 4-3. まとめ表

| 地域 | 公開データの機械収集 | 契約（ToS）による禁止 | 写真の再利用 |
|---|---|---|---|
| 米国 | CFAA上はグレー〜セーフ（ログアウト時） | **有効。trespass/misappropriation で負けうる（hiQ）** | **明確に違法（VHT / CoStar）** |
| EU | **sui generis DB権で保護されうる** | **有効（Ryanair C-30/14）** | **明確に違法（Renckhoff）** |
| 日本 | 著作権法30条の4等の解釈次第だが、**事業の中核データとしての再配信は別問題** | 規約違反＝債務不履行 | 明確に違法 |

---

## 5. 「合法の抜け道」の現実性評価

依頼者が挙げた5案を、調査結果に照らして採点する。

### (a) アフィリエイト提携で公式にフィードをもらう
**判定：日本の不動産では不可。旅行・宿泊では可。**
- 日本のASP（A8.net、バリューコマース）の不動産案件は**リードジェン広告のみで、物件データフィードは提供されていない**【確に近い未確認＝痕跡ゼロ】
- 一方 **Booking.com Demand API はアフィリエイトパートナーに開かれており、写真のimgタグ利用が明文で許諾されている**【確】。これが唯一機能する「アフィリエイト経由フィード」
- **現実性：不動産では 5%。宿泊・中期滞在では 80%**

### (b) 海外向けポータルは掲載を増やしたいので個人サイトにも配信してくれる
**判定：ポータルは配信してくれない。しかしポータルの"供給元"は配信してくれる。**
- 調査した限り、**掲載を増やしたい海外向けポータル（Kyero、Green-Acres、thinkSPAIN、Properstar）は全て「受け取る側」であって「配る側」ではない**【確】。彼らのXMLは inbound 専用
- ただし **ListGlobally/Properstar は100以上のポータルへ"配信"している**【確】。つまり**配信先ポータルとしてネットワークに入る枠は存在する**。個人サイトが受け入れられるかは公開情報がなく【未】、直接交渉するしかない
- **現実性：ポータル直の配信 = 5%。syndicator への配信先参加 = 25%（要交渉）**

### (c) 物件オーナー/エージェントに直接投稿してもらう
**判定：★これが本命。しかも「投稿してもらう」より「既に持っているXMLフィードを向けてもらう」方が10倍速い。**
- 国際不動産エージェントは**既に Kyero XML 形式のフィードを持っている**【確】。Kyero、Green-Acres、thinkSPAIN、Resales-Online、Inmobalia が同一フォーマット圏を形成している【確】
- スペインには **Resales Online（Costa del Sol / Costa Blanca、1,300超の代理店）**、**Inmobalia**、**MLSCosta**、**Inmovilla（30以上のポータルへ配信可）** といった MLS/CRM が存在し、いずれも XML/API フィードを標準機能として持つ【確】
- エージェントにとって新しい掲載先は**限界費用ゼロでリードが増える**ので、断る理由がない
- **写真の権利も、エージェント経由なら書面で取れる**（エージェントは掲載権を持っている）
- **現実性：70%。ただし営業工数が本体。「エンジニアリングの問題」ではなく「アウトバウンド営業の問題」になる**

### (d) 公開APIがある国だけで始める
**判定：豪州（Domain）が唯一の候補。次点で西（Idealista）。ただし両方とも「承認」の壁がある。**
- Domain は**キーはセルフサーブ**だが、**T&C が「Approved Purpose に指定された態様でのみ表示可」**としている【確】。消費者向けポータル用途は Domain の承認事項であり、**Domain は自ら「あなたと競合しうる製品を作る」と留保している**【確】。→ 承認される確率は低いと見るべき【推】
- Idealista は**申請自体は誰でも出せる**が、承認は完全に裁量【確】。開発枠は月100コール【単】＝プロダクションには全く足りない
- **現実性：Domain = 30%（承認次第）。Idealista = 20%（承認＋レート制限）**

### (e) ディープリンクのみでデータは持たない
**判定：合法性は最も高いが、依頼者の要件「写真付きで表示」を満たさない。**
- リンクだけなら著作権も規約もほぼ問題にならない
- しかし**写真もスペックも表示できないなら、それは「検索サイト」ではなく「リンク集」であり、ユーザーは元サイトに行くだけ**
- **現実性：法的には 95%、事業的には 5%**

### 追加：本調査で見つかった第6の道

**(f) 「写真なしデータAPI」＋「写真は自分で作る」**
- RentCast（$0〜$449/月）、PropertyData（£28/月〜）、Homedata（無料枠あり）、ATTOM、不動産情報ライブラリ、URA API は**すべて合法・セルフサーブで、写真がない**
- 写真がないなら、**写真を必要としないプロダクト**（分析、スコアリング、アラート、投資判断支援）に振ることはできる
- ただしこれは「物件リスティングを表示するサイト」という当初の構想を捨てることを意味する
- **現実性：法的に 95%、ただし依頼者の要件を満たさない**

---

## 6. 今日から合法に始められる組み合わせ ── トップ3

### 【1位】欧州の国際向けエージェントから直接XMLフィードを受け取る（Kyero XML 互換）

**なぜ1位か**：写真の権利チェーンが唯一クリーンで、費用ゼロで、承認待ちがなく、日本の宅建業法の適用外（＝海外物件）で、しかも Kyero・Green-Acres・thinkSPAIN が実際に通った実証済みの道だから。

**具体的手順**
1. **Kyero XML Import Specification を読んで実装する**。<https://help.kyero.com/estate-agents/xml-import-specification>（確認日 2026-08-29）。エクスポート仕様も <https://help.kyero.com/xml-export-specification>（同）。これが国際不動産の事実上の標準【確】
2. **同時に Resales-Online / Inmobalia / Inmovilla の形式にも対応**しておく。スペインのCRMはこの4形式のいずれかを吐く【確】
3. **対象エージェントのリストを作る**。Costa del Sol / Costa Blanca / Algarve / トスカーナ など、**英語対応の国際向けエージェント**。Kyero・Green-Acres・thinkSPAIN の掲載社リストがそのまま営業リストになる
4. **打診文面の骨子**：「新しい日本語（＋英語）市場向けポータルを立ち上げる。掲載は無料、リードは無償で直送。既にお持ちの Kyero XML フィードのURLをいただければ、こちらで取り込む」
5. **必ず書面で取るもの（ここを省略したら全部無意味）**：
   - 物件データおよび**写真を、あなたのサイトおよびアプリで表示する非独占的ライセンス**
   - **エージェントが当該写真について再許諾する権利を有することの表明保証（warranty）**と補償条項（indemnity）
   - 掲載終了時の削除義務（VHT判例が示す通り、ライセンスは「当該物件の販売に関連する使用」に限定されるのが業界慣行）
   - 画像は**エージェント側サーバのURL参照か、自ホストか**を明記
6. **50社に打診して10社返ってくれば、数千件の写真付き物件が合法に手に入る**

**リスク**：営業が全て。エンジニアリングは1週間、営業は6ヶ月。ソロで最も嫌いな作業に事業の成否が乗る。**ここを直視できないならこの事業自体を諦めた方がよい。**

---

### 【2位】豪州 Domain API（Agents & Listings）

**なぜ2位か**：世界で唯一「今日サインアップして、今日キーが出て、写真付きリスティングが返ってくる」大手ポータルAPIだから。ただし**契約上の承認が本番公開の前提**なので1位にはできない。

**具体的手順**
1. <https://developer.domain.com.au/>（確認日 2026-08-29）で GitHub / Google / メールでサインアップ
2. プロジェクトを作成すると **「Agencies and Listings」「Properties and Locations」に即時アクセスできる**【確】。**500 calls/day**【単】、Sandbox / Production 両方のホストが公開【確】
3. `POST /v1/listings/residential/_search` で検索。応答は PropertyListing / Project オブジェクト。**画像は propertyDetails の images コレクション**（media コレクションは Virtual Tour / Video 専用）【確】
4. **本番公開の前に必ず api@domain.com.au に用途を申告し、Approved Purpose の書面承認を取る**。T&C は「Approved Purpose に指定された場所・態様でのみサブセットを表示可、内容改変禁止、API出所の明示と所定の帰属表示が必須」と定める【確】
5. 料金は**AUD建て・GST別の Product Schedule で個別契約**、業種と月間コール数でセグメント【確】。**公開料金表は存在しない**

**リスク（最大）**：Domain は T&C で**「あなたのビジネス・ウェブサイト・アプリと競合する製品やサービスを開発する場合がある」と明示的に留保**している【確】。**消費者向け物件検索ポータルは Domain 本体との真正面の競合**なので、Approved Purpose として承認されない可能性が高い【推】。
**→ だから手順4を先にやること。コードを書く前に、メールを1通送って承認可否を確かめる。** これが今日できる最も情報価値の高い1アクション。

---

### 【3位】Booking.com Demand API（中期滞在・家具付き賃貸に振る）

**なぜ3位か**：**写真の使用が書面で明示的に許諾されている、本調査で見つかった唯一のセルフサーブAPI**だから。ただし「不動産」ではなく「宿泊」である。

**具体的手順**
1. **Affiliate Partner Programme に登録**。<https://www.booking.com/affiliate-program/v2/index.html>（確認日 2026-08-29）。**要件はアクティブなウェブサイト／ブログ。SNSのみのパブリッシャーは受け付けられない**【確】。審査は**通常1〜5営業日**【確】
2. Partner Centre にログインし、**APIキートークンと X-Affiliate-Id を生成**【確】
3. Demand API v3 を叩く。<https://developers.booking.com/demand>（確認日 2026-08-29）
4. **写真の扱い（明文の許諾）**：「ホテル画像のURLを保存し、HTMLの img タグで使用すること。**画像ファイル自体のダウンロードは許可されない**」【確】
5. **Monthly Stays / 長期滞在**に絞り込めば、「住まい探し」に隣接した製品になる

**注意**：**「Connectivity Partner」のポータル新規登録は現在停止中**（新パートナー向けの利用規約更新のため）という記述がある【確】。ただしこれは Connectivity（供給側）の話であり、Affiliate（需要側）とは別系統。**登録時に実際に通るかは自分で確認すること**【未】。

---

### 【次点／並行してやるべきこと】

**Nestoria API の生死を自分で確認する。** <https://www.nestoria.co.uk/help/api>（確認日 2026-08-29、**本調査ではegress遮断で内容未確認**）。かつて個人開発者に開かれていた数少ない多国籍物件検索APIで、生きていれば29カ国をカバーする【確】。ページは存在するが稼働は未確認。**5分で確かめられて、当たれば最大のリターンがある。最優先の検証項目。**

**RentCast の写真フィールドの有無を無料枠で確認する。** Developer プラン $0 / 50リクエストで即座に検証可能【確】。写真があれば米国の風景が変わる。**なければ「米国は完全に閉じた」が確定する。**

---

## 7. 絶対に無理な領域（ここに時間を使ってはいけない）

1. **米国MLS / IDX の物件と写真を、免許ブローカーのスポンサーなしに自社ポータルに表示すること。**
   NAR方針上、MLS参加は**有効な不動産ブローカー免許保有者**に限定される【確】。さらに決定的なのは、**データライセンスを持つベンダーですら「自社のための一般公開の物件閲覧サイト」を作れない**という運用ルール【確】。Bridge、MLS Grid、Trestle、SimplyRETS はすべてこの制約の下流にある。**免許を取らない限り、迂回路は存在しない。**

2. **Zillow / Redfin / Realtor.com / Rightmove / Zoopla / SUUMO / LIFULL HOME'S / at home / CoStar・Apartments.com のデータと写真を、合法に取得して自サイトに再掲載すること。**
   公開APIがないか（Zillowは2021-09-30に廃止済み【確】）、inbound専用か、規約で明確に禁止されている。

3. **REINS。** 宅建業者限定。議論の余地なし【確】。

4. **RapidAPI / Apify / Datafiniti 等から買ったデータの「写真」を公開表示すること。**
   売り手自身が禁じている（Datafiniti規約【確】）か、そもそも権利を持っていない。Zillow の C&D【確】と CoStar v. CREXi【確】が実証している。**「APIを買った」ことは著作権のライセンスにならない。**

5. **大手ポータルからの画像ホットリンク。**
   EUでは Renckhoff / VG Bild-Kunst により高確率で侵害【確・要旨】。米国は管轄で割れている【確】。規約違反は全管轄で確実。

6. **CREA DDF（カナダ）。** CREA会員＋有効なRETSアカウントが必須【確】。

7. **「政府オープンデータで募集中物件を写真付きで入手する」。** 本調査の範囲では、そのような国は見つからなかった【確・網羅性は限定的】。

---

## 8. 未確認事項リスト（次に潰すべき順）

| # | 項目 | なぜ重要か | 確認方法 |
|---|---|---|---|
| 1 | **Nestoria API が稼働しているか** | 生きていれば29カ国の物件検索が個人に開く | nestoria.co.uk/help/api を直接叩く |
| 2 | **RentCast のレスポンスに写真URLがあるか** | 米国が完全に閉じるかどうかが決まる | 無料枠（50 req）で1回叩く |
| 3 | **Domain が消費者向けポータル用途を Approved Purpose として承認するか** | 2位案の生死 | api@domain.com.au にメール1通 |
| 4 | **Idealista が個人・小規模事業者に本番枠を出すか、写真（multimedia）を許すか** | 欧州で唯一の outbound API | developers.idealista.com/access-request で申請 |
| 5 | **ListGlobally / Properstar が新規の配信先ポータルを受け入れるか** | 数万件を一度に入手できる唯一の集約経路 | Properstar に直接問い合わせ |
| 6 | **RentCast / Domain / Idealista の利用規約の原文条項** | 本調査では egress 遮断で読めていない | 各サイトの規約ページを直接読む |
| 7 | **各ポータルの robots.txt の実態** | 本調査では**1件も読めていない** | 各サイトを直接取得 |
| 8 | **日本の自治体で空き家バンクを画像付きオープンデータ公開している例の網羅** | 日本国内で唯一合法に写真を扱える可能性 | 各自治体オープンデータカタログを横断 |
| 9 | **海外物件の紹介で報酬を受け取る場合の宅建業法・景表法・特商法の扱い** | 収益化モデルの前提 | 弁護士確認（RETIO論文は2018年で古い） |
| 10 | **Booking.com Affiliate の新規登録が現在通るか** | 3位案の生死 | 実際に登録申請する |

---

## 9. 最後に ── 楽観を1つも残さないための総括

12ラウンドで甘い見立てが全部崩れてきたという前提に立って、この調査の結論を最も厳しく言い直す。

**この事業のボトルネックは技術ではない。データ調達であり、それは営業と法務の問題である。**

- 「APIを見つける」フェーズは、この調査で終わった。**見つからなかった**が答えである。
- 残った3経路のうち、1位は**半年のアウトバウンド営業**、2位は**Domainの承認という他人の意思決定**、3位は**不動産ではない領域への転進**を意味する。
- どれも「週末に作って公開する」タイプの仕事ではない。
- 唯一、**今日30分でできて情報価値が最大なのは、上記の未確認事項 #1〜#3（Nestoriaを叩く／RentCastを叩く／Domainにメールを出す）** である。コードを1行も書く前に、この3つをやること。3つとも空振りなら、1位案（エージェント営業）に腹を括るか、事業ごと畳むかの二択になる。

**「技術的に可能」と「法的に安全」の距離は、この分野では地球1周分ある。** hiQ は第9巡回区で勝ったが会社は消えた。Zillow は写真で2回負けている。CREXi は CoStar と5年戦っている。**個人がこの戦場に、規約違反のデータ調達で入っていくのは、成功したら死ぬ設計である。**

---

## 付録：出典一覧（全て確認日 2026-08-29）

※「[遮断]」= 本セッションの egress プロキシが 403 で遮断したため**原文は未読**。検索エンジン経由の要約により内容を把握した。

### 米国 — MLS / IDX
- NAR「Qualification for MLS Participation and IDX」<https://www.nar.realtor/about-nar/policies/qualification-for-mls-participation-and-idx> [遮断]
- NAR IDX Policy Statement 7.58 <https://www.nar.realtor/handbook-on-multiple-listing-policy/advertising-print-and-electronic-section-1-internet-data-exchange-idx-policy-policy-statement-7-58> [遮断]
- Repliers「MLS® Data Access Requirements: Who Can Use MLS® APIs」<https://help.repliers.com/en/article/mls-data-access-requirements-who-can-use-mls-apis-wyl8lw/> [遮断] ← 「ベンダーは自社向けの一般公開閲覧サイトを作れない」の出典
- MLS Grid FAQ <https://www.mlsgrid.com/faq> [遮断] ／ Resources <https://www.mlsgrid.com/resources> [遮断] ／ Docs <https://docs.mlsgrid.com/> [遮断]
- SDMLS Master Data Access Agreement（PDF）<https://sdmls.com/wp-content/uploads/2025/12/SDMLS-Master-Data-Access-Agreement.pdf> ← 「Listing Data には text, photographs が含まれる」
- Canopy MLS Data Licensing <https://go.canopymls.com/Data/default.aspx> ← 非参加者ライセンスは理事会承認が必要
- OneKey MLS Data Delivery Resources <https://support.onekeymls.com/hc/en-us/articles/27251536794644-Data-Delivery-Resources> ← ベンダー $250/月＋$20/ライセンス
- CRMLS IDX Resources <https://go.crmls.org/idx-resources/> ← Trestle $75/MLS/月、IDX $85/月、Broker $25/月
- Trestle Subscription Wizard <https://trestle.corelogic.com/SubscriptionWizard/> ／ Cotality Trestle <https://www.cotality.com/products/trestle>
- Inman「CoreLogic's Trestle Now Open For Business」<https://www.inman.com/2017/03/24/corelogics-trestle-now-open-for-business-will-tech-vendors-bite/>
- SimplyRETS FAQ <https://simplyrets.com/faq> ／ Getting set up <https://simplyrets.com/blog/getting-set-up> ／ Service Agreement <https://simplyrets.com/serviceagreement>
- Bridge Interactive Bridge API <https://www.bridgeinteractive.com/developers/bridge-api/> [遮断] ／ Zillow Group Data <https://www.bridgeinteractive.com/developers/zillow-group-data/> [遮断]
- Zillow Group Developers（MLS/Broker Data）<https://www.zillowgroup.com/developers/api/mls-broker-data/reviews-api/> [遮断]
- MIAMI REALTORS「Get started with the Bridge API in 4 easy steps」<https://www.miamirealtors.com/wp-content/uploads/bsk-pdf-manager/2019/12/Get-started-with-the-Bridge-API-in-4-easy-steps.pdf>
- MIAMI REALTORS「Bridge Interactive Understanding the RESO Web API」<https://www.miamirealtors.com/wp-content/uploads/bsk-pdf-manager/2022/07/Bridge-Interactive-Understanding-the-RESO-Web-API.pdf>
- ListHub / Move 関連：HousingWire <https://www.housingwire.com/articles/33001-exclusive-move-owned-listhub-terminates-trulia-relationship/> ／ Stellar MLS Distribution <https://www.stellarmls.com/distribution>

> ⚠ Zillow / Bridge の「$500/月〜」という金額は **zillapi.com（自らスクレイパーAPIを売る事業者）由来**であり、一次ソース確認ができていない。**この数字を計画に使わないこと。**

### 米国 — データベンダー
- RentCast Pricing <https://www.rentcast.io/pricing> [遮断] ／ API <https://www.rentcast.io/api> [遮断] ／ Docs <https://developers.rentcast.io/reference/introduction> [遮断]
- ATTOM API FAQ <https://www.attomdata.com/solutions/property-data-api/faqs/> ／ Developer Platform <https://api.developer.attomdata.com/home> ／ ATTOM Cloud <https://cloud.attomdata.com>
- Estated Docs v4 <https://estated.com/developers/docs/v4> ／ <https://estated.com/> （ATTOM 統合・2026年中に廃止）
- Datafiniti Terms of Use <https://www.datafiniti.co/terms> ← **image URL 由来画像の公開表示禁止・大幅改変なき再配布禁止**
- Datafiniti Property Data Docs <https://docs.datafiniti.co/docs/api-property-data> ／ Schema <https://docs.datafiniti.co/docs/property-data-schema>
- Redfin Data Center（2026年5月再構築）— 二次報道経由で確認
- CoStar Group Legal / Zillow 訴訟 <https://www.costargroup.com/press-room/legal/litigation-zillow>
- CoStar v. CREXi 更新 <https://www.costargroup.com/press-room/2025/costar-group-provides-update-about-ongoing-legal-battle-crexi>

### 英国
- Rightmove Real Time Datafeed Specification v1.4.1（PDF）<https://media.rightmove.co.uk/ps/pdf/guides/adf/Rightmove_Real_Time_Datafeed_Specification.pdf>
- Rightmove API Docs（Commercial Listings API、エージェント向け）<https://api-docs.rightmove.co.uk/docs/property-feed-api-product/1/overview>
- Zoopla Developers <https://developers.zoopla.co.uk/> ／ Member Support APIs <https://support.zoopla.co.uk/hc/en-gb/sections/360004580137-API-s>
- Mario Menti「How not to run an API (looking at you, Zoopla)」<https://medium.com/@mariomenti/how-not-to-run-an-api-looking-at-you-zoopla-bda247e27d15>
- OnTheMarket Realtime Datafeed（Rightmove API 準拠）<https://www.scribd.com/document/906651333/Onthemarket-Realtime-Datafeed> ／ <https://estateagentfeeds.com/onthemarket-real-time-data-feed-integration/>
- PropertyData API <https://propertydata.co.uk/api> ／ Pricing <https://propertydata.co.uk/api/pricing>
- Homedata <https://homedata.co.uk/> [遮断] ／ Pricing <https://homedata.co.uk/pricing> [遮断] ／ About <https://homedata.co.uk/about> [遮断] ／ Home.co.uk 提携 <https://home.co.uk/homedata>
- Nestoria API <https://www.nestoria.co.uk/help/api> [遮断・稼働未確認] ／ LIFULL Connect <https://www.lifullconnect.com/brands/nestoria/>

### 欧州大陸
- Idealista Developers <http://developers.idealista.com/> [遮断] ／ Access Request <https://developers.idealista.com/access-request> [遮断]
- Idealista General Terms <https://www.idealista.com/ayuda/articulos/legal-statement/?lang=en>
- 非公式Pythonクライアント（月100コール等の記述元）<https://github.com/yagueto/idealista-api> ／ <https://github.com/Cavitedev/BuscaIdealista>
- ImmoScout24 API Developer Portal <https://api.immobilienscout24.de/api-docs/introduction/> [遮断] ／ Customer Website tutorial <https://api.immobilienscout24.de/api-docs/tutorials/customer-website/> [遮断]
- EstateSync（独ポータル群への配信）<https://estatesync.com/en/>
- Immobiliare.it Mission Control 統合ガイド <https://feed.immobiliare.it/integration/ii/docs/import/get-start> ／ Insights API <https://www.immobiliare.it/insights/en/api/>
- SeLoger / AVIV：Stream Estate「API SeLoger : Mythes, Réalités」<https://stream.estate/fr/blog/api-seloger-existe-elle-alternatives> ／ Journal de l'Agence（CaaS API）<https://www.journaldelagence.com/1402748-a-travers-lapi-caas...>
- Funda Partner API（廃止・非稼働）<https://github.com/edgarschaap/Funda.PartnerApi> ／ <https://tussendoor.nl/plugins/wordpress-funda-koppeling/>
- Kyero XML Import Specification <https://help.kyero.com/estate-agents/xml-import-specification> ／ XML Export Specification <https://help.kyero.com/xml-export-specification> ／ 対応PMS一覧 <https://help.kyero.com/estate-agents/compatible-property-management-systems>
- Green-Acres Automatic listing transfer <https://www.green-acres.pt/en/GatewayInfo> ／ Agency registration <https://www.green-acres.fr/en/Register/Agency>
- thinkSPAIN（XMLフィード受入）<https://terrenos.es/en/portals/thinkspain.com>
- Properstar / ListGlobally：<https://www.properstar.com/what-is-properstar> ／ <https://agent.properstar.com/en> ／ <https://dashboard.properstar.com/global> ／ MyStateMLS 提携 <https://www.mystatemls.com/blog/product_updates/what-you-need-to-know-about-our-listglobally-partnership.html>
- Resales Online <https://www.resales-online.com/> ／ MLS <https://www.resales-online.com/mls/> ／ Pricing <https://www.resales-online.com/pricing/>
- Inmobalia CRM（Resales Online / Kyero XML 互換）<https://www.inmobalia.com/>
- MLSCosta <https://www.mlscosta.com/en/agent-in-spain> ／ Inmovilla 解説 <https://inmotech.com.es/multi-listing-service-mls-costa-del-sol/>
- HousingAnywhere Developers <https://developers.housinganywhere.com/> ／ Docs <https://docs.housinganywhere.com/> ／ 統合ガイド <https://housinganywhere.com/how-to-integrate-property-database>

### 日本
- REINS Q&A <https://www.reins.or.jp/qa/>（R11で確認）
- SUUMO 利用規約 <https://suumo.jp/edit/kiyaku/> ／ <https://cdn.p.recruit.co.jp/terms/suu-t-1003/index.html>（R11、原文条項番号未確認）
- LIFULL「まちむすび 生成AI API」<https://lifull.com/news/34546/>
- LIFULL HOME'S PRESS「不動産情報ライブラリのAPI活用事例」<https://www.homes.co.jp/cont/press/opinion/opinion_00417/>
- アットホーム ATBB / 一括登録システム <https://business.athome.jp/service/ikkatsu_system/> ／ 不動産データプロ <https://business.athome.jp/service/datapro/>
- アットホーム空き家バンク × いまばり空き家バンク API連携（全国初、2023年）<https://www.athome.co.jp/corporate/news/release/services/akiya-bank-202304/>
- 国交省 空き家・空き地バンク総合情報ページ <https://www.mlit.go.jp/totikensangyo/const/sosei_const_tk3_000131.html>
- 国交省 全国版空き家・空き地バンク（アットホーム）促進事業 <https://www.mlit.go.jp/jutakukentiku/house/content/001604078.pdf>
- 不動産情報ライブラリ（API無料公開、33コンテンツ）<https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/tochi_fudousan_kensetsugyo_tk17_000001_00038.html>（R11）
- **高川佳子「国際的な不動産取引における宅建業法の適用関係」RETIO、2018-03-02** <https://www.retio.or.jp/wp-content/uploads/2024/11/houmu_17_002_02.pdf> ← 「宅地＝日本国内所在」の根拠
- 国交省「不動産業の国際化」<https://www.mlit.go.jp/totikensangyo/const/totikensangyo_const_tk1_000057.html>
- A8.net <https://www.a8.net/about.html>（不動産案件はリードジェン型）
- 健美家「海外不動産投資と宅建免許の関係」<https://www.kenbiya.com/ar/ns/jiji/legal_knowledge/7503.html>

### カナダ / 豪州 / アジア / 中東 / 中南米
- CREA DDF Policy and Rules（2024年1月改訂）<https://www.crea.ca/files/technology/english/DDFR-Policy-and-Rules-February-2024-ENG.pdf> [遮断]
- CREA Support DDF <https://support.crea.ca/DDF> [遮断] ／ Repliers「Compliance Requirements For Using CREA's DDF」<https://help.repliers.com/en/article/compliance-requirements-for-using-creas-ddf-1jqsdic/> [遮断]
- Domain Developer Portal <https://developer.domain.com.au/> [遮断] ／ APIs <https://developer.domain.com.au/docs/latest/apis/> [遮断] ／ Terms <https://developer.domain.com.au/docs/latest/support/terms/> [遮断] ／ FAQ <https://developer.domain.com.au/docs/v2/support/faq/> [遮断]
- Domain 残余検索エンドポイント <https://developer.domain.com.au/docs/v1/apis/pkg_agents_listings/references/listings_detailedresidentialsearch/> [遮断]
- **Domain Group API Terms and Conditions** <https://www.domain.com.au/group/api-terms-and-conditions/> ← 「Approved Purpose に指定された態様でのみ表示可／改変禁止／帰属表示必須／競合製品開発の留保」
- Domain 画像規定（Breach listings, images and URLs）<https://help.domain.com.au/hc/en-us/articles/360012121513-Breach-listings-images-and-URLs>
- 13Labs「Australian Property Data APIs Compared」<https://www.13labs.au/guides/australian-property-data-apis-compared> ← 「Domain のみがセルフサーブでキー発行」
- Computerworld「Domain launches open APIs for third-party developers」<https://www.computerworld.com/article/1656355/domain-launches-open-apis-for-third-party-developers.html>
- Medium「How to get Aussie property price guides using Python & the Domain API」<https://medium.com/@alexdambra/how-to-get-aussie-property-price-guides-using-python-afe871efac96> ← 500 calls/day
- Singapore URA Data Service APIs <https://www.developer.tech.gov.sg/products/categories/data-and-apis/ura-apis/overview>
- BayutAPI（**自ら「非公式・Bayutと無関係」と明記**）<https://bayutapi.dev/> ／ <https://bayutapi.com/documentation.html>
- LeadSquared Property Listing UAE Connector（業者→ポータルのXML push）<https://help.leadsquared.com/property-listing-uae-connector/>

### 旅行・宿泊（写真許諾の唯一の明文例）
- Booking.com Demand API <https://developers.booking.com/demand> ／ Prerequisites <https://developers.booking.com/demand/docs/getting-started/prerequisites> ／ Auth <https://developers.booking.com/demand/docs/development-guide/authentication>
- Booking.com Affiliate Programme <https://www.booking.com/affiliate-program/v2/index.html> ／ Sign-Up KB <https://affiliates.support.booking.com/kb/s/article/Affiliate-Partner-Programme-Sign-Up> ／ API Access KB <https://affiliates.support.booking.com/kb/s/article/API-access>
- Booking.com Legacy API Permitted Use（**画像URLのimgタグ利用可／ファイルDL不可**）<https://legacy.developers.booking.com/api/commercial/index.html?page_url=permitted-use>
- Partnerships Hub API V3 <https://partnerships.booking.com/api-v3>

### 判例・法務
- **hiQ Labs v. LinkedIn**（9th Cir. 2022-04-18）<https://law.justia.com/cases/federal/appellate-courts/ca9/17-16783/17-16783-2022-04-18.html>
- **hiQ 和解・$500,000判決（2022-12-06）** <https://www.privacyworld.blog/2022/12/linkedins-data-scraping-battle-with-hiq-labs-ends-with-proposed-judgment/> ／ Zwillgen <https://www.zwillgen.com/alternative-data/hiq-v-linkedin-wrapped-up-web-scraping-lessons-learned/> ／ Morgan Lewis <https://www.morganlewis.com/blogs/sourcingatmorganlewis/2022/12/linkedin-v-hiq-landmark-data-scraping-suit-provides-guidance-to-data-scrapers-and-web-operators>
- **Meta v. Bright Data**（N.D. Cal. 2024-01-23）<https://www.fbm.com/publications/major-decision-affects-law-of-scraping-and-online-data-collection-meta-platforms-v-bright-data/> ／ Lowenstein <https://www.lowenstein.com/news-insights/publications/client-alerts/meta-v-bright-data-ruling-has-important-implications-for-webscraping-activities-by-investment-advisers-im>
- **X Corp. v. Bright Data**（N.D. Cal. 2024-05-10、著作権プリエンプション）<https://www.skadden.com/insights/publications/2024/05/district-court-adopts-broad-view> ／ <https://www.proskauer.com/release/proskauer-secures-dismissal-of-scraping-claims-against-bright-data>
- **2025-2026 の動向（Google v. SerpApi 等）** Zwillgen「How Artificial Intelligence is Shaping Web Scraping Litigation」<https://www.zwillgen.com/alternative-data/how-artificial-intelligence-shaping-web-scraping-litigation/>
- **CJEU Ryanair v. PR Aviation（C-30/14, 2015）** Pinsent Masons <https://www.pinsentmasons.com/out-law/news/website-operators-can-prohibit-screen-scraping-of-unprotected-data-via-terms-and-conditions-says-eu-court-in-ryanair-case> ／ MediaLaws <https://www.medialaws.eu/ecj-clarifies-database-directive-scope-in-screen-scraping-case/> ／ IPLens <https://iplens.org/2015/05/01/ecj-the-owner-of-an-online-database-not-protected-by-copyright-or-sui-generis-right-may-limit-its-use-by-contract/>
- フランスにおけるスクレイピング対抗（Hogan Lovells）<https://www.hoganlovells.com/en/publications/france-protecting-a-website-from-unlawful-data-scraping>
- **VHT v. Zillow**（9th Cir. 2019）<https://cdn.ca9.uscourts.gov/datastore/opinions/2019/03/15/17-35587.pdf> ／ 再審後$1.927M <https://www.inman.com/2022/01/28/zillow-ordered-to-pay-vht-2m-as-listing-photo-saga-concludes/> ／ Loeb & Loeb <https://www.loeb.com/en/insights/publications/2023/06/vht-inc-v-zillow-group-inc-et-al>
- CRMLS「What Photography Lawsuits Can Teach Listing Brokers About Copyright in the MLS」<https://blog.crmls.org/updates/what-photography-lawsuits-can-teach-listing-brokers-about-copyright-in-the-mls/>
- **Server test の分裂**：Wikipedia <https://en.wikipedia.org/wiki/Server_test> ／ Wilson Sonsini <https://www.wsgr.com/en/insights/thinking-of-framing-or-embedding-content-new-york-federal-courts-question-the-copyright-server-test.html> ／ Arnold & Porter <https://www.arnoldporter.com/en/perspectives/advisories/2019/12/embedding-online-content> ／ 第5巡回区係属中 <https://www.mondaq.com/unitedstates/copyright/1805848/is-embedding-someone-elses-image-copyright-infringement-the-fifth-circuit-may-finally-tell-us>

### 公開地理データ
- Overture Maps FAQ <https://overturemaps.org/about/faq/> ／ Buildings Guide <https://docs.overturemaps.org/guides/buildings/> ／ AWS Open Data <https://registry.opendata.aws/overture/> ← **物件リスティングは含まれない**
