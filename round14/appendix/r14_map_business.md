# R14 / 「他人のデータを地図に載せる」サービスは、個人から事業に育つのか

調査日: 2026-08-29（本文中の全URLの確認日は 2026-08-29）
調査対象: 自前コンテンツを持たず、他者のデータ／ストリーム／センサーを地図にマッピングするサービスの実例

---

## 0. 調査方法とその限界（先に開示）

- 本調査は **WebSearch のみ**で実施した。実行環境のegressプロキシにより WebFetch が全ドメインでブロックされ、Wikipedia・企業公式サイト・Hacker News・Similarweb などへの**直接アクセスができなかった**。したがって多くの数値は検索エンジン経由の要約であり、一次ソースの原文照合は行えていない。
- 数値には以下のラベルを必ず付けた:
  - **【確認】** = 公的開示・当事者発表・複数の報道で一致するもの
  - **【報道】** = メディア1〜2本に依拠、原文未照合
  - **【第三者推定】** = getlatka / Tracxn / ZoomInfo / Growjo / Crunchbase / Semrush / Similarweb などの推定値。**誤差が大きく、しばしば桁を外す**
  - **【当方推測】** = 事実からの筆者の推論であり、確認された事実ではない
- 非公開企業の売上は原則不明である。「たぶん儲かっている」は書かず、根拠のレベルを明示した。

---

## 1. 実例マトリクス

