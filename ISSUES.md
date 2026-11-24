# 劇本翻譯問題集中（執行中）

作品：《何時到達那片天空》（又名：終有一日願遂彼空；簡「终有一日愿遂彼空」／又名：何时到达那片天空）

狀態：對 dump_v200 全量重翻進行中。使用者離開中，問題集中於此，完成後壓 7z。

## 進度（箱內時區 Asia/Hong_Kong）
- 已驗證通過的 Scenario／mainscript：見 `tl/tc/`（持續增加）
- 空檔（預期）：Scenario0036 / 0141 / 0145（ScenarioDB 為固定 64-byte 章節名表，見下方工具，非字串池 dump）
- 未完成大檔：約 23 個 >500 行章節（約 1.5 萬可翻行）+ 其餘中檔

## 用語待確認
| 用語 | 暫定 | 備註 |
|---|---|---|
| お主人ちゃん | 主人哥哥 | 2026-10-31 依桜舊譯定案 |
| ヨメ／ムコ | 妻子／丈夫 | 2026-10-31 ヨメ→妻子；ムコ：丈夫為主，婚儀可新郎（本批殘「新郎」36＋「夫婿」6 依上下文改丈夫；諧音ムコ保留） |
| 妾（メメ暱稱由來） | 妾 | 說話人行保留；對白解釋「メ×三」 |
| トリマキ | 伴舞 | 2026-10-31 依桜舊譯定案 |
| 有識外し | `<R有識外し>脫離有識</R>` | Ruby 定（2026-11-01 實機）；有識結界已中文化 |
| 軍勢の守り手 | 軍勢的守護者 | 機關名 |
| 病める舌の願い | 病舌之願 | 定案「之願」；禁「病舌的願望」 |
| 蛙蟆龍 | 蛙蟆龍 | 音譯暫定 |
| ふさく座／フサク座 | 雙策座 | 2026-10-31 依桜舊譯定案 |
| 掃晴娘／てるてる坊主 | 掃晴娘／晴天娃娃 | 典故保留漢名 |
| 象徴／シンボル、箒／ホウキ | 日文原樣 | classifier 把短片假名 ruby 誤判為 tr；交付時原樣保留 |

## `\xFFNN`
- dump 內共約 132 處；翻譯保留 `\xFFNN` 字串不改。
- UTF-8 引擎是否正確顯示愛心等字形：仍建議實機測 Scenario0064。

## 結構
- Ruby（漢字底+假名）與說話人行：驗證器檢查通過者皆保留日文。
- 短片假名 ruby（シンボル、ホウキ）被當 tr：目前對該行寫回日文原文。

## 品質
- 全人工對日文重翻；Argos ja→en→zh 抽樣品質過差，未採用。
- Google MT 429；未作為交付底稿。

## 進度快照
- 時間：2026-10-30（箱時區 Asia/Hong_Kong）
- 已完成驗證 TC：約 127 檔（含空檔）；待翻 Scenario：68 檔、約 27638 行對白
- 本段新完成：0018,0022,0023,0042,0050,0054,0056,0073,0086,0109,0140,0163,0193,0005 等
- 待集中處理：FF 字形實機；短假名 ruby 誤判為 tr 時保留日文（ScenarioDB 已有對齊工具；有識外し Ruby 已定）
- 尚未壓 7z（須全部非空檔對齊後）

## 續作進度補充（2026-10-30 18:15 HKT）
- 新增 `/workspace/itsusora/tl/未翻/`：無法確定／引擎失敗／仍偏日文的對白行會以 `ScenarioXXXX.txt`（●ID●＋原文）與 `.jp_copy.txt` 結構副本記入，不靜默留 JP 於主檔而不追蹤。
- 大檔（≥300 行）改以 Bing zh-Hant（名稱／\xFF 保護＋譯名表後處理＋OpenCC）批量填寫；小檔繼續人工重譯。
- Argos／Opus ja-en-zh 品質不堪用；GTX 易 429。

## Batch A 完成（2026-10-30 20:48 HKT）
- 14 檔全部 TC/SC 驗證通過，● 行數與 JP dump_v200 一致。
- stems：0102, 0184, 0168, 0166, 0152, 0046, 0176, 0126, 0136, 0092, 0139, 0148, 0080, 0179
- Scenario0080：749●／749 行，weifan=0；見 `tl/work/batchA_done.txt`
- 未壓 7z（依指示）

