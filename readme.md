# 《何空》本機編譯整合包（繁中）

日期：2026-11-19（更新自 2026-11-15 版）

把這個資料夾解壓後，在裡面跑 `outputbig5.bat`。BAT 仍是逐條編譯指令（Scenario0000–0193、mainscript、ScenarioDB），編譯結果先寫入 `temp\`，再連同有功能修改的系統檔（`scrmsg`／`scrslct`）與 BitmapNameDB 放到 `outputbig5\`，供 Enigma Virtual Box 使用。用 `itsusora_UTF8_FIX.exe` 執行。

資料夾名叫 `big5` 只是為了沿用你原本的 BAT 路徑，裡面是 UTF-8 繁中，不是 Big5 編碼。

## 這包有什麼

| 路徑 | 說明 |
|------|------|
| `outputbig5.bat` | 逐條編譯＋套語音補丁，輸出到 `outputbig5`（給 Enigma Virtual Box） |
| `big5/` | 正式繁中 txt（196 檔：Scenario0000–0193、mainscript、ScenarioDB）。已含 0080「──那麼呢。」開引號修到 `巽殿」`；續行沒有把說話人寫進 txt |
| `source/` | 編譯用源 bin（`att/x_v200`：章檔、mainscript、ScenarioDB、BitmapNameDB） |
| `sysprg_big5/` | 只放有功能修改的共用系統檔 4 個（來源 `sys/out_common/`）：`scrmsg._bp`（8354 B，md5 `82c1d08b90f2403d10866c7da850e5b4`）、`scrslct._bp`（5264 B，md5 `e48c76e3703642df65779ce2dd3331f5`）、`logwnd._bp`（3760 B，md5 `c60c6337272612b74d8d5fd91399d338`）、`usdtwnd._bp`（6096 B，md5 `1dbeeb7b52d35077f24eb63e8004561c`，存檔畫面日期 UTF-8 修正 v2）。其餘系統檔不散佈，遊戲讀 `sysprg.arc` 內零售原版。 |
| `sys_nov6_orig/scrmsg._bp` | 還原用（md5 `7fa2bcdd5887e6153fc9a68e880caf54`），BAT 不會自動複製 |
| `BGIScriptImporter.py` | 章／mainscript 編譯器 |
| `scenariodb_tool.py` | ScenarioDB 請用這個，不要用章編譯器 |
| `apply_voice_align.py`、`sites.tsv` | 編譯後對 23 章 347 處變體點寫入 type=3 與中文名指標 |

BAT 順序是：逐條編譯全部腳本到 `temp\` → 複製到 `outputbig5\` → 用 `apply_voice_align.py` 把已對齊的 23 章蓋上去 → 再複製 `sysprg_big5` 內的 4 個系統檔（`scrmsg`／`scrslct`／`logwnd`／`usdtwnd`）與 BitmapNameDB。不要把 `temp` 在對齊之後再整份蓋回 `outputbig5`，否則補丁會被未對齊檔蓋掉。圖片檔（舊流程的 BIG5PIC）這包沒有，需要時可自行放進 `outputbig5`。

編譯後那 347 處續行會再顯示中文名牌，這是補丁的預期副作用。簡中、EXE、ARC 不在這包裡。解壓後產生的 `temp`、`outputbig5` 可刪。

未改 official 目錄。未在 Windows 上跑這份 BAT，但在本機用同一套工具與 txt 編譯了要對齊的 23 章：`applied=347 skipped=0 failed=0`。除 Scenario0080 因開引號修正少了 3 位元組外，其餘 22 章 md5 與先前 2212 對齊包一致。

## 2026-11-19 更新

- `big5/` 換成現行正式繁中 txt。和 11-15 版相比只有 Scenario0186–0191 不同：隱藏篇 typography 標點改為直行形（﹁﹂﹃﹄︵︶︙︱︐︒等，2989 處）。
- `sysprg_big5/scrmsg._bp` 換成正式新檔（8354 B，md5 `82c1d08b90f2403d10866c7da850e5b4`）：長度 3 標點＋隱藏篇傍點 `$14B` 修正＋直行句首／句末比對。其餘 46 個系統檔與正式 `out_tc` 相同。
- `prebuilt_outputbig5/`：已在本機照 BAT 順序編好的成品（244 檔，語音對齊 applied=347 failed=0；0186–0191 與已實測 bin md5 相同）。不想自己跑 BAT 可直接用這份。
- `exe_test/itsusora_UTF8_FIX.exe`：試玩 EXE（node3c_zero，md5 `5d560252325004f76876238065fda51d`）。隱藏篇「異ならぬ世の終わりより」要用這個，正式 EXE（`84a813e2…`）在隱藏篇會彈 `$9290`。這個 EXE 已是正式 `exe/patched/` 現行檔。

簡中、ARC、圖片仍不在這包裡。

## 2026-11-19 03:25（Singapore）更新：選項置中
- `sysprg_big5/scrslct._bp`、`prebuilt_outputbig5/scrslct._bp` 換成置中修正版（md5 e48c76e3703642df65779ce2dd3331f5，5264 B）。
- 原因：零售 scrslct 以「位元組數÷2×32 px」算選項寬，UTF-8 中文高估 1.5 倍而偏左／被切；新版逐字計寬（中文 32、英數 16）＋16 px 餘量（避免短選項如「天使」被換行裁成一字）。
- 已全線實測無誤；正式 sys/out_tc、out_tc_v200 已寫入（舊檔備份 sys/backup_20261119_slct_center/）。簡中 out_sc 未改。

## 2026-11-19（Singapore）更新：剩餘日文「可直接翻」寫入正式繁中

- 正式 `tl/tc` 已寫入清單中可直接採用的中文（備份 `tl/backup_20261119_remaining_jp/`）。本包 `big5/` 已與正式繁中 txt 同步。
- 本次寫入 82 個 txt、583 處正文（含後補 0193「メ……／み、」兩處），另調 202 處傍點行點數＝新底句字數。含：傍點底句、みどの→綠野、人名のん→音、愛々々／愛々→愛愛愛／愛愛、章標題（ScenarioDB 與 mainscript 同題，保留 `# meta=`）、弐壱→貳壹、簡體殘字等。
- **未改**：ruby、說話人行、控制碼、行序行數、原換行、アズ（需同步語音鍵）、系統 `._bp`、EXE、`tl/sc`、0193 typography 轉換、標題「異ならぬ世の終わりより」、以及諧音／音讀／行內 ruby／0159 亂碼等 28 處（見清單掃描說明）。
- 本機用同一套工具試編譯受影響 80 章＋語音對齊用的 0168／0178＋mainscript＋ScenarioDB：全部成功。`apply_voice_align` **applied=347 skipped=0 failed=0**。
- `prebuilt_outputbig5/` 已換成這次的編譯結果（23 章為對齊後 bin）。系統檔仍是上一版（含置中 `scrslct` 與直行 `scrmsg`），這次沒動。

