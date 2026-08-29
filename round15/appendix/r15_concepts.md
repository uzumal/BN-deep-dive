# 第15ラウンド 自家計測コンセプト生成・敵対的検証

- 実施日 / 全URL確認日: **2026-08-29**
- 封筒: ①中核データを自分で計測 ②IT色（ネットワーク限定せず） ③世界規模 ④ソロ＋AI ⑤時系列が堀 ⑥広告・アフィリ前提＝トラフィック必須、B2B営業前提は減点、監視型は加点
- 実行した敵対的検索: **44クエリ**（製品語彙 × ユーザー語彙 × 日英）
- 本ラウンドの成績: 生成した発想 38 → **提出前に自ら棄却 14** → 一覧掲載 24 → トップ5

---

## 0. 方法論の宣言（過去12件の空白主張誤認への対応）

本ラウンドでは「空白」という語を、**検索クエリと発見物を明記した場合にのみ**使う。以下の3段階でラベルする。

| ラベル | 意味 |
|---|---|
| **飽和** | 同じ出力を出す商用プレイヤーが2社以上。棄却 |
| **部分占有** | 隣接プレイヤーはいるが出力が違う。差分を明記できれば生存 |
| **学術のみ** | 論文・単発調査はあるが継続運用の公開プロダクトが無い。最も有望 |

「学術のみ」を最有望と位置づける理由: 論文は**一度測って終わり**であり、⑤の時系列の堀と正面から食い違う。つまり先行研究の存在は競合ではなく、**題材の妥当性の第三者証明**として使える。

さらに本ラウンドの自己規律として、**トップ5候補には他候補の2倍の検索を課した**（第12ラウンドで「自薦案の検証が甘くなる」と実証されたため）。結果、当初1位だった「地域別価格差」と「サブスク値上げ履歴」は、その追加検索で自ら落ちた（§3参照）。

---

## 1. コンセプト一覧（24件）

---

### C01. クラウド死亡観測所（Cloud Deathwatch）★トップ5-1

**一行**: 世界のネット接続家電・IoT製品のクラウド基盤を毎日叩き続け、「その製品が死んだ瞬間」を人間より先に検知して記録する常設観測所。

**計測**: VPS（数カ国）から、消費者向けIoTベンダーのクラウド API エンドポイント／OTAファーム更新サーバ／MQTT・WebSocket 接続先／コンパニオンアプリのストア掲載状態を、機種系列ごとに1日1〜4回プローブ。取得するのは (a) HTTPステータスと TLS 証明書の失効/更新、(b) ファーム版数の停止（最終更新からの経過日数）、(c) アプリのストア消滅・最終更新日、(d) サポートページの404化。エンドポイントはコンパニオンアプリのAPK静的解析（ドメイン抽出）とDNS/証明書透明性ログから自動発見する。**他社APIは使わない。相手のサーバに自分でパケットを打つ。**

**トラフィック源**: ①報道引用が構造的に発生する——Wemo/Nest/Insteon/Neato の各終了は The Register・9to5・Ars・ITmedia が毎回記事化しており、記者が必ず「他にどれが危ないのか」を探す。②検索: "is X still supported" / "X サービス終了" は事件のたびにスパイクする恒常語彙。③コミュニティ: Home Assistant・r/smarthome・HN は「クラウド死」に極めて反応が強い。④**予測記事が最大の武器**——「ファーム更新が18か月止まっている機種トップ50」は事件が起きる前に出せる唯一のコンテンツ。

**隣接アフィリ**: 買い替えガジェット（Amazon/楽天）、ローカル制御ハブ（Home Assistant Green、Hubitat、SwitchBotハブ）、Zigbee/Z-Wave/Matter機器、NAS・録画機、延長保証。単価も件数も出る帯。**「あなたの機器は死にます→代替はこれ」は購買直結の導線**であり、比較記事より意図が強い。

**時系列の堀**: プローブ履歴は後から買えない。「Belkinのファーム更新が実際に止まったのは告知の何か月前だったか」は、**その期間に叩き続けていた者しか持てない**。かつ、死亡はランダムに起きるので、履歴の価値は年数に対して線形以上に増える。

**敵対的検索**（2026-08-29 実施、5クエリ）:
- `IoT device cloud shutdown bricked tracker database smart home discontinued server abandoned`
- `smart home device end of support tracker when cloud service dies monitor database IoT sunset`
- `"will stop working" list smart devices discontinued support database site tracks`
- `PIRG "Electronic Waste Graveyard" database how many devices tracked methodology`
- `スマート家電 IoT クラウド サービス終了 使えなくなる 一覧 監視 サイト 通知`

**発見した既存プレイヤー**:
- **U.S. PIRG "Electronic Waste Graveyard"** https://pirg.org/edfund/resources/electronic-waste-graveyard/ （確認日 2026-08-29）— **最も近い競合**。100点超の製品を掲載、ブランド/カテゴリ/失われ方（即死・緩慢死・課金の壁）でソート可。2026年版で累計17億ポンドのe-waste換算。ただし**人手キュレーションの年次アドボカシー資料**であり、計測していない・通知が無い・米国中心・「次に危ない機種」を出さない。
- **GitHub unixorn/internet-of-trash** https://github.com/unixorn/internet-of-trash （確認日 2026-08-29）— 手動リスト。
- **FTC報告**: レビュー対象の接続機器の**89%がサポート終了時期を一切表示していない** https://innovation.consumerreports.org/what-the-ftc-report-means-for-consumers/ （確認日 2026-08-29）。米17消費者団体がFTCにガイドライン制定を要請（日本語報道: https://internet.watch.impress.co.jp/docs/yajiuma/1621752.html 確認日 2026-08-29）。
- **apisunset.com** https://apisunset.com/ （確認日 2026-08-29）— 開発者向けAPI廃止アラート。15+プロバイダの**changelogを読む**方式で、消費者機器も計測もしない。
- 日本語圏: Qrio初代の終了 https://www.itmedia.co.jp/news/articles/2305/17/news113_2.html 、RATOC IFTTT連携終了 https://iot.ratocsystems.com/news/notices/6068/ （いずれも確認日 2026-08-29）。**個別事件の記事はあるが、一覧・監視サイトは日本語圏に存在しない。**

**判定**: **部分占有 → 生存**。PIRGは「墓標」、こちらは「心電図」。差分は (1)自動計測 vs 手動収集、(2)死亡後の記録 vs **死亡前の予兆検出**、(3)米国アドボカシー vs 全球、(4)通知が作れる。

**合法性**: 公開エンドポイントへの低頻度GET/HEADは通常の閲覧の範囲。守る線 = 認証を突破しない・レート制限を尊重（1機種1日数回）・robots.txt遵守・DoS的挙動をしない・APK解析は自分が正規入手したもののみ（リバースエンジニアリングは日本著作権法30条の4／米DMCA §1201の相互運用性例外の範囲を超えない）。ベンダー名を出す以上、事実摘示の正確性（名誉毀損）に注意し、「更新が止まっている」という**観測事実**のみを書き「終了する」と断定しない。

**弱点（自己申告）**: (a)エンドポイント発見が最大の工数で、機種ごとに人手が要る——完全自動化は幻想。(b)「更新が止まった」≠「終了」の偽陽性が必ず出る。(c)対象が日米欧のメジャー機種に偏り、真の全球化は難しい。(d)PIRGが計測を始めたら（技術的には可能）先行の3年分の履歴しか差が残らない。(e)アフィリの成約は「壊れた直後」に集中し、平常時の収益はほぼ広告のみ。

---

### C02. オフライン生存度データベース（Does It Work Unplugged?）

**一行**: 「ネットが切れたらこの機器は何ができなくなるか」を実機で測って公開する台帳。C01の姉妹編で、死ぬ**前**に効く。

**計測**: 手元の実機を、①正常、②インターネット遮断（LANは生存）、③ベンダードメインのみDNSブラックホール、の3条件で操作し、機能ごとに可否を記録。加えて、コンパニオンアプリの通信先をmitmproxyで観測し「操作1回がどこまで往復するか（ローカル完結かクラウド往復か）」をレイテンシで判定。ユーザー投稿も同一手順書で受ける。

**トラフィック源**: 購入前検索（"○○ works without internet" / "○○ ローカル制御"）は購買直前の高意図語彙。Home Assistantコミュニティ（世界規模・熱量最大）。C01の事件記事から流入。

**隣接アフィリ**: そのままガジェット購入。**「クラウド不要な代替品」への送客はアフィリ適性が極めて高い**（比較でなく指名買いを作る）。

**堀**: 実機テストの積み上げと、ファーム更新でローカル制御が**後から奪われた**履歴（＝改悪の証拠）。

**敵対的検索**: `smart home device works without internet local control database offline capability list Home Assistant`（2026-08-29）
**発見**: Vesternet、The Home Smart Home、setsmarthome 等のブログ記事群が「TP-Link Kasa / Tuya / Meross はHA連携を謳いながら全コマンドがベンダークラウド経由」といった具体的知見を持つ（https://www.vesternet.com/blogs/smart-home/building-a-truly-offline-smart-home-a-complete-guide-to-local-processing 確認日 2026-08-29）。ただし**機種×機能の網羅的な測定台帳は見つからなかった**。Home Assistantの統合一覧は「連携可否」であって「ネット断で何が残るか」ではない。
**判定**: 学術・コミュニティ知のみ → 生存。ただし単独では弱く、**C01に統合すべき**。

**合法性**: 自分の所有機器の測定なので最も安全。**本一覧で最も法的リスクが低い案**。
**弱点**: 実機購入コストが線形にかかる（＝ソロの上限が明確）。ユーザー投稿の品質管理。ファーム版数ごとに結果が変わり、台帳が腐る速度が速い。