| # | サービス | 立ち上げ規模 / 初期コスト | 最初のトラフィックの出所 | 収益モデル | 実際に食えているか | 堀（コンテンツを持たない構造で何を持ったか） | 現在 |
|---|---|---|---|---|---|---|---|
| 1 | **Flightradar24** (SE) | 2006年 個人2人の趣味。自宅屋根にADS-B受信機。初期コストは受信機実費 | **既存の航空券価格比較サイト**に載せた + 2010年アイスランド火山噴火でメディアが殺到（4/16に1日400万訪問） | フリーミアム(Silver/Gold/Business) + 広告 + B2Bデータ販売 | **明確にYes。** 2024年売上 SEK 418.8〜420M(約$41.4M)、+18%、利益率52%【報道】 | 世界最大のクラウドソースADS-B網 5万局超 + 履歴DB + 報道での引用ブランド | 存続・成長。2025年 Sprints Capitalに35%売却、EV SEK 4.1bn(約$500M)、創業者$175M受領・65%保持【報道】 |
| 2 | **MarineTraffic** (GR) | 2007年 エーゲ大学 Dimitris Lekkas准教授の**学術プロジェクト**。ボランティアAIS受信機 | 学術コミュニティ + 海事業界のプロ。B2Cバズ経由ではない | フリーミアム + 衛星AIS等の有料機能 + API/データ販売(B2B) | Yes。2021売上$10.7M【第三者推定】/ 2022売上€18.5M・従業員206人【第三者推定】 | AIS受信局網 + 履歴 + 海運業界の業務インフラとしての地位 | **2023年3月 Kplerが買収**（FleetMonと同時、金額非公開）。ブランドは存続 |
| 3 | **Windy.com** (CZ) | 2014年。創業者 **Ivo Lukačovič = Seznam.cz創業者、チェコの億万長者(資産約$1.3B)**。ソロ・無資金ではない | 創業者の資本・技術チーム・知名度。パラグライダー/カイト等のニッチから | **広告なし・Premiumサブスク一本**（$18.99→$25.99→$34.99/年と値上げ継続） | Yes、高収益。売上 CZK 128M(2022)→217M(2023,税引後益60M)→321.6M(2024,益82.4M)→405M(直近年,益72.3M)。従業員15→25→34人【チェコ報道・決算ベース】 | 気象モデルの統合・描画品質・サブスク基盤・ブランド。**データ自体は各国気象機関(=他人のもの)** | 存続。Meteoblue(CH)の過半数取得。Microsoftの買収提案を拒否と報道【報道・未確定】 |
| 4 | **Ventusky / InMeteo** (CZ) | 2015年 David Prantl。**彼は14歳(2006)で気象ポータル in-počasí を自作しチェコ最大級に育てていた**。兄弟ら少人数 | **既存ポータル in-počasí のオーディエンス** + 描画の美しさによる話題化 | Premiumサブスク（年$10〜20、Premium+あり）。**「進歩はサブスク販売のみで賄われている」と自称**。外部資金ゼロ | Yes（小規模）。年商$1M【第三者推定】。ventusky.com 18.34M訪問/月(2026年1月)【第三者推定】 | 描画品質・多言語・アプリ。データはDWD/NOAA(=他人のもの) | 存続 |
| 5 | **Numbeo** (RS) | 2009年 Mladen Adamović（元Google 2007-09）が個人で開始。現在も従業員3人 | 地道なSEO + メディア/論文からの引用蓄積（バズ由来の記録なし） | **広告 + APIサブスク販売** | Yes（小規模）。売上非公開。2.67M訪問/月【第三者推定】 | **他人のデータですらなく、ユーザーに作らせたデータ**。10年超の時系列 + 「生活費比較=Numbeo」の指名ポジション + API顧客 | 存続 |
| 6 | **PurpleAir** (US) | 2015年 Adrian Dybwad が自宅周辺の粉塵を測るために開始。最初は**80台を自作して無料配布** | 近所→地域コミュニティ→行政・研究機関 | **ハードウェア販売が主**（$139〜$299）+ APIポイント課金 | Yes。売上$4M・従業員8人【第三者推定】。5年で3万台超出荷【報道】 | **センサーを買った人がそのまま地図のノードになる**（ハード収益とネットワーク効果が一致）+ 2016年からの時系列 | 存続 |
| 7 | **iNaturalist** (US) | 2008年 UC Berkeley修士の最終課題（Ueda / Agrin / Kline）。**初日2日で16アカウント・33観察** | 大学 → CalAcademy(2014) → National Geographic(2017)という**機関の後ろ盾** | **寄付・助成金がほぼ全て**。2024年Form 990: 収入$4.71M(寄付94.2%)、支出$3.05M、資産$5.93M。累計調達$11.5M | 「食えている」が**商業ではなくフィランソロピー**。2023年7月に$10M助成で独立501(c)(3) | 2.5億観察超の一次生物多様性DB + 研究界での引用 + AI種同定モデル | 存続。月間約35万人が観察を記録 |
| 8 | **Flighty** (US) | 2019年 Ryan Jones（元Apple、以前に個人で Weather Line を運営）。現在2〜3人 | **18ヶ月のベータ(frequent flyer/パイロット) → ローンチ数日で App Store Editor's Choice**。広告出稿なし | サブスク（$5/週、$60/年、$300買切）。外部資金$0 | Yes、高収益。**月商約$500K（年$6M規模）**【第三者記事】 | データは航空データベンダーから**購入**（=コスト）。堀は**UX・通知の速さ（航空会社より早い）・ブランド・共有リンクの成長ループ** | 存続 |
| 9 | **MyRadar / ACME AtronOmatic** (US) | Andy Green、会社は1999年から。2012年アプリ公開。**最初の10年は政府提供データのみ** | アプリストア + 米国の悪天候イベント | 広告 + アプリ内課金 | 存続はしているが**DL数の割に薄い**。DL 1000万〜5000万（情報源で幅）、直近月 DL 7万・収益$4万【第三者推定】 | 米国の気象アプリとしての定着。近年は自前衛星(HORIS)まで作り「他人のデータ」から脱却しようとしている | 存続 |
| 10 | **Blitzortung / LightningMaps** (DE) | 2007年 Egon Wanke(大学教授)ら3名。**ボランティアが受信機を自費で購入・組立** | 無線・気象のホビイストコミュニティ | **収益なし。「私的プロジェクトで商業的利益はない。組織も契約も会費もない」。データの商業利用は禁止** | No（意図的に非商業） | **約1800局/83カ国の受信機網 + TOA測位アルゴリズム**。技術的堀は最強クラスだが換金を放棄 | 存続（非営利） |
| 11 | **OpenSky Network** (CH) | 2012年 armasuisse + カイザースラウテルン大 + オックスフォード大の研究プロジェクト。2015年に非営利association化 | 研究者・大学・armasuisse | 寄付・助成・研究協力 + 一部プレミアム【第三者記述、一次未確認】 | No（非営利として維持） | 受信機7000局超 + 全生データのアーカイブ + **150本超の査読論文という学術的正統性** | 存続（非営利） |
| 12 | **ADS-B Exchange** (US) | Dan Streufert が「フィルタしない」ADS-B集約として個人運営。コミュニティのフィーダーが支える | 「検閲されない飛行追跡」という**思想的ポジション**（ElonJet等の追跡で報道） | 買収前: 広告除去サブスク等。買収後: 商用API/データ製品 | 買収により換金は成立。ただし**堀が歩いて出て行った** | コミュニティのフィーダー網（=法的には運営者の資産だが、実効支配はコミュニティ側） | **2023年1月25日 JETNET（PE Silversmith Capital傘下）が買収**（金額非公開）。**フィーダーの15〜20%が離脱【Stanford推定・記事内引用】**。2週間で adsb.fi / ADSB.lol / ADSB One / TheAirTraffic が発生 → adsb.one+adsb.fi が **airplanes.live** に統合 |
| 13 | **earth.nullschool.net** (東京在住の個人) | 2013年末公開。**東京在住のソフトウェアエンジニア Cameron Beccario** が「HTML/CSS/JSを学ぶ個人的チャレンジ」として。OSS | 可視化の美しさによる自然拡散（教科書・論文・博物館展示・ドキュメンタリー・ニュースに引用） | **寄付のみ**（Ko-fi / Nullschool Technologies Inc., 従業員1） | **No。世界的知名度に達しても本人は「家族と仕事の合間の趣味」と明言** | 7年分の履歴アーカイブ + ブランド。だが換金導線がない | 存続（趣味） |
| 14 | **Zoom Earth** (UK) | Paul Neave（Neave Interactive Ltd）。前身は2005年の Flash Earth。個人〜極小規模 | 前身サイトからの継続 + ハリケーン/山火事イベント | 広告(AdSense) + Zoom Earth Pro サブスク。外部資金なし | 存続はする。**11.34M訪問/月(2025年8月)【第三者推定】でも小規模**。主要オーディエンスは**インド・米国・フィリピン = 低CPM地域**【第三者推定】 | 衛星画像の集約と描画。**データは全て他人のもの** | 存続 |
| 15 | **Radio Garden** (NL) | 2013-16年 Netherlands Institute for Sound and Vision + Transnational Radio Knowledge Platform + 欧州5大学の**研究プロジェクト**。設計は Jonathan Puckey (Studio Puckey)。**初期コストは公的研究資金(HERA)** | 2016年12月公開直後にメディアが一斉に取り上げ（NPR / Vice / Google Experiments掲載）。本人談「**これほどの成功に対する計画はなかった**」 | 広告 + アプリ内課金（広告除去）。**外部資金調達なし** | 小さい。DL 1000万+(Google Play表示)〜2900万【第三者推定】。**2025年5月頃から広告が常時・侵襲的になったというユーザー不満 = 収益化圧力の兆候**【ユーザーレビュー】 | 4万局超のラジオ局DBのキュレーション + ブランド | 存続（Radio Garden B.V.） |
| 16 | **Drive & Listen** (TR/DE) | 2020年4月 Erkam Şeker（個人エンジニア）。Heroku上の個人プロジェクト | パンデミックのタイミング + SNS拡散。**1500万UU超**。多数のクローンを生んだ | **実質なし**（Buy Me a Coffee） | No | なし（他人のドライブ動画 + 他人のラジオストリーム） | 存続（driveandlisten.app に移転、趣味） |
| 17 | **WindowSwap** (SG) | 2020年 シンガポール在住の夫婦（**両者とも広告代理店のクリエイティブディレクター**） | パンデミック + 「史上最もバイラルなサイトの一つ」。5M UU / 20M+ view / 110カ国12,000投稿(2021時点) | ブランドコラボ（Coca-Cola、Velux）、アーティストコラボ | 継続的な収益事業になった証拠は見つからず。**広告業界のポートフォリオとしての価値化** | ユーザー投稿の窓の映像（=クラウドソース）だが換金構造がない | サイトは存続 |
| 18 | **lucent.earth** | 2026年に話題化した「世界中のウェブカメラを3Dグローブに載せる」個人開発サイト | 2026年4月頃に教育系ブログ等で紹介【報道】 | **不明** | **不明** | **不明** | 存在は確認。**開発者名・収益化の有無・トラフィックは今回の環境では確認できず**（当該ドメインへの到達不可、HN/Redditスレも特定できず） |
| 19 | **Inside Airbnb** (US) | 2015年2月 Murray Cox（アーティスト/アクティビスト/技術者）が個人で開始。デザイナーの友人を巻き込み、**本人はパートタイムのコンサル収入で生活しながらボランティア運営** | 住宅危機という**政治的争点**があり、報道・都市政策の側から引かれた | 助成金には慎重（政治性が非営利の優先度と合わない）、ホテル業界の資金も拒否。**公開直後から研究者が「データに金を払う」と言ってきた** → ミッション整合的なデータ販売 | 小さいが持続。のち **Housing Justice Data Lab**（NY州非営利法人、501(c)(3)申請中）を設立 | 「Airbnbに批判的な独立データ」というポジション + 都市政策・報道での引用 + 長期の時系列 | 存続。2026年7月からサンパウロ / ボゴタ / ナイロビの公開ダッシュボードを追加 |
| 20 | **AirDNA**（対比） | 2014年、Airbnbホストが創業。最初からB2B | 業界向け直販 | **B2B SaaS**（短期賃貸の投資分析） | Yes。1.3M+ユーザー、1500万物件、12万マーケット。売上$8.3M【Crunchbase推定・未検証】 | 同じスクレイピングデータでも**顧客が不動産投資家＝意思決定に金がかかる人** | 2022年 PE の Alpine Investors が買収。2024年に Arrivalist と Uplisting を買収 |
| 21 | **Citymapper**（対比・失敗） | VC調達済み、ソロではない。公共交通のオープンデータ(=他人のデータ)を地図化 | ロンドン発、口コミで数百万MAU | 有料化を反復して失敗（Citymapper Pass、Citymapper Club $2.99/月） | **No。2021年 売上£5.1M / 損失£7.4M（2020年損失£6.3M）** | 経路探索の品質。だが**オープンデータ上の差別化は模倣可能** | **2023年3月 Via が$73.9Mで買収、「fire sale」と報道**。買収後は有料機能を無料化 |
| 22 | **TeleGeography 海底ケーブルマップ**（対比・別解） | 既存のリサーチ会社が運営 | 毎年の新版が定期的にバズる | **無料マップは集客資産**。マップのスポンサー枠販売 + 裏のDBを Transport Networks Research Service として有料 + JSON/GeoJSON APIの年間ライセンス | Yes（本体事業で回収） | **地図そのものを売らず、地図をリード獲得装置にする** | 存続 |
| 23 | **shipmap.org / Kiln**（対比・別解） | 2016年、可視化スタジオ Kiln（Robin Houston / Duncan Clark）+ UCLのデータ | Information is Beautiful Awards 金賞、SNSで大拡散 | 直接収益なし。**受注獲得のポートフォリオ**（Kilnは2012年から可視化コンサル） | 会社としてはYes（受託で回収） | 可視化技術の実証 | 存続 |
| 24 | **Nomad List / nomads.com**（参考） | 2014年 Pieter Levels がソロ。**公開スプレッドシートをTwitterで共有 → バイラル → 1ヶ月でMVP**。HNにも投稿 | **本人のTwitter + Hacker News**。build in public | 2016年に$9.99/月サブスク導入。2019年に$1M ARR超。$5.3M(2024)【第三者推定】/ 総ARR $3.1M(2025)【第三者推定】 | Yes | データは他人（Numbeo等）から。堀は**コミュニティとブランドと本人のフォロワー**（2023年35万→2025年60万） | 存続。**「フォロワーゼロからの反例」ではなく「フォロワーを作ることが事業の一部だった」例** |
| 25 | **Watch Duty**（参考・最新の成功例） | 2021年8月 John Mills。**自己資金$1Mを投入**し、シリコンバレーの知人エンジニアを動員 | 山火事という災害イベント。2025年1月のLA山火事で**App Store総合1位**、8Mユーザーに急伸 | 非営利。寄付$35万未満(2022) → $120万(2023) → $560万(2024) → 約$600万(2025) | 非営利として成立。ユーザー2000万人超 | スキャナー無線・カメラ・衛星・公式発表(=他人の情報)を**約300人のボランティア"reporter"が人力で検証** = 自動化できない品質 | 存続。CEOがTIME100(2025) |

