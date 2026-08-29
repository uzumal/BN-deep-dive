# R14 / ポインタ型コンテンツ源・全世界棚卸し

**調査日：2026-08-29（本文中の全URLの確認日は同日）**
**対象者の制約：日本在住ソロエンジニア／フォロワーゼロ／広告予算なし／日英可／元Cisco SE・Webエンジニア／運用費 月$0〜20**
**総合判定：ポインタ型データ源は「山ほどある」。しかし"それを地球儀に載せる"というアイデアは、2026年8月時点で構造的にほぼ全域が埋まっている。最大の発見は overwatch.earth（32レイヤの実在する集約グローブ）である。**

---

## 0. 調査手法と制約の開示（先に全部書く）

### 0-1. 実施したこと
- **WebSearch を 82クエリ実行**（製品語彙×ユーザー語彙×日英）。全クエリは §6 に列挙した。
- 各候補について「無料枠の実数」「第三者表示の可否」「件数」「既存競合」を個別に照会。

### 0-2. 制約（重大）
本セッションの egress プロキシが、**多くの一次ソースへの直接アクセスを遮断**した。curl / WebFetch とも遮断され、迂回は行っていない。

遮断された主要ドメイン（＝規約原文の逐条確認ができなかった先）：
`api.windy.com` / `de1.api.radio-browser.info` / `openskynetwork.github.io` / `www.inaturalist.org` / `en.wikipedia.org` / `gbfs.org` / **`overwatch.earth`** / `tuxxin.com` / `scoutforge.net` / `docs.mapillary.com`

**到達できたのは `github.com` のみ**（GBFS systems.csv の行数はここで実測）。
したがって本レポートは **検索エンジン経由の一次ソース要約＋二次資料** で構成されている。R13 と同じ confidence 記法を厳守する：

- **【確】** = 複数経路で裏取り済み、または一次ソースの記述として引用可能
- **【単】** = 単一の二次ソースのみ。要自己確認
- **【推】** = 推論。証拠なし
- **【未】** = 調べたが確認できなかった（≠存在しない）

**「空白」と書いた箇所には、必ず実行クエリと発見物を添えた。** 過去12件の事実誤認の再発防止のため、証拠が弱い空白主張は「空白かもしれない（要自己検証）」と明記して格下げしてある。

---

## 1. 結論サマリ（最初に全部書く）

### 1-1. 最重要発見：**overwatch.earth が既に32レイヤを実装している**

> 「overwatch.earth is a free, real-time 3D globe that overlays **32 live global data layers** on one interactive Earth — flights, ships, earthquakes, wildfires, satellites and more.」【確】
> <https://overwatch.earth/>（確認日 2026-08-29、本体はegress遮断・検索経由要約）

同サイトが既に載せているレイヤ（判明分）【確】：

| 群 | 実装済みレイヤ |
|---|---|
| 環境 | 地震（USGS＋EMSC）、山火事（NASA FIRMS）、雷（Blitzortung）、オーロラ（NOAA OVATION）、大気質（OpenAQ）、気象警報（NWS）、災害アラート、海洋ブイ、火山、火球 |
| 移動体 | 航空機、船舶、衛星＋ISS＋Starlink全機（CelesTrak TLE）、ロケット打上（Launch Library 2） |
| **デジタル/IT** | **海底ケーブル（TeleGeography）、インターネット障害（Cloudflare Radar＋IODA）、データセンター・IX（PeeringDB）、BGP経路事故（leak/hijack/outage, WorldIP.io）** |
| 好奇心 | **Wikipedia ライブ編集**、**数千台の公開ウェブカメラ**、**iNaturalist 観察**、NASA Deep Space Network アンテナ |

**依頼の【調査範囲】に挙げられた項目のうち、少なくとも 13項目が1サイトに実装済みである。**
つまり「IT色の強いレイヤを地球儀に載せる」という発想自体が、既に一人の先行者に丸ごと取られている。

さらに同種の集約グローブがもう1つある：
- **God's Eye View**（bilawalsidhu/gods-eye-view）「a photorealistic 3D globe with live aircraft, ships, satellites, earthquakes, traffic, and public cameras、**open source**」【確】<https://github.com/bilawalsidhu/gods-eye-view>
- **World Monitor**「conflicts, shipping chokepoints, military flights, markets and cyber on one free live world map, with AI analysis」【確】<https://www.worldmonitor.app/>

### 1-2. 構造的な結論：**「ポインタ型グローブ」は2026年に飽和産業である**

理由は明快で、**参入コストがゼロだから**である。ストレージも帯域も要らない、APIは無料、globe.gl は MIT、Vercel/Cloudflare Pages は無料枠。**参入障壁がゼロということは、既に全員が入っているということ**であり、実際そうなっていた。

本調査で「単一データ源 × 世界地図」の組合せを 20カテゴリ以上照会したが、**空いていたのは 2〜3件だけ**である。

### 1-3. 楽観を禁じるための一行

**「◯◯を世界地図にマッピングする」で思いつく◯◯は、ほぼ全て既にある。**
lucent.earth が成立したのは「安く作れたから」ではなく「2024〜25年にIRL配信という新カテゴリが立ち上がった瞬間に居たから」である。**構造（ポインタ型）は真似できるが、タイミングは真似できない。**

---

## 2. 候補一覧表（63件）

### 凡例
- **無料枠**：確認できた実数のみ記載。数値がない場合は「実数未確認」と明記
- **第三者表示**：自分のサイトで画像/映像/音声を見せてよいか（規約上）
- **母数**：`世界の関心層の桁 / ゼロフォロワーのソロが1年目に現実的に到達しうる月間UUの桁`（楽観禁止）
- **IT度**：★〜★★★（依頼主のIT嗜好への適合度）

---

### 2-A. 映像・音声（8件）

| # | ソース | 無料枠（実数） | 認証 | 第三者表示の可否 | 位置粒度・件数 | 既存競合 | 母数 | IT度 |
|---|---|---|---|---|---|---|---|---|
| 1 | **YouTube Data API v3**<br><https://developers.google.com/youtube/v3> | **10,000 units/日**。`search.list` は **1回100 units → 実質1日100検索**【確】。read=1, write=50 | OAuth/APIキー | **公式 iframe 埋込のみ許諾**。動画ファイル取得・別プレイヤー再生は不可 | 配信者の自己申告位置。位置は API から直接は取れず、説明文/タイトル解析が必要【推】 | **lucent.earth**、**StreamsCharts IRL map**（<https://streamscharts.com/tools/irl-map>）【確】 | 10^6 / 10^3 | ★★ |
| 2 | **Twitch Helix API**<br><https://dev.twitch.tv/docs/api/guide> | **App token で 800 points/分**（1req=1point が既定）。`Get Streams` は1回最大100件【確】 | OAuth必須（無料） | Twitch Embed は**親ドメイン申告必須**。埋込自体は許諾 | 同上（位置は自己申告） | 同上 | 10^6 / 10^3 | ★★ |
| 3 | **Windy Webcams API**<br><https://api.windy.com/webcams/> | **Trial 500 req/日**【単】。**画像URLのトークンが10分で失効**、無料枠は**低解像度のみ**【単】 | APIキー | 規約原文未確認【未】（egress遮断） | 緯度経度あり。数万台規模 | **Windy本体**、LiveCamsMap、camera-map.com(JP, 7,500台超)、ARGOS ATLAS(177,700台)、TrafficVision.live(155,000台)、OpenCCTV(99,910台)、EarthCam、webcamtaxi、LiveCamAtlas、Webcamera24、OpenWebcamDB、Tomarigi(JP・昼夜グローブ)、PicLive(JP)、LiveAtlas(JP)、miru-lab(JP)【確】 | 10^7 / 10^3 | ★ |
| 4 | **IPTV-org**<br><https://github.com/iptv-org/iptv> / api リポジトリ | **完全無料・無制限**（GitHub Pages の静的JSON）【確】 | 不要 | **Unlicense（パブリックドメイン）**。ただし「リポジトリは動画を保持しない、公開ストリームURLへのユーザ投稿リンクのみ」＝**リンク先の合法性は保証されない**【確】 | 国コード。数万チャンネル | **TVAtlas（3Dグローブ実装済み）**、IPTV World（グローブ実装済み）、TV Garden、Tvivu（11,000ch/178カ国）、globetv.app、tvglobe.live、worldtvchannels【確】 | 10^6 / 10^3 | ★★ |
| 5 | **Radio Browser API**<br><https://all.api.radio-browser.info/> | **無料・認証不要**。「webservice can be used freely but without guarantee to work」【確】。**具体的レート上限の明文は未確認【未】** | 不要 | ストリームURLへのリンク。局側の許諾は各局次第 | 国・都市・座標。**25,603局（うち767 broken）〜45,000局**（ミラーで差）【単】 | **Radio Garden**（決定版）、**Radiocast（7,000局グローブ）**、worldradiomap.com、radio-map.com、free-map.org Global Local Radio Map、Drive&Listen【確】 | 10^6 / 10^3 | ★★ |
| 6 | **各国DOT交通カメラ**（511系）<br>例：<https://hub.arcgis.com/maps/GEMA-SOC::gdot-live-traffic-cameras> | 機関ごと。多くは無料・無認証 | 機関ごと | **機関ごとにバラバラ**。TrafficLandが「50以上のDOTと**契約**して再配信」を事業にしている＝**契約が要る領域である証拠**【確】 | 緯度経度。世界で10万台超 | ARGOS ATLAS(177,700)、TrafficVision.live(155,000/130カ国)、OpenCCTV(99,910)、TrafficLand(18,000/200都市)、Vizzion(100,000/40カ国・商用)【確】 | 10^6 / 10^3 | ★★ |
| 7 | **LiveATC.net**<br><https://www.liveatc.net/map/feedmap.php> | 無料聴取。**API/再配信の規約は未確認【未】** | 不要（聴取） | **【未】。埋込・再配信の可否は要原文確認。ボランティア受信機由来のため制約が強いと推定【推】** | 空港単位。数百空港【確】 | LiveATC本体のカバレッジマップ、FR24のATC付きライブ配信【確】 | 10^5 / 10^2 | ★★ |
| 8 | **Broadcastify**<br><https://www.broadcastify.com/listen/> | **7,340フィード**を無料聴取【確】。API は有料（Premium） | 一部要 | 商用API契約前提【推】 | 郡・都市単位（主に米国） | Broadcastify本体 | 10^5 / 10^2 | ★★ |