---

### C03. アドレス流出台帳（Leak Ledger）★トップ5-2

**一行**: 企業ごとに専用メールアドレスを1つずつ発行して登録し、「どの企業のアドレスに、いつ、誰から、何通の迷惑メールが来たか」を実測して公開する台帳。

**計測**: 自前ドメインのキャッチオール（例 `netflix.2026-03.xxxx@ledger.example`）で、対象サービスに実際に登録する。以後、受信メールを (a)差出人ドメイン、(b)初回スパム到達までの日数、(c)月間通数、(d)トラッキングピクセル有無、(e)配信停止リンクの実効性（押した後に止まるか）で自動分類。**登録という行為そのものが計測装置**。加えてブラウザ拡張/エイリアス発行クライアントを配り、ユーザーが自分のエイリアスを匿名で寄付できるようにして母数を伸ばす。

**トラフィック源**: ①「○○ 登録 迷惑メール」「is it safe to give X my email」は恒常検索。②企業名ページが自然にロングテールを作る（1社1ページ×数千社）。③報道: 「大手N社のうちM社があなたのアドレスを第三者に渡していた」は各国メディアが必ず拾う型。④privacy系コミュニティの拡散力が高い。

**隣接アフィリ**: エイリアス/転送サービス（SimpleLogin, addy.io, Fastmail）、パスワードマネージャ、**データ削除代行（Incogni / DeleteMe＝アフィリ単価が業界最高帯）**、VPN、迷惑メールフィルタ。題材と商材が一直線で、広告よりアフィリの方が主収入になりうる稀な案。

**時系列の堀**: **本一覧で最強**。「2026年3月に登録したアドレスに2028年から中国語スパムが来た」は、2026年に登録していないと絶対に作れない。金でも買えず、AIでも生成できず、後発は最短でも自分が登録した日からしか始められない。**登録日が資産になる構造**。

**敵対的検索**（4クエリ、2026-08-29）:
- `email honeypot unique address per company which companies share sell your email measurement study tracker`
- `"which companies" sell share your email address public database spam per company signup test`
- `email alias service detects which website leaked your address public leaderboard SimpleLogin Addy statistics`
- `迷惑メール 登録した企業 特定 エイリアス 実測 どの企業が売っているか 調査`

**発見した既存プレイヤー**:
- **EmailAlias.io "Email Aliases with Leak Detection"** https://emailalias.io/ （確認日 2026-08-29）— **最も近い競合**。ただし**個人の受信箱の道具**であり、集計された公開台帳・企業ランキングを出していない。
- SimpleLogin / addy.io / DuckDuckGo Email Protection — いずれも同じく個人向け道具。**公開統計を出していない**（本検索で確認できず）。
- 学術: ACM 2025 "Evaluating Website Data Leaks through Spam Collection on Honeypots" https://dl.acm.org/doi/pdf/10.1145/3714393.3726493 （確認日 2026-08-29）。手法の妥当性は査読済み＝題材の第三者証明。
- 日本語圏: エイリアス活用の解説記事のみ（https://zer0tech.co.jp/database/post-5792/ 確認日 2026-08-29）。**企業別の実測公開は日本語圏に存在しない。**
- 参考: PCWorld「Gmailの+トリックで誰が売ったか分かる」https://www.pcworld.com/article/1936106/gmail-trick-reveals-which-companies-sell-your-data.html （確認日 2026-08-29）— **手法は民間伝承として既知。誰も台帳にしていないだけ。**

**判定**: **学術のみ＋道具は既存 → 生存**。差分は「個人の道具」ではなく「**公開された企業別の判決文**」であること。

**合法性**: 登録は自分の意思による正規登録で、虚偽の身元は使わない（規約違反リスクを避けるため氏名等は実在の自分／許容される範囲に留める）。公開時は**観測事実のみ**（「このアドレスは○社にのみ渡した。以後この差出人から受信した」）を書き、「売った」と断定しない——**因果の断定が最大の法的地雷**（名誉毀損・信用毀損）。GDPR/個人情報保護法上、扱うのは自分のアドレスなので基本的に問題ないが、ユーザー寄付分は匿名化と同意設計が必須。

**弱点（自己申告）**: (a)**立ち上がりが遅い**——登録から結果が出るまで数か月〜年。⑥のトラフィックが最初の1年ほぼ生まれない。(b)EmailAlias.io等が公開ランキングを足せば差が消える（技術的障壁は低い）。(c)スパム業者はタグを剥がす／別経路で本アドレスを拾うため、偽陰性が構造的に出る。(d)「漏らした」と書けない以上、見出しの威力が落ちる。(e)企業数を増やすほど登録の手作業が増え、ソロの上限に当たる。

---

### C04. 開封追跡指数（Who Opens Your Mail）

**一行**: 受信したメールに仕込まれた追跡ピクセルを実測し、「どの企業がどれだけあなたを見ているか」を企業別に公開する。

**計測**: C03と同一の受信基盤を再利用。HTMLメールを解析し、1×1画像・リダイレクタ付きリンク・外部リソースの数と宛先をカウント。差出人企業ごとに「1通あたり追跡要素数」「追跡先ドメイン」「CNIL/Garanteの同意基準に照らした位置づけ」を時系列で出す。

**トラフィック源**: 報道（プライバシー系は各国で記事化されやすい）、privacyコミュニティ、企業名ロングテール。
**隣接アフィリ**: Proton Mail、追跡ブロック系、VPN、エイリアスサービス。C03と完全に同じ商材＝**同じ受信箱から2つの商品が出る**。
**堀**: C03と共有。追跡強度の経年変化（Apple MPP以降どう変わったか）は測っていないと出せない。

**敵対的検索**: `email open tracking pixel which senders track you measurement index public ranking companies`（2026-08-29）
**発見**: 解説記事のみ（Proton https://proton.me/blog/pixel-tracking 、Mailjet の CNIL/Garante ガイダンス解説 https://documentation.mailjet.com/hc/en-us/articles/51109335532571-Email-Tracking-Pixels-and-Consent-CNIL-and-Garante-Guidance 、いずれも確認日 2026-08-29）。**企業別の公開指数は発見できず。**
**判定**: 部分空白 → 生存。ただし**C03の副産物として作るべきで、単独では立たない**。
**合法性**: 自分宛メールの解析であり問題は小さい。公開時の企業名記載は事実の範囲に限定。
**弱点**: Apple Mail Privacy Protection が開封率を汚染しており「追跡の有無」は測れても「追跡の成否」は測れない。単独の検索需要が薄い。

---

### C05. 同意実効性観測所（Did "Reject All" Actually Work?）★トップ5-3

**一行**: サイトの「すべて拒否」ボタンを実際にクリックし、**その後もトラッカーが動いているか**を測り続け、サイトごとに合否を出す常設監視。

**計測**: Playwright/Puppeteer でヘッドレスブラウザを走らせ、①同意バナーを自動判別して「すべて拒否」を押す、②押した後のセッションで発火する第三者リクエスト・Cookie・fingerprinting API 呼び出しを記録、③「押さない場合」「すべて許可の場合」と3条件で差分を取る。EU/日本/米国の複数国VPSから同一手順を回し、国別の挙動差も測る。**ここが決定的な差**——既存の走査ツールは「何が読み込まれたか」を見るが、**「あなたの意思表示が無視されたか」は見ていない**。

**トラフィック源**: ①報道と規制——EUのGDPR執行、CNIL/Garanteの制裁は継続的にニュースになり、記者は「誰が守っていないか」の一次データを常に探している。②サイト名のロングテール（1ドメイン1判定ページ）。③「このサイトは安全か」系の恒常検索に接続。④EU規制当局・NGO（noyb等）が引用しうる＝**被引用は無料の最強の宣伝**。

**隣接アフィリ**: VPN、広告ブロッカー、プライバシーブラウザ、データ削除代行、パスワードマネージャ。

**堀**: 「このサイトは2026年時点で拒否を無視していたが、2027年の制裁後に直った」という**改善/悪化の履歴**。規制の効果測定という、規制当局自身が持っていない時系列。

**敵対的検索**（3クエリ、2026-08-29）:
- `cookie banner reject all actually works measurement study tracking still happens consent violation automated`
- `dark pattern longitudinal monitoring automated archive website changes over time deceptive design tracker`
- （既知プレイヤーの再確認）Blacklight / The Markup

**発見した既存プレイヤー**:
- 学術: **BannerClick** https://bannerclick.github.io/ （確認日 2026-08-29）— バナー操作と追跡Cookieの関係を測る研究プロジェクト。**継続運用の公開サービスではない**。
- 学術: 「EU約97,000サイトのうち、拒否選択肢を提供するサイトの**65.4%が明示的拒否の後もデータ収集していた**」（アムステルダム大学 https://www.uva.nl/en/shared-content/faculteiten/en/faculteit-der-rechtsgeleerdheid/news/2024/03/control-your-cookies.html 確認日 2026-08-29）。2026年の行動ターゲティング研究では「Reject All で第三者Cookieホストは約70%減るが、興味関連広告は依然表示される」。
- arXiv: "Thou Shalt Not Reject: Analyzing Accept-Or-Pay Cookie Banners on the Web" https://arxiv.org/pdf/2310.01108 （確認日 2026-08-29）。
- **既知プレイヤーとの差分**: **Blacklight（The Markup）は単発スキャンで、拒否を押さず、履歴を保持しない**。securityheaders.com はヘッダのみ。OpenTermsArchive は文言の変更であって挙動ではない。
**判定**: **学術のみ → 生存**。「論文は一度測って終わる」構造がそのまま堀になる典型例。