---

## 2. 育った例の共通条件

実例を並べると、**5つの条件のうち最低2つを満たしたものだけが事業になっている**。

### 条件1: 地図が「データ取得装置」になっている（自分で網を持った）
- Flightradar24（5万局のADS-B網）、MarineTraffic（AIS局）、PurpleAir（センサー販売＝ハード収益とネットワークが一致）、Blitzortung / OpenSky（非営利だが技術的堀は最強）、iNaturalist（観察投稿）、Numbeo（価格投稿）。
- 対して、**他人のAPIを叩いて描画しているだけ**の層（Zoom Earth、earth.nullschool、Radio Garden、Drive & Listen、lucent.earth）は、この堀を一切持たない。
- 重要な非対称: **網を持つと、供給者が自分になるので規約リスクが消え、かつAPI販売の権利が生まれる。**

### 条件2: 履歴を貯めた（リアルタイムはコモディティ、過去は資産）
- FR24の有料プランの中核は履歴。MarineTrafficも履歴と分析。PurpleAirは2016年からの記録。iNaturalistは2.5億観察。Numbeoは十数年の時系列。earth.nullschoolでさえ7年分のアーカイブを持つ（換金していないだけ）。
- **リアルタイムだけの地図は翌日に価値ゼロ。課金ポイントはほぼ常に「過去」と「アラート」に発生する。**

