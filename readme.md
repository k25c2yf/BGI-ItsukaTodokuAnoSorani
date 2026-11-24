# 《何空》本機編譯整合包（繁中）

日期：2026-11-23（更新自 2026-11-22 版；Asia/Singapore UTC+8）

把這個資料夾解壓後，在裡面跑 `outputbig5.bat`。BAT 仍是逐條編譯指令（Scenario0000–0193、mainscript、ScenarioDB），編譯結果先寫入 `temp\`，再連同有功能修改的系統檔（`scrmsg`／`scrslct`）與 BitmapNameDB 放到 `outputbig5\`，供 Enigma Virtual Box 使用。用 `itsusora_UTF8_FIX.exe` 執行。

資料夾名叫 `big5` 只是為了沿用你原本的 BAT 路徑，裡面是 UTF-8 繁中，不是 Big5 編碼。

**字型：本包系統畫面與對白改用 Microsoft JhengHei（微軟正黑體）。請先安裝此字型（Wine：把 `msjh.ttc` 放進字型目錄）。建議刪除舊的 `BGI.gdb` 備份後再啟動，以免沿用舊字型快取。** 簡中 `ipl` 沒有這次字型變更。


## 這包有什麼

| 路徑 | 說明 |
|------|------|
| `outputbig5.bat` | 逐條編譯＋套語音補丁，輸出到 `outputbig5`（給 Enigma Virtual Box） |
| `big5/` | 正式繁中 txt（196 檔：Scenario0000–0193、mainscript、ScenarioDB）。已含 0080「──那麼呢。」開引號修到 `巽殿」`；續行沒有把說話人寫進 txt |
| `source/` | 編譯用源 bin（`att/x_v200`：章檔、mainscript、ScenarioDB、BitmapNameDB） |
| `sysprg_big5/` | 共用系統檔 4 個（來源 `sys/out_common/`，字型 v3）：`scrmsg._bp`（8354 B，md5 `4e25b476490fc2d7f01f5a8786d96f91`）、`scrslct._bp`（5264 B，md5 `b7bd2405498839dffd30ef561243ded5`）、`logwnd._bp`（3760 B，md5 `df08ce4252c953020cde09525030c6f2`）、`usdtwnd._bp`（6096 B，md5 `21560b510c1097fe63625da1a2845eb3`）。另加繁中 `ipl._bp`（2400 B，md5 `5a78c35b303bca122eb7d91a82e1c22f`，視窗標題「何時到達那片天空」；載入時 syscall 81:64 把客戶區設成 1280×960；並以 `B0:C1("Microsoft JhengHei", 3)` 登錄字型編號 2；來源 `sys/out_ipl/tc/`）。以及 `msgwndctrl._bp`（1552 B，md5 `acacc64a7df70e72c165a1621de253bc`）、`userdata._bp`（3344 B，md5 `8aa6917448f7716749b090d15e311ca2`）：把訊息窗／預設字型編號改為 2（會覆蓋 `sysprg.arc` 零售原版）。其餘系統檔不散佈：其餘 `sysprg` 類仍由 `sysprg.arc` 提供零售原版；`ipl` 會覆蓋 `system.arc`。 |
| `ipl_sc/` | 簡中 `ipl._bp`（2352 B，md5 `10015d18ddf529c3ae3028b1f70f0035`，視窗標題「终有一日愿遂彼空」，同樣在載入時把客戶區設成 1280×960；來源 `sys/out_ipl/sc/`）。BAT 不會複製這份；做簡中包時再換上。 |
| `sys_nov6_orig/scrmsg._bp` | 還原用（md5 `7fa2bcdd5887e6153fc9a68e880caf54`），BAT 不會自動複製 |
| `BGIScriptImporter.py` | 章／mainscript 編譯器 |
| `scenariodb_tool.py` | ScenarioDB 請用這個，不要用章編譯器 |
| `apply_voice_align.py`、`sites.tsv` | 編譯後對 23 章 347 處變體點寫入 type=3 與中文名指標 |

BAT 順序是：逐條編譯全部腳本到 `temp\` → 複製到 `outputbig5\` → 用 `apply_voice_align.py` 把已對齊的 23 章蓋上去 → 再複製 `sysprg_big5` 內的 4 個共用系統檔（`scrmsg`／`scrslct`／`logwnd`／`usdtwnd`）、繁中 `ipl._bp`、`msgwndctrl._bp`、`userdata._bp` 與 BitmapNameDB。不要把 `temp` 在對齊之後再整份蓋回 `outputbig5`，否則補丁會被未對齊檔蓋掉。圖片檔（舊流程的 BIG5PIC）這包沒有，需要時可自行放進 `outputbig5`。

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

## 2026-11-19 13:50（Singapore）更新：ipl 分繁簡（視窗標題）

系統檔裡只有 `ipl._bp` 會把繁簡差異顯示出來（視窗標題／遊戲名）。其餘內部字串仍共用、不分繁簡。

- 正式目錄：`sys/out_ipl/tc/ipl._bp`（md5 `04c842d7f4a004616d1da9fc9da7b89c`）標題「何時到達那片天空」；`sys/out_ipl/sc/ipl._bp`（md5 `63fc89d658f4bb4d7c71c73a2f99a7de`）標題「终有一日愿遂彼空」。兩檔指令序列相同，只差這一處標題；錯誤訊息與啟動檢查用識別字（如 `ItsukaTodokuAnoSorani`、封包檔名）未改。
- 本包 `sysprg_big5/`、`prebuilt_outputbig5/` 與 `outputbig5.bat` 使用繁中版。簡中版放在 `ipl_sc/`，BAT 不會自動複製。
- `ipl` 不在 `sysprg.arc`，而在 `system.arc`：散佈的 `ipl._bp` 會蓋過封包裡的零售日文標題。`launcher._bp` 仍不散佈（安裝介面，遊戲執行不必）。
- 未改劇本、EXE、其餘 4 個共用系統檔、`tl/sc` 其餘檔。

## 2026-11-20 03:20（Singapore）更新：ipl 載入時把視窗加大為 1280×960

何空設定裡沒有改視窗大小的選項，因此在 ipl 建窗流程（`90:0C`／`90:4C`／`90:00`）之後加入 `push 1280; push 960; syscall 81:64`。Wine 煙測用正式未改 EXE 開到標題，客戶區是精確的 1280×960。EXE、解析度表與內部畫布仍是 800×600，沒有改。

- 正式目錄：`sys/out_ipl/tc/ipl._bp`（2352 B，md5 `7059c00acccda1c3f99335ec4efebfeb`）標題「何時到達那片天空」；`sys/out_ipl/sc/ipl._bp`（2352 B，md5 `10015d18ddf529c3ae3028b1f70f0035`）標題「终有一日愿遂彼空」。兩檔指令相同，只差標題。
- 本包 `sysprg_big5/`、`prebuilt_outputbig5/` 已同步繁中版；`ipl_sc/` 已同步簡中版。
- 舊檔備份在 `sys/backup_20261120_ipl_pre_8164/`（繁 md5 `04c842d7…`、簡 md5 `63fc89d6…`）。
- 視窗可能先以 800×600 出現，等 ipl 跑到 `81:64` 再變成 1280×960。1080p 工作區放得下；更大的螢幕可自行開全螢幕。
- 未改劇本、EXE、其餘 4 個共用系統檔、`tl/sc` 其餘檔、零售 `sys/orig/ipl._bp`。


## 2026-11-21（香港時間 Asia/Hong_Kong）更新：正式繁中寫入諧音 ruby v6，並修正選項標題

- 正式繁中已寫入 v6 測試：49 章行內 `<R日文>中文</R>`（約 160 處＋既有有識外し）以及 23 處兩行 ruby 小字改回日文（家政婦／ヨメ、策／むち等）。
- 三處底字／後句對不齊仍未改：0124 汝等 vs 你們、0157 是魔術 vs 魔術、0188 包吉／斯圖特加 vs 鮑基／舒通。
- `scrslct._bp` 顯示標題「選択肢」→「選項」（md5 `31776d436e7b32e4a592eb1200036e38`，5264 B）；「選択肢数」未改。logwnd 分頁本來就是「選項」。已寫入 `sys/out_common`、本包 `sysprg_big5` 與 `prebuilt_outputbig5`。
- `big5/` 已與正式 `tl/tc` 196 檔同步；`prebuilt_outputbig5/` 已重編＋語音對齊 applied=347 skipped=0 failed=0。
- 本包含正式 `tl/tc/` 繁中 TXT。
- EXE 仍是 node3c_zero（md5 `5d560252325004f76876238065fda51d`，1623552 B）、ipl 仍是 1280×960（繁 md5 `7059c00acccda1c3f99335ec4efebfeb`、簡 md5 `10015d18ddf529c3ae3028b1f70f0035`）、其餘三個共用系統檔、簡中未改。


## 2026-11-22（Asia/Singapore UTC+8）更新：評審 12 條＋全書簡體轉繁體測試稿，並打整合包

正式 `tl/tc`、`tl/sc`、`sys`、EXE **未寫入**。本包是獨立暫存編譯，不覆蓋 2026-11-21 整合包，也不改本機 `local_build_tc_20261119`。

- `big5/` 與本包內的 `tl/tc/`：以**當日正式繁中**為底（已含 2026-11-22 寫入正式稿的 kunui／雲戌亥 ruby v3，例如 0115『<Rクヌイ>雲亥</R>』『<Rモイヌ>雲戌</R>』），再疊加測試目錄 `tl/review/fixtxt_test_20261122/` 的全部 TXT。
- 測試疊加包含兩批、相對正式稿共 **45 檔 72 行**：
  1. 評審必須修正 12 行，外加 0129 ●000740●「追踪」→「追蹤」。已核對本包編譯用稿含：0060 ●032152●「愛愛醬，打擾了。」、mainscript ●013436●婚約者、ScenarioDB ●154●婚約者、0185 ●000036●《自無異之世的終焉》。
  2. 全書對白／旁白剩餘簡體改繁體（42 檔、60 行、86 個字），例如 0010「那里／放松」→「那裡／放鬆」、0143「遗留／独自／离去／边看边自问」→繁體、0188「夸瓦西尔」→「夸瓦西爾」、0191「亲眼」→「親眼」。說話人行、行內 Ruby 日文小字、兩行 Ruby 底字／讀音、0159 亂碼段、0186–0191 直行標點未改。「宝吉」「下里去」及王后／里名／余／范／夸／遥／著着等排除項維持現稿。詳見測試包 `itsusora_fixtxt_test_20261122_v2.7z` 的 NOTE.md（本目錄亦附 `NOTE_fixtxt_test_20261122.md`）。
- `prebuilt_outputbig5/` 已在本機依 BAT 順序重編全部 194 章＋mainscript＋ScenarioDB（ScenarioDB overflow=0），再跑 `apply_voice_align`：**applied=347 skipped=0 failed=0**（23 章）。
- 系統檔與 EXE 與現行正式檔相同，相對 2026-11-21 包未改：`scrmsg` `82c1d08b90f2403d10866c7da850e5b4`、`scrslct` `31776d436e7b32e4a592eb1200036e38`、`logwnd` `c60c6337272612b74d8d5fd91399d338`、`usdtwnd` `1dbeeb7b52d35077f24eb63e8004561c`、繁中 ipl（1280×960）`7059c00acccda1c3f99335ec4efebfeb`、簡中 ipl `10015d18ddf529c3ae3028b1f70f0035`、試玩 EXE node3c_zero `5d560252325004f76876238065fda51d`。
- 資料夾名稱改為 `local_build_tc_20261122`（BAT 仍在本目錄內以相對路徑執行）。解壓後請在此目錄跑 `outputbig5.bat`；不想自己編譯可直接用 `prebuilt_outputbig5/`。

## 2026-11-23（Asia/Singapore UTC+8）更新：系統字型改為微軟正黑體（font v3）並打整合包

已將測試通過的 font v3 寫入正式目錄，並重建本整合包（不覆蓋 2026-11-22 包）。

- **使用前請先安裝 Microsoft JhengHei（微軟正黑體）。Wine 請放入 `msjh.ttc`。建議刪除舊的 `BGI.gdb` 備份後再啟動。** 否則畫面可能仍走 ＭＳ ゴシック／字型連結缺字。
- 正式寫入：`sys/out_ipl/tc/ipl._bp`（2400 B，md5 `5a78c35b303bca122eb7d91a82e1c22f`；`B0:C1("Microsoft JhengHei", charset=3／BIG5)` 登錄為字型編號 2，並把預設字型編號設為 2）；`sys/out_common` 四檔（`scrmsg` `4e25b476490fc2d7f01f5a8786d96f91`、`scrslct` `b7bd2405498839dffd30ef561243ded5`、`logwnd` `df08ce4252c953020cde09525030c6f2`、`usdtwnd` `21560b510c1097fe63625da1a2845eb3`）把 `91:88`／`91:9C`／`91:9D`／`92:1C` 的字型編號改為 2（含 LOG 記錄內文）。另將 `msgwndctrl._bp`（`acacc64a7df70e72c165a1621de253bc`）、`userdata._bp`（`8aa6917448f7716749b090d15e311ca2`）寫入正式 UTF-8 繁中樹 `sys/out_tc`、`sys/out_tc_v200`，並納入本包 `sysprg_big5/`／`prebuilt_outputbig5/` 與 `outputbig5.bat`（會覆蓋 `sysprg.arc`）。舊檔備份在 `sys/backup_20261123_font_jhenghei/`。
- **未改**：簡中 `sys/out_ipl/sc/ipl._bp`（仍為 `10015d18ddf529c3ae3028b1f70f0035`，沒有這次字型變更）、`sys/out_sc`、`sys/orig_v200`、EXE（仍為 node3c_zero，md5 `5d560252325004f76876238065fda51d`）。其餘 sysprg（title／yesnownd／cnfgwnd 等）未寫入正式目錄；完整測試檔仍在 `itsusora_font_jhenghei_test_20261122_v3.7z`。
- `big5/` 與本包 `tl/tc/` 仍與現行正式繁中 198 檔一致（196 txt）。`prebuilt_outputbig5/` 已依 BAT 順序重編全部 194 章＋mainscript＋ScenarioDB（ScenarioDB overflow=0），再跑 `apply_voice_align`：**applied=347 skipped=0 failed=0**（23 章）。
- 資料夾名稱改為 `local_build_tc_20261123`。解壓後請在此目錄跑 `outputbig5.bat`；不想自己編譯可直接用 `prebuilt_outputbig5/`。