**合法性**: 通常のブラウジングと同じ操作であり、認証もクロールの大量負荷も伴わない。**本一覧で2番目に法的リスクが低い**。守る線 = 1サイト1日1回以下、robots.txt尊重、ログインの背後には入らない。公開時は「観測条件（日時・国・ブラウザ）」を必ず併記し、断定を避ける。

**弱点（自己申告）**: (a)**消費者の検索需要が薄い**——人は「このサイトは拒否を守るか」を検索しない。トラフィックが報道と規制当局への依存に偏り、⑥の要件を満たす確度が本トップ5で最も低い。(b)同意バナーの自動判別は総当たりで壊れやすく、偽陰性が常時出る。(c)「違反」と書けば法務リスク、書かなければ見出しが弱いというジレンマ。(d)研究者が同じ装置を無料で公開する可能性が常にある（学術の慣行として起こりうる）。

---

### C06. デジタル改悪台帳（Downgrade Ledger）★トップ5-4

**一行**: 「昔できたのに、いつの間にかできなくなったこと」を、更新履歴とアーカイブの差分で機械的に検出して残す台帳。

**計測**: ①アプリストアのバージョン履歴とリリースノートを全言語で収集し差分、②公式ヘルプ/機能ページを定期取得して**消えた記述**を検出（自前クロール＋自前スナップショット）、③プラン制限値（容量GB・人数・回数）の数値抽出と経時比較、④APKの機能フラグ/文字列の差分。「追加」ではなく**「削除」だけを抽出**するのが設計の核。

**トラフィック源**: ①「○○ 機能 なくなった」「why did X remove Y」は事件のたびに急増する恒常語彙。②HN/Reddit/はてブでの拡散力が極めて高い（enshittification は2020年代の共有語彙になっている）。③報道: Evernote/Netflix/Sonos型の改悪は必ず記事になり、記者が年表を探す。④年次「改悪ランキング」は毎年出せる定番コンテンツ。

**隣接アフィリ**: 代替サービス（乗り換え先SaaSのアフィリは単価が高い）、自己ホスト用NAS/VPS、データ移行ツール、買い切り型ソフト。**「改悪された→乗り換え先」は最も自然な送客**。

**堀**: 公式は改悪の記録を残さない（ヘルプページは書き換えられ、リリースノートは"bug fixes"に丸められる）。**消される前に自分で撮ったスナップショットだけが証拠になる**。Wayback Machine は網羅性と粒度が足りず、プラン数値の構造化はしていない。

**敵対的検索**（3クエリ、2026-08-29）:
- `enshittification tracker features removed from apps over time archive what changed downgrade`
- `free tier changes tracker cloud services free plan shrinking history monitor`
- `SaaS pricing page change tracker developer tools price history GitHub Figma Notion monitor`

**発見した既存プレイヤー**:
- **agentdeals.dev /pricing-changes** https://agentdeals.dev/pricing-changes （確認日 2026-08-29）— **最も近い競合**。開発者ツールの価格変更287件以上（無料枠廃止・上限削減・値上げ）をタイムラインで提供。ただし**開発者ツール限定＋価格軸限定**で、消費者向けアプリの機能削除は扱わない。
- SaaS価格ページ監視は**飽和**: SaaS Price Pulse https://www.saaspricepulse.com/ 、PricePulse https://www.getpricepulse.com/ （44社を1時間毎にdiff）、Apify actors 複数、PageCrawl、Verid（すべて確認日 2026-08-29）。ただし**全てB2B競合監視向け**で、消費者向けの「改悪年表」ではない。
- 概念記事は多数あるが（Cory Doctorow の enshittification 系）、**機能削除を機械的に検出して蓄積する台帳は発見できなかった**。
**判定**: **部分占有 → 生存**。差分は (1)価格ではなく**機能の消失**、(2)B2B競合監視ではなく**消費者の記憶の代替**、(3)開発者ツールではなく全カテゴリ。

**合法性**: 公開ページの低頻度クロールと引用。EUでは契約（利用規約）によるスクレイピング禁止が有効（Ryanair v. PR Aviation、第13ラウンドの確定事項）なので、**規約でクロールを禁じているサイトは対象から外す**運用が必要。引用は必要最小限＋出典明示（日本著作権法32条）。

**弱点（自己申告）**: (a)アフィリ商材が弱い（改悪に怒る人は金を払う気分ではない）。(b)バズは大きいが**持続しない**——事件駆動で、平常時のトラフィックが薄い。(c)「改悪」の定義が主観に寄りやすく、編集判断が必要＝自動化しきれない。(d)agentdeals が消費者側に広げれば正面衝突。(e)対象企業からの削除要請リスク。

---

### C07. 地理ブロック地図帳（Geoblock Atlas）★トップ5-5

**一行**: 「そのサイト／サービスは、どの国から実際に見えるのか」を各国のVPSから毎日叩いて地図と年表にする。

**計測**: 20〜40か国のVPS（1台$3〜5/月、無料枠併用可）から、対象ドメイン群に同一のHTTPリクエストを送り、①403/451、②地域リダイレクト、③「お住まいの地域ではご利用いただけません」文言、④DNS応答差、⑤TLS handshake の可否を判定。**国家による検閲（OONI/IODAの領域）ではなく、企業が自主的に閉めている扉**を対象にする。GDPR回避で欧州を閉めた米メディア、制裁対応で閉めた金融、ライセンスで閉めた配信、AI規制で遅らせた新機能——これらは全部「企業の判断」であり、誰も継続測定していない。

**トラフィック源**: ①「なぜ日本から○○が使えないのか」「is X available in Japan」は恒常検索で、**新サービスのローンチのたびに世界中で同時多発する**。②報道: 「新機能がEUだけ来ない」はDSA/AI Act時代の定番ニュース。③1ドメイン×1国のロングテールページが自動生成できる（構造上、数万ページ）。④VPNコミュニティ。

**隣接アフィリ**: **VPN（アフィリ単価が業界最高帯の一つ）**、eSIM/国際SIM、レジデンシャルプロキシ、国際転送サービス、海外送金。題材と商材が完全に一致する。

**堀**: 「2026年8月に○社は欧州を閉めた」という**閉鎖の日付**。企業は告知しないので、叩き続けた者しか知らない。規制と閉鎖の因果を語れる唯一のデータになる。

**敵対的検索**（4クエリ、2026-08-29）:
- `geoblocking measurement which websites block visitors from country tracker GDPR blocked US news sites Europe`
- `AI service availability by country tracker which countries can access ChatGPT Gemini Claude rollout map`
- `feature availability by country locale tracker which features missing in Japan Europe measured product parity`
- `same website different content by country measurement geo content divergence what visitors see study`

**発見した既存プレイヤー**:
- **学術**: ミシガン大 "403 Forbidden" 研究 https://eecs.engin.umich.edu/stories/403-forbidden-study-reveals-new-data-on-region-specific-website-blocking-practices （確認日 2026-08-29）— Alexa Top 10K を177か国の観測点から測定。国あたり中央値3ドメイン、最大はシリアの71ドメイン。**単発研究であり継続公開サービスではない**。
- **voidly.ai AI Censorship Index** https://voidly.ai/ai-blocked （確認日 2026-08-29）— **最も近い競合**。130か国のAIサービス到達性。ただし**AIサービス限定**で、一般のウェブ全体を扱わない。
- 既知プレイヤーとの差分: **OONI/IODA/Censored Planet は「国家による検閲」**が対象。本案は**企業の自主的閉鎖**が対象で、測定対象が排他的。Cloudflare Radar は自社トラフィックの集計であって能動測定ではない。
- ロケール別機能差分は**専用トラッカーが見つからなかった**（TrackStreetはEC商品、IQVIAは医薬品）。
**判定**: **部分占有＋学術のみ → 生存**。ただしトップ5で**最も競合に近い**（voidly.ai が対象を広げれば衝突）。

**合法性**: 各国VPSからの通常アクセス。**ここで守る線が1本ある**——地域制限を「回避して中身を取得する」のは EU の C-392/19 VG Bild-Kunst（技術的措置の回避＝侵害）に触れうる。本案は**「閉まっているという事実」だけを記録し、中身は取らない**設計にすることで回避する。VPNの使い方を指南する記事は、配信サービスの規約違反を教唆する形になるため、**アフィリの書き方に線引きが必要**（「安くする方法」ではなく「見えるかどうか」に限定）。

**弱点（自己申告）**: (a)**VPNアフィリのSEOは世界最激戦区**で、予算ゼロ・フォロワーゼロの個人が「best VPN」で勝てる見込みはゼロ。勝てるのは「is X available in Y」のロングテールだけで、単価の高い記事には届かない。(b)データセンターIPは多くのサイトにブロックされ、「地域制限」と「DC遮断」の区別が難しい＝**偽陽性が構造的に出る**。(c)voidly.ai との差が「対象の広さ」だけであり、防御力が弱い。(d)VPS40台の運用は月$120〜200で、本一覧で最もランニングコストが高い。

---

### C08. 権限ラベル差分アーカイブ（Privacy Label Diff Archive）

**一行**: App Store のプライバシーラベルと Google Play の「データの安全性」を全世界の全ストアで定点取得し、「いつ、どのアプリが、何を集め始めたか」を差分で残す。

**計測**: 主要アプリ数千本について、各ストアフロント（Appleは175地域）から公開ページを定期取得し、ラベル項目・要求権限・SDK申告・最終更新日を構造化して差分保存。ベンダーはラベルを**リリースと無関係に随時書き換えられる**（Apple公式）ため、変更は告知なく起きる＝**取り続けた者しか気づけない**。