---

### 2-B. 移動体（7件）

| # | ソース | 無料枠（実数） | 認証 | 第三者表示 | 粒度・件数 | 既存競合 | 母数 | IT度 |
|---|---|---|---|---|---|---|---|---|
| 9 | **OpenSky Network**<br><https://opensky-network.org/> | 匿名/登録でクレジット制。**具体値は本調査で未確認【未】**（docs が egress遮断）。研究用途は無料 | 任意（登録で枠増） | 研究・非商用が原則【推】。**商用は要問合せ【単】** | 緯度経度・秒単位。全世界の ADS-B | FlightRadar24、FlightAware、AirNav Radar、adsbexchange【確】 | 10^7 / 10^3 | ★★★ |
| 10 | **adsb.lol / airplanes.live / adsb.fi**<br><https://api.adsb.lol/docs> | **キー不要・無料**。「rate limits are dynamic based on the environment load」、将来はフィーダー限定のキー制に移行予定【確】 | 現状不要 | **ODbL ライセンスの open data**【確】＝再配布可（同一ライセンス継承） | 緯度経度・秒単位 | 上記＋globe.airplanes.live（tar1090）、ADSB IQ【確】 | 10^7 / 10^3 | ★★★ |
| 11 | **AISStream.io**<br><https://aisstream.io/> | **無料**。**IP あたり3接続／アカウントあたり3購読**。**2026年9月から非圧縮接続に帯域制限**、超過分はドロップ【確】 | 無料キー要 | **ブラウザからの直接接続は禁止**。「自分のサーバから接続し、必要な情報だけをクライアントにプロキシせよ」【確】 | 緯度経度。全世界のAIS | **MarineTraffic**、VesselFinder、ShipFinder、Global Fishing Watch【確】 | 10^6 / 10^3 | ★★ |
| 12 | **AISHub**<br><https://www.aishub.net/> | **無料だが「自分でAIS受信機を建てて提供する」ことが条件**【推・要確認【未】】 | 要 | 【未】 | 同上 | 同上 | 10^6 / 10^2 | ★★ |
| 13 | **GTFS-Realtime（Mobility Database 経由）**<br><https://mobilitydatabase.org/> | 「**6,000+ feeds、99カ国以上**、everyone has free access」＋API提供【確】 | 一部の事業者はキー要 | 事業者ごとにライセンス（多くは open） | 車両単位の緯度経度 | **Catenary Maps**（Rust/Svelteのグローバル実装）、**TRAVIC**（260都市超）、**Traze**（全世界）、Transitland【確】 | 10^6 / 10^3 | ★★ |
| 14 | **GBFS（バイクシェア）**<br><https://github.com/MobilityData/gbfs/blob/master/systems.csv> | **完全無料**。systems.csv は **1,536行（≒1,535システム）**（GitHub上で実測、2026-08-29）【確】。「920+ systems in 46 countries」【単】 | 不要（一部要） | 「This catalog is public data that cannot be owned or sold by anyone」【確】 | ステーション/車両の緯度経度 | CityBikes、各都市のバイクシェアマップ【推】 | 10^5 / 10^2 | ★ |
| 15 | **Launch Library 2（The Space Devs）**<br><https://ll.thespacedevs.com/2.2.0/> | **キー不要・無料。匿名は約15 req/時/IP**【確】。キー登録で増枠 | 任意 | 「public, documented, key-less API intended for third-party use」【確】 | 射場の緯度経度。**今後600件超＋過去7,500件超**【確】 | overwatch.earth（実装済）、Space Launch Now、NextSpaceflight【確】 | 10^5 / 10^2 | ★★ |

---

### 2-C. 自然・環境（10件）

| # | ソース | 無料枠 | 認証 | 第三者表示 | 粒度・件数 | 既存競合 | 母数 | IT度 |
|---|---|---|---|---|---|---|---|---|
| 16 | **NASA FIRMS**<br><https://firms.modaps.eosdis.nasa.gov/api/area/> | **MAP_KEY で 5,000 transactions / 10分**【確】 | 無料キー | 米政府データ＝実質パブリックドメイン【推】 | 375m〜1km の検知点 | **FIRMS本体のFire Map**、Zoom Earth、Watch Duty、overwatch.earth【確】 | 10^6 / 10^3 | ★ |
| 17 | **USGS Earthquake GeoJSON**<br><https://earthquake.usgs.gov/earthquakes/feed/> | **無料・キー不要**【推・広く知られた事実】 | 不要 | 米政府データ | 震源の緯度経度・深さ | **USGS本体の地図**、EMSC、overwatch.earth、無数のクローン【確】 | 10^7 / 10^3 | ★ |
| 18 | **Blitzortung（雷）**<br><https://www.blitzortung.org/> | **公開APIは存在しない**。「there is no Blitzortung API for external implementation」【確】。生データはプロジェクト参加者（受信機提供者）のみ | 参加者限定 | **商用利用は明確に禁止**（「Commercial use of data from Blitzortung.org is prohibited, even by the users that send data」）【確】。CC-BY-SA 4.0 は**非商用プロジェクトに限る**【確】 | 落雷点の緯度経度 | Blitzortung本体、LightningMaps.org、Windy、overwatch.earth【確】 | 10^6 / 10^2 | ★ |
| 19 | **OpenAQ**<br><https://docs.openaq.org/> | **無料キー必須**。「very generous rate limit」だが**数値は明文化されていない**【確】。超過で429 | 無料キー | 規約あり（要原文確認【未】） | 観測局の緯度経度 | IQAir、WAQI/aqicn、PurpleAir、overwatch.earth【確】 | 10^6 / 10^3 | ★ |
| 20 | **NOAA SWPC（オーロラ）/ NWS Alerts**<br><https://services.swpc.noaa.gov/> | 無料・キー不要【推】 | 不要 | 米政府データ | グリッド／警報ポリゴン | SpaceWeatherLive、Aurora Forecast各種、overwatch.earth【確】 | 10^6 / 10^2 | ★ |
| 21 | **Smithsonian GVP（火山）**<br><https://volcano.si.edu/> | 無料 | 不要 | 学術利用中心【推】 | 火山の緯度経度。約1,300火山【推】 | GVP本体、overwatch.earth【確】 | 10^5 / 10^2 | ★ |
| 22 | **NOAA NDBC ブイ / CO-OPS 潮汐**<br><https://www.ndbc.noaa.gov/> | 無料・キー不要【推】 | 不要 | 米政府データ | ブイの緯度経度 | NDBC本体、overwatch.earth（ocean buoys実装済）【確】 | 10^5 / 10^2 | ★ |
| 23 | **Safecast（放射線）**<br><https://api.safecast.org/> | **無料・サインアップ不要**。S3バルクエクスポート＋SNSトピックあり【確】 | 不要 | **全データ CC0（パブリックドメイン）**＝最強の許諾【確】 | 測定点の緯度経度。**1.5億件超**【確】 | **Safecast本体のtilemap**（<https://safecast.org/tilemap>）【確】 | 10^4 / 10^2 | ★ |
| 24 | **Sensor.Community（旧 Luftdaten）**<br><https://data.sensor.community/static/v1/data.json> | **無料**。直近5分の全センサ値を1本のJSONで配布。日次CSVアーカイブあり【確】 | 不要 | オープンデータ【推】 | センサの緯度経度。数千〜万台 | **maps.sensor.community**（本体）【確】 | 10^4 / 10^2 | ★★ |
| 25 | **Raspberry Shake（市民地震計）**<br><https://data.raspberryshake.org/fdsnws/> | **FDSN Web Service で無料**。ただし**リアルタイムではなくT-30分以降**【確】 | 不要 | 学術ライセンス【推】 | 観測点の緯度経度。**70カ国2,500局超**【確】 | **stationview.raspberryshake.org**（本体）【確】 | 10^4 / 10^2 | ★★ |

---

### 2-D. インフラ・IT（16件）★依頼主の嗜好に最も近い群