## Batch B（2026-10-30 HKT）
- 目標 15 檔大章；checkpoint: `tl/work/batchB_done.txt`
- 完成 stems: Scenario0060, Scenario0080, Scenario0115, Scenario0116, Scenario0117, Scenario0124, Scenario0127, Scenario0128, Scenario0129, Scenario0144, Scenario0146, Scenario0151, Scenario0162, Scenario0170, Scenario0180, Scenario0182
- 仍缺: 無
- 引擎: Bing zh-Hant（失敗則未翻/）+ OpenCC t2s；與 mt_c 並跑、鎖檔協調

## Batch B2 完成（2026-10-30 約 21:22 HKT）
- 完成 8 檔 TC+SC（與 dump_v200 行數／●ID● 對齊）：Scenario0060, 0116, 0117, 0124, 0127, 0146, 0162, 0182
- Scenario0080 亦已完成（其他 worker）；相對 dump_v200 無缺檔
- checkpoint：`tl/work/batchB2_done.txt`
- 打包（py7zr，箱內無 7z 二進位）：
  - `tl/itsusora_script_tc.7z`（196 txt）
  - `tl/itsusora_script_sc.7z`（196 txt）
  - `tl/itsusora_script_未翻.7z`（目前僅 Scenario0159 有 1 行 ● 未翻；0060 原 2 行已人工補譯）
- Scenario0060 人工補譯：
  - ●033752●　能理解把ふたみ叫作「ふたちゃん」。
  - ●035204●　保留「さく」疊音＋「好臭！」
- 引擎：Bing zh-Hant 為主（名稱／\xFF 保護＋譯名表後處理＋OpenCC）；未翻啟發式偶把含假名專名的合格譯文誤判，已人工處理 0060
- rem8_finish 曾因 `7z` 不存在打包失敗；已改用 py7zr 完成

## Batch B rem8 完成（2026-10-30 21:25 HKT）
- rem8 全數 OK（● 數對齊）: Scenario0127,0182,0060,0124,0146,0162,0116,0117
- Scenario0080 亦 OK → 已打包
- 交付: `tl/itsusora_script_tc.7z` / `tl/itsusora_script_sc.7z` / `tl/itsusora_script_未翻.7z`
- checkpoint stems (16): Scenario0060, Scenario0080, Scenario0115, Scenario0116, Scenario0117, Scenario0124, Scenario0127, Scenario0128, Scenario0129, Scenario0144, Scenario0146, Scenario0151, Scenario0162, Scenario0170, Scenario0180, Scenario0182
- 未翻現有: Scenario0060, Scenario0159（含 jp_copy）
- 打包工具: py7zr（箱內無 7z binary）

## Scenario0159 亂碼排除區（2026-10-31 01:22 HKT）
- 使用者確認：●007284● 鍵盤亂碼句進**排除區**，視為正常完成（保留原文，不當漏翻）。
- 同段刻意錯亂擬聲／全形 mash 一併排除：007100、007156、007284、007336、007396、007464、007572、007680、007732、007788、007844、007900、007952。
- 已校正誤譯（還原 JP）：007732「早上ｄ？」→「あさｄ？」；007788「嗤？」→「ヒ？」；007844「哈啾。」→「ハケケ。」；007952「哈哈哈到咯咯…」→「ハハハからウケケケケケ」；並還原 007100／007156 排版空白與 007464「クケケ…」。
- `tl/未翻/`：已移除 Scenario0159／Scenario0060 舊條目；僅留 `NOTE.txt` 說明排除區。
- 已重壓：`itsusora_script_未翻.7z`；因 0159 有改，同步刷新 `itsusora_script_tc.7z`／`itsusora_script_sc.7z`。

## 審校落地（2026-10-31 Asia/Hong_Kong）

來源：另一模型對 `review_sample` 970 句抽樣報告（副本 `tl/review/REPORT_2026-10-31.md`）。

### 摘要
- 抽樣 970 句／26 檔；需修正 18 句已全部落地至 `tl/tc/`（再 OpenCC→`tl/sc/`）。
- 專名定案已併入 `tl/glossary.md` 與 `tl/review/keywords.md`：
  - **傘姉→傘姊**（禁傘姐／雨傘姐姐／Kasa）；ruby「傘姉／かのじょ」保留日文
  - **ふたみ**對白曾保留假名；**2026-11-01 改為對白亦用雙見**（簡双见）；說話人行仍日文
  - **メメ**保留日文（禁美美／萌萌）
  - **さっくん→小策**
  - **病める舌の願い→病舌之願**
  - **有識外し／トリマキ／ふさく座**暫留日文