**トラフィック源**: 「○○ アプリ 危険」「what data does X collect」は恒常検索。プライバシー系報道。アプリ名ロングテール。
**隣接アフィリ**: VPN、プライバシー系アプリ、データ削除代行、代替アプリ。
**堀**: ラベルの改訂履歴。公式は過去版を残さない。

**敵対的検索**（2クエリ、2026-08-29）: `app privacy label changes over time tracker App Store data safety monitoring` / `Android app permission change history tracker alert APK diff monitoring service`
**発見**: 学術のみ（MDPI 2024「Apple プライバシーラベルの整合性検証」https://www.mdpi.com/2078-2489/15/9/551 、CHI 2022 https://dl.acm.org/doi/fullHtml/10.1145/3491101.3519739 、いずれも確認日 2026-08-29）。**端末内アプリ**は存在する（Google Play「App Update History」等）が、これは**自分の端末のローカル記録**であって公開データベースではない。**AppCensus** https://cltc.berkeley.edu/publication/mobile-app-privacy-analysis-with-appcensus/ （確認日 2026-08-29）は計装Android実機での動的解析という別次元の装置で、ソロでは再現不能。
**判定**: 学術＋端末内アプリのみ → 生存（ただしC03/C05とプライバシー帯で客層が完全に重なる）。
**合法性**: ストア公開ページの取得。ストア規約のスクレイピング条項に注意。
**弱点**: ラベルは**自己申告**なので「嘘を測っている」だけで、真実は測れない（真実にはAppCensus級の装置が要る）。差分の大半が些末で、見出しになるものが少ない。

---

### C09. 解約導線カルテ（The Cancel Path）

**一行**: 実際に契約して実際に解約し、「何クリック・何画面・何回の引き止め・何日かかったか」を測って企業別に公開する。

**計測**: 対象サービスに実登録→解約フローを人手＋スクリプトで通し、画面遷移数・必須クリック数・ダークパターン類型（引き止め、事前選択、退会ボタンの視認性）・電話/チャット強制の有無・完了までの実日数を記録。全画面をスクリーンショットで保全。米FTCのclick-to-cancel規則（2025年7月8日に手続上の瑕疵で無効化）以後、**「規制が消えた後に各社が導線を戻したか」を測れるのは実測者だけ**。

**トラフィック源**: **「how to cancel X」「○○ 解約 方法」は世界最大級の恒常検索語彙の一つ**。ここが本案の最大の強み。
**隣接アフィリ**: サブスク管理アプリ、家計簿、バーチャルカード、代替サービス。
**堀**: 規則の施行・無効化の前後で導線がどう動いたかの証拠。

**敵対的検索**（2クエリ、2026-08-29）: `how hard to cancel subscription database clicks to cancel measured tracker` / `dark pattern longitudinal monitoring automated archive website changes over time deceptive design tracker`
**発見**: **RecurDash** https://recurdash.com/subscription-pricing （確認日 2026-08-29）が235サービスの価格表と**解約ガイドへのリンク**を持つ。joinchargeback.com 等の解約ガイド系コンテンツファームが多数。**ただし「難易度を測って数値化した公開台帳」は発見できなかった**——ガイドは「やり方」を書くが「どれだけ酷いか」を測っていない。
**判定**: 部分占有 → 条件付き生存。**「how to cancel」の検索面は既にコンテンツファームで飽和**しており、個人が上位を取るのは困難。勝ち筋は「難易度ランキング」という別の見出しのみ。
**合法性**: 自分が契約者として自分の契約を解約する行為なので適法。ただし**実費が毎月発生**する。公開時は事実のみ。
**弱点**: **自動化できない＝ソロの上限が最も低い**。実費（月額×社数）が線形。1社の測定に1か月かかる。C06と客層が重なる。

---

### C10. 通知量実測（Notification Load Index）

**一行**: 主要アプリを実機/エミュレータに入れて放置し、「1週間で何通プッシュが来るか」をアプリ別に測って公開する。

**計測**: Android エミュレータ農場（またはテスト端末）に対象アプリを新規インストールし、初期設定のまま放置。通知を NotificationListenerService で全件記録し、アプリ別・時間帯別・種別（機能通知／広告通知）に分類。国別ストアで挙動が変わるかも測る。

**トラフィック源**: 「通知 多い アプリ」「stop notifications from X」、ランキング記事のバズ、報道。
**隣接アフィリ**: 集中支援アプリ、ペアレンタルコントロール、端末買い替え。
**堀**: 「このアプリは3年で通知が4倍になった」という増加曲線。

**敵対的検索**: `push notification volume index which apps send the most notifications measurement study ranking`（2026-08-29）
**発見**: **Airship 2026 Benchmarks（6,810億通・30億ユーザー・15業種）** https://www.airship.com/blog/your-guide-to-airships-mobile-app-push-notification-benchmarks-for-2026/ 、Pushwoosh（600アプリ）、Business of Apps（確認日いずれも 2026-08-29）。**すべてマーケター向けの業種平均ベンチマークで、「このアプリが何通送るか」という消費者向けの実名ランキングは存在しない**。
**判定**: 部分占有（B2B側のみ） → 生存。差分は「業種平均」vs「実名の実測」。
**合法性**: 自分の端末での受信記録。アプリ規約の自動化条項に注意。
**弱点**: エミュレータでは実ユーザー扱いされず通知が来ない/減る可能性（挙動の代表性が疑わしい）。アカウント作成の手間。**「測定の妥当性」への突っ込みに弱い**。

---

### C11. 世界遅延台帳（Global Punctuality Ledger）

**一行**: 世界99か国6,000超の公共交通リアルタイムフィードを保存し続け、誰も持っていない「世界の定時性の歴史」を作る。

**計測**: Mobility Database に登録された GTFS / GTFS-Realtime フィードを数十秒〜数分間隔でポーリングし、車両位置と予定時刻の差分を計算して保存。**GTFS-RTは更新のたびに上書きされ履歴が残らない**——これが構造的な堀。自分で保存し続けた者だけが過去を持つ。

**トラフィック源**: 「○○線 遅延 統計」の恒常検索、都市比較のバズ（「世界で最も遅れる地下鉄」）、報道引用、旅行前検索。
**隣接アフィリ**: 鉄道パス、旅行、遅延補償保険、乗換アプリ。
**堀**: 極めて強い。フィードは揮発性で、後から買えない。

**敵対的検索**（2クエリ、2026-08-29）:
- `global public transit punctuality index GTFS realtime measured delays comparison cities worldwide`
- `public transit realtime feed archive historical GTFS-RT data nobody stores delay history worldwide project`
- `train delay statistics website compare countries punctuality data site 鉄道 遅延 統計 世界 比較 サイト`

**発見した既存プレイヤー**:
- **chuuchuu.com "European Train Punctuality Rankings 2025"** https://chuuchuu.com/2025wrapped （確認日 2026-08-29）— **欧州鉄道は既に取られている**。
- OSS/学術: **gtfs-realtime-capsule（Two Sigma Data Clinic）** https://github.com/tsdataclinic/gtfs-realtime-capsule 、**gtfsrdb** https://github.com/mattwigway/gtfsrdb 、Cornell Tech の BusObservatory（いずれも確認日 2026-08-29）。**アーカイブの道具は既に無料で存在する**。
- 公的: 欧州委員会、英ORR、Statista が国別統計を出す。**ただし各国で定時性の定義が違い比較不能**という指摘があり、統一計測の余地は残る。
- Mobility Database https://mobilitydatabase.org/ （確認日 2026-08-29）— 99か国6,000超フィードのカタログ。
**判定**: **部分占有 → 条件付き**。欧州鉄道は取られ、道具はOSSで無料。残る空白は「バス・地下鉄を含む全球・統一定義」。
**合法性**: 公的機関のオープンデータだが、**第14ラウンドの教訓どおりライセンス確認が必須**（非商用条項があると広告収入と衝突する）。フィードごとの個別確認が要る。
**弱点**: (a)保存コストが本一覧で最大（数千フィード×数十秒間隔）。(b)検索需要が**都市ローカルに分裂**し、世界規模の一つの面にならない。(c)「自分で計測」というより「他人の配信の保存」であり、封筒①との緊張が最も強い案。(d)道具が無料で存在する＝参入障壁が低い。

---

### C12. AI拒否地図（The Refusal Atlas）

**一行**: 同じ質問を言語と接続元を変えて主要AIに投げ続け、「どの国・どの言語では答えてもらえないか」を毎日記録する。

**計測**: 固定プローブ集（政治・医療・法律・地域史など数百問）を、①20言語、②複数国VPS、③各主要モデルに対して毎日実行。拒否率・回答長・回答内容の乖離を測る。**答えの良し悪し（既存プレイヤーの土俵）ではなく、「答えるか否かの地理的・言語的な非対称」だけを測る**。

**トラフィック源**: 報道（AI検閲は世界中で記事になる）、研究者引用、コミュニティ。
**隣接アフィリ**: AIサブスク、VPN、翻訳ツール。
**堀**: モデル更新のたびに変わる拒否境界の年表。誰も保存していない。