| # | ソース | 無料枠（実数） | 認証 | 第三者表示 | 粒度・件数 | 既存競合 | 母数 | IT度 |
|---|---|---|---|---|---|---|---|---|
| 26 | **Cloudflare Radar API**<br><https://developers.cloudflare.com/radar/> | **無料**。Custom Token（Account>Radar, Read）で発行【確】 | 無料トークン | **⚠ データは CC BY-NC 4.0＝非商用限定**【確】。**収益化する製品には使えない** | 国・AS単位（点ではない） | **Cloudflare Radar本体**、**overwatch.earth（実装済）**、World Monitor【確】 | 10^5 / 10^2 | ★★★ |
| 27 | **IODA（Georgia Tech）**<br><https://ioda.inetintel.cc.gatech.edu/> | **無料・公開API**。「the only public, open source platform that—through dashboards and APIs—provides near real-time...」【確】 | 【未】 | 学術・公益用途【推】 | 国・地域・AS単位 | **IODA本体のダッシュボード**、**overwatch.earth（実装済）**【確】 | 10^4 / 10^2 | ★★★ |
| 28 | **OpenCelliD**<br><https://opencellid.org/> | APIは「データを提供するアプリには無料」。**ユーザ報告で「1日50回で遮断」**【単】。**CSV一括DLはトークンあたり1日2回**【確】 | 無料キー | **CC BY-SA 4.0**＝表示可・継承義務あり【確】 | 基地局の緯度経度。**約4,000万セル**【単】 | OpenCelliD本体、CellMapper、Mozilla Location Service（終了）【推】 | 10^5 / 10^2 | ★★★ |
| 29 | **WiGLE**<br><https://api.wigle.net/> | **スライディングスケールの日次クエリ上限**。**新規アカウントは5件/日程度まで落ちる**【確】。人間らしい利用と実データ投稿で自動増加 | 要アカウント | **⚠ 収益化するなら商用ライセンス契約が必須**【確】 | AP の緯度経度。**17.3億ネットワーク（うち17.1億がGPS測位済）** (2025-11時点)【確】 | WiGLE本体のマップ | 10^5 / 10^2 | ★★★ |
| 30 | **TeleGeography Submarine Cable Map**<br><https://www.submarinecablemap.com/api/v3/cable/cable-geo.json> | **無料の JSON/GeoJSON API**（S3配信）【確】 | 不要 | **⚠ CC BY-NC-SA 3.0＝非商用・継承**【確】。収益化不可 | ケーブル線形＋陸揚局の点 | **submarinecablemap.com本体**、**Infrapedia**（600ケーブル/1,450陸揚局/10,000施設/300 IX）、**map.kmcd.dev**、overwatch.earth【確】 | 10^5 / 10^2 | ★★★ |
| 31 | **PeeringDB**<br><https://www.peeringdb.com/ (API: /api) | **無料**。2022年から**レート制限あり**、匿名は認証ユーザより低い枠【確】。数値は未確認【未】。**peeringdb-py でローカル全同期が公式推奨の回避策**【確】 | 任意（推奨） | ユーザ維持のDB。再利用は概ね可【推】 | IX・施設・ネットの住所/座標 | **PeeringDB本体**、**Infrapedia**、**overwatch.earth（実装済）**、map.kmcd.dev【確】 | 10^4 / 10^2 | ★★★ |
| 32 | **RIPE Atlas**<br><https://atlas.ripe.net/docs/apis/rest-api-reference/probes/> | **無料**。**API全体 300 q/s、計測API 150 q/s**、超過で429【確】。ステータスは5分キャッシュ【確】 | 任意 | 公開プローブ情報は公開【推】 | プローブの緯度経度。**約12,000プローブ＋800アンカー**（2022-04時点）【確】 | **RIPE Atlas本体のマップ**、RIPEstat【確】 | 10^4 / 10^2 | ★★★ |
| 33 | **Tor Onionoo**<br><https://metrics.torproject.org/onionoo.html> | **無料・キー不要**【確】。明示的レート上限は未確認【未】 | 不要 | Tor Project の公開メトリクス | リレーの国・座標（GeoIP） | **Tor Metrics本体**、Relay Radar（metrics.nothingtohide.nl）、metrics.1aeo.com、旧TorFlow【確】 | 10^4 / 10^2 | ★★★ |
| 34 | **Bitnodes（Bitcoinノード）**<br><https://bitnodes.io/api/ | **⚠ 匿名は同一IPから 1日10リクエストのみ**。20万req/日はPROプラン限定【確】。スナップショットは約10分毎 | 不要（10/日） | 【未】 | ノードの GeoIP 座標。数万ノード | **bitnodes.io/nodes/live-map**（本体）、newhedge、btcnodes.io【確】 | 10^5 / 10^2 | ★★★ |
| 35 | **M-Lab / Ookla Open Data**<br><https://registry.opendata.aws/speedtest-global-performance/> | **無料**。AWS Open Data Sponsorship、サブスク不要。M-Lab は BigQuery 無料【確】 | 不要 | オープンデータ。Ookla for Good【確】 | **z16タイル（赤道で約610m四方）**。2019〜2024年分【確】 | Ookla本体のマップ、各国ブロードバンドマップ【推】 | 10^4 / 10^2 | ★★★ |
| 36 | **OONI（検閲観測）**<br><https://api.ooni.io/ / <https://explorer.ooni.org/> | **無料の公開API**。JSONで生データDL可【確】 | 不要 | オープンデータ（公益）【推】 | 国・AS単位。**242カ国・28,000ネットワーク・20億計測超**【確】 | **OONI Explorer本体**、World Monitor【確】 | 10^4 / 10^2 | ★★★ |
| 37 | **The Things Network（LoRaWAN GW）**<br><https://ttnmapper.org/> | Packet Broker Mapper API（新API）【確】。数値未確認【未】 | 【未】 | 【未】 | ゲートウェイの緯度経度 | **ttnmapper.org**（本体のカバレッジマップ）【確】 | 10^3 / 10^2 | ★★★ |
| 38 | **Meshtastic 公開MQTT**<br>mqtt.meshtastic.org | 無料。ノードは「OK to MQTT」設定が必要【確】 | 不要 | ノード側のオプトイン前提【確】 | ノードの緯度経度。7日無通信で自動削除 | **meshmap.net**、**meshtastic.liamcottle.net**、map.meshnet.si、LoRaMeshDevices Hub、MeshCore/LetsMesh【確】＝**完全飽和** | 10^4 / 10^2 | ★★★ |
| 39 | **SondeHub（ラジオゾンデ）**<br><https://sondehub.org/> | **無料API（live＋historical）**【確】 | 【未】 | **CC BY-SA 2.0**【確】 | 気球の3D軌跡 | **sondehub.org本体**、amateur.sondehub.org、radiosondy.info【確】 | 10^3 / 10^2 | ★★★ |
| 40 | **aprs.fi API**<br><https://aprs.fi/page/api> | 無料キー（要アカウント）。**レート制限あり、数値非公開**。増枠は要相談【確】 | 要キー | **⚠ 規約が明確に禁止：「It may not be used to simply copy all of the data to another site providing exactly the same features as aprs.fi」**【確】＝**同種の地図サービスは規約違反** | 局の緯度経度 | aprs.fi本体、APRS.direct、PSKReporter【確】 | 10^4 / 10^2 | ★★★ |
| 41 | **公開SDR受信機ディレクトリ**（KiwiSDR/WebSDR/Web-888/OpenWebRX）<br><http://rx.linkfanel.net/> | 各ディレクトリは無料閲覧。**公式APIなし**【推】 | 不要 | 【未】 | 受信機の緯度経度。数百〜千台 | **rx-tx.info**（最も包括的）、**rx.linkfanel.net**、**rx.skywavelinux.com**、kiwisdr.com/public、websdr.org、ab9il.net【確】＝**飽和** | 10^4 / 10^2 | ★★★ |

---

### 2-E. 知識・文化（8件）

| # | ソース | 無料枠 | 認証 | 第三者表示 | 粒度・件数 | 既存競合 | 母数 | IT度 |
|---|---|---|---|---|---|---|---|---|
| 42 | **Wikipedia GeoData / Geosearch＋EventStreams**<br><https://www.mediawiki.org/wiki/API:Geosearch> | 無料。MediaWiki API の一般レート内 | 不要 | **CC BY-SA**（本文）。埋込・引用可 | 記事の緯度経度。数百万記事【推】 | **overwatch.earth/wikipedia**、**theplanetthinks.com（3Dグローブ）**、Wikipedia Recent Changes Map（LaPorte/Hashemi）、WikiMap、seealso.org【確】＝**完全飽和** | 10^5 / 10^2 | ★★ |
| 43 | **OpenStreetMap（Overpass＋minutely diffs）**<br><https://wiki.openstreetmap.org/wiki/Realtime_edit_viewers> | 無料（Overpassは公共サーバの負荷配慮必須） | 不要 | **ODbL**（継承義務） | ノード/ウェイの座標 | **Show Me The Way（osmlab）**、osm-live-map、osm-livechanges【確】＝飽和 | 10^4 / 10^2 | ★★ |
| 44 | **Mapillary**<br><https://www.mapillary.com/developer/api-documentation> | 「Viewing imagery and using APIs is free」【確】。**レート上限の数値は未確認【未】** | 無料トークン | **画像は CC BY-SA 4.0**＝表示可・帰属必須・継承。ただし**商用利用は ToS §12 の追加条項に服する**【確】 | 画像1枚ごとの緯度経度・方位 | Mapillary本体、KartaView、**MapiGuesser（Mapillary版GeoGuessr）**【確】 | 10^5 / 10^2 | ★★ |
| 45 | **Panoramax**<br><https://api.panoramax.xyz/> | 無料。**APIコードは MIT**【確】 | 不要（閲覧） | **画像は CC BY-SA 4.0**【確】 | 画像の緯度経度。**2025年時点でインスタンス6つ**（IGN/OSM France＋台湾・ウェールズ等）【確】＝**カバレッジは薄い** | Panoramax本体のビューア。**第三者製品はほぼ見当たらない【単】** | 10^3 / 10^2 | ★★ |
| 46 | **Met Museum Collection API**<br><https://metmuseum.github.io/> | **キー不要・登録不要。80 req/秒**【確】 | 不要 | **CC0 画像 406,000点**＝完全自由【確】 | `geographyType/city/state/country` フィールド。**総47万点超**【確】 | **ArtAtlas**（世界の美術品を地図化）、Tate Art Maps、SMK geolocation、GeoGallery、Mapping Paintings【確】 | 10^5 / 10^2 | ★ |
| 47 | **Rijksmuseum / Europeana / Smithsonian Open Access** | 無料キー（各館）。数値未確認【未】 | 無料キー | 館ごと（CC0が多い）【推】 | 制作地・所蔵地 | 同上 | 10^5 / 10^2 | ★ |
| 48 | **David Rumsey / Old Maps Online（IIIF）**<br><https://www.davidrumsey.com/view/georeferencer> | 無料閲覧。**147,000点超がオンライン**【確】 | 不要 | 【未】（Rumseyは概ね寛容だが要原文確認） | ジオリファレンス済み古地図の矩形 | **Old Maps Online本体**、NLS Georeferencer、British Library Georeferencer、Rumsey本体のGeoreferencer v4【確】＝飽和 | 10^4 / 10^2 | ★ |
| 49 | **radio aporee ::: maps（フィールド録音）**<br><https://aporee.org/maps/> | 無料閲覧。API有無は【未】 | 不要 | CC系【推】 | 録音地点の緯度経度。2006年〜 | **aporee本体が決定版**。earth.fm、各種soundmap【確】＝飽和 | 10^3 / 10^2 | ★ |

