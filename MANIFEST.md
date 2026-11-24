# 簡中正式稿同步上傳包（由現行繁中轉寫）

- 打包時間：2026-11-25 03:20（香港時間 UTC+8）
- 對照倉庫：https://github.com/k25c2yf/BGI-ItsukaTodokuAnoSorani （`main`，建議上傳到 `gbk/` 與根目錄 `outputgb.bat`）
- 本包未 git push、未改 EXE、未改繁中正式 `tl/tc`、未改共用系統檔、未改簡中 ipl（不加正黑體）。

## 來源與做法

- 來源：現行正式繁中 `/workspace/itsusora/tl/tc/`（已含 11-21 pun-ruby、11-22 FIXTXT 12 條＋簡體轉繁體 60 行、kunui ruby v3、アズ→阿茲、章名《自無異之世的終焉》等）。
- 轉換：本專案既有 `/workspace/itsusora/tl/work/tlkit.py` 的 `tc_to_sc_file` 規則——OpenCC `t2s`；說話人整行若等於 `SPEAKERS` 表（日文系統人名如 ふたみ／メメ，以及同形的 策／此芽／傘 等）則原樣保留；`\xFFxx` 不轉（現行正式稿已無此殘留）。
- Ruby：`<R日文>中文</R>` 只轉中文底字，日文讀音不轉（避免 乾く→干く、有識外し→有识外し）。兩行 Ruby 的讀音行（依日文 dump 分類）亦不轉。
- 編碼／換行：對齊該檔正式繁中（Scenario／mainscript 為 UTF-8 BOM，換行與對應 tc 相同；ScenarioDB.txt 無 BOM、LF；空檔維持空檔）。不強制改成 tlkit 早期一律 CRLF+BOM。
- 寫入前備份：`/workspace/itsusora/tl/backup_20261125_sc_sync_from_tc/`（196 個當時的正式 sc txt）。替換以同檔案系統 `cp` 再 `mv`。

## 變動統計

- 寫入正式 `tl/sc/`：**106 檔、3454 行**用字有變。其餘 90 個 txt 轉換後與原正式簡中完全相同，未覆寫。
- 全部正式簡中 txt 仍為 **196** 檔（Scenario0000–0193、mainscript、ScenarioDB.txt），與繁中檔數、●ID●、行數對齊。
- 其中 `mainscript.txt` 由 391 行補到 **523** 行（補上正式繁中已有的 132 條語音代碼行，如 MFu／MKo 等）。

用字有變的檔（檔名／差異行數／舊行數→新行數）：