**敵対的検索**（2クエリ、2026-08-29）: `LLM refusal rate by language country same question answered differently measurement tracker censorship` / `LLM political bias tracker over time measurement TrackingAI model answers change monitor`
**発見**: 学術多数（arXiv "What Large Language Models Do Not Talk About" https://arxiv.org/pdf/2504.03803 、SomaliBench https://arxiv.org/pdf/2605.25420 、OECD.AI の Reject Rate 指標。確認日いずれも 2026-08-29）。**TrackingAI.org** https://www.trackingai.org/ （maximumtruth.org 経由で確認、2026-08-29）が16のチャットボットに毎日 political compass を投げて記録——**「毎日プローブして記録する」という装置は既に存在する**。ただし対象は政治的立場であって**言語・地域による拒否の非対称ではない**。
**判定**: 部分占有 → 生存。ただし**TrackingAI が言語軸を足すのは一晩でできる**。防御力が弱い。
**合法性**: 各AIの利用規約（自動化・ベンチマーク公開の可否）を個別確認。多国VPSからのアクセスは規約上グレーになりうる。
**弱点**: API費用が毎日かかる（数百問×20言語×複数モデル）。既知プレイヤー（Artificial Analysis、aistupidlevel）の隣で、差分が「軸の違い」だけ。

---

### C13. AI引用腐敗率（Citation Rot Watch）

**一行**: AIが答えに付けたURLを毎日踏みに行き、「404だった率」「存在しない記事だった率」をモデル別に記録し続ける。

**計測**: 固定質問集を各AI検索に投げ、返ってきた引用URLを自動でHTTP検証（404/410/リダイレクト/内容不一致）。「壊れている」だけでなく「そもそも存在したことがない（捏造）」を、Wayback Machine 照合と本文一致で切り分ける。
**トラフィック源**: 報道（AI信頼性は最頻出テーマ）、研究者、ジャーナリズム界隈。
**隣接アフィリ**: AIサブスク、ファクトチェック/リサーチツール。
**堀**: モデル世代ごとの腐敗率の推移。

**敵対的検索**: `AI chatbot citation accuracy measurement fabricated broken links tracker over time study`（2026-08-29）
**発見**: **Tow Center（Columbia）「AI Search Has a Citation Problem」** https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php （8エンジン×200テスト、60%超が誤り。確認日 2026-08-29）、SE Ranking「ChatGPTはAI Overviewsの2倍404を引用」https://seranking.com/blog/broken-links-in-chatgpt/ （確認日 2026-08-29）。**いずれも単発調査で、継続する公開ダッシュボードは発見できなかった。**
**判定**: 学術・単発調査のみ → 生存。
**合法性**: 各AIの規約次第。大量自動クエリは規約違反になりうる。
**弱点**: 読者が開発者・記者に偏り、消費者トラフィックが薄い＝⑥に弱い。Artificial Analysis が隣接。

---

### C14. ロケール差分観測所（Locale Parity Watch）

**一行**: 同じ製品の機能一覧・ヘルプ・設定画面を全言語版で取得し、「日本語版／EU版だけ無い機能」を機械的に洗い出す。

**計測**: 主要サービスのヘルプセンター・機能ページ・アプリ内文言リソースを、言語×地域の全組合せで定期取得し、機能項目の集合差を計算。C07（アクセス可否）が「入れるか」、こちらは「入った先で何が無いか」。
**トラフィック源**: 「○○ 日本 使えない」「why is X not available in Japan」は日本発の視点が強みになる恒常検索。EU（DSA/DMA/AI Act由来の機能遅延）でも同型の需要。
**隣接アフィリ**: VPN、代替サービス、海外SIM。
**堀**: 機能が日本に来るまでの遅延日数の年表（「Googleの新機能は平均何日遅れて日本に来るか」）。

**敵対的検索**: `feature availability by country locale tracker which features missing in Japan Europe measured product parity`（2026-08-29）
**発見**: 専用トラッカーは**発見できず**。TrackStreet（EC商品の国際可視性）、IQVIA（医薬品の国別上市）、Microsoft の Copilot 国際提供状況ページなど、**用途が全く違うものしか出てこない**。Google Pixel の機能パリティはコミュニティスレッドでの議論止まり。
**判定**: 空白（本検索の範囲で） → 生存。**日本発の独自性（③の加点）が最も出る案**。
**合法性**: 公開ヘルプページのクロール。規約確認。
**弱点**: 機能項目の同定が言語間で難しく（翻訳ゆれ）、偽陽性が多い。ヘルプページの構造変更で常に壊れる。バズはするが単価の高い商材が無い。

---

### C15. ストア消滅検知（Storefront Vanish Watch）

**一行**: 175のApp Storeフロントと全Google Play地域を毎日走査し、「どの国から、どのアプリが、いつ消えたか」を検知する。

**計測**: 各ストアフロントの公開ページ／検索結果を巡回し、アプリの掲載有無・版数・年齢制限・掲載名の変化を差分検出。規制による削除、企業の撤退、制裁、ローカライズ廃止を区別してタグ付け。
**トラフィック源**: 報道（「○○が△国から消えた」は必ずニュースになる）、恒常検索「○○ 消えた ダウンロードできない」。
**隣接アフィリ**: VPN、代替アプリ、APK配布は扱わない（違法性）。
**堀**: 消滅の日付。ストアは履歴を残さない。

**敵対的検索**: `app removed from app store by country tracker takedown monitoring`（C15用に §1のストア系2クエリと併せて実施、2026-08-29）
**発見**: appfigures / Sensor Tower / data.ai 系のB2Bアナリティクスが版数と掲載を持つが、**高額なB2B契約前提で、消費者向けの「消滅年表」は存在しない**。delisted系はゲーム専門で飽和（§3参照）。
**判定**: 部分占有（B2Bのみ） → 生存。ただしB2Bデータ屋が同じデータを既に持っており、公開する気になれば一瞬。
**合法性**: ストア規約のスクレイピング条項が最大の障害。**Appleの規約は自動巡回に厳しい**。
**弱点**: 規約リスクが本一覧で高い部類。C07/C14と客層が重なり、3案とも作る意味は薄い。

---

### C16. パーソナライズ価格の実証（Price Mirror）

**一行**: 同じ商品を、条件だけ変えた複数のブラウザから同時に見て、「人によって値段が違うか」を実証し続ける。

**計測**: 同一時刻に、①クリーンなブラウザ、②閲覧履歴を積んだブラウザ、③ログイン済み、④iOS UA/Android UA、⑤複数国IP——の並列セッションで同一商品ページを取得し価格を比較。差が出た組合せだけを記録する。ブラウザ拡張でユーザーからも「あなたが見た価格」を匿名収集して母数を作る。
**トラフィック源**: 「同じ商品なのに値段が違う」は感情的に強い題材で拡散する。報道（FTCのsurveillance pricing調査以後、各国で継続テーマ）。
**隣接アフィリ**: VPN、価格比較、プライバシーブラウザ、クレカ/ポイント。
**堀**: 「どの店がいつからパーソナライズを始めたか」の年表。

**敵対的検索**: `personalized pricing detection measurement same product different price by device login tracker study`（2026-08-29）
**発見**: **FTC surveillance pricing 調査**（2025年1月 https://www.ftc.gov/news-events/news/press-releases/2025/01/ftc-surveillance-pricing-study-indicates-wide-range-personal-data-used-set-individualized-consumer 確認日 2026-08-29）、arXiv 2013 "Crowd-assisted Search for Price Discrimination in E-Commerce" https://arxiv.org/pdf/1307.4531 （確認日 2026-08-29）。**継続運用の公開検出サービスは発見できず。**
**判定**: 学術・規制調査のみ → 生存。
**合法性**: **本一覧で最もリスクが高い部類**。EC サイトの規約はほぼ全社が自動アクセスを禁じ、EUでは契約によるスクレイピング禁止が有効（Ryanair v. PR Aviation）。米hiQ v. LinkedIn は「勝っていない」（第13ラウンドの確定事項: CFAAは回避したが2022年12月に$50万の判決＋恒久差止で会社消滅）。**anti-bot（DataDome等）との軍拡競争にソロで勝てない。**
**弱点**: 上記の法的・技術的障壁が致命的。加えて「差が出なかった」という結論はニュースにならず、空振りの期待値が高い。**トップ5に入れなかった最大の理由**。

---

### C17. 総額実測（True Total Price）

**一行**: 「表示価格」と「最後に請求される額」の差を、決済直前まで進んで測り、業種別に公開する。

**計測**: チケット・宿泊・航空・レンタカー・サブスクの購入フローを決済直前まで自動で進め、各ステップの表示額を記録。米FTCのjunk fee規則（2025年5月12日施行、ホテルとライブチケットが対象）の**遵守率を実測**する。
**トラフィック源**: 「resort fee」「隠れ手数料」は恒常。規制報道。
**隣接アフィリ**: 旅行（アフィリ単価が高い帯）、クレカ、保険。
**堀**: 規則施行前後の遵守率の推移。

**敵対的検索**（2クエリ、2026-08-29）: `hidden fees junk fees measurement tracker actual checkout price vs advertised hotels tickets study` / `resort fee database total price tracker hotel real price including fees website`
**発見**: **resortfeechecker.com** https://www.resortfeechecker.com/about.html （2,000ホテル超のリゾート料金DB。確認日 2026-08-29）が**ホテル領域を既に占有**。UseCalcPro等の計算機は多数。ホテル以外（チケット・レンタカー・航空の付帯料金）の継続実測は発見できず。
**判定**: 部分占有 → 条件付き。ホテルは撤退、それ以外なら空白。
**合法性**: **C16と同じ深刻な問題**。決済フローの自動化は規約違反が濃厚で、anti-botも最強クラス。
**弱点**: 法的リスクが実質的な棄却理由。トップ5に入れない。

---

### C18. ガチャ実測台帳（Odds Audit）

**一行**: 公表確率と、実際に出た確率を、ゲーム横断で突き合わせ続ける監査台帳。