### 条件3: 業務・プロが使った（B2Cのバズではなく、B2Bの請求書）
- MarineTraffic（海運）、FR24（航空会社・メディア・保険）、ADSBx→JETNET（ビジネスジェット市場分析）、AirDNA（不動産投資）、Numbeo（API顧客）、Inside Airbnb（研究者・自治体）。
- **B2Cフリーミアム単体で大きくなったのは FR24 / Windy / Ventusky / Flighty の4例のみ。そしてこの4例は全員、創業時点で「既存のオーディエンス」か「資本」か「プラットフォームの推薦」を持っていた。**

### 条件4: 初期トラフィックは「事件」「既存資産」「キュレーション」で来た。SNSの自力拡散でゼロから来た例はほぼない
| サービス | フォロワーゼロを埋めた要素 |
|---|---|
| Flightradar24 | **既存の航空券比較サイト** + アイスランド火山噴火（事件） |
| Ventusky | 創業者が9年運営していた**チェコ最大級の気象ポータル** |
| Windy | 創業者がチェコ有数の富豪・Seznam創業者（**資本と知名度**） |
| Flighty | 18ヶ月のベータ + **App Store Editor's Choice**（プラットフォームのキュレーション） |
| Watch Duty | **自己資金$1M** + 山火事（事件） |
| Nomad List | **本人のTwitter + Hacker News** |
| Radio Garden | **公的研究資金** + NPR/Vice等のメディア |
| Inside Airbnb | **住宅危機という政治的争点**（報道が引いた） |
| MarineTraffic | **大学という機関の後ろ盾** |
| iNaturalist | **大学 → CalAcademy → National Geographic** |
| PurpleAir | ご近所に**80台を無料配布**（物理的な種まき） |

→ **「フォロワーゼロ・広告予算ゼロ」から純粋に立ち上がった例は、今回の調査範囲では見つからなかった。**
唯一近いのが **Numbeo**（元Googleエンジニアが個人で開始、SEOと引用の蓄積）と **earth.nullschool**（可視化の質だけで世界的知名度）。ただし前者は10年以上かけて3人規模、後者は事業になっていない。

### 条件5: 課金対象が「見る」ではなく「知らせる・調べる・持ち出す」だった
- Flighty = 通知（航空会社より早く遅延を知らせる）
- FR24 Gold = 履歴 + アラート
- Windy / Ventusky Premium = 高解像度モデル・長期予報（=判断材料）
- PurpleAir = ハードウェア（物理）
- Numbeo = API（データの持ち出し）
- Inside Airbnb = データセット（研究・政策の材料）

**誰も「きれいな地図を見る権利」には払わない。「自分に関係する変化の通知」と「データの持ち出し」に払う。** これが実例から読める最も一貫した法則。

---

## 3. 消えた／趣味で終わった例の共通条件

1. **データ供給者との関係がない。** 自分では何も集めていないので、上流のAPI/ストリームが止まれば終わる。差別化も描画の美しさだけになる。（Zoom Earth、Drive & Listen、lucent.earth）
2. **見た瞬間に価値が完結する。** 滞在時間は長いが、再訪の理由がない。（WindowSwap、Drive & Listen、Radio Garden）
3. **ユーザーが「自分の対象」を持たない。** 自分の便・自分の家の空気・自分の街の火事、に相当するものがない → アラートが作れない → サブスクの理由が発生しない。
4. **オーディエンスが低CPM地域に偏る。** Zoom Earth の主要オーディエンスはインド・米国・フィリピン。**バナー広告のCPMは先進国の数分の一**であり、しかも地図はタイル配信の帯域コストがトラフィックに比例して増える。**地図系×広告は構造的に最悪の組み合わせ。**
5. **無料が既に十分すぎる。** Citymapper は全機能無料で数百万MAUを得たあとに有料化を試み、反発して失敗、買収後は再び無料化された。
6. **コミュニティが堀の場合、所有権と実効支配がズレている。** ADS-B Exchange は売却の瞬間にフィーダーの15〜20%が離脱し【Stanford推定】、2週間で4つの代替ネットワークが立った。**クラウドソース網は、法的には運営者の資産だが、実効的にはコミュニティの人質でもある。**

---

## 4. 過去判定「純粋な眺め見型はバズっても定着・収益が弱い」の再評価

### 結論: **判定は基本的に正しい。実例が強く裏づける。ただし3点の修正が要る。**

#### 4-1. 判定の正しさを支える実例

| 事例 | 到達したトラフィック | 実際の収益 |
|---|---|---|
| earth.nullschool.net | 教科書・論文・博物館展示・ドキュメンタリー・ニュースに引用される世界的知名度、13年間継続 | **寄付のみ、従業員1人、本人が「趣味」と明言** |
| Drive & Listen | 1500万UU超、多数のクローンを誘発 | **Buy Me a Coffee** |
| WindowSwap | 「史上最もバイラルなサイトの一つ」、5M UU / 20M view | ブランドコラボ止まり |
| Radio Garden | DL 1000万+〜2900万 | 広告 + 広告除去課金。**2025年に広告を侵襲的にせざるを得ないところまで来ている** |
| Zoom Earth | 1134万訪問/月 | 広告 + Pro。個人〜極小規模のまま |
| Citymapper | 数百万MAU、£50M超を調達 | **売上£5.1M / 損失£7.4M → $73.9Mでfire sale** |