`Scenario0002.txt` 4行（364→364）, `Scenario0004.txt` 2行（287→287）, `Scenario0005.txt` 3行（217→217）, `Scenario0010.txt` 4行（291→291）, `Scenario0011.txt` 8行（304→304）, `Scenario0012.txt` 1行（146→146）, `Scenario0013.txt` 7行（316→316）, `Scenario0016.txt` 5行（272→272）, `Scenario0017.txt` 17行（371→371）, `Scenario0018.txt` 7行（227→227）, `Scenario0019.txt` 2行（58→58）, `Scenario0022.txt` 12行（234→234）, `Scenario0023.txt` 5行（197→197）, `Scenario0028.txt` 6行（169→169）, `Scenario0029.txt` 2行（45→45）, `Scenario0031.txt` 2行（20→20）, `Scenario0033.txt` 2行（248→248）, `Scenario0040.txt` 1行（6→6）, `Scenario0046.txt` 16行（577→577）, `Scenario0049.txt` 16行（323→323）, `Scenario0050.txt` 3行（255→255）, `Scenario0052.txt` 2行（122→122）, `Scenario0054.txt` 2行（250→250）, `Scenario0059.txt` 1行（123→123）, `Scenario0060.txt` 39行（1010→1010）, `Scenario0062.txt` 15行（509→509）, `Scenario0064.txt` 5行（344→344）, `Scenario0066.txt` 1行（78→78）, `Scenario0069.txt` 1行（117→117）, `Scenario0071.txt` 14行（392→392）, `Scenario0073.txt` 3行（248→248）, `Scenario0078.txt` 2行（107→107）, `Scenario0080.txt` 33行（749→749）, `Scenario0083.txt` 12行（300→300）, `Scenario0084.txt` 2行（169→169）, `Scenario0089.txt` 2行（4→4）, `Scenario0092.txt` 17行（664→664）, `Scenario0094.txt` 1行（65→65）, `Scenario0097.txt` 8行（278→278）, `Scenario0098.txt` 3行（97→97）, `Scenario0100.txt` 2行（21→21）, `Scenario0102.txt` 23行（366→366）, `Scenario0103.txt` 12行（134→134）, `Scenario0104.txt` 4行（165→165）, `Scenario0105.txt` 9行（255→255）, `Scenario0107.txt` 1行（38→38）, `Scenario0108.txt` 51行（366→366）, `Scenario0109.txt` 8行（231→231）, `Scenario0112.txt` 18行（314→314）, `Scenario0113.txt` 3行（428→428）, `Scenario0115.txt` 61行（939→939）, `Scenario0116.txt` 48行（1359→1359）, `Scenario0117.txt` 26行（1526→1526）, `Scenario0119.txt` 52行（838→838）, `Scenario0121.txt` 14行（446→446）, `Scenario0122.txt` 25行（878→878）, `Scenario0124.txt` 55行（1028→1028）, `Scenario0126.txt` 37行（601→601）, `Scenario0127.txt` 59行（968→968）, `Scenario0128.txt` 49行（856→856）, `Scenario0129.txt` 48行（925→925）, `Scenario0130.txt` 21行（476→476）, `Scenario0131.txt` 3行（296→296）, `Scenario0133.txt` 23行（498→498）, `Scenario0136.txt` 15行（645→645）, `Scenario0139.txt` 24行（673→673）, `Scenario0142.txt` 3行（131→131）, `Scenario0143.txt` 22行（505→505）, `Scenario0144.txt` 38行（833→833）, `Scenario0146.txt` 68行（1086→1086）, `Scenario0148.txt` 48行（708→708）, `Scenario0150.txt` 4行（267→267）, `Scenario0151.txt` 79行（982→982）, `Scenario0152.txt` 22行（574→574）, `Scenario0153.txt` 8行（401→401）, `Scenario0155.txt` 2行（119→119）, `Scenario0156.txt` 46行（855→855）, `Scenario0157.txt` 5行（231→231）, `Scenario0158.txt` 21行（743→743）, `Scenario0159.txt` 63行（851→851）, `Scenario0160.txt` 13行（262→262）, `Scenario0162.txt` 49行（1154→1154）, `Scenario0163.txt` 2行（211→211）, `Scenario0166.txt` 4行（420→420）, `Scenario0168.txt` 10行（391→391）, `Scenario0170.txt` 42行（901→901）, `Scenario0171.txt` 4行（139→139）, `Scenario0173.txt` 23行（359→359）, `Scenario0175.txt` 17行（472→472）, `Scenario0176.txt` 19行（596→596）, `Scenario0178.txt` 16行（524→524）, `Scenario0179.txt` 39行（754→754）, `Scenario0180.txt` 41行（835→835）, `Scenario0181.txt` 4行（128→128）, `Scenario0182.txt` 28行（1009→1009）, `Scenario0184.txt` 21行（374→374）, `Scenario0185.txt` 1行（1→1）, `Scenario0186.txt` 128行（158→158）, `Scenario0187.txt` 199行（257→257）, `Scenario0188.txt` 349行（396→396）, `Scenario0189.txt` 197行（223→223）, `Scenario0190.txt` 179行（184→184）, `Scenario0191.txt` 121行（148→148）, `Scenario0193.txt` 7行（307→307）, `ScenarioDB.txt` 11行（194→194）, `mainscript.txt` 522行（391→523）

## 驗證

- 檔數 196＝196；全書 ●ID● 與行數與 `tl/tc` 一致（對白／旁白 48433 條有 ID 的行皆對上）；BOM／換行與對應繁中檔一致。
- `SPEAKERS` 整行保留 7467 處（含兩行 Ruby 讀音中的 ふたみ／みどの／のん，以及 策／此芽／傘 等）。
- 行內 Ruby 日文讀音 172 處全部未改；無 乾く→干く 之類誤轉。
- FIXTXT 12 條已轉簡並抽檢通過：那么／要么／什么／怎么／当主／追踪；0060「爱爱酱，打扰了。」「爱爱酱」；mainscript／ScenarioDB「婚约者」；0185「自无异之世的终焉」。
- 關鍵詞：阿兹、婚约者、自无异之世的终焉 已在 mainscript／ScenarioDB；舊「梅酱／美酱／婚約者」已不在簡中稿。再跑一次 t2s，對白／旁白無殘留應轉未轉的繁體。
- 編譯產物 `tl/sc/ScenarioDB`、`ScenarioDB.GBK` 未改（仍舊，需另以 `scenariodb_tool.py apply` 重編，本包只提供 txt）。