**計測**: プレイヤーからの排出ログをクライアント（アプリ/拡張/OCR）で構造化収集し、公表値に対するカイ二乗検定を継続実施。加えて自分でも一定額を回して基準系列を持つ。日本の景品表示法・消費者庁の指針、中国の公示義務、EUの動きと突き合わせる。
**トラフィック源**: ゲームコミュニティの熱量は世界最大級。「○○ 確率 おかしい」は恒常。報道（ガチャは各国で規制テーマ）。
**隣接アフィリ**: ゲーム課金（規約上難あり）、ゲーミング機器、攻略サイト広告。
**堀**: 公表確率の改訂履歴と実測の乖離の年表。**日本発の独自性が強い（③の加点）**。

**敵対的検索**: `gacha drop rate measurement crowdsourced actual vs advertised probability tracker game`（2026-08-29）
**発見**: 計算機は多数（gachacalc.com、hakaru.io、Hu Tao等）。**Bruin** https://getbruin.com/use-cases/mobile-gaming/gacha-pull-rate-calibration/ （確認日 2026-08-29）は**開発者側**の実測vs設定値の検証ツール。**プレイヤー側からの、ゲーム横断の実測監査は発見できなかった**（個別ゲームのWiki/スプレッドシートは各所に存在）。
**判定**: 部分占有 → 生存。ただし**個別ゲームのコミュニティが既に自前で回しており、横断化の需要が本当にあるか未検証**。
**合法性**: **リスクが高い**。ゲームの規約はクライアント改変・自動化をほぼ全社が禁止。OCRや手入力に限れば緩和されるが、収集の質が落ちる。運営からの法的圧力の実例が業界にある。
**弱点**: フォロワーゼロで投稿を集める鶏卵問題が本一覧で最も厳しい（C03と違い、自分一人では母数を作れない）。規約リスク。

---

### C19. サポート応答実測（Do They Answer?）

**一行**: 実際に問い合わせを送り、返事が来るまでの時間と中身を企業別に測り続ける。
**計測**: 同一文面の問い合わせを各社の全チャネル（メール/チャット/フォーム）に投げ、初回応答時間・解決までの往復数・AI応答か人間かを記録。
**トラフィック源**: 「○○ 問い合わせ つながらない」の恒常検索。
**隣接アフィリ**: 代替サービス、消費者相談。
**堀**: 応答時間の経年悪化（AI化の実測）。
**敵対的検索**: `customer support response time measured comparison companies actual reply time test tracker`（2026-08-29）
**発見**: ベンチマーク統計のみ（stealthagents、Jitbit「1000社の平均」https://www.jitbit.com/news/2266-average-customer-support-metrics-from-1000-companies/ 確認日 2026-08-29）。いずれも**業界平均であって実名の実測ではない**。
**判定**: 部分占有（平均値のみ） → 生存だが弱い。
**合法性**: 虚偽の問い合わせを大量に送るのは業務妨害になりうる。**実在の契約に基づく正当な問い合わせに限定**する必要があり、それは規模を殺す。
**弱点**: 自動化不能、実費、法的グレー。**C09と同じ「人力の壁」**。

---

### C20. 公開カメラ活動指数（Open Lens Index）

**一行**: 世界の公開カメラ映像を毎時解析し、人・車の数の変化を「活動指数」として時系列化する。
**計測**: 利用が明示的に許諾された公開カメラのみを対象に、YOLO系で人/車を計数し、地点別の日次指数を作る。
**トラフィック源**: 報道（経済指標・観光・災害）、旅行前検索。
**隣接アフィリ**: 旅行、宿泊。
**堀**: 計数の履歴。映像は残らないが数字は残る。
**敵対的検索**（2クエリ、2026-08-29）: `public webcam video analysis economic activity index counting cars people automated measurement` / `tourist crowding real time measurement webcam computer vision overtourism index global`
**発見**: 学術・公的機関のみ（英ONS https://datasciencecampus.ons.gov.uk/projects/estimating-vehicle-and-pedestrian-activity-from-town-and-city-traffic-cameras/ 、MDPI の公開ウェブカメラ検証 https://www.mdpi.com/2673-7590/5/3/87 、コペンハーゲンのpublic-eye。確認日いずれも 2026-08-29）。商用はB2B（Isarsoft, Camlytics）。
**判定**: 学術のみ → 生存。**ただし第14ラウンドの結論（ライブカメラ地図は英語圏12＋日本語圏5製品で飽和、overwatch.earthが32レイヤ実装済み）に隣接**しており、「地図に載せる」形にした瞬間に飽和領域へ落ちる。**指数化に徹する場合のみ生存。**
**合法性**: **最大の障害**。第14ラウンドで確認済みのとおり、Windy Webcams は画像URLが10分で失効、多くの無料APIに非商用条項がある。カメラ運営者の許諾が個別に要る。夜間・悪天候で精度が落ちる（MDPI）。
**弱点**: 許諾交渉が実質B2B営業（④に抵触）。精度の説明責任。

---

### C21. リンク腐敗観測所（Rot Watch）

**一行**: 報道・政府・学術のリンクを固定パネルで毎週叩き、「ウェブが消えていく速度」を測り続ける。
**計測**: 主要メディア・政府ドメインの記事内リンクを固定サンプルで抽出し、週次でHTTP検証。**「いつ死んだか」を週単位で特定できるのは継続測定者だけ**（Waybackは「いつ最後に生きていたか」しか分からない）。
**トラフィック源**: 報道・学術。
**隣接アフィリ**: アーカイブ/ホスティング、ブックマークサービス。弱い。
**堀**: 死亡日の精度。
**敵対的検索**: `link rot observatory continuous measurement dead links news websites over time tracker`（2026-08-29）
**発見**: **Pew Research（2024）** https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/ （ニュースページの23%が壊れたリンクを含む。確認日 2026-08-29）、Ahrefs（200万ドメイン、9年で66.5%が死亡）、Internet Archive の新ツール、Wikipedia IABot。**継続する公開オブザーバトリは無いが、単発調査が権威ある形で既に存在する。**
**判定**: 部分占有 → 生存だが弱い。
**合法性**: 低頻度のHEADリクエスト。問題は小さい。
**弱点**: **消費者トラフィックがほぼゼロ**。⑥を満たさない。アフィリ商材が無い。

---

### C22. 端末パッチ遅延指数（Patch Latency Index）

**一行**: 家庭用ルータ・スマホの実機のファーム版数を追い、「脆弱性公表からパッチが届くまでの日数」をメーカー別に測る。
**計測**: メーカーのファーム配布サーバを定期取得して版数と公開日を記録し、CVE公表日との差を計算。
**トラフィック源**: 購入前検索、セキュリティ報道。
**隣接アフィリ**: ルータ買い替え、VPN、セキュリティ製品。
**堀**: 遅延日数の年表。
**敵対的検索**: `consumer device security patch latency index measured how fast vendors update routers phones tracker`（2026-08-29）
**発見**: **android-device-security.org** https://www.android-device-security.org/attributes/ （確認日 2026-08-29）、Anant Shrivastava の Android Device Security Patch Tracker https://anantshri.medium.com/android-device-security-patch-tracker-ec732672d9aa （確認日 2026-08-29）。**Androidは既に占有**。ルータ側は「平均2.3年に1回の大型更新、68%が自動更新非対応」といった調査はあるが継続トラッカーは見つからず。
**判定**: **Android=飽和、ルータ=部分空白**。ルータ限定なら生存。
**合法性**: 公開配布サーバの取得。問題は小さい。
**弱点**: ルータのファーム配布は機種ごとにバラバラで自動化が難しい。C01と装置が重複し、C01の方が題材として強い。

---

### C23. ブランドドメイン失効レーダー（Expiry Radar）

**一行**: 有名企業・自治体・学校のドメインの有効期限を追い、「失効寸前」「失効して第三者が取得した」瞬間を検知する。
**計測**: WHOIS/RDAP と DNS を定期取得し、期限・NS変更・登録者変更を検知。証明書透明性ログと突合してなりすまし候補を洗う。
**トラフィック源**: 報道（企業ドメインの失効は必ずニュースになる）、セキュリティ界隈。
**隣接アフィリ**: ドメイン管理、監視サービス、セキュリティ。
**堀**: 失効イベントの履歴。
**敵対的検索**: `certificate transparency phishing lookalike domain consumer facing new scam sites radar public feed`（2026-08-29）
**発見**: **B2Bブランド保護で飽和**（Bolster, Breachsense, Styx, Hardenize。確認日いずれも 2026-08-29）。crt.sh / Censys は既知プレイヤー。
**判定**: **飽和寄り → 弱い**。消費者向けの角度（ScamAdviser的）も既存が強い。
**弱点**: B2B前提の領域で、⑥に反する。掲載は一覧の網羅性のためであり、推奨しない。

---

### C24. AIモデル差し替え検知（Model Swap Detector）

**一行**: 同じ名前のモデルの中身が黙って変わっていないかを、行動指紋で毎日確かめる。
**計測**: 固定プローブ集への応答分布（logprob、拒否パターン、埋め込み）を毎日取り、変化点検定で差し替え・量子化を検出。
**トラフィック源**: 開発者コミュニティ、報道。
**隣接アフィリ**: AIサブスク、API仲介。
**堀**: 差し替えの日付の記録。
**敵対的検索**: `detect silent model swap LLM fingerprint provider changed model behind same name measurement`（2026-08-29）
**発見**: **Pebblous「Silent AI model updates: 16 providers measured」** https://blog.pebblous.ai/report/silent-model-updates-disclosure-gap/en/ （確認日 2026-08-29）が**既に16プロバイダを実測**。OSS **fpverify** https://github.com/Mohamed7415/fpverify （確認日 2026-08-29）、arXiv の行動指紋論文複数、CISPA監査（2026年3月、shadow API の45.83%が同一性検証に失敗）。
**判定**: **飽和 → 棄却推奨**。既知の aistupidlevel / Artificial Analysis とも重なる。一覧掲載は網羅性のため。