これらは「収益が弱い」を超えて、**トラフィックと収益がほぼ無相関である**ことを示している。

#### 4-2. 修正1: 「眺め見型」と「監視型」を分けるべき
落ちるのは**眺め見型（見て終わり）**であって、「他人のデータを地図に載せる」構造そのものではない。
同じ構造でも、**ユーザーが特定のオブジェクトを継続的に追跡する**タイプは、通知が作れるのでサブスクが成立している:
- 自分の便 → **Flighty**（2〜3人で年$6M規模）
- 自分の街の火事 → **Watch Duty**（2000万ユーザー）
- 自分の船・航路 → **MarineTraffic**
- 自分の家の空気 → **PurpleAir**

**「旅行地図」も、「見る旅行地図」ではなく「自分の予定・自分のフライト・自分の物件を監視する道具」に変換できるなら、判定は変わりうる。**しかし過去ラウンドで棄却された形（純粋な探索・眺め見）のままなら、判定は維持で正しい。

#### 4-3. 修正2: 「バズっても定着しない」→「バズは定着の必要条件でも十分条件でもない」
FR24 の火山噴火、Watch Duty の山火事では、バズが実際に事業の起爆剤になった。差は**バズが来たときに受け皿があったか**である:
- FR24 は既に「受信機を提供して網に参加する」導線と有料アプリを持っていた
- Watch Duty は既に「地域を購読する」通知の構造を持っていた
- earth.nullschool / Drive & Listen は受け皿を作らなかった（作らないと選択した）

つまり因果は「眺め見だから収益が弱い」ではなく、**「見る以外にやることを用意していないから収益が弱い」**。
ただしソロが受け皿（通知基盤、課金、サポート）を作るコストは軽くないので、**実務上の結論（棄却）を変える必要はない**。

#### 4-4. 修正3（最も重要）: 「母数が大きいこと」を重視する方針は、実例に照らすと危険
- Zoom Earth: 1100万訪問/月 → 極小規模
- Radio Garden: 2900万DL → 広告を強化せざるを得ない
- MyRadar: DL数千万 → 直近月$4万【第三者推定】
- Flighty: 上記より桁で小さいユーザー数 → **年$6M規模**

**ARPUが3桁違う。** 「母数が大きいこと」に価値があるのは広告モデルを前提にした場合だけで、しかも**個人開発の広告モデルは（低CPM地域への偏り、地図のタイル配信コスト、AdSenseの単価）ほぼ確実に負ける**。
評価軸を「母数」から「**1人あたりいくら払う理由があるか**」に移すべき。これは実例が最も強く示している一点。

#### 4-5. 依頼主の3条件は、実例上ほぼ両立しない
- 「興味本位で見たくなる」＋「母数が大きい」= earth.nullschool / Zoom Earth / Radio Garden / Drive & Listen / lucent.earth のクラスタ。**このクラスタは全員、事業になっていない**（存続はする）。
- 「10人規模の事業」に到達したのは MarineTraffic / Numbeo / Flighty / Ventusky / PurpleAir。**このクラスタは全員、興味本位ではなく「用がある人」に売っている。**
- FR24 と MarineTraffic だけが両立している（無料の眺め見が入口、二階に業務データ）。だが**両者とも二階部分は「自分で集めたデータ」で成立している。他人のAPIを再描画しているだけでは二階が作れない**（規約上も、差別化上も）。

---

## 5. 収益化の現実的な選択肢の序列（ソロ・フォロワーゼロ・広告予算ゼロ）

期待値の高い順。根拠は全て上記の実例。

### 1位: 特定業界のプロ向けの「データ持ち出し」（API / CSV / 定期レポート）
- 根拠: **Numbeo（3人でAPI販売）**、**Inside Airbnb（公開直後から研究者が「金を払う」と言ってきた）**、MarineTraffic、AirDNA、TeleGeography。
- 個人でも成立する理由: **顧客が数十社でよい。フォロワーが要らない。営業がインバウンド**（データを公開していれば向こうから来る）。
- 成立条件:
  - 元データの利用規約で**再配布・二次利用が許されること**（ここが最大の落とし穴）
  - **正規化・名寄せ・時系列化に労力がかかること**（誰でも同じことができるならAPIは売れない）

### 2位: 「自分のオブジェクト」の監視 + 通知のサブスク
- 根拠: **Flighty（2〜3人で年$6M規模）**、FR24 Gold、Windy / Ventusky Premium。
- 成立条件: ユーザーが継続的に気にする**具体的な対象**（自分の便、船、物件、価格、規制、案件）が定義できること。
- 実際の単価レンジ: **年$10〜60**（Ventusky $10-20 / Windy $35 / Flighty $60）。ここが個人開発の現実的な価格帯。

### 3位: 履歴・アーカイブへのアクセス課金
- 根拠: FR24 の有料機能の中核が履歴。PurpleAir は2016年からの記録。Numbeo は十数年の時系列。
- ソロ向けの含意: **今日から溜め始めること自体に価値がある。後から遡れない。** ストレージは安い。1年後に「誰も持っていない1年分の履歴」という資産ができる。これはフォロワーゼロでも今日から実行できる唯一の堀構築。

### 4位: 地図を「名刺」にして、受注（受託・コンサル・可視化）で回収
- 根拠: **Kiln / shipmap.org**（可視化スタジオの代表作として受注に転換）、**TeleGeography**（無料マップ + スポンサー枠 + 有料リサーチ）、WindowSwap（広告業界のポートフォリオ化）。
- 個人にとって**最も速い現金化**。ただしバズの賞味期限内に問い合わせを受ける設計（連絡先・実績ページ・「この技術で受注します」の明示）が必須。