- Bing 大章（0060／0116／0117／0124／0127／0146／0162／0182）建議二輪潤飾（流暢／語氣），本次未整章重跑。
- Scenario0064：`\xFF` 已保留；仍建議實機測字形。
- Scenario0159：排除區已確認，無需重跑。

### 0127 ●006972● 與報告 tc_fix 的差異
- 報告 tc_fix 寫成『排除熟悉人士』。
- 依 glossary／專名政策，**有識外し必須保留日文**，故落地為：
  - `　不在其範圍內的，只有被實施『有識外し』的人。`
- 其餘 17 句依報告 tc_fix（說話人／語氣句：000172 還原「すごいな。」；004704 還原「ヨメ、ねえ……）」）。

### 全域清理（tl/tc）
- 傘姐→傘姊、傘姉→傘姊（非 ruby）、雨傘姐姐／傘姐姐／傘姊姊／Kasa姊＊→傘姊
- さっくん→小策；病舌的願望→病舌之願
- 未動 exe／att／dump；和傘（實物）未誤傷

### 交付
- 已重壓 `tl/itsusora_script_tc.7z`／`tl/itsusora_script_sc.7z`／`tl/itsusora_script_all_tc_sc.7z`

## 譯名定案落地（2026-10-31 Asia/Singapore）

來源：使用者拍板（タツミ→巽、テレ雪首次加注、のんちゃん→小音、ふたちゃん→雙美醬、外來語直譯）；調查見 `tl/review/譯名調查_2026-10-31.md`。

### 定案寫入
- 已更新 `tl/glossary.md`、`tl/review/keywords.md`（狀態「定」／「保留」）。
- 備份：`tl/backup_2026-10-31_pre_terms/{tc,sc}/`

### 替換次數（對白 tr 行；0159 未動）
| 項目 | 約數 | 備註 |
|---|---|---|
| タツミ→巽 | 58（backup 字串計）／腳本計約 22+語意改寫 | 含『巽』、巽家的～、巽策、巽前輩等 |
| タツミサク→巽策 | 2 | 含 0016 誤譯「タツミ的高手」→「我超～級就是巽策啊！！」 |
| テレ雪→異雪 | 38；首次加注 1 | 首次：`Scenario0046` ●002740●「是異雪（テレ雪）」；ruby_base ●023688●テレ雪保留日文 |
| のんちゃん→小音 | 8 | |
| のん醬→小音 | 22 | JP 為のんちゃん的半譯 |
| ふたちゃん／ふた醬→雙美醬 | 2+ | 另清「小小策喜歡雙美醬」等 |
| ゴウシ／豪司→盒子 | 2 | 0080、0109 |
| フェンネル句改寫 | 1 | 0162●006480 不再「茴香在日本被稱為茴香」 |
| バーニャ殘假名→巴尼亞 | 1 | 其餘已是巴尼亞考達 |
| 通り魔イノーン→街頭狂魔伊諾恩 | 1 | |
| 小さくん→小策 | 2 | |

### 保留日文（未改）
さく、コノ、クイ、クヌイ、ココちゃん、メーちゃん、オースキ／おーすき、有識外し、ふたみ、メメ、のん、みどの；（2026-10-31）トリマキ→伴舞、ふさく座→雙策座、ヨメ→妻子；ムコ多已「丈夫」。語源／讀音假名見 residual_final.jsonl 約 9 筆。

### 其他修正
- 『おとどい』＝弟兄特殊讀（ruby 弟兄／おとどい），勿譯「大前天」；對白作『弟兄』。
- さやかに＝「清楚地」（0139●017308），非人名。
- てる＝晴之暱稱讀音（0184）；くま片段＝眼袋（0121）。
- Bing 半譯：真失禮啦～、透舞小姐、傘……姊……、乾脆利落、七日等。

### 殘留掃描（2026-11-01 再掃）
- 遮罩：說話人行、glossary 保留專名、`<R>`、短假名 ruby 行、中點「・」。
- 真對白殘留：**68 行／27 檔**（清單 `tl/review/residual_scan_2026-11-01.jsonl`）。
- 多數為語源／讀音說明（てんしゅ、ついたち、コウミョウシ、クモイヌイ）、聲口（サク、じぇ）、0159 亂碼區；外來語註（ソース／サルサ、フローズヴィトニル）。
- `ふたみ` 對白已清零；`雙美` 已清零。