## 尚待確認／不能自動轉的用語

- **牠**：OpenCC `t2s` 不把「牠」轉成「它」。現行簡中 0122／0097／0133／0179 仍為「牠」（與繁中用字對齊）。若簡中要統一為「它」，需另案人工決定，本次不擅自改。
- **裏→里**：正式繁中刻意保留的「裏」（如手裏劍／裏志願者）經 t2s 已作「里」。這是 OpenCC 預設，簡中通常用「里」。
- 其他異體（著／着、吃／喫、台／臺 等）依 OpenCC `t2s` 預設，未另加本專案 s2tw 掃描時的例外表。

## outputgb.bat

倉庫根目錄原有的 `outputgb.bat` 屬於其他專案（A_Ken／A_Tan、`BGIScriptInserter_Lib.py`），不能用來編何空。本包這份是依現行正式 `outputbig5.bat`（與 2026-11-23 整合包正文相同）對齊改寫的簡中編譯流程：

- 腳本路徑 `./gbk/`（對應倉庫 `gbk/`）；輸出 `outputgbk`；先寫 `temp` 再複製。
- 章清單與 `outputbig5.bat` 相同：Scenario0000–0193、mainscript 用 `BGIScriptImporter.py`；ScenarioDB 用 `scenariodb_tool.py apply --enc utf-8`（不再用舊 `output_sc.bat` 那樣對 ScenarioDB 跑 Importer）。
- 編譯後跑 `apply_voice_align.py`（`sites.tsv`）。
- 系統檔：複製共用的 `sysprg_big5` 四檔（scrmsg／scrslct／logwnd／usdtwnd，即官方 `sys/out_common` 現況）；**ipl 用 `ipl_sc\ipl._bp`**（官方簡中 ipl，md5 `10015d18ddf529c3ae3028b1f70f0035`，不加正黑體）。**不複製** `sysprg_big5` 的 ipl／msgwndctrl／userdata（font v3，僅繁中）。倉庫若尚無 `ipl_sc\`，請從 11-23 包或 `sys/out_ipl/sc/ipl._bp` 放入後再編譯。
- `BitmapNameDB` 照常複製；`SCPIC` 一行僅 `@echo`（與繁中包對 BIG5PIC 的寫法相同，不強制複製）。

## 上傳建議

- 把本包 `gbk/*.txt`（196 個，含未改檔）一次覆寫進倉庫 `gbk/`，讓倉庫簡中與本機正式稿對齊。
- **請刪除或替換**倉庫舊的 `gbk/itsusora_script_sc.7z`（2026-10-31～11-01），以免兩套簡中並存。
- 把 `outputgb.bat` 放到倉庫根目錄，取代那份其他專案的 bat。
- 本包不含 EXE、系統 `_bp`、舊 7z。

## 檔案清單（md5）

- `outputgb.bat`：19014 B，md5 `1b8128af0da0f9f7e0699a6d5747c20b`

| 倉庫相對路徑 | 大小（B） | md5 | 本次是否改寫 | 差異行數 |
|---|---:|---|---|---:|
| `outputgb.bat` | 19014 | `1b8128af0da0f9f7e0699a6d5747c20b` | 是（依 outputbig5.bat 新寫） | — |
| `gbk/Scenario0000.txt` | 68 | `42332b70d1b07e946517018ba2729411` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0001.txt` | 86 | `8311e3ffb16b60609e81b68a1412fd7e` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0002.txt` | 17215 | `9d7110e60ab5efe049ea2b946c824d52` | 是 | 4 |
| `gbk/Scenario0003.txt` | 33 | `ab4bde5563cbafaa1368c53d70a0e353` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0004.txt` | 11536 | `c69dc4791ed3a51cfb32fcc09da0e633` | 是 | 2 |
| `gbk/Scenario0005.txt` | 8671 | `963ea16494339e4f13c0a84d5ffe2806` | 是 | 3 |
| `gbk/Scenario0006.txt` | 33 | `cffad7421960e2fac37d2a8c49225a75` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0007.txt` | 4089 | `0a34e3185f1d685d7b0867250f07efb8` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0008.txt` | 1040 | `0e58bee761d57044a5a991dc22bcb74f` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0009.txt` | 1115 | `7659633e193add3b8f7b3a3f20eb386d` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0010.txt` | 13509 | `903c634a6c0acb1b26bc9c27710662f1` | 是 | 4 |
| `gbk/Scenario0011.txt` | 13640 | `22d76bcf2ab7c3c418f8037b08dbdd59` | 是 | 8 |
| `gbk/Scenario0012.txt` | 5875 | `97a514f7b65850d6e390e1ed5f5457cb` | 是 | 1 |
| `gbk/Scenario0013.txt` | 15907 | `2b9ea13c7228d43afa343867a822b726` | 是 | 7 |
| `gbk/Scenario0014.txt` | 5470 | `ef078ece2b3a5798282ea95ddb7535eb` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0015.txt` | 33 | `67fe79b29a9fd4469826c69a7d0a75d0` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0016.txt` | 12673 | `205ddd88c9bc1cae3fc40b6eeccbadd0` | 是 | 5 |
| `gbk/Scenario0017.txt` | 19166 | `27572a03d452da23fbf5343a1f329246` | 是 | 17 |
| `gbk/Scenario0018.txt` | 9396 | `a2814c86d8d9a2900f63b434b4c27ddb` | 是 | 7 |
| `gbk/Scenario0019.txt` | 2242 | `eae52a699442887b7d960a7ee70f178f` | 是 | 2 |
| `gbk/Scenario0020.txt` | 1219 | `0d8562f2485b4de1a3c5c83a67c0c608` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0021.txt` | 11538 | `45baec96dc2ea7be1dd2e37c30c25290` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0022.txt` | 9786 | `37ddc49eed54958ea72024486a4e78a3` | 是 | 12 |
| `gbk/Scenario0023.txt` | 8414 | `e19d4a2a337f5eea554712007842b2c5` | 是 | 5 |
| `gbk/Scenario0024.txt` | 33 | `535c2d0ac8c4e250ca075dbaedb51de8` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0025.txt` | 6223 | `9101d3dc9b8f710b95f87741a6bebd4c` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0026.txt` | 2675 | `297af349dc442fdd291ba8a7ec08c09e` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0027.txt` | 6163 | `fea3c644ff11699cbf72b6f1e6bdab9b` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0028.txt` | 7545 | `539f48491a2ba4c976da5aba1079aefa` | 是 | 6 |
| `gbk/Scenario0029.txt` | 1622 | `9d08a739e139090143f972c58609a41e` | 是 | 2 |
| `gbk/Scenario0030.txt` | 835 | `70aadcf841842400de5068bebca75ff2` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0031.txt` | 1096 | `09e9829e657575f8b7dc933430aeaa9c` | 是 | 2 |
| `gbk/Scenario0032.txt` | 2245 | `bfde8a628a004c3ce612dd2f2b41409c` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0033.txt` | 11506 | `66e1f33800a8dc204fc3085fd2805f7b` | 是 | 2 |
| `gbk/Scenario0034.txt` | 3249 | `4d4f3d1c278d8ab3d04c3c5cf3ced8e9` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0035.txt` | 33 | `9be535befb5b55a692803dcfae24fdc3` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0036.txt` | 0 | `d41d8cd98f00b204e9800998ecf8427e` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0037.txt` | 2795 | `48947558380a8a3554e36cde9105800e` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0038.txt` | 1026 | `e4236e75767e34bcc541afd80ed8ff49` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0039.txt` | 319 | `74a3a74d5b40ff57af1ef5016647c588` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0040.txt` | 309 | `2eadd77bf1ab29faee971a6adeeb8df6` | 是 | 1 |
| `gbk/Scenario0041.txt` | 1241 | `f3acd929e6c60fb2e6598d83a86879b7` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0042.txt` | 11421 | `a5c31f348fa3091555667c672665fc43` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0043.txt` | 5627 | `9843edc5302e09fcee4a110c34b50d96` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0044.txt` | 555 | `e0bd06005c0f6aa8dc6e877899c3eac2` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0045.txt` | 33 | `6f14d55caa7cf722d57a378bd24d8295` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0046.txt` | 31068 | `c5011aa606064cb22d2ff74166792a12` | 是 | 16 |
| `gbk/Scenario0047.txt` | 33 | `4098cce189e03b3e52a61d9c7d4aca0a` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0048.txt` | 6038 | `ff0e36c8a43adaacf24679343e7c183e` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0049.txt` | 14020 | `b7abe198a534ef28d7309f48a476b536` | 是 | 16 |
| `gbk/Scenario0050.txt` | 10415 | `589a68eaf80e269012bb9355d51a88c0` | 是 | 3 |
| `gbk/Scenario0051.txt` | 33 | `f7ba0be97110cbb3335cb525d9d856ec` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0052.txt` | 4160 | `0ddb4bb07f0ebeedc7c024fe0c16cd75` | 是 | 2 |
| `gbk/Scenario0053.txt` | 1808 | `0a720511bcb49f1673c2a1a71c2180b9` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0054.txt` | 10628 | `c363e9fe8db559c752b7e0339c07b570` | 是 | 2 |
| `gbk/Scenario0055.txt` | 88 | `3c631a3f55e2bf50eb04ea1705785fb4` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0056.txt` | 10614 | `bf50f78aab6ee54fa574836297d98c07` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0057.txt` | 33 | `869985e9d5d5dca63c51c3c7ad009402` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0058.txt` | 860 | `c2182b3427630c04080fef05fb18f418` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0059.txt` | 4674 | `0f29eccc4131220777a8f78dbc4052e8` | 是 | 1 |
| `gbk/Scenario0060.txt` | 47216 | `f2f4c0009e812067c99954a26bf98fb6` | 是 | 39 |
| `gbk/Scenario0061.txt` | 33 | `13d4f8639090b3363585d532bd2ec515` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0062.txt` | 22284 | `f2894c6bb14fd2ff452fb02bba5c49d5` | 是 | 15 |
| `gbk/Scenario0063.txt` | 33 | `df156f4cf597c40554c987edcd817269` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0064.txt` | 14963 | `dd49959274b3f51e7b54a27a7cb403a3` | 是 | 5 |
| `gbk/Scenario0065.txt` | 33 | `1a0d31d3d96f3ba6a7b708daee867715` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0066.txt` | 3230 | `32097587843905bbfffbd1d676686932` | 是 | 1 |
| `gbk/Scenario0067.txt` | 6904 | `1f91de21f7ad766d2fa5ce4de8c12e49` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0068.txt` | 301 | `dae4a3f08d7e0a29cab9c6bc6ecb5109` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0069.txt` | 5430 | `3c4f622ba0e415f3c2764917171e5334` | 是 | 1 |
| `gbk/Scenario0070.txt` | 32 | `38c28a2e5da5c556dd534ecb7ccab192` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0071.txt` | 16938 | `378f2aa0d4371ecdf2c58e5487d3f48a` | 是 | 14 |
| `gbk/Scenario0072.txt` | 3508 | `9896550fbf83a966c77d3e027b2406b1` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0073.txt` | 10790 | `be1a2c07a3ba14e059d55387b132854f` | 是 | 3 |
| `gbk/Scenario0074.txt` | 1553 | `e5e3f6e30ecdad5007eebdba2be9562c` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0075.txt` | 32 | `887c2289c334a3ad9c085446946ec4d2` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0076.txt` | 1461 | `29fe5f8332a3b1dd42c6513012332d29` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0077.txt` | 3500 | `76f23521fdae8ee951b44bc1531cf433` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0078.txt` | 4822 | `07cf78c953474f281bcf6a23946cfdf7` | 是 | 2 |
| `gbk/Scenario0079.txt` | 32 | `474c30e0e0a950c725865373f2f939e4` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0080.txt` | 36677 | `10476646e619310ac4dbc8e4a4309c90` | 是 | 33 |
| `gbk/Scenario0081.txt` | 32 | `8edc0a270ef2cc8a0f106851a9a320c3` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0082.txt` | 1477 | `2593981c1752980dee4fe3295de3530e` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0083.txt` | 15528 | `d150f17fce2e87895f51613210ef5303` | 是 | 12 |
| `gbk/Scenario0084.txt` | 7155 | `0eb41c1b375f0df52971e9c6e09ff30e` | 是 | 2 |
| `gbk/Scenario0085.txt` | 33 | `61d823203e1fda2735468b4a2716bca1` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0086.txt` | 9358 | `776c6c9b61bfae294bdefff9362bd167` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0087.txt` | 1079 | `68a417b5d23a3a69dbe77765490fe81b` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0088.txt` | 2410 | `271cf325876082abee85e3778fce36cd` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0089.txt` | 122 | `b799f7ca49ac127bf08a451afba84900` | 是 | 2 |
| `gbk/Scenario0090.txt` | 1700 | `02326d59cdcbf4fbf48d59e95e38d6b9` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0091.txt` | 33 | `f58af1f0eacedc9419b4c18afc80ea9a` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0092.txt` | 31773 | `60c33bf6a8a9ff9c9dcc20b0128c2aad` | 是 | 17 |
| `gbk/Scenario0093.txt` | 33 | `f1361f44390750790340ce5118dd2a52` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0094.txt` | 2474 | `7107f9393b220907a536795ae7e87fca` | 是 | 1 |
| `gbk/Scenario0095.txt` | 2970 | `f450f2147ed175125427aaa56c6d5bf8` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0096.txt` | 1604 | `b2c900b381f310073f1f6960a88bb74d` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0097.txt` | 11852 | `9fae8afc2a778f6627bf724cb7caceea` | 是 | 8 |
| `gbk/Scenario0098.txt` | 4216 | `1b4cf3e6abd312fca073c85afbc56299` | 是 | 3 |
| `gbk/Scenario0099.txt` | 123 | `b6961f32fe81d51800b88c350b94f5bb` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0100.txt` | 786 | `9a82c14201821e20490fe2a0372a4c8e` | 是 | 2 |
| `gbk/Scenario0101.txt` | 33 | `85a26d5e6c9b2dabfc7a088dd736d365` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0102.txt` | 17067 | `c58782280e2cf377cb13f35a4cf7b398` | 是 | 23 |
| `gbk/Scenario0103.txt` | 5699 | `788f901350a7b192b32f112804efb682` | 是 | 12 |
| `gbk/Scenario0104.txt` | 6936 | `c151951f9481ca783327ac97560ebff7` | 是 | 4 |
| `gbk/Scenario0105.txt` | 11890 | `b843b49fe4bb3672748d43082e9d8974` | 是 | 9 |
| `gbk/Scenario0106.txt` | 5131 | `73704760d5cf30de2006e70dff697054` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0107.txt` | 1298 | `d85ac6f889eacfd8b783f45709ec461b` | 是 | 1 |
| `gbk/Scenario0108.txt` | 16373 | `903d1e3ab7d99fd73e17efc069c8ae22` | 是 | 51 |
| `gbk/Scenario0109.txt` | 8857 | `bddd8ab7b70dbdd22ce8eafca588b4bd` | 是 | 8 |
| `gbk/Scenario0110.txt` | 92 | `8b1f1b1125d9f3ec267f313baacaed78` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0111.txt` | 71 | `ece16cf43f6d09b647908bf720f0ff0e` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0112.txt` | 15398 | `1082aaf586b05d1b296608d5bc1af6ae` | 是 | 18 |
| `gbk/Scenario0113.txt` | 19400 | `b513717962f0b217889540972124dc3a` | 是 | 3 |
| `gbk/Scenario0114.txt` | 74 | `db39ac272f7a2ced64a01b67ee88e5d3` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0115.txt` | 47079 | `de8b36691f3561052bdad6168ee32c71` | 是 | 61 |
| `gbk/Scenario0116.txt` | 59778 | `62667d9999e0dc749f9750d9820c48ab` | 是 | 48 |
| `gbk/Scenario0117.txt` | 62804 | `dc438556f93e1e9c80ecc3a00d5885ee` | 是 | 26 |
| `gbk/Scenario0118.txt` | 62 | `4182e11cd6fc2695440cec88b94e3cbe` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0119.txt` | 41545 | `6b53ca08acde72841d0b5b256d3694ce` | 是 | 52 |
| `gbk/Scenario0120.txt` | 77 | `aa65cdf8ff1a065fbb099d60060a795a` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0121.txt` | 25616 | `9952737c76e2fb32cf50f7b1ea191ff2` | 是 | 14 |
| `gbk/Scenario0122.txt` | 36177 | `74f4bd99b016dc2a2b6496754740b443` | 是 | 25 |
| `gbk/Scenario0123.txt` | 74 | `2ce9ac14c6092e8f249aebc85ec75dd2` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0124.txt` | 49279 | `ed44d53303110621effa85b4446abe26` | 是 | 55 |
| `gbk/Scenario0125.txt` | 77 | `8545530aa394c18c9a1fc70264da828a` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0126.txt` | 31807 | `2f7ff44e8167f76de8b586da4994654b` | 是 | 37 |
| `gbk/Scenario0127.txt` | 51542 | `af2908c24e3c74ce5c22b40fc3a53e1c` | 是 | 59 |
| `gbk/Scenario0128.txt` | 45316 | `746d44361d4d786ada8ee4635c1a97ef` | 是 | 49 |
| `gbk/Scenario0129.txt` | 47136 | `e2d9ef71e40f255259396bb3ccc29691` | 是 | 48 |
| `gbk/Scenario0130.txt` | 22937 | `fa503c11ac4b3ee38cb937b8369c9698` | 是 | 21 |
| `gbk/Scenario0131.txt` | 17975 | `5ca10b98d544460b27730a2c9837d74a` | 是 | 3 |
| `gbk/Scenario0132.txt` | 68 | `da5089728a8eace95270e75ff16a7fd9` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0133.txt` | 23582 | `cdde49fa4ac239bf8213e0e108f829a4` | 是 | 23 |
| `gbk/Scenario0134.txt` | 80 | `0ca65c2b3912810646b2d36bf56f2515` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0135.txt` | 65 | `a8fe489f9432b2dedf49946fed280445` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0136.txt` | 34964 | `798ef3cb29363e866b7afa6e542d3f8c` | 是 | 15 |
| `gbk/Scenario0137.txt` | 65 | `900df3cbfd8163b1dd8f64a9a7c68390` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0138.txt` | 10011 | `adf47d672e3d4dcbd713c3c0a41fbaba` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0139.txt` | 36120 | `dc24155f21c203850a49be7cb87131e4` | 是 | 24 |
| `gbk/Scenario0140.txt` | 9365 | `3377d04db9c603351abfe4be3bd1cc5d` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0141.txt` | 0 | `d41d8cd98f00b204e9800998ecf8427e` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0142.txt` | 6140 | `a21e05273f841c216b8b73720bff09dc` | 是 | 3 |
| `gbk/Scenario0143.txt` | 23951 | `5a65b0e26a3a2dbb4178a8588750d0f9` | 是 | 22 |
| `gbk/Scenario0144.txt` | 43623 | `e631850671cca9809da57fbb91e14eb2` | 是 | 38 |
| `gbk/Scenario0145.txt` | 0 | `d41d8cd98f00b204e9800998ecf8427e` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0146.txt` | 56732 | `c61662f4769f5a804e337035745262f3` | 是 | 68 |
| `gbk/Scenario0147.txt` | 65 | `c89dab7d8739eb20d6b0bafef3c88e72` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0148.txt` | 34495 | `9fb4ce2b926ad0f213232bca024ca9e6` | 是 | 48 |
| `gbk/Scenario0149.txt` | 65 | `3f8cd283973138c1f0d9bf0b4e1187b9` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0150.txt` | 13882 | `c17802de86ad352ae838a482be9429bb` | 是 | 4 |
| `gbk/Scenario0151.txt` | 46765 | `a4114411eeb07f90deea34ca1bccb267` | 是 | 79 |
| `gbk/Scenario0152.txt` | 31433 | `38ef3119b6e925ac8496b53bc043136f` | 是 | 22 |
| `gbk/Scenario0153.txt` | 19865 | `98e93ad6d67f67572fceca8c808b3f8a` | 是 | 8 |
| `gbk/Scenario0154.txt` | 65 | `1521b95342cb305aa09786fa522fd876` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0155.txt` | 6999 | `c49ec681e29e74e6d2930d105928b608` | 是 | 2 |
| `gbk/Scenario0156.txt` | 45397 | `441e1e3c63b275533898c6dcb28dd6e6` | 是 | 46 |
| `gbk/Scenario0157.txt` | 11321 | `54dd6f144d1248b31d6a8350837614b6` | 是 | 5 |
| `gbk/Scenario0158.txt` | 39000 | `a4570f7d96db5215781be3276b6c1e22` | 是 | 21 |
| `gbk/Scenario0159.txt` | 40222 | `b9a9c5dde9fda72fbb5baab127c9f416` | 是 | 63 |
| `gbk/Scenario0160.txt` | 11746 | `db79a02344947b08f729f600bae9515b` | 是 | 13 |
| `gbk/Scenario0161.txt` | 68 | `cbbda8797ca2bd28d1abb0518e58d06d` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0162.txt` | 54745 | `0cb7675956f8244bb5d57966a83f57c2` | 是 | 49 |
| `gbk/Scenario0163.txt` | 8372 | `5bc0b2c21e43f51c040c6a6d175fb296` | 是 | 2 |
| `gbk/Scenario0164.txt` | 83 | `85846c15224b7f37e08522bb9d010545` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0165.txt` | 77 | `e8d8402797a0d26c66a234b3db6939b2` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0166.txt` | 17572 | `cd54becd84e5ab03181c139f8ccf7e88` | 是 | 4 |
| `gbk/Scenario0167.txt` | 74 | `27fa260f78dd7038a4c7817e5d630d79` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0168.txt` | 16854 | `1fd3eb9fd991a497c401ccefaccffbf6` | 是 | 10 |
| `gbk/Scenario0169.txt` | 71 | `ff76302906dcbe31b9aa943066183807` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0170.txt` | 50802 | `aba6a3c6d7bcbbb5fc34643d1f6762f2` | 是 | 42 |
| `gbk/Scenario0171.txt` | 6650 | `2a0b9463c49b96304947cb06dc6d36fe` | 是 | 4 |
| `gbk/Scenario0172.txt` | 59 | `cbabfeb04bca75ab7f8ab8bc3058aa57` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0173.txt` | 19727 | `9d8c9a0a6be71a2f3f9bf3d2d0bdacad` | 是 | 23 |
| `gbk/Scenario0174.txt` | 2483 | `c9c2c0fbb549663acec121dc94a3dfe2` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0175.txt` | 25213 | `6828978ee412ad9743a8d855d6ce0789` | 是 | 17 |
| `gbk/Scenario0176.txt` | 31070 | `09b49080f71925f100b03eaaa9625ac5` | 是 | 19 |
| `gbk/Scenario0177.txt` | 68 | `85cb8e0197c27f1d86fea6c7b49ef791` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0178.txt` | 28277 | `1d90406f7c748b50b8bf05096741adc6` | 是 | 16 |
| `gbk/Scenario0179.txt` | 38794 | `6a994e60bc9d096350d9e8b2badee0e7` | 是 | 39 |
| `gbk/Scenario0180.txt` | 49464 | `45f1c5d5066610bdbb6c26b1249cad25` | 是 | 41 |
| `gbk/Scenario0181.txt` | 5702 | `117347f4c6d88fa716068aa44a303606` | 是 | 4 |
| `gbk/Scenario0182.txt` | 46279 | `719777d2782d6c7d5d11266fc680309f` | 是 | 28 |
| `gbk/Scenario0183.txt` | 65 | `760227bb2ec1d0178d1998ad2e8738a3` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0184.txt` | 17758 | `5f4c98bc64ae7fb9ad8588ed6b321b26` | 是 | 21 |
| `gbk/Scenario0185.txt` | 86 | `6bbc30af99090e52902807ad286a08d5` | 是 | 1 |
| `gbk/Scenario0186.txt` | 7624 | `9a615002e4f4a52308df71a1566c7a53` | 是 | 128 |
| `gbk/Scenario0187.txt` | 15817 | `aa086e612e824192457496a055db3e50` | 是 | 199 |
| `gbk/Scenario0188.txt` | 30318 | `87aaff30febd7a755fd8cc6837ce6588` | 是 | 349 |
| `gbk/Scenario0189.txt` | 12686 | `ff0962682f0fe827cda7756adcc80654` | 是 | 197 |
| `gbk/Scenario0190.txt` | 11126 | `7f13977eb3864596e0b7cb1111b663f3` | 是 | 179 |
| `gbk/Scenario0191.txt` | 6880 | `3a416003ec478ba9cb54f83d7886798c` | 是 | 121 |
| `gbk/Scenario0192.txt` | 71 | `f5cece8475e21183cc0c51dea4a3313f` | 否（已與轉換結果相同） | 0 |
| `gbk/Scenario0193.txt` | 11144 | `93836a06c342a5cb4e0a2505f4a14f48` | 是 | 7 |
| `gbk/ScenarioDB.txt` | 6699 | `443aa99100be720d969f03fd144d40ee` | 是 | 11 |
| `gbk/mainscript.txt` | 13341 | `11e07441bdd0855ba54add7d5d38f869` | 是 | 522 |