### 5位: ハードウェア／キット販売（ネットワークを買ってもらう）
- 根拠: **PurpleAir**（$139-299、売上$4M、8人）、FR24（受信機キット約7000台を配布）。
- 堀としては最強（買った人が離脱しない、ハード収益とネットワーク効果が一致）。
- ソロには在庫・物流・サポートが重い。**日本発だと技適・PSE等の規制コストが上乗せされる**（要別途確認）。

### 6位: 寄付
- 根拠: **earth.nullschool（世界的知名度で従業員1人）**、Drive & Listen（Buy Me a Coffee）、Blitzortung（そもそも受け取らない）。
- **明確に「食えない」。** 生活費の足しにならないと考えるべき。世界最高クラスの知名度に到達しても結果は変わらなかった。

### 7位（最下位）: ディスプレイ広告
- 根拠: Zoom Earth（1100万訪問/月でも小規模、低CPM地域偏重）、Radio Garden（2900万DLで広告を侵襲的にせざるを得ない）、MyRadar（DL数千万で直近月$4万【第三者推定】）。
- **「母数が大きい」戦略の実際の終着点がこれ。** 地図はタイル配信の帯域コストが収益に比例して増えるため、特に相性が悪い。

### 番外: 買収（EXIT）
- MarineTraffic → Kpler、ADSBx → JETNET、Citymapper → Via（fire sale $73.9M）、Windy（Microsoftの提案を拒否と報道）。
- **買われるのは「データ / ネットワーク / 業界での地位」であって、トラフィックではない。**
  Citymapper の数百万MAU は $73.9M（fire sale）にしかならず、MarineTraffic の AIS 網と206人の事業は Kpler の中核になった。

---

## 6. 最終的な問いへの回答（要約）

**Q1. 「他人のデータを地図に載せるだけ」のサービスは、個人から事業に育つのか。**
育つ。ただし**「載せるだけ」のまま育った例はゼロ**。育った全例が、途中で以下のいずれかに変質している:
(a) 自分でデータを集める網を持った（FR24、MarineTraffic、PurpleAir、Numbeo）
(b) 履歴を貯めて過去を売った（FR24、PurpleAir、Inside Airbnb）
(c) 特定業界のプロの業務に入り込んだ（MarineTraffic、AirDNA、Numbeo）
(d) 「見る」を「知らせる」に変えた（Flighty、Watch Duty）

**Q2. 消えた/趣味で終わった例の共通条件。**
データ供給者との関係がない／見た瞬間に価値が完結する／ユーザーに「自分の対象」がない／低CPM地域偏重／無料で十分すぎる／コミュニティの実効支配を握れていない。

**Q3. 過去判定は正しいか。**
**正しい。** earth.nullschool（世界的知名度・13年・従業員1）と Citymapper（数百万MAU・損失£7.4M・fire sale）という両極端の実例が、トラフィックと収益の無相関を実証している。
修正すべきは「母数が大きいこと」を評価軸に置く方針のほう。**母数ではなくARPUで評価すべき。**

**Q4. 収益化の序列。**
API/データ販売 > 監視・通知サブスク > 履歴課金 > 受注への転換 > ハード販売 >> 寄付 >>> 広告。

---

## 7. 事実と推測の区分（明示）

### 確認できた事実（複数ソース一致 or 公的開示）
- FR24 は2006年に個人2人の趣味として始まり、2010年の火山噴火が転機で、2025年にSprints Capitalへ35%売却（創業者$175M受領・65%保持）
- MarineTraffic は2007年エーゲ大学の学術プロジェクト発、2023年3月にKplerが買収
- Windy の創業者 Ivo Lukačovič は Seznam.cz 創業者でチェコの億万長者
- Ventusky の David Prantl は2006年（14歳）から気象ポータル in-počasí を運営していた
- ADS-B Exchange は2023年1月25日にJETNET（Silversmith Capital傘下）が買収し、コミュニティが反発、複数の代替ネットワークが2週間以内に発生、後にairplanes.liveへ統合
- Blitzortung はデータの商業利用を禁止し、組織・契約・会費が存在しない
- earth.nullschool は東京在住のCameron Beccarioによる個人プロジェクトで、収益は寄付のみ、法人の従業員は1
- Radio Garden は公的研究資金（HERA / Sound and Vision）で作られ、成功に対する事業計画がなかったと本人が述べている
- Citymapper は2021年に売上£5.1M・損失£7.4M、2023年にViaへ$73.9Mで売却
- iNaturalist の2024年Form 990: 収入$4.71M（寄付94.2%）、支出$3.05M
- Watch Duty は創業者が自己資金$1Mを投入、非営利、寄付は2022年$35万未満→2025年約$600万
- Inside Airbnb は公開直後から研究者からのデータ購入要請を受け、それを収益源にした
- PurpleAir は2015年に80台を自作・無料配布して始まり、ハードウェア販売（$139-299）が主収益

### 第三者推定であり、桁を疑うべき数値
- FR24 の従業員数（36人 vs 71人と情報源で不一致）
- MarineTraffic の売上（2021 $10.7M / 2022 €18.5M）と従業員206人
- Ventusky の年商$1M、Windy の「$3.5M ARR」（**チェコ報道の CZK 405M ≒ $18M と大きく矛盾。チェコ報道のほうを採るべき**）
- Zoom Earth / Ventusky / Numbeo のトラフィック数値（Semrush / Similarweb）
- Flighty の月商$500K（Starter Story等の記事ベース、本人の公式開示ではない）
- MyRadar のDL数（1000万 vs 5000万）と直近月収益$4万
- Nomad List の$5.3M / $3.1M
- AirDNA の$8.3M（Crunchbase推定、記事自体が「未検証」と明記）