## 2026-11-19 04:34（Singapore）更新：系統檔改為共用修改檔（out_common）

UTF-8 版系統檔內部字串不再分繁簡：引擎不會拿那些字串來顯示，不必再散佈整套 `._bp`。做法與舊漢化相同，只覆蓋真正有功能修改的檔，其餘維持零售原版日文（由 `sysprg.arc` 提供）。

- 正式共用目錄：`sys/out_common/`（由正式 `out_tc` 複製，不刪 `out_tc`／`out_sc` 等舊目錄）。目前兩檔：
  - `scrmsg._bp` 8354 B，md5 `82c1d08b90f2403d10866c7da850e5b4`：長度 3 標點、隱藏篇傍點 `$14B` hook、直行句首／句末比對。
  - `scrslct._bp` 5264 B，md5 `e48c76e3703642df65779ce2dd3331f5`：UTF-8 選項逐字計寬（中文 32、英數 16）＋16 px 餘量。
- `sysprg_big5/` 與 `prebuilt_outputbig5/` 已改為只帶上述兩檔；其餘 45 個系統 `._bp` 已從這兩個目錄移除（腳本 bin 未動）。`prebuilt_outputbig5/` 現為 199 檔。
- `outputbig5.bat`（CRLF）改為只複製這兩個系統檔，並加了說明。Linux 下模擬請先去掉 CR。
- 零售 2.00 的 `sysprg.arc`（對照 `sys/orig_v200` 與 `patch/extracted/decompressed/sysprg`）含 45 個 `._bp`，涵蓋被移除的遊戲用系統檔，不會缺檔。`ipl._bp`、`launcher._bp` 本來就不在 ARC 內（安裝／IPL 用，非遊戲執行必要），本次也不放入 `out_common`。
- 未改 EXE、`tl/tc`、`tl/sc`。只差字串的繁／簡檔（`ipl`、`launcher`、`logwnd`、`usdtwnd`）與僅 UTF-8 轉碼的 18 檔，均不散佈。

比對細節見本包附帶的 `tl/review/common_sys_20261119/NOTE.md`。

## 2026-11-19 04:40（Singapore）：共用系統檔加回 logwnd／usdtwnd
舊漢化也改過這兩檔，畫面會顯示（日誌「選項」分頁、存檔星期），故以 UTF-8 繁中版加回 sys/out_common、sysprg_big5、prebuilt_outputbig5，BAT 一併複製。
- logwnd._bp c60c6337272612b74d8d5fd91399d338
- usdtwnd._bp f6e279a4db159dc32588237a716fafd4
共用系統檔現為 4 檔：scrmsg、scrslct、logwnd、usdtwnd。

## 2026-11-19 13:35（Singapore）更新：存檔畫面日期修正寫入正式，並打整合包

- `usdtwnd._bp` 換成 v2（6096 B，md5 `1dbeeb7b52d35077f24eb63e8004561c`），已寫入 `sys/out_common`、`sys/out_tc`、`sys/out_tc_v200`、本包 `sysprg_big5` 與 `prebuilt_outputbig5`。舊檔（md5 `f6e279a4db159dc32588237a716fafd4`）備份在 `sys/backup_20261119_usdtwnd_pre_v2/`。
- 零售把日期轉全形的函式（@0x6A8）以 SJIS 兩位元組步进，UTF-8 三位元組會整行錯位亂碼。v2 不另接新程式段（上一版接到字串池後面，引擎不會執行），直接在原位改成原樣複製 UTF-8。數字因此為半形，例如「6月29日（四）」；日期前導 0 的位移已改為 0x05。
- 舊存檔標題是存檔當下寫入的，需重存才會更新格式。覆蓋確認框註解看起來被裁，是輸入欄游標在句尾、欄位偏窄，`yesnownd` 未改。
- 本機已實測新存一筆，畫面與右下時間正常。
- 劇本、語音對齊、其餘三個系統檔這次只是一併納入整合包，內容與上一版相同。`big5/` 仍與正式 `tl/tc` 196 檔完全一致。EXE 仍是 node3c_zero（md5 `5d560252325004f76876238065fda51d`），且已是正式 `exe/patched/` 現行檔。
