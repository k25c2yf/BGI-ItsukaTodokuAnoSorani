# 字型 v3：Microsoft JhengHei（微軟正黑體）

日期：2026-11-23（Asia/Singapore UTC+8）

**使用本包前請先安裝 Microsoft JhengHei（微軟正黑體）。Wine 請把 `msjh.ttc` 放進字型目錄。建議刪除舊的 `BGI.gdb` 備份後再啟動，以免沿用舊字型快取。**

繁中 `ipl._bp` 以 `B0:C1("Microsoft JhengHei", 3)`（charset BIG5）把正黑體登錄為字型編號 2，系統檔（對白窗、選項、LOG 記錄、存檔畫面、`msgwndctrl`、`userdata` 預設）改用編號 2。簡中 `ipl` 沒有這次字型變更，請勿把本包繁中 ipl 與簡中混用後指望簡中也換成正黑體。

EXE（node3c_zero，md5 `5d560252325004f76876238065fda51d`）未改。