### 当方の推測（事実ではない）
- Zoom Earth・Radio Garden・MyRadar の収益が「規模の割に薄い」という評価は、トラフィック規模と広告単価・オーディエンス地域から導いた推論である
- lucent.earth が「Radio Garden / Drive & Listen と同型の経路を辿る可能性が高い」は構造からの推測であり、根拠となる実データはない
- 「地図×広告は帯域コストがトラフィックに比例するため特に相性が悪い」は一般論からの推論であり、個別事例のP/Lで確認したものではない

---

## 8. 未解決・追加調査が要る点

1. **lucent.earth** — 開発者名、収益化の有無、トラフィック、HN/Redditでの反応。今回の実行環境ではドメイン到達不可のため未確認。**次回は別環境から lucent.earth 本体と HN Algolia を直接読むべき。**
2. FR24の初期アプリ価格・初期収益（2010〜2013）— 一次情報未取得。「個人が最初にいくら稼いだか」は依頼主にとって最も参考になる数字だが確認できていない。
3. Numbeo / Zoom Earth / Radio Garden の実売上 — 全て非公開。
4. ADS-B Exchange の買収額、およびフィーダー離脱率15-20%の一次ソース（記事内でStanfordの推定として引用されているだけ）。
5. MarineTraffic の買収額（非公開）。
6. 日本国内の同型サービス（例: 気象・不動産・交通の可視化）の事例は今回の調査対象外。**日本語圏の公的データ正規化という方向は Numbeo 型（少人数API事業）に構造が近く、別途調査の価値がある。**

---

## 9. ソース一覧（全て確認日 2026-08-29）

### Flightradar24
- https://en.wikipedia.org/wiki/Flightradar24 （検索経由の要約のみ、直接アクセス不可）
- https://www.flightradar24.com/about/
- https://www.flightradar24.com/blog/inside-flightradar24/flightradar24-now-has-over-50000-active-data-sharers-around-the-world/
- https://www.flightradar24.com/blog/marking-10-years-since-eyjafjallajokull/
- https://mexicobusiness.news/aerospace/news/flightradar24-sells-35-stake-us500-million
- https://www.mainsights.io/ma-news/sprints-capital-acquires-35-stake-in-swedish-aviation-data-firm-flightradar24-at-an-ev-of-sek-41bn-and-evebitda-of-15x
- https://app.dealroom.co/news/note/flightradar24-s-pe-deal-founders-story
- https://startupfounderstories.com/stories/mikael-robertsson-flightradar24-flight-tracking
- https://thefriendlyskies.net/article/guide-to-flightradar24/

### MarineTraffic
- https://en.wikipedia.org/wiki/MarineTraffic
- https://www.kpler.com/blog/kpler-acquires-marinetraffic-and-fleetmon-for-maritime-sector-expansion
- https://help.marinetraffic.com/hc/en-us/articles/360017663458-MarineTraffic-is-now-part-of-Kpler
- https://maritime-executive.com/article/kpler-buys-marinetraffic-and-fleetmon-consolidating-ais-tracking
- https://getlatka.com/companies/marinetraffic
- https://craft.co/marinetraffic/financials

### Windy.com
- https://en.wikipedia.org/wiki/Windy_(weather_service)
- https://www.lupa.cz/aktuality/lukacovicovo-windy-vytahlo-trzby-na-stovky-milionu-prioritou-je-kvalita-sluzeb-ne-zisk/
- https://cc.cz/windy-iva-lukacovice-dal-slape-aplikace-pro-pocasi-utrzila-ctvrt-miliardy-a-zdvojnasobila-zisk/
- https://cc.cz/z-50-na-400-milionu-za-pet-let-aplikace-na-pocasi-windy-iva-lukacovice-dal-roste-a-naramne-vydelava/
- https://www.e15.cz/byznys/majitel-seznamu-lukacovic-ma-dalsi-rostouci-byznys-windy-se-blizi-pul-miliarde-a-generuje-zisk-1433581
- https://www.forbes.com/sites/forbesinternational/2017/02/06/can-a-czech-millionaire-sell-wind-and-snow/
- https://community.windy.com/topic/37725/35-premium-subscription-price-hike
- https://getlatka.com/companies/windy.com

### Ventusky / InMeteo
- https://www.ventusky.com/about
- https://my.ventusky.com/premium/
- https://www.letemsvetemapplem.eu/en/2021/10/10/rozhovor-s-davidem-prantlem-pres-jehoz-aplikace-in-pocasi-a-ventusky-sleduji-pocasi-miliony-lidi-z-celeho-sveta/
- https://tracxn.com/d/companies/ventusky/__KW41VlzrofxEPwcIJIPY6z6jSPkHGy1zG4ZGf1fh0Lo
- https://www.similarweb.com/website/ventusky.com/

### Blitzortung / LightningMaps
- https://blitzortung.org/Documents/TOA_Blitzortung_RED.pdf
- https://www.lightningmaps.org/about?lang=en
- https://www.lightningmaps.org/notes
- https://en.wikipedia.org/wiki/Blitzortung

### Radio Garden
- https://en.wikipedia.org/wiki/Radio_Garden
- https://puckey.studio/projects/radio-garden
- https://www.npr.org/2016/12/18/506045527/jonathan-puckey-s-radio-garden-knows-no-borders
- https://www.vice.com/en/article/radio-garden-global-radio-jonathan-puckey-interview/
- https://experiments.withgoogle.com/radio-garden
- https://play.google.com/store/apps/details?id=com.jonathanpuckey.radiogarden
- https://tracxn.com/d/companies/radio-garden/__K_X3m64BdZ9BWQuuaAJsiiC49II8BX_QnrO5863hQyk

### Zoom Earth
- https://zoom.earth/legal/terms/
- https://neave-interactive.fandom.com/wiki/Zoom_Earth
- https://www.semrush.com/website/zoom.earth/overview/
- https://tracxn.com/d/companies/zoom-earth/__r_R5rIZ6F7ANliE9IewTb0GkkRby930Rzf2FtJ4KW9w