---

### 2-F. 生物・アウトドア（8件）

| # | ソース | 無料枠 | 認証 | 第三者表示 | 粒度・件数 | 既存競合 | 母数 | IT度 |
|---|---|---|---|---|---|---|---|---|
| 50 | **iNaturalist API**<br><https://api.inaturalist.org/v2/docs/> | **最大100 req/分（推奨60）、1日10,000未満**【確】 | 一部要 | **⚠ 写真の大半は CC-BY-NC**（商用不可）。さらに**「photos in the static.inaturalist.org domain do not have open licenses」**＝ホスト先ドメインでライセンスが判別できる【確】 | 観察の緯度経度（希少種は座標難読化） | **iNaturalist本体のマップ**、**overwatch.earth（実装済）**【確】 | 10^6 / 10^3 | ★ |
| 51 | **eBird API 2.0**<br><https://documenter.getpostman.com/view/664302/S1ENwy59> | **非商用に限り無料、約1,000 req/日**【単】 | 無料キー（eBirdアカウント） | eBird Data Access Terms に服する。**商用は別途**【確】 | 観察の緯度経度・ホットスポット | eBird本体、BirdWeather【確】 | 10^6 / 10^2 | ★ |
| 52 | **GBIF**<br><https://techdocs.gbif.org/en/openapi/ | **キー不要・無料**。**1クエリの hard limit は offset+limit=100,000**、超える場合は非同期ダウンロード【確】 | 不要 | **CC0 / CC BY / CC BY-NC の3種**（データセットごと）【確】 | 出現の緯度経度。**27億件超・1,000万種超**【確】 | GBIF本体のマップ、OBIS【確】 | 10^5 / 10^2 | ★ |
| 53 | **xeno-canto API v3**<br><https://xeno-canto.org/explore/api | **非商用は無制限（fair use）、1,000 req/時**【単】 | 無料キー（登録会員） | **全録音がCCライセンス**（一部オープン）【確】 | 録音の緯度経度・国・bbox。**100万件超・12,900種**【確】 | **BirdWeather（app.birdweather.com、2,000局の live map）**、**BirdNET LiveMap（Cornell）**、xeno-canto本体【確】 | 10^5 / 10^2 | ★ |
| 54 | **Movebank（動物追跡）**<br><https://www.movebank.org/> | 無料REST API【確】 | 要（多くの研究はアクセス許可制） | **⚠ データ所有者が権利を保持、study単位の許諾**【確】。公開データは一部 | 個体の軌跡 | Movebank本体、各研究のトラッカー、OCEARCH【推】 | 10^4 / 10^2 | ★ |
| 55 | **Global Fishing Watch API**<br><https://globalfishingwatch.org/our-apis/ | **自己登録でトークン発行、無料**【確】 | 要トークン | **⚠ 非商用に限る**（academic/NGO/free and open で public good に資するもの）【確】 | 船舶のAIS軌跡 | GFW本体のマップ【確】 | 10^5 / 10^2 | ★★ |
| 56 | **OpenBeta（クライミング）**<br><https://climb-api.openbeta.io/docs/> | **⚠ 無料アクセスは「OSIライセンスのオープンソースプロジェクト」に限定**【確】 | 要 | 登攀データは **CC Public Domain**（写真を除く）【確】 | ルートの緯度経度 | Mountain Project、theCrag、OpenBeta本体【確】 | 10^4 / 10^2 | ★ |
| 57 | **iOverlander**<br><https://ioverlander.com/> | KML/GPX/CSV エクスポートは**Unlimited プラン（有料）限定**【確】 | 要 | **⚠ 「All downloads are for personal use only, and may not be distributed by any means without written consent」＝再配布禁止**【確】 | POI の緯度経度 | iOverlander本体、Park4Night、Campendium【推】 | 10^5 / 10^2 | ★ |

---

### 2-G. 経済・生活・その他（6件）

| # | ソース | 無料枠 | 認証 | 第三者表示 | 粒度・件数 | 既存競合 | 母数 | IT度 |
|---|---|---|---|---|---|---|---|---|
| 58 | **Open Brewery DB**<br><https://www.openbrewerydb.org/ | **サインアップ・APIキー・レート制限なし**（fair-use のみ）【確】 | 不要 | オープン【推】 | 醸造所の緯度経度 | 各種ビールマップ【推】 | 10^4 / 10^2 | ★ |
| 59 | **Open Charge Map**<br><https://openchargemap.org/site/develop/api | **無料キー**。`maxresults>250` の呼び出しにレート制限【確】 | 無料キー | **データ提供元ごとにライセンスが異なる**【確】 | 充電器の緯度経度 | OCM本体、PlugShare、ABRP【推】 | 10^5 / 10^2 | ★ |
| 60 | **GDELT GEO 2.0 / DOC 2.0**<br><https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/ | **無料・キー不要**。15分ごと更新、直近7日を全65言語で【確】。30日超のクエリはサイズ上限に当たる【確】 | 不要 | 記事へのリンク＋600字スニペット。**元記事は各社の著作物**（リンクは可） | 地名メンション。**16億件超（2017-04以降）**【確】 | **GDELT本体の Live Visual News Map / Geographic News Search / Global Conflict Dashboard**、World News Pulse（humanhistories.org）【確】＝飽和 | 10^5 / 10^2 | ★★ |
| 61 | **Bandsintown API**<br>api@bandsintown.com | 無料。稼働率99.96%【確】。数値上限【未】 | 要（申請） | 【未】 | 会場の緯度経度 | **MapEvent（181,000イベント/180カ国）**、**GIGMAP**、**Concert Map**、Avanzert、Songkick、Bandsintown本体【確】＝飽和 | 10^5 / 10^2 | ★ |
| 62 | **Booking.com Demand API（アフィリエイト）**<br><https://developers.booking.com/demand> | アフィリエイト登録（要アクティブなサイト、審査1〜5営業日）【確・R13より】 | 要 | **★本調査群で唯一「imgタグでの画像利用」が明文で許諾されているセルフサーブAPI**：「ホテル画像のURLを保存し、HTMLのimgタグで使用すること。画像ファイル自体のダウンロードは許可されない」【確・R13】 | 宿の緯度経度 | 全ての旅行サイト（超飽和） | 10^7 / 10^2 | ★ |
| 63 | **Overture Maps / Foursquare OS Places**<br><https://docs.overturemaps.org/> / <https://docs.foursquare.com/data-products/docs/fsq-os-places-release-notes> | **無料一括DL**。Foursquare は**1億POI超**、月次更新、**Apache 2.0**【確】。Overture は **CDLA Permissive 2.0 / Apache 2.0、OSM由来なしでODbLの継承義務なし**【確】 | 不要 | **商用利用可・継承義務なし＝ライセンス的に最も自由なPOI基盤**【確】 | POI の緯度経度。1億件超 | Overture/Foursquare 本体、あらゆる地図製品 | 10^5 / 10^2 | ★★ |

**合計 63件。**（依頼の30件以上を満たす）

---

## 3. 「まだ空いている」候補トップ5（敵対的検索の証拠つき）

> **前置き（重要）**：82クエリの掃討の結果、**自信をもって「空白」と言えるのは実質2件**である。以下は確度順で、3位以下は「空白の可能性はあるが証拠が弱い＝自己検証必須」と明記する。**空白だと言い切らない**ことが、過去12件の誤認の再発を防ぐ唯一の方法である。

---

### 【1位】公開ライブカメラの「意味検索・条件検索」層（Vision-LLM インデックス）
**何か**：既存の何十万台という公開カメラ映像に対し、定期的に画像を1枚取ってVLMで説明文を生成し、**「いま雪が降っているカメラ」「いま人が多い広場」「いま夕焼けが綺麗な海岸」を自然文で横断検索できる**ようにする層。カメラ本体は他人がホストするのでポインタ型のまま。

**敵対的検索（実行クエリと結果）**
| クエリ | 発見物 | 判定 |
|---|---|---|
| `AI describes live webcams world map "what is happening" real time captions globe` | LiveCamsMap（地図のみ）、Webcamera24（地図のみ）、**World Monitor**（AI分析だが対象は船・機・市場・ケーブルであって**カメラ映像ではない**）、Google Maps の Ask Maps（別物） | **該当なし** |
| `semantic search live webcams vision AI index "find cameras where" snow beach crowded` | **TrafficVision.live**が「computer vision on live video cameras to draw bounding boxes around vehicles、real-time vehicle counts」【確】＝**車両カウントのみ。自然文検索ではない**。Vision-Environnement（地図＋天気）、Outdooractive（5万台、カテゴリ閲覧のみ）、OpenWebcamDB（ディレクトリ）、Insecam/CamHacker（違法性の高い露出カメラ、論外） | **自然文検索の実装は見当たらない【単】** |
| `世界地図 ライブカメラ ライブ配信 マッピング サービス 個人開発` | camera-map.com(7,500台)、LiveAtlas、PicLive、Tomarigi(昼夜グローブ)、miru-lab。**いずれも位置・カテゴリ検索のみ** | **日本語圏でも該当なし** |