---

## 2. 敵対的検索を通過したトップ5

順位は「①〜⑥の封筒適合 × 検索で残った空白の広さ × ソロで実際に着手できるか」で決めた。

---

### 第1位: C01 クラウド死亡観測所

**なぜ1位か**: 依頼主が挙げた「Tracerouteで全世界の障害を検知」という**形と最も同型**である。分散した観測点から他人のインフラを常時叩き、異常を人間より先に見つけ、消費者が検索する言葉（"is X down" ではなく "is X still supported"）に着地する。そして traceroute 版と違い、**この題材には ThousandEyes も Catchpoint も Downdetector も入っていない**——彼らは「今落ちているか」を見るが、「二度と戻らないのか」は誰も見ていない。

**検索クエリと結果**（全て 2026-08-29）:

| クエリ | 結果 |
|---|---|
| `IoT device cloud shutdown bricked tracker database smart home discontinued server abandoned` | 報道とGitHub手動リスト（unixorn/internet-of-trash）のみ。計測系なし |
| `smart home device end of support tracker when cloud service dies monitor database IoT sunset` | 「専用のend-of-supportトラッカーDBは見つからなかった」。Belkin Wemo 2026-01-31終了、Nest 1/2世代、Devolo等の個別報道 |
| `"will stop working" list smart devices discontinued support database site tracks` | **US PIRG Electronic Waste Graveyard** が唯一の該当。100点超、手動、年次 |
| `PIRG "Electronic Waste Graveyard" database how many devices tracked methodology` | 100製品超、ブランド/カテゴリ/失われ方でソート可、累計17億ポンド換算。**計測でも監視でもなくアドボカシー資料** |
| `スマート家電 IoT クラウド サービス終了 使えなくなる 一覧 監視 サイト 通知` | Qrio・LINE CLOVA・RATOC等の**個別事件記事のみ**。「一覧で監視するサイトや通知機能に関する情報は見つからなかった」 |

**通過理由**: 唯一の近接競合PIRGとの差が4つとも構造的（自動計測／予兆検出／全球／通知）。FTC調査で「89%が終了時期を非開示」＝**測る以外に知る方法がないことが公的に確認されている**。⑥のトラフィックは報道引用が構造的に発生する型で、アフィリは買い替え需要に直結。監視型（加点）が自然に作れる。

---

### 第2位: C03 アドレス流出台帳

**なぜ2位か**: **⑤の時系列の堀が本一覧で最も強い**。登録日そのものが資産であり、後発は資金でも計算力でも追いつけない。かつ、隣接アフィリ（データ削除代行、エイリアス、VPN）が単価の高い帯に一直線で並ぶ。

**検索クエリと結果**（全て 2026-08-29）:

| クエリ | 結果 |
|---|---|
| `email honeypot unique address per company which companies share sell your email measurement study tracker` | 手法は既知（ACM 2025論文、Email Geeksの実践報告）。**「どの企業が売っているかを列挙した包括的調査は見つからなかった」** |
| `"which companies" sell share your email address public database spam per company signup test` | データブローカー一般論のみ。**「企業別のテスト結果の一覧は含まれていない」** |
| `email alias service detects which website leaked your address public leaderboard SimpleLogin Addy statistics` | **EmailAlias.io（leak detection付き）** が最接近。ただし**「公開リーダーボードや企業別統計に関する情報は見つからなかった」** |
| `迷惑メール 登録した企業 特定 エイリアス 実測 どの企業が売っているか 調査` | エイリアス活用の解説記事のみ。**「どの企業が実際にメールアドレスを売っているかという具体的な調査結果は含まれていない」** |

**通過理由**: 4クエリすべてで「手法は既知、台帳は不在」という同じ形の結果が出た。**道具は売られているのに、その道具で測った結果が誰も公開していない**——これは最も安全な空白の形である（需要が実証済みで、供給だけが無い）。

**ただし、自薦への追加の厳しさ**: EmailAlias.io が集計ページを足せば構造的優位は消える。**この案の防御はコードではなく「登録日」だけ**である。したがって、もし着手するなら**当日から数百社への登録を始めること自体が事業の開始**であり、サイト構築は後回しでよい。逆に言えば、着手が遅れるほど価値が減る唯一の案でもある。

---

### 第3位: C05 同意実効性観測所

**検索クエリと結果**（全て 2026-08-29）:

| クエリ | 結果 |
|---|---|
| `cookie banner reject all actually works measurement study tracking still happens consent violation automated` | 学術のみ。BannerClick（研究プロジェクト）、アムステルダム大（EU97,000サイトの65.4%が拒否後も収集）、arXiv複数。**継続運用の公開サービス無し** |
| `dark pattern longitudinal monitoring automated archive website changes over time deceptive design tracker` | arXiv論文群のみ（DECEPTICON、AidUI、50 Shades等）。「4時間ごとに監視」した研究はあるが**研究期間限定** |
| （既知確認）Blacklight / The Markup | 単発スキャン。**拒否ボタンを押さない。履歴を残さない** |

**通過理由**: 既知プレイヤーリストにある Blacklight との差が**測定行為そのもの**にある（押すか押さないか）。学術が繰り返し「守られていない」と示しているのに、誰も継続監視していない。規制当局・NGOによる被引用は、フォロワーゼロの個人にとって唯一現実的な初期集客経路である（第14ラウンドの「初期集客は例外なくニュース事件か既存トラフィック」という結論と整合する）。

**自薦への厳しさ**: **⑥のトラフィック要件を満たす確度がトップ5で最も低い**。消費者はこの質問を検索しない。もし採るなら、C03/C05/C08 を「プライバシー計測所」として1つの面に統合し、C03の検索需要でC05を養う設計にしない限り単独では立たない。

---

### 第4位: C06 デジタル改悪台帳

**検索クエリと結果**（全て 2026-08-29）:

| クエリ | 結果 |
|---|---|
| `enshittification tracker features removed from apps over time archive what changed downgrade` | 概念解説と個別事例（Netflix Interactive廃止、Evernote 50ノート制限）のみ。**「機能削除を記録した公開アーカイブは見つからなかった」** |
| `free tier changes tracker cloud services free plan shrinking history monitor` | **agentdeals.dev** が開発者ツールの価格変更287件超をタイムライン化。**消費者向けアプリの機能削除は対象外** |
| `SaaS pricing page change tracker developer tools price history GitHub Figma Notion monitor` | **飽和**（SaaS Price Pulse、SaaS Price Tracker、PricePulse 44社を1時間毎、Apify actors、PageCrawl、Verid）。ただし**全てB2B競合監視** |

**通過理由**: 価格軸は完全に埋まっているが、**機能軸は空いている**という明確な境界が引けた。かつ「価格は上がっていないのに中身が減った」は価格トラッカーが構造的に検出できない現象である。

**自薦への厳しさ**: バズは大きいがアフィリ商材が弱く、事件駆動でトラフィックが不安定。**⑥の「繰り返し見に来る」を満たさない**。第14ラウンドの「眺め見型 vs 監視型」の区別で言えば眺め見型であり、通知課金への道が細い。

---

### 第5位: C07 地理ブロック地図帳

**検索クエリと結果**（全て 2026-08-29）:

| クエリ | 結果 |
|---|---|
| `geoblocking measurement which websites block visitors from country tracker GDPR blocked US news sites Europe` | **ミシガン大の単発研究のみ**（Top 10K × 177か国、国あたり中央値3ドメイン、最大シリア71）。継続サービス無し |
| `AI service availability by country tracker which countries can access ChatGPT Gemini Claude rollout map` | **voidly.ai AI Censorship Index（130か国）** が存在。**AIサービス限定** |
| `feature availability by country locale tracker which features missing in Japan Europe measured product parity` | 該当トラッカー無し（EC商品/医薬品の別物のみ） |
| `same website different content by country measurement geo content divergence what visitors see study` | SEO解説記事のみ。計測プロダクト無し |

**通過理由**: 既知プレイヤー（OONI/IODA/Censored Planet）が**国家検閲**を測るのに対し、**企業の自主的閉鎖**は誰も測っていないという排他的な境界が確認できた。VPNアフィリという単価の高い商材と題材が一致する数少ない案。

**自薦への厳しさ**: **VPNのSEOは世界最激戦区**であり、フォロワーゼロ・予算ゼロで収益語彙に届く見込みは低い。ロングテール（"is X available in Y"）に限れば取れるが、それはCPMの低い面である。加えてデータセンターIP遮断との区別という技術的な偽陽性問題があり、ランニングコスト（VPS 20〜40台）も本一覧最大。**5位に置いたが、4位以上との差は小さくない。**

---

## 3. 提出前に自ら棄却したもの（14件）

「良さそうに見えたが、検索して落ちた」記録。すべて 2026-08-29 実施。