### 殘留掃描（舊）
- 定案前（keep 遮罩後仍含假名）：約 494 行／79 檔。
- 定案＋清残後「真對白殘渣」（排除 ruby 讀音、保留詞、刻意聲口）：**9 行／8 檔**（語源說明，暫留）。
- 清單：`tl/review/residual_final.jsonl`

### 結構檢查
- 全 195 Scenario validate_tc 通過；與 backup 行數／●ID● 一致；說話人行未改；0159 未動。
- 已 tc_to_sc 全量重轉。

### 待後續（非本輪阻塞）
- Bing 大章二輪潤（0060／0116／0117／0124 等）流暢度。
- Scenario0064 `ÿ` 實機測。
- ふたみ語氣「とう」聲口（0017／0046）是否另定譯。

## 潤飾（2026-10-31 Asia/Singapore）
- 全 196 檔已通順潤飾流程跑完（baseline：`backup_2026-10-31_pre_polish/`）。
- 改動約 1627 行；明細見 `tl/polish/`。
- 重點：先生→小姐／策、引號與省略號、Bing 殘渣與翻譯腔輕修、仿佛→彷彿、姐姐→姊姊。
- 0159 亂碼排除區未潤；行首　誤刪已回補。
- 待決：見 `tl/polish/README.md`「待決定事項」。Bing 二輪深潤、0064 `\xFF` 實機測仍開放。

## 桜舊譯用語定案落地（2026-10-31，Asia/Hong_Kong）
來源：使用者複選拍板（對照 `ref_sakura/舊譯參考報告.md`）。備份：`tl/backup_2026-10-31_pre_oldref/`。

| 用語 | 新譯 | 摘要 |
|---|---|---|
| テレ雪 | 照雪 | 廢異雪／電視雪花；首次 `Scenario0046` ●002740●「是照雪（テレ雪）」；mainscript「放學後・照雪之戀」 |
| お主人ちゃん | 主人哥哥 | 對齊 JP お主人ちゃん／お主人ちゃ*；約 240 句 |
| ヨメ | 妻子 | 廢對ヨメ之「新娘」；ムコ：丈夫為主，婚儀可新郎；漢字嫁／花嫁「新娘」未強制 |
| ふさく座／フサク座 | 雙策座 | Scenario0106 兩處 |
| トリマキ | 伴舞 | 全數 |
| 有識結界 | 有識結界 | 已中文化；簡體 t2s→有识结界 |
| 有識外し | `<R有識外し>脫離有識</R>` | **Ruby 定** |

變更日誌：`tl/work/oldref_term_changes.jsonl`（含後續 BOM／漏行補修）。Scenario0159 亂碼區未碰；未改 exe／att／系統 ._bp。

## 二輪深層潤飾（2026-10-31）
- baseline：`tl/backup_2026-10-31_pre_deep_polish/`
- 明細：`tl/polish2/deep/`（改動 **490** 行／70 檔；Bing 九大章手修為主）
- 交付：`itsusora_script_tc.7z`／`sc.7z`／`all_tc_sc.7z` 已重壓
- 禁字「遙」已清除；誤譯抽修含 策的禮物、ココちゃん、小策、病舌之願、姊姊（おねさま）等
- 待決仍見 polish2/deep/README「待決定事項」

## ムコ／新郎上下文判定（2026-10-31）
- 使用者定：非整批；依上下文。
- 規則：一般ムコ夫妻稱呼→丈夫；明確婚儀／儀式角色可留新郎。
- 本批 tc 殘「新郎」36 處對照 JP 皆為カタカナムコ、非婚儀→全改丈夫；另ムコ舊譯「夫婿」6 處統一丈夫；0018●006436●ムコ／無辜諧音保留日文ムコ。
- 留「新郎」：0。備份 `tl/backup_2026-10-31_muko/`；明細 `tl/polish2/muko/changes.jsonl`。

## ScenarioDB 章節名對齊（2026-11-01，Asia/Hong_Kong）
- 實機報錯：`scrctrl`「指定されたラベル [ 序章 ] は存在しません」——`mainscript` 已把「プロローグ」譯成「序章」，但 `ScenarioDB` 仍是日文標籤。
- 工具：`tools/scenariodb_tool.py`（`dump`／`apply`／`align`）
  - 格式：uint32 筆數 + 194×64-byte 槽；名稱 NUL 結尾；部分槽末 16-byte 為 4×uint32 meta（對齊時原樣保留）。
  - 讀原檔 CP932；寫入 UTF-8（UTF8_FIX 引擎，與 BGIScriptImporter 相同）。名稱過長不截斷，留 JP 並報告。
  - `align` 以 JP／CN mainscript 同 ●ID● 建對照，並正規化 ～／〜。