**空白と言える根拠**：3方向のクエリで「映像内容を意味的に索引した横断検索」の実例が1件も出なかった。最も近いTrafficVision.liveも車両検知に限定される。

**しかし正直に言う致命的な弱点**：
1. **月$0では成立しない。** 1万台×1日6回×VLM推論 = 180万推論/月。安価な小型モデルでも数十〜数百ドル。**カメラ数を100〜1,000台に絞る**か、**1日1〜2回に落とす**設計が必須。
2. **カメラのリストをどこから得るか**が最大の関門。Windy Webcams API は無料枠 **500 req/日＋画像URLトークン10分失効＋低解像度**【単】で、大規模索引には向かない。ARGOS/TrafficVision/OpenCCTV のリストを取ることは彼らの規約違反になる可能性が高い【推】。**各国DOTの公式フィードから自分で集める**のが唯一クリーンな道で、これは労働集約。
3. 「面白いが1回見て終わり」になりやすい。

**IT度**：★★（映像＋推論パイプラインという意味では技術的には面白い）
**母数**：10^6 / **10^3**

---

### 【2位】世界の議会・自治体の公開配信マップ（Civic Streams World Map）
**何か**：世界中の国会・地方議会・市議会が YouTube 等で流している**公開審議映像**を、地図上にマッピングする。ポインタ型そのもの（YouTube埋込のみ）。

**敵対的検索（実行クエリと結果）**
| クエリ | 発見物 | 判定 |
|---|---|---|
| `city council meetings livestream map local government YouTube live civic map project` | **Civic Stream（civicstream.tv）**「live and on-demand video of city council meetings from across the **United States**、find your city, watch the meeting, and see the agenda — free, no signup」【確】。BoxCast（配信ベンダー）、各市の個別ページ | **米国限定の1社のみ。世界地図版は存在しない** |
| `parliament live stream world map watch legislatures globally directory site` | 欧州議会、豪、NZ、BBC Parliament の**個別ページ**。IPU（列国議会同盟）は**183カ国の議会リストを持つが地図も配信集約もない**【確】 | 検索結果の要約が明言：「**The search results show individual parliament streaming services rather than a single centralized world map directory for all legislatures globally**」 |

**空白と言える根拠**：Civic Stream が米国だけを埋めており、その外は誰も埋めていない。IPU が「国の一覧」を持っているのに「配信の一覧」が存在しないというギャップが明確。

**正直な弱点**：
1. **母数が小さい。** 一般人は議会中継を眺めない。想定は記者・シビックテック・研究者で **10^2〜10^3 UU/月**。
2. **YouTube Data API の1日100検索**という枠で世界の議会チャンネルを発見・追跡するのは苦しい。**Wikidata で立法府リストを引き、チャンネルIDを手作業で1回だけ紐付ける**設計にすれば枠は足りる【推】。
3. 収益化がほぼ不可能。**「作品」であって「事業」ではない。**

**IT度**：★（技術的には平凡）
**母数**：10^4 / **10^2**

---

### 【3位・要自己検証】求人の世界地図（Geo Job Map）
**敵対的検索**
| クエリ | 発見物 | 判定 |
|---|---|---|
| `job postings world map remote jobs interactive globe visualization site` | **WFH Map**（wfhmap.com、5カ国・733職種・3,500都市の**リモート比率の統計**であって求人票そのものではない）【確】、**Stapply AI Job Map**（map.stapply.ai、**AI企業の求人に限定**、Show HN）【確】、Jobboard Finder（求人サイトの数の地図） | **「世界の求人票を地図に載せる」製品は見当たらない** |
| `world map of job openings by city interactive global jobs map Adzuna visualization` | GitHub の `gitcordier/jobmap`（Adzuna＋Nominatim＋Leaflet の**個人の習作**）、Adzuna 公式は「APIでビジュアライゼーションを作れる」と言うだけ | **製品化された実例なし【単】** |

**空白の格下げ理由（正直に）**：
- **Adzuna 無料枠の実数が確定できない。** 「hundreds per day」「1,000 calls/月（≒33/日）」「250/日」と**情報源が3つとも食い違う**【単・矛盾】。<https://developer.adzuna.com/docs/terms_of_service>（確認日 2026-08-29、内容は未読【未】）
- Adzuna の `redirect_url` は**Adzuna経由のリダイレクト**で、descriptionは切り詰められる＝**「Adzunaに送客するためのAPI」であって「データを渡すAPI」ではない**【確】。**地図はできるが、その地図はAdzunaのアフィリエイト画面になる。**
- 地図が空白でも、**求人という事業は世界一激戦**。地図であることが優位性になる保証はゼロ。

---

### 【4位・要自己検証】「ライブ・ポインタ」の MCP サーバ（人間向けグローブではなく、AIエージェント向けの供給層）
**発想**：2026年は「地球儀を人に見せる」より「エージェントに live pointer を食わせる」ほうが空いている可能性。飛行機・船・カメラ・ラジオ・IPTV・地震・配信を**1本のMCPで引ける**サーバ。

**敵対的検索**
| クエリ | 発見物 | 判定 |
|---|---|---|
| `MCP server geospatial live data earth observation flights ships webcams model context protocol` | **Sparkgeo の「77+ Geospatial MCP Servers, Mapped and Categorized」**【確】<https://sparkgeo.com/blog/geospatial-mcp-servers-mapped-and-categorized/>、<https://github.com/sparkgeo/geo-mcp-servers>。内訳は **geocoding / routing / PostGIS / STAC・衛星画像 / QGIS・ArcGIS / weather / 商用ロケーション基盤**。NASA-MCP、Planet MCP、GeoSight MCP、Earthdata MCP など | **既に77件ある。ただし列挙された分類に「live pointer feeds（航空機・船舶・カメラ・配信）」は含まれていない【単】** |

**空白の格下げ理由（極めて重要）**：
**77件のリストを全部読めていない**（egress遮断で `sparkgeo.com` の本文まで到達できず、検索要約のみ）。**この空白主張は最も脆い。** 着手前に必ず `github.com/sparkgeo/geo-mcp-servers` を自分の目で全件読むこと（github.com は本セッションでも到達できた）。リポジトリ自身が「a shared index to check **before building a new server from scratch**」と述べている【確】＝重複を防ぐために存在する索引である。

---

### 【5位・空白ではない。だが構造的な参入障壁が"規約側"にある唯一の領域】交通カメラの「許諾済み」再配信
**発見**：TrafficLand は「**contractual redistribution agreements with over 50 Departments of Transportation**」を持ち「the largest **authorized** aggregator and distributor of live traffic video in the U.S.」を名乗る【確】。一方 ARGOS ATLAS（177,700台）、TrafficVision.live（155,000台）、OpenCCTV（99,910台）は**契約の有無を明示していない**【未】。

**含意**：この領域は「地図が空いている」のではなく「**許諾が空いている**」。ゼロ円で真似できるのは無許諾の集約であり、そこは既に3社が埋めた。**許諾を取りに行く経路（各国DOTに1件ずつ申請する）は誰も網羅していない可能性が高い**が、それはコード0行・交渉100件の仕事であり、ソロの1年目の戦い方ではない。

**なぜ5位に置くか**：**「ポインタ型は誰でも真似できる＝防御力ゼロ」という本調査最大の教訓を、最も具体的に示す事例だから。** 防御力は技術ではなく許諾から来る。R13で得た結論（「合法な写真表示は書面の許諾からしか来ない」）と完全に同型である。

---

## 4. 飽和していて手を出すべきでない領域（正直に）

**以下は全て、複数の確立プレイヤーが存在する。ソロが新規参入する理由はない。**