### R01. 地域別価格差の実測（同じSaaS/アプリが国で違う値段）
**当初の期待**: 最有力候補。VPNアフィリと完全一致、世界規模、検索需要大。
**実行クエリ**: `app store subscription price by country tracker history database` / `SaaS regional pricing difference tracker geographic price discrimination measurement` / `サブスク 国別 価格 比較 一番安い国 VPN サイト`
**発見**: **完全飽和**。AppPriceLens（175か国超・50アプリ超）https://apppricelens.com/ 、AppPriceWatch（30か国超）https://apppricewatch.com/ 、viewappprice.com、Adapty Price Radar（50か国超、B2B）https://adapty.io/subscription-price-radar/ 、PricePush。日本語圏でも **VPN Life が28か国3サービスの比較ツールを公開済み** https://note.com/vpn_life/n/nd9d7c7c491ff 。
**棄却理由**: 英語圏3社＋日本語圏1社が同一の出力を無料で出している。差分が作れない。**「自分の推し案ほど厳しく」の指示に従って追加検索した結果、1位候補が最初に落ちた。**

### R02. サブスク値上げ履歴の台帳
**実行クエリ**: `subscription price increase history tracker Netflix Spotify price hike database`
**発見**: **飽和**。streamingpricetracker.com 、keepingupwithinflation.com/tracker/streaming-wars/ 、**RecurDash（235サービス）** https://recurdash.com/subscription-pricing 、pricetimeline.com 、SubBuddy、Global Inflation Calculator（17サービス）。
**棄却理由**: 6サービス以上が同じ台帳を作っている。時系列の堀も既に他人が持っている。

### R03. 無料枠縮小ウォッチ（Free Tier Watch）
**実行クエリ**: `free tier changes tracker cloud services free plan shrinking history monitor`
**発見**: **agentdeals.dev /pricing-changes** が287件超を型別・年別・カテゴリ別のタイムラインで既に提供。
**棄却理由**: 直撃。C06（機能削除）に軸をずらして残した。

### R04. SaaS価格ページ監視
**実行クエリ**: `SaaS pricing page change tracker developer tools price history GitHub Figma Notion monitor`
**発見**: **飽和**。SaaS Price Pulse、SaaS Price Tracker、PricePulse（44社・1時間毎diff）、Apify actors 3種、PageCrawl、Verid（API+SDK）。
**棄却理由**: 飽和かつ全てB2B（⑥に反する）。

### R05. 利用規約の変更追跡
**実行クエリ**: `terms of service change alert consumer tracker what changed plain English monitoring`
**発見**: **飽和**。**TOSTracker（91,789文書）** https://tostracker.app/ 、Policy Change Radar https://policychangeradar.com/ 、Visualping、PageCrawl。既知プレイヤーの OpenTermsArchive に加えて商用が複数。
**棄却理由**: 既知リストの想定を超えて商用が増えており、差分が無い。

### R06. ゲームサーバのping実測
**実行クエリ**: `game server latency ping measurement global comparison tracker esports`
**発見**: **飽和**。Pong.com（19ゲーム、実データセンター併設エッジから計測）、checkping.io（23ゲーム）、pingtestlive.com（100+サーバ）、gamepingr、tolzon、gameserverping.net。
**棄却理由**: 6サービス以上。

### R07. AIサービスの国別提供状況
**実行クエリ**: `AI service availability by country tracker which countries can access ChatGPT Gemini Claude rollout map`
**発見**: **voidly.ai AI Censorship Index（130か国、13サービス）**、aistatus.org、lmmarketcap.com/status（427モデル/60プロバイダ）。
**棄却理由**: 直撃。C07で「AI以外のウェブ全体」に広げて残した。

### R08. 偽レビュー判定
**実行クエリ**: `fake review detection site after Fakespot shutdown 2026 review authenticity checker alternative`
**発見**: **飽和**。Fakespot は2025-07-01に終了、ReviewMeta も2026年初に停止したが、**空白は即座に埋まった**——FakeFind https://fakefind.ai/ 、RateBud（Amazon 20か国対応）https://www.ratebud.ai/ 、ReviewAI、SureVett、Knockoff、さらに**Firefox内蔵のReview Checker**。
**棄却理由**: 「大手が撤退した＝空白」という直感が最も危険であることの実例。**撤退から1年で6社以上が参入していた。**

### R09. 配信停止コンテンツの追跡（delisted games/streaming）
**実行クエリ**: `delisted removed digital games ebooks streaming content disappeared tracker archive database`
**発見**: **飽和**。delistedgames.com 、Steam Tracker（7,782タイトル削除を記録）、Wikipedia の List of delisted video games、gertlushgaming の Delisted Games Database。
**棄却理由**: ゲーム領域は完全占有。他媒体は需要が薄い。

### R10. ウェブページの広告占有率
**実行クエリ**: `website ad load measurement tracker how many ads news sites page weight over time index`
**発見**: **adbloat.com（2026）** https://adbloat.com/ が「46の実トラッカーをブラウザで発火させ、MB・リクエスト数・年間ロード時間を報告」。Pingdom のトラッカー影響調査も既存。
**棄却理由**: 直撃。

### R11. AIの政治的バイアスの定点観測
**実行クエリ**: `LLM political bias tracker over time measurement TrackingAI model answers change monitor`
**発見**: **TrackingAI.org が毎日16チャットボットに62問のpolitical compassを投げて全回答をDB化**。OpenAIの自社評価（約500プロンプト/100トピック）、Manhattan Institute、LLM-PLI。
**棄却理由**: 直撃。C12で「言語・地域による拒否の非対称」に軸をずらして残したが、それも防御は薄い。

### R12. アプリ肥大化指数（App Bloat Index）
**実行クエリ**: `app size bloat index tracker apps getting bigger over time measurement app store download size history`
**発見**: **BloatWatch.org（400アプリ超の独立オブザーバトリ）** https://bloatwatch.org/ 。開発者側はSentry Size Analysis、Emerge Tools。TRG Datacentersの10年推移調査も既存。
**棄却理由**: 直撃。「面白くて誰もやっていなさそう」な案ほど既にやられている。

### R13. AIモデルの黙った差し替え検知
**実行クエリ**: `detect silent model swap LLM fingerprint provider changed model behind same name measurement`
**発見**: **Pebblous が16プロバイダを実測公開済み**、OSS fpverify、arXiv行動指紋論文複数、CISPA監査。既知の aistupidlevel とも重複。
**棄却理由**: 飽和。一覧にはC24として網羅性のためだけに残し、推奨しない。

### R14. SMSフィッシング（smishing）の全球観測
**実行クエリ**: `smishing SMS spam honeypot global measurement phone numbers multiple countries scam text database`
**発見**: **Hiyaが10万本超のハニーポット電話回線を複数国に保有**。ACM IMC 2025の研究（64.5k件の報告画像、66言語）。
**棄却理由**: 装置の規模でソロが勝てない（10万回線 vs 現実的に20回線）。日本の「電話番号検索」領域も電話帳ナビ/jpnumber等で飽和。

**補足で落としたもの**: リゾート料金DB（resortfeechecker.com が2,000ホテル超で占有）、Androidパッチ遅延（android-device-security.org が占有）、フードデリバリー実配達時間（Intouch Insightの600件覆面調査＋物理的な注文コストでソロ不可）、AI生成コンテンツ比率（Graphite/Ahrefs/Originality.aiが占有）、AIクローラーのrobots.txt許諾変化（Cloudflare Radar＋KI-Zugangsindex＋HasData AI Crawler Block Index）。

---

## 4. 全体の自己申告

### この一覧が満たしていない可能性のあること

1. **④「ソロ＋AIで運用可能」を本当に満たすのは半分以下**。C09（解約導線）、C19（サポート応答）、C20（カメラ許諾）は人力か交渉が律速で、④に実質抵触する。C02も実機購入コストが線形。
2. **⑥のトラフィックを構造的に満たすのは C01・C06・C07・C09 の4件だけ**。C05・C13・C21 は報道と専門家に依存し、広告収入の母数が作れない懸念が残る。第14ラウンドが「広告は収益化序列の最下位」と結論づけた点は、依頼主の宣言（広告・アフィリで始める）と正面から衝突したままである。本ラウンドはその衝突を解消していない——**アフィリ単価の高い商材（データ削除代行、VPN、買い替えガジェット）に隣接する案を上位に置くことで緩和を試みただけ**である。
3. **「自分で計測」の定義の揺れ**。C11（GTFS-RT保存）は「他人の配信の保存」に近く、封筒①との緊張が最も強い。C08（ストアのラベル取得）も「他社の自己申告の収集」であって計測ではない。この2件は厳密には封筒違反と判定される余地がある。
4. **法的リスクで実質棄却すべきものが上位に混ざっていない代わりに、面白い案が落ちている**。C16（パーソナライズ価格）とC17（総額実測）は題材として本一覧で最も強い部類だが、EC規約・anti-bot・Ryanair判例・hiQの結末を踏まえてトップ5から外した。**これは臆病な判断かもしれない**——依頼主が法的リスクを取る用意があるなら、この2件は再評価に値する。
5. **本ラウンドは第9〜14ラウンドの結論（住まいクラスタ／へやログ）と接続していない**。封筒が入れ替わったため別空間を探索したが、**過去6ラウンドの資産（不動産の法的整理、Kyero経路、確信度61%）は本一覧のどれにも引き継がれていない**。もし本ラウンドの案に進むなら、それは方向転換であって発展ではない。

### 本ラウンドで最も価値があったと思う発見

**「大手が撤退した領域は空白ではない」**（R08、Fakespot）。Mozillaが2025年7月にFakespotを閉じ、ReviewMetaも2026年初に消えたが、1年で6社以上が参入していた。**撤退は需要の証明であって供給の不在ではない。** 同じ論理は「学術研究がある領域」にも当てはまるが、符号が逆になる——**論文は一度測って終わるので、継続測定の空白を証明する。** 本ラウンドのトップ5は全てこの非対称性の上に立っている。