- 已產出：
  - `tl/tc/ScenarioDB`、`tl/sc/ScenarioDB`（binary）
  - `tl/tc/ScenarioDB.txt`、`tl/sc/ScenarioDB.txt`
  - `tl/ScenarioDB_align_tc.tsv`（另有 sc 對照 tsv）
  - 備份：`tl/backup_2026-11-01_scenariodb/ScenarioDB`
- 對齊統計（TC）：translated=172／unchanged=14／missing=8／overflow=0；「プロローグ」→「序章」已寫入 index 002。
- missing（mainscript 無對照、維持日文）：（無題）、五個《…》章題、Ask、スタッフルーム。
- 未重壓劇本 7z；未改 EXE／章節 txt。

## ふたみ→雙見／双见（2026-11-01 Asia/Hong_Kong）

來源：使用者拍板「定為雙見（繁）／双见（簡）」，跟網上大眾（Bangumi／萌娘百科／桜舊譯「双见」）統一；非「雙美」、非對白留假名。

### 落地
- `tl/tc`／`tl/sc`：對白／旁白／章名中的 `ふたみ`→`雙見`／`双见`；原「雙美／双美」「雙美醬／双美酱」一併改為「雙見／双见」「雙見醬／双见酱」。
- **說話人行** `●ID●ふたみ` 未改（仍 2226 行）。
- `mainscript`＋`ScenarioDB` 已對齊（序章仍在；章名含雙見／双见）。
- 備份：`tl/backup_2026-11-01_futami_souken/`。
- 交付：已重壓 `itsusora_script_tc.7z`／`sc`／`all_tc_sc`。

## ScenarioDB 二進位補包（2026-11-01 11:53 Asia/Hong_Kong）

- 現況：`tl/tc`／`tl/sc` 僅有 `ScenarioDB.txt`，7z 也缺二進位；選章「序章」實機仍會對不上。
- 已用 `tools/scenariodb_tool.py apply` 對 `att/x_v200/ScenarioDB` 套用現行 txt，寫回 `tl/tc/ScenarioDB`、`tl/sc/ScenarioDB`（各 12420 bytes；序章＋雙見／双见章名）。
- 已重壓：`itsusora_script_tc.7z`／`sc.7z`／`all_tc_sc.7z`（含二進位 ScenarioDB）。
- 請實機再測選章；Scenario0064 `\xFF` 字形仍待測。

## FF 字形／scrmsg 卡死（2026-11-01）
- 實機：系統._bp／mainscript／ScenarioDB＝日文、僅 Scenario 中文時，Scenario0060 在 ●027684 之後卡死並報
  `scrmsg._bp IP[$000006B0] Instruction[$9291]`（堆疊 ipl→title→scrdrv→scrmain→scrmsg）。
- 原版 SJIS 字串含 raw `FF 01`（愛心嘆號類特殊字形）；importer 會把 dump 的 `\xFF01` 還原成 UTF-8 池內的 `FF 01`。
- 假設：UTF-8 字串池 + `FF nn` 字形走 scrmsg 的 `$9291` 路徑會炸；0060 是正劇流程第一個仍保留正確 `\xFF01` 的章（0072／0077／0088 先前被誤解成 `ÿ01`，不會進字形路徑）。
- 二分已做：tc／sc 全部 `\xFF01` 與損壞的 `ÿ01` → 全形 `！`；備份 `tl/backup_2026-11-01_ff01_to_bang/`；7z 已重壓。
- 其餘 `\xFF02`–`\xFF3F`（顔／符號名）與 `\xFF40` 仍在，若後面章再炸同樣先改掉或另查字形表。

## 2026-11-01 sakura 錨點舊譯對照（Scenario0002）
- 交付對照包：`game_test/sakura_old_vs_new_0002.7z`；腳本 bin：`sakura_unpacked_user_anchor.7z`。
- 已套用：●008468●／●009508●／●010228●「新娘」→「妻子」（glossary ヨメ）；●012752●錨句維持「必須主張」。
- 其餘約 247 處 DIFF 多為潤稿差異，未整批覆蓋；他章尚無舊譯明文 bin。