### earth.nullschool.net
- https://earth.nullschool.net/about
- https://nullschool.net/
- https://ko-fi.com/cambecc
- https://github.com/cambecc/earth
- https://bsky.app/profile/cambecc.bsky.social/post/3kg4nhtk7xe2p

### ADS-B Exchange / 代替ネットワーク
- https://www.jetnet.com/resources/press-releases/jetnet-acquires-ads-b-exchange
- https://www.rtl-sdr.com/ads-b-exchange-acquired-by-private-firm-jetnet/
- https://hackaday.com/2023/01/26/ads-b-exchange-sells-up-contributors-unhappy/
- https://www.forbes.com/sites/cyrusfarivar/2023/02/02/adsb-exchange-flight-tracking-elonjet/
- https://news.ycombinator.com/item?id=34520355
- https://airplanes.live/history-and-moving-forward/
- https://blog.jettip.net/in-the-wild-west-of-uncensored-flight-tracking-wholl-be-the-spiritual-sucessor-of-ads-b-exchange
- https://www.adsbexchange.com/products/enterprise-api/

### OpenSky Network
- https://opensky-network.org/about
- https://en.wikipedia.org/wiki/OpenSky_Network
- https://doi.org/10.1145/3765613.3797548 （OpenSky: How a Security Project Became Global Infrastructure, ACM WiSec 2026）
- https://www.mdpi.com/2504-3900/59/1/1

### lucent.earth
- https://lucent.earth/ （**到達不可**）
- https://larryferlazzo.edublogs.org/2026/04/09/lucent-earth-shows-you-web-cams-from-around-the-world/

### Inside Airbnb
- https://insideairbnb.com/about/
- https://insideairbnb.com/
- https://murraycox.com/projects/inside-airbnb/
- https://nightingaledvs.com/what-data-visualization-and-analysis-taught-one-activist-about-airbnbs-impact-on-communities/
- https://morethancode.cc/2018/05/30/practitioner-profile-murray-cox.html
- https://eteron.org/en/interview/murray-cox/

### Numbeo
- https://en.wikipedia.org/wiki/Numbeo
- https://www.numbeo.com/common/about.jsp
- https://www.numbeo.com/common/motivation_and_methodology.jsp
- https://www.similarweb.com/website/numbeo.com/
- https://rocketreach.co/numbeo-management_b5ec4dc0f42e7357

### PurpleAir
- https://www2.purpleair.com/blogs/blog-home/the-purpleair-story
- https://www.purpleair.com/blog/the-purpleair-story
- https://community.purpleair.com/t/api-pricing/4523
- https://usmanufacturingreport.com/article/purpleair/
- https://www.crunchbase.com/organization/purpleair

### iNaturalist
- https://www.inaturalist.org/pages/financials
- https://www.inaturalist.org/pages/spinoff_faq
- https://www.inaturalist.org/stats/2025/
- https://forum.inaturalist.org/t/taking-a-look-at-inaturalists-latest-form-990-2024/74540
- https://baynature.org/2023/09/12/science-nature/urban-nature/inaturalist-strikes-out-on-its-own/
- https://www.ischool.berkeley.edu/sites/default/files/iNaturalist_Final_Writeup.pdf
- https://projects.propublica.org/nonprofits/organizations/921296468

### 対比事例（Flighty / MyRadar / Citymapper / AirDNA / Watch Duty / Nomad List / Kiln / TeleGeography / Drive & Listen / WindowSwap）
- https://www.revenuecat.com/blog/growth/ryan-jones-flighty-launched-podcast-2025
- https://mercury.com/blog/flighty-app-case-study
- https://stratechery.com/2025/an-interview-with-ryan-jones-about-flighty-and-building-apps-in-2025/
- https://www.starterstory.com/flighty-breakdown
- https://developer.apple.com/news/?id=970ncww4
- https://en.wikipedia.org/wiki/MyRadar
- https://acmeaom.com/
- https://www.floridatrend.com/article/29787/an-orlando-app-developer-builds-on-his-50-million-downloaded-myradar/
- https://techcrunch.com/2023/03/16/via-acquires-trip-planning-app-citymapper-to-boost-transit-tech/
- https://www.neowin.net/news/citymapper-saw-losses-in-2021-of-74-million-up-from-63-million-in-2020/
- https://news.bloomberglaw.com/mergers-and-acquisitions/journey-planning-app-citymapper-sold-to-transit-tech-company-via
- https://www.airdna.co/
- https://www.rentalscaleup.com/airdna-and-transparent-acquired/
- https://www.watchduty.org/about/about-us
- https://en.wikipedia.org/wiki/Watch_Duty
- https://mcj.vc/inevitable-podcast/watch-duty
- https://www.businesswire.com/news/home/20251030766225/en/Watch-Duty-and-GoFundMe-Partner-to-Strengthen-Disaster-Response
- https://getlatka.com/companies/nomad-list
- https://www.starterstory.com/stories/nomad-list-breakdown
- https://www.softwaregrowth.io/blog/how-pieter-levels-grew-nomad-list
- https://www.shipmap.org/
- https://www.kiln.digital/
- https://www.informationisbeautifulawards.com/showcase/1580-shipmap-org
- https://www.submarinecablemap.com/
- https://www2.telegeography.com/sponsor-a-map
- https://www2.telegeography.com/map-services
- https://laughingsquid.com/drive-and-listen/
- https://buymeacoffee.com/erkam
- https://www.travelmassive.com/posts/drive-and-listen-358152052
- https://en.wikipedia.org/wiki/WindowSwap
- https://musebyclios.com/advertising/2-minutes-with-vaishnav-balasubramaniam-and-sonali-ranjit-creators-of-windowswap/
- https://www.vaibal.com/work/windowswap