| 領域 | 既存プレイヤー（実在確認済み） | 判定 |
|---|---|---|
| **航空機追跡** | FlightRadar24、FlightAware、AirNav Radar、ADSBexchange、adsb.lol、airplanes.live、adsb.fi、ADSB IQ、overwatch.earth | **論外。世界最大級の地図製品カテゴリ** |
| **船舶追跡** | MarineTraffic、VesselFinder、ShipFinder、Global Fishing Watch、overwatch.earth | **論外** |
| **気象** | Windy、Ventusky、Zoom Earth、各国気象局 | **論外** |
| **地震** | USGS本体、EMSC、Raspberry Shake StationView、overwatch.earth、無数のクローン | **論外** |
| **雷** | Blitzortung、LightningMaps.org、Windy、overwatch.earth。**加えて商用利用が規約で明確に禁止**【確】 | **論外＋規約で不可** |
| **山火事** | NASA FIRMS本体、Zoom Earth、Watch Duty、overwatch.earth | **論外** |
| **大気質** | IQAir、WAQI/aqicn、PurpleAir、Sensor.Community本体、overwatch.earth | **論外** |
| **ライブカメラの地図** | ARGOS ATLAS(177,700)、TrafficVision.live(155,000)、OpenCCTV(99,910)、EarthCam、Windy、LiveCamsMap、Webcamera24、webcamtaxi、LiveCamAtlas、OpenWebcamDB、Outdooractive(50,000)、Vision-Environnement、**日本語圏でも camera-map.com / LiveAtlas / PicLive / Tomarigi / miru-lab**【確】 | **世界で最も飽和した地図カテゴリの一つ** |
| **ネットラジオのグローブ** | **Radio Garden**（決定版）、Radiocast(7,000局グローブ)、worldradiomap、radio-map.com、free-map.org、Drive&Listen | **論外。Radio Gardenが概念を所有している** |
| **IPTV / 世界のテレビ** | **TVAtlas（3Dグローブ）**、**IPTV World（グローブ）**、TV Garden、Tvivu(11,000ch)、globetv.app、tvglobe.live、worldtvchannels、GlobalFreeTV | **論外。iptv-orgを使ったグローブは既に複数実装済み** |
| **ライブ配信のグローブ** | **lucent.earth**、**StreamsCharts IRL map** | **論外（依頼主の参照元そのもの）** |
| **Wikipedia編集グローブ** | **theplanetthinks.com（3D）**、**overwatch.earth/wikipedia**、Wikipedia Recent Changes Map、WikiMap | **論外** |
| **OSM編集ライブ** | Show Me The Way (osmlab)、osm-live-map、osm-livechanges | **論外** |
| **公共交通のライブ車両** | **Catenary Maps**、**TRAVIC**(260都市)、**Traze**(全世界)、Transitland | **論外** |
| **Meshtastic / LoRaメッシュ** | meshmap.net、meshtastic.liamcottle.net、map.meshnet.si、LoRaMeshDevices Hub | **論外** |
| **公開SDR受信機** | rx-tx.info、rx.linkfanel.net、rx.skywavelinux.com、kiwisdr.com/public、websdr.org | **論外** |
| **Torリレー / Bitcoinノード** | Tor Metrics、Relay Radar、metrics.1aeo.com／bitnodes.io live-map、newhedge、btcnodes.io | **論外。加えてBitnodesは匿名10req/日で実装不能**【確】 |
| **海底ケーブル・インターネット地図** | submarinecablemap.com、**Infrapedia**(600ケーブル/1,450陸揚局/10,000施設/300IX)、**map.kmcd.dev**、overwatch.earth | **論外＋CC BY-NC-SAで商用不可**【確】 |
| **クラウドリージョン/DC地図** | Alkira Interactive Cloud Map、**Infra Atlas**、Build5Nines、cloudregionsmap、Google Cloud Location Finder API | **論外** |
| **traceroute可視化** | traceroute-mapper、gsuite.tools、VisualRoute、traceroute-online.com、geotraceroute.com、ToolCheckers、yougetsignal | **論外（7製品を即座に確認）** |
| **サイバー攻撃マップ** | Kaspersky、cyberattackmap.net ほか多数 | **論外（かつ大半が演出であり実データですらない）** |
| **鳥の声・鳥の観察** | **BirdWeather（2,000局のlive map）**、**BirdNET LiveMap（Cornell）**、eBird本体、iNaturalist本体 | **論外** |
| **フィールド録音・サウンドマップ** | radio aporee（2006年〜の決定版）、earth.fm | **論外** |
| **コンサート・イベント** | **MapEvent(181,000件/180カ国)**、**GIGMAP**、Concert Map、Avanzert、Songkick、Bandsintown | **論外** |
| **ニュース（GDELT）** | GDELT本体の Live Visual News Map / Geographic News Search / Global Conflict Dashboard、World News Pulse | **論外（データ提供者自身が最良の地図を出している）** |
| **古地図・ジオリファレンス** | Old Maps Online、David Rumsey Georeferencer v4、NLS、British Library | **論外** |
| **美術品の地図** | ArtAtlas、Tate Art Maps、SMK、GeoGallery、Mapping Paintings | **論外** |
| **GeoGuessr系（オープン画像）** | **MapiGuesser（Mapillary）**、WorldGuessr、OpenGuessr、GeoGame、EarthGuessr、City Guesser、Globetrotter ほか12製品 | **論外** |
| **「32レイヤ全部載せ」の集約グローブ** | **overwatch.earth**、**God's Eye View（OSS）**、World Monitor | **論外。ここに向かうのは自殺行為** |

---

## 5. 規約上の地雷まとめ（着手前に必ず読むこと）

**「無料API」と「第三者表示していいデータ」はまったく別物である。** 本調査で確認できた明確な地雷：

| ソース | 地雷 | 影響 |
|---|---|---|
| **Cloudflare Radar** | データは **CC BY-NC 4.0**【確】 | **収益化した瞬間に違反。広告・サブスク不可** |
| **TeleGeography 海底ケーブル** | **CC BY-NC-SA 3.0**【確】 | 同上＋継承義務 |
| **Blitzortung（雷）** | **商用利用を明文で禁止**、公開APIなし【確】 | 使えない |
| **aprs.fi** | **「aprs.fiと同じ機能を提供する別サイトへの全データコピー」を明文で禁止**【確】 | 地図サービスそのものが規約違反になりうる |
| **WiGLE** | 収益化するなら**商用ライセンス契約が必須**。新規アカウントは**1日5クエリ**【確】 | 事実上使えない |
| **Bitnodes** | 匿名 **1日10リクエスト**【確】 | 実装不能 |
| **iNaturalist** | 写真の大半が **CC-BY-NC**、`static.inaturalist.org` の画像は**オープンライセンスではない**【確】 | 写真表示は種類を選別しないと侵害 |
| **Global Fishing Watch** | **非商用限定**【確】 | 収益化不可 |
| **OpenBeta** | 無料APIは**OSIライセンスのOSSプロジェクト限定**【確】 | クローズドな製品では使えない |
| **iOverlander** | **個人利用限定・再配布禁止**【確】 | 使えない |
| **Electricity Maps** | 無料枠は**1ゾーンのみ・非商用**【確】 | 世界地図は無料枠では作れない |
| **AISStream.io** | **ブラウザからの直接接続禁止**、自前サーバでプロキシせよ【確】 | 「サーバ0円」が崩れる（Cloudflare Workers等が必要） |
| **eBird** | 非商用に限り無料【単】 | 収益化不可 |
| **Mapillary / Panoramax / OpenCelliD / SondeHub** | **CC BY-SA（継承義務）**【確】 | 自作部分まで継承が及ぶ設計かを要検討 |
| **iptv-org** | Unlicense だが「**リンク先の合法性は保証しない**」【確】 | 権利者からの削除要求は自分に来る |
| **Windy Webcams** | 画像URLトークンが**10分で失効**、無料枠は**低解像度**、**500 req/日**【単】 | キャッシュ不可＝スケールしない |
| **Booking.com Demand API** | **★唯一「imgタグでの画像利用」が明文で許諾**【確・R13】 | **これが「正しい許諾の形」の唯一の見本** |

**逆に、ライセンス的に最も自由なのは：**
- **Safecast（CC0）**、**Met Museum（CC0画像406,000点）**、**Foursquare OS Places（Apache 2.0、1億POI）／Overture（CDLA Permissive 2.0）**、**adsb.lol（ODbL）**、**米政府データ（USGS/NOAA/NASA FIRMS）**

---

## 6. 実行した敵対的検索クエリ全リスト（82件・証拠）

英語60件・日本語1件・製品語彙とユーザー語彙を混在。以下は全て 2026-08-29 実行。

**競合掃討系（この調査の主目的）**
1. `lucent.earth live streams 3D globe map YouTube Twitch` → StreamsCharts IRL map を発見
2. `globe.gl 3D globe visualization project r/InternetIsBeautiful map`
3. `overwatch.earth globe visualizations list what data` → **32レイヤの集約グローブを発見（最重要）**
4. `"overwatch.earth" Reddit HackerNews launch 2025 2026` → ヒットせず（ゲームのOverwatchに埋没）
5. `overwatch.earth about 32 layers data sources credits BGP PeeringDB data centers` → 全レイヤの内訳を確認
6. `live TV channels world map IPTV globe watch television by country map project` → TVAtlas / IPTV World（両方グローブ）
7. `traffic cameras world map aggregator global DOT live traffic cam site` → ARGOS ATLAS / TrafficVision.live / OpenCCTV / TrafficLand / Vizzion
8. `field recordings sound map world radio aporee soundscape geotagged audio map project` → aporee
9. `job postings world map remote jobs interactive globe visualization site` → WFH Map / Stapply
10. `GitHub commits live world map realtime visualization open source contributions globe` → GitHub Globe / **God's Eye View**
11. `cloud regions map AWS Azure GCP datacenter world map interactive site` → Alkira / Infra Atlas ほか
12. `global public transit live vehicle map GTFS realtime buses trains worldwide one map` → Catenary / TRAVIC / Traze
13. `世界地図 ライブカメラ ライブ配信 マッピング サービス 個人開発` → camera-map.com / LiveAtlas / PicLive / Tomarigi / miru-lab
14. `virtual travel site random live webcam ambient sounds world explore "take me somewhere"` → WindowSwap / GlobeGenie / virtualvacation.us / LiveCamAtlas / EarthCamTV
15. `OpenStreetMap live edit map realtime visualization "osm" live changes globe` → Show Me The Way ほか
16. `Wikipedia live edits map visualization realtime wikipedia edits globe project` → theplanetthinks.com / overwatch.earth/wikipedia ほか
17. `Meshtastic node map MQTT public nodes worldwide map project` → meshmap.net ほか4件
18. `KiwiSDR public receivers map WebSDR listen worldwide sdr.hu successor` → rx-tx.info ほか5件
19. `BirdWeather live bird detections map BirdNET global station map` → **BirdWeather（2,000局）/ BirdNET LiveMap**
20. `bird song world map listen globe xeno-canto map project interactive`
21. `"concerts tonight" world map live music events globe interactive map site` → MapEvent / GIGMAP / Concert Map / Avanzert
22. `city council meetings livestream map local government YouTube live civic map project` → **Civic Stream（米国限定）**
23. `parliament live stream world map watch legislatures globally directory site` → **世界地図版なしを確認**
24. `AI describes live webcams world map "what is happening" real time captions globe` → **該当なし**
25. `semantic search live webcams vision AI index "find cameras where" snow beach crowded` → **該当なし（TrafficVisionは車両カウントのみ）**
26. `pick a city hear its radio see its webcam watch its TV combined local media map site` → worldradiomap / Drive&Listen
27. `internet infrastructure map visit cable landing stations data centers tourism Infrapedia telegeography alternative` → Infrapedia / map.kmcd.dev
28. `GDELT news world map live globe visualization project geotagged headlines` → GDELT本体の3製品 + World News Pulse
29. `MCP server geospatial live data earth observation flights ships webcams model context protocol` → **Sparkgeo 77+ MCPリスト**
30. `listen to the world map radio scanner LiveATC Broadcastify combined audio globe project` → Radio Garden / Radiocast / worldradiomap
31. `airport live webcam plane spotting map ADS-B LiveATC combined site globe` → FR24 / AirNav Radar Cameras / EarthLive24
32. `Show HN 2026 interactive globe live data map side project Hacker News launch` → Asciimap ほか
33. `map artworks by place depicted museum collections world map Europeana geolocated art project` → **ArtAtlas / Tate Art Maps / GeoGallery**
34. `world map of job openings by city interactive global jobs map Adzuna visualization` → GitHub習作のみ
35. `GeoGuessr alternative Mapillary Panoramax open street level imagery guessing game free` → **MapiGuesser** ほか12製品
36. `traceroute visualization world map show your packets route online tool 2026` → 7製品

