# 劇本翻譯問題集中（執行中）

狀態：對 dump_v200 全量重翻進行中。使用者離開中，問題集中於此，完成後壓 7z。

## 進度（箱內時區 Asia/Hong_Kong）
- 已驗證通過的 Scenario／mainscript：見 `tl/tc/`（持續增加）
- 空檔（預期）：Scenario0036 / 0141 / 0145、ScenarioDB
- 未完成大檔：約 23 個 >500 行章節（約 1.5 萬可翻行）+ 其餘中檔

## 用語待確認
| 用語 | 暫定 | 備註 |
|---|---|---|
| お主人ちゃん | 主人 | 與已完成檔一致；可改「小主人」 |
| ヨメ／ムコ | 新娘／新郎 | ふたみ自稱語氣濃時可保留「ヨメ」 |
| 妾（メメ暱稱由來） | 妾 | 說話人行保留；對白解釋「メ×三」 |
| トリマキ | トリマキ | 透舞對策的綽號，暫留日文 |
| 有識外し | 有識外し | 世界觀專有；待定譯或加注 |
| 軍勢の守り手 | 軍勢的守護者 | 機關名 |
| 病める舌の願い | 病舌之願 | 傘姐相關；可再潤 |
| 蛙蟆龍 | 蛙蟆龍 | 音譯暫定 |
| ふさく座／フサク座 | ふさく座 | 雙關「ふたみ+策」；對白內保留 |
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
- 待集中處理：有識外し；FF 字形實機；ScenarioDB 章節名另工具；短假名 ruby 誤判為 tr 時保留日文
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