**データ源の無料枠・規約確認系（46件）**
37. `Windy webcams API free tier requests per day pricing`
38. `radio-browser.info API free rate limit stations count`
39. `RIPE Atlas probes API public map number of probes rate limit`
40. `PeeringDB API free rate limit internet exchange points geolocation`
41. `bitnodes.io API bitcoin nodes map free geolocation snapshot`
42. `Tor Onionoo API relay details free rate limit relay count`
43. `Cloudflare Radar API free API token rate limit internet outages data`
44. `"Cloudflare Radar" API free to use API token requirements attribution terms of use data`
45. `OpenCelliD API free access token limit cell towers count download license`
46. `WiGLE API free daily query limit terms of service redistribution wifi networks count`
47. `TeleGeography submarine cable map open data GitHub license API`
48. `The Things Network gateway map API public gateways count TTN Mapper`
49. `aprs.fi API key free rate limit terms of use APRS stations`
50. `Raspberry Shake station map API free citizen seismograph FDSN web service`
51. `Sensor.Community API free open data sensors count map Luftdaten`
52. `adsb.lol airplanes.live adsb.fi free ADS-B API no key aircraft data terms`
53. `aisstream.io free AIS websocket API vessel positions limit terms`
54. `Mobility Database GTFS Realtime feeds count free API transitland catalog`
55. `GBFS systems.csv how many bikeshare systems worldwide 2026 open license`（＋GitHubで systems.csv = 1,536行を実測）
56. `Wikipedia geosearch API GeoData extension coordinates articles count EventStreams recent changes`
57. `YouTube Data API v3 quota 10000 units per day search cost 100 units live streams eventType`
58. `Twitch Helix API rate limit 800 points per minute free get streams`
59. `Mapillary API v4 rate limit free images license CC BY-SA terms of use third party display`
60. `iNaturalist API rate limit 100 requests per minute photo license CC third party display`
61. `eBird API 2.0 key free rate limit terms of use display data third party`
62. `GBIF API free no key rate limit occurrence records count license CC0 CC-BY`
63. `Met Museum Collection API free rate limit 80 requests per second CC0 images geography field`
64. `GDELT GEO 2.0 API free no key geotagged news events limit terms`
65. `IODA Georgia Tech internet outage detection API free public data`
66. `M-Lab Ookla open dataset speedtest tiles BigQuery free license AWS Open Data`
67. `Panoramax open street level imagery API license coverage 2026`
68. `Blitzortung.org terms of use data restrictions non-commercial API access lightning`
69. `Open Charge Map API free key rate limit POI count license`
70. `Launch Library 2 "The Space Devs" API free rate limit 15 requests per hour launches`
71. `Global Fishing Watch API free token vessel AIS terms non-commercial Movebank animal tracking API`
72. `NASA FIRMS API MAP_KEY transaction limit 5000 per 10 minutes OpenAQ API key rate limit`
73. `explore.org live cams embed policy YouTube embedded terms zoo aquarium livestream`
74. `Bandsintown API Songkick API deprecated new developer access 2026 events location`
75. `xeno-canto API bird sound recordings license CC geotagged count rate limit`
76. `Old Maps Online API David Rumsey IIIF georeferenced historical maps free access terms`
77. `Overture Maps places dataset Foursquare open source places 100 million POI license free download`
78. `Safecast API radiation measurements open data tilemap license CC0`
79. `OONI API measurements free open data internet censorship country probe explorer`
80. `Electricity Maps free API tier personal use limit carbon intensity zones 2026`
81. `Open Brewery DB API free rate limit iOverlander data export OpenBeta climbing API license`
82. `SondeHub radiosonde tracker map API amateur weather balloon live`

---

## 7. 総括 — 楽観を1つも残さないために

### 7-1. 潰れた前提
1. **「ポインタ型だから安い＝有利」は誤り。** 安いということは参入障壁がないということで、実際に全カテゴリが埋まっていた。**安さは競争優位ではなく、競争が起きる条件である。**
2. **「IT色の強いデータは競合が少ない」は誤り。** BGP・PeeringDB・海底ケーブル・Cloudflare Radar・IODA は **overwatch.earth が既に1サイトに実装済み**。むしろIT系は「作れる人＝作る人」なので最も早く埋まる。
3. **「無料APIなら何でも表示できる」は誤り。** Cloudflare Radar(BY-NC)、TeleGeography(BY-NC-SA)、Blitzortung(商用禁止)、GFW(非商用)、WiGLE(商用ライセンス要)、iNaturalist(BY-NC)、Electricity Maps(1ゾーン)——**IT系ほどNC条項が多い**という皮肉な傾向がある。
4. **「日本語圏なら空いている」も誤り。** ライブカメラだけで camera-map.com / LiveAtlas / PicLive / Tomarigi（昼夜グローブ！）/ miru-lab が既にある。

### 7-2. 生き残った空白（確度順）
| 順位 | 候補 | 確度 | 母数（ソロ1年目） |
|---|---|---|---|
| 1 | 公開ライブカメラの**意味検索層**（VLM索引） | **中**（3方向のクエリで該当なし） | 10^3 |
| 2 | **世界の議会・自治体の公開配信マップ** | **中**（Civic Streamが米国限定と確認） | 10^2 |
| 3 | 求人の世界地図 | **低**（Adzuna無料枠が3情報源で矛盾、かつ送客API） | 10^2 |
| 4 | live pointer の MCP サーバ | **低**（77件のリストを読めていない。要自己検証） | 10^2 |
| 5 | 交通カメラの**許諾済み**再配信 | 空白ではない（構造の教訓として掲載） | — |

### 7-3. 最も重要な設計上の示唆

**lucent.earth を模倣すべきは「ポインタ型アーキテクチャ」ではなく「まだカテゴリ名がない対象を最初に地図に載せたこと」である。**

本調査で唯一「規約が明示的に第三者表示を許諾していた」のは Booking.com Demand API（imgタグ利用の明文許諾）であり、唯一「無許諾では作れない」構造が残っていたのは交通カメラの authorized aggregation だった。**この2つが指しているのは同じ結論——ポインタ型で防御力を持てるのは、データの入手経路ではなく、表示の許諾を書面で持っていることである。**

### 7-4. 着手前に自分で必ず確認すべきこと（本調査で確認できなかった項目）
| # | 未確認事項 | 影響 | 確認方法 |
|---|---|---|---|
| 1 | **overwatch.earth の実物**（本セッションはegress遮断で本体未閲覧） | 全ての「空白」判定の前提 | ブラウザで <https://overwatch.earth/about> を開く（5分） |
| 2 | `github.com/sparkgeo/geo-mcp-servers` の**全77件** | 候補4位の生死 | リポジトリを全件読む（15分） |
| 3 | **Windy Webcams API の無料枠の一次ソース** | 候補1位の生死（500req/日・10分失効・低解像度） | <https://api.windy.com/webcams/pricing> を開く |
| 4 | **Adzuna 無料枠の実数**（3情報源が矛盾） | 候補3位の生死 | developer.adzuna.com で自分でキーを取り、429が出る回数を測る |
| 5 | **Radio Browser の実レート制限** | 明文がない | de1.api.radio-browser.info を実際に叩く |
| 6 | **LiveATC の再配信規約** | 音声系の可否 | liveatc.net の ToS 原文 |
| 7 | **OpenSky の無料クレジット実数** | 航空系（ただし飽和領域） | openskynetwork.github.io/opensky-api/rest.html |
| 8 | **PeeringDB の匿名レート実数** | IT系レイヤの実装可否 | docs.peeringdb.com |

---

## 8. 参照URL一覧（全て確認日 2026-08-29）

**競合・先行製品**
- overwatch.earth <https://overwatch.earth/> ／ <https://overwatch.earth/about>（本体はegress遮断・検索経由で内容確認）
- overwatch.earth 紹介記事 <https://tuxxin.com/blog/introducing-overwatch-earth-live-planet-globe>（遮断）
- God's Eye View <https://github.com/bilawalsidhu/gods-eye-view>
- World Monitor <https://www.worldmonitor.app/>
- Internet Infrastructure Map <https://map.kmcd.dev/> ／ Infrapedia <https://www.infrapedia.com/about-us>
- StreamsCharts IRL Map <https://streamscharts.com/tools/irl-map>
- TVAtlas <https://tvatlas.app/> ／ IPTV World <https://iptvworld.app/> ／ TV Garden <https://tvgarden.co/> ／ Tvivu <https://tvivu.com/country>
- ARGOS ATLAS <https://argosatlas.com/> ／ TrafficVision.live <https://trafficvision.live/> ／ OpenCCTV <https://opencctv.org/cameras/traffic> ／ TrafficLand <http://www.trafficland.com/> ／ Vizzion <https://www.vizzion.com/vizrt.html>
- LiveCamsMap <https://livecamsmap.com/> ／ Webcamera24 <https://webcamera24.com/map/> ／ OpenWebcamDB <https://openwebcamdb.com/> ／ webcamtaxi <https://www.webcamtaxi.com/en/>
- 日本語：ライブカメラ検索マップ <https://camera-map.com/> ／ LiveAtlas <https://live-atlas.com/> ／ PicLive <https://www.piclive.net/> ／ Tomarigi <https://tomarigi.me/world> ／ みるラボ <https://miru-lab.jp/contents/world-live-cam> ／ note まとめ <https://note.com/ohba_artlife/n/n52b9113d0378>
- Radio Garden <https://radio.garden/> ／ worldradiomap <https://worldradiomap.com/> ／ radio-map <https://www.radio-map.com/>
- The Planet Thinks <https://theplanetthinks.com/> ／ overwatch Wikipedia globe <https://overwatch.earth/wikipedia>
- Show Me The Way / OSM realtime viewers <https://wiki.openstreetmap.org/wiki/Realtime_edit_viewers> ／ <https://github.com/osmlab/osm-live-map>
- Catenary / TRAVIC / Traze（GTFS可視化） <https://old.gtfs.org/resources/visualizations/>
- meshmap.net <https://meshmap.net/> ／ <https://github.com/liamcottle/meshtastic-map>
- rx-tx.info <https://rx-tx.info/map-sdr-points> ／ <http://rx.linkfanel.net/> ／ <https://rx.skywavelinux.com/>
- bitnodes live map <https://bitnodes.io/nodes/live-map/>
- Tor Relay Radar <https://metrics.nothingtohide.nl/misc/all.html>
- BirdWeather <https://app.birdweather.com/> ／ BirdNET LiveMap <https://birdnet.cornell.edu/map>
- MapEvent <https://mapevent.world/concerts-tonight/> ／ GIGMAP <https://gigmap.global/> ／ Concert Map <https://www.concert-map.com/>
- Civic Stream <https://civicstream.tv/watch/>
- ArtAtlas <https://artatlas.it/> ／ Tate Art Maps <https://www.tate.org.uk/about-us/projects/art-maps>
- MapiGuesser 他 GeoGuessr代替 <https://googlemapsmania.blogspot.com/2024/04/four-free-alternatives-to-geoguessr.html>
- traceroute可視化 <https://stefansundin.github.io/traceroute-mapper/> ／ <https://geotraceroute.com/> ／ <https://visualroute.visualware.com/>
- WFH Map <https://wfhmap.com/> ／ Stapply Job Map <https://news.ycombinator.com/item?id=46037065>
- radio aporee <https://aporee.org/maps/>
- Sparkgeo Geospatial MCP list <https://sparkgeo.com/blog/geospatial-mcp-servers-mapped-and-categorized/> ／ <https://github.com/sparkgeo/geo-mcp-servers>

**データ源**
- YouTube Data API <https://developers.google.com/youtube/v3> ／ Twitch <https://dev.twitch.tv/docs/api/guide>
- Windy Webcams <https://api.windy.com/webcams/pricing>（遮断）
- iptv-org <https://github.com/iptv-org/iptv> ／ api <https://github.com/iptv-org/api>
- Radio Browser <https://all.api.radio-browser.info/>（遮断）
- adsb.lol <https://api.adsb.lol/docs> ／ <https://github.com/adsblol/api> ／ airplanes.live <https://airplanes.live/>
- OpenSky <https://openskynetwork.github.io/opensky-api/rest.html>（遮断）
- AISStream <https://aisstream.io/documentation>
- Mobility Database <https://mobilitydatabase.org/> ／ GBFS systems.csv <https://github.com/MobilityData/gbfs/blob/master/systems.csv>（**1,536行を実測**）
- Launch Library 2 <https://ll.thespacedevs.com/2.2.0/> ／ <https://thespacedevs.com/llapi>
- NASA FIRMS <https://firms.modaps.eosdis.nasa.gov/api/area/> ／ OpenAQ <https://docs.openaq.org/using-the-api/rate-limits>
- Blitzortung <https://www.blitzortung.org/> ／ LightningMaps About <https://www.lightningmaps.org/about>
- Safecast <https://safecast.org/data/> ／ <https://registry.opendata.aws/safecast/>
- Sensor.Community <https://github.com/opendata-stuttgart/meta/wiki/EN-APIs> ／ <https://maps.sensor.community/>
- Raspberry Shake FDSN <https://manual.raspberryshake.org/fdsn.html> ／ <https://stationview.raspberryshake.org/>
- Cloudflare Radar <https://developers.cloudflare.com/radar/> ／ <https://radar.cloudflare.com/about>
- IODA <https://ioda.inetintel.cc.gatech.edu/>
- OpenCelliD <https://opencellid.org/downloads.php> ／ wiki <https://wiki.opencellid.org/wiki/API>
- WiGLE <https://api.wigle.net/> ／ policy <https://wigle.net/policy.html> ／ stats <https://wigle.net/stats>
- Submarine Cable Map API <https://www.submarinecablemap.com/api/v3/cable/cable-geo.json> ／ ライセンス <https://www2.telegeography.com/license-geocoded-map-data>
- PeeringDB <https://www.peeringdb.com/> ／ docs <https://docs.peeringdb.com/faq/>
- RIPE Atlas <https://atlas.ripe.net/docs/apis/rest-api-reference/probes/> ／ best practices <https://atlas.ripe.net/docs/howtos/best-practices/>
- Onionoo <https://metrics.torproject.org/onionoo.html>
- Bitnodes API <https://bitnodes.io/api/>
- Ookla Open Data <https://registry.opendata.aws/speedtest-global-performance/> ／ <https://github.com/teamookla/ookla-open-data>
- OONI <https://ooni.org/data/> ／ <https://explorer.ooni.org/>
- TTN Mapper <https://ttnmapper.org/> ／ SondeHub <https://sondehub.org/>
- aprs.fi API <https://aprs.fi/page/api> ／ ToS <https://aprs.fi/page/tos>
- Wikipedia Geosearch <https://www.mediawiki.org/wiki/API:Geosearch> ／ GeoData <https://www.mediawiki.org/wiki/Extension:GeoData>
- Mapillary <https://www.mapillary.com/developer/api-documentation> ／ CC BY-SA <https://help.mapillary.com/hc/en-us/articles/115001770409-CC-BY-SA-license-for-open-data> ／ ToS <https://www.mapillary.com/terms>
- Panoramax <https://api.panoramax.xyz/>
- Met Museum <https://metmuseum.github.io/>
- David Rumsey Georeferencer <https://www.davidrumsey.com/view/georeferencer>
- iNaturalist API <https://api.inaturalist.org/v2/docs/> ／ recommended practices <https://www.inaturalist.org/pages/api+recommended+practices>（遮断）
- eBird API <https://documenter.getpostman.com/view/664302/S1ENwy59> ／ ToU <https://www.birds.cornell.edu/home/ebird-api-terms-of-use/>
- GBIF <https://techdocs.gbif.org/en/openapi/> ／ terms <https://www.gbif.org/terms>
- xeno-canto <https://xeno-canto.org/> ／ GBIF dataset <https://www.gbif.org/dataset/b1047888-ae52-4179-9dd5-5448ea342a24>
- Movebank <https://www.movebank.org/> ／ Global Fishing Watch <https://globalfishingwatch.org/our-apis/>
- OpenBeta <https://climb-api.openbeta.io/docs/> ／ <https://github.com/OpenBeta/climbing-data>
- iOverlander <https://ioverlander.com/faq>
- Open Brewery DB <https://www.openbrewerydb.org/faq> ／ Open Charge Map <https://openchargemap.org/site/develop/api>
- GDELT <https://blog.gdeltproject.org/gdelt-geo-2-0-api-debuts/> ／ <https://gdeltproject.org/data.html>
- Bandsintown status <https://status.bandsintown.com>
- Booking.com Demand API <https://developers.booking.com/demand> ／ アフィリエイト <https://www.booking.com/affiliate-program/v2/index.html>
- Overture <https://docs.overturemaps.org/guides/places/> ／ Foursquare OS Places <https://docs.foursquare.com/data-products/docs/fsq-os-places-release-notes>
- Electricity Maps Free Tier <https://www.electricitymaps.com/free-tier-api>
- Adzuna developer <https://developer.adzuna.com/> ／ ToS <https://developer.adzuna.com/docs/terms_of_service>
- LiveATC feed map <https://www.liveatc.net/map/feedmap.php> ／ Broadcastify <https://www.broadcastify.com/listen/>
- explore.org <https://explore.org/livecams>

---

**（本レポート終わり）**
