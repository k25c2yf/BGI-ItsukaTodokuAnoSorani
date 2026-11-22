#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate itsusora route map deliverables from already-verified mainscript facts."""
from __future__ import annotations

import hashlib
import html
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

OUT = Path("/workspace/itsusora/tl/review/route_map_20261114")
FONT_REG = Path("/home/box/.local/share/fonts/cjk/ResourceHanRoundedTW-Regular.ttf")
FONT_BD = Path("/home/box/.local/share/fonts/cjk/ResourceHanRoundedTW-Bold.ttf")
FONT_FALLBACK = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")

# Exact TC strings from tl/tc/mainscript.txt
C1 = ("天使", "惡魔")
C2 = ("出面制止。", "在一旁觀望。")
C3 = ("「竟對公主如此無禮！」斥責的貴族派", "「什麼公主不公主的」自暴自棄的庶民派")
C3_SHORT = ("貴族派（斥責「竟對公主如此無禮！」）", "庶民派（「什麼公主不公主的」自暴自棄）")
C4 = ("雖然難得……", "回答櫻守姬的提問。")  # U+2026 x2

# Choice string IDs: first occurrence in mainscript = choice-array push (UI order)
IDS = {
    "天使": "mainscript●002440● / Scenario0008 / ScenarioDB●008●",
    "惡魔": "mainscript●002500● / Scenario0009 / ScenarioDB●009●",
    "出面制止。": "mainscript●003804● / Scenario0019 / ScenarioDB●019●",
    "在一旁觀望。": "mainscript●003864● / Scenario0020 / ScenarioDB●020●",
    C3[0]: "mainscript●004860● / Scenario0029 / ScenarioDB●029●",
    C3[1]: "mainscript●004920● / Scenario0030 / ScenarioDB●030●",
    C4[0]: "mainscript●005580● / Scenario0034 / ScenarioDB●034●",
    C4[1]: "mainscript●005640● / Scenario0033 / ScenarioDB●033●",
}

def flags(pick1, pick2, pick3, pick4, first_play=False):
    """pick* are 1 or 2. first_play: 天使 is auto (not a visible choice)."""
    F = 0
    K = 0
    talk = False
    angel_auto = first_play
    if first_play or pick1 == 1:
        F += 1  # 天使
    # 惡魔: no increment
    if pick2 == 1:
        F += 1  # 出面制止
    if pick3 == 1:
        K += 1  # 貴族
    if pick4 == 2:
        K += 1
        talk = True
    return F, K, talk, angel_auto

def ending(F, K):
    if K > F:
        return "此芽"
    if F == 0 and K == 0:
        return "傘"
    return "雙見"

def mid_notes(F, K, talk):
    parts = []
    parts.append("有此芽對話（假日・有通過此芽對話）" if talk else "無此芽對話（假日・未通過此芽對話）")
    if K > F:
        parts.append("觸發：朝・此芽的「誓言」、放學後・櫻守姬的規矩、火災〜此芽、交錯的心意〜此芽")
        parts.append("不走〜雙見／〜傘切片")
    else:
        parts.append("不觸發「誓言」與此芽向切片")
        if F == 0 and K == 0:
            parts.append("觸發〜傘／〜其他：照雪之戀〜傘、看家〜傘、食之王（傘的惡夢／和傘／四次元和傘）等；明日起是雙子座〜其他")
        else:
            parts.append("觸發〜雙見切片：明日起是雙子座〜雙見、對照陽菜的認識〜雙見、關於巽家〜雙見、雙子座最後一天〜雙見")
    return "；".join(parts)

def chapters(F, K, ending_name):
    common = "共通 Scenario0002–0109（含旗標切片）"
    if ending_name == "此芽":
        return f"{common} → 此芽 Scenario0135–0163（逃亡者〜過去的清算）"
    # 雙見／傘 share 0111–0112
    shared = "斜陽的心情／炎之子 Scenario0111–0112"
    if ending_name == "傘":
        return f"{common} → {shared} → 傘 Scenario0165–0184（無法放開這雙手〜傘姊後記）"
    return f"{common} → {shared} → 雙見 Scenario0113–0133（雙見回家〜雙見後記２）"

def choice_seq(picks, first_play):
    labels = []
    if not first_play:
        labels.append(C1[picks[0] - 1])
    labels.append(C2[picks[1] - 1])
    labels.append(C3[picks[2] - 1])
    labels.append(C4[picks[3] - 1])
    return "→".join(labels)

def choice_ids(picks, first_play):
    ids = []
    if not first_play:
        ids.append(IDS[C1[picks[0] - 1]])
    ids.append(IDS[C2[picks[1] - 1]])
    ids.append(IDS[C3[picks[2] - 1]])
    ids.append(IDS[C4[picks[3] - 1]])
    return " | ".join(ids)

def route_code(picks, first_play):
    if first_play:
        return f"{picks[1]}-{picks[2]}-{picks[3]}"
    return f"{picks[0]}-{picks[1]}-{picks[2]}-{picks[3]}"

def all_routes():
    rows = []
    # first play: 8 codes
    for a in (1,):  # auto 天使
        for b in (1, 2):
            for c in (1, 2):
                for d in (1, 2):
                    picks = (a, b, c, d)
                    F, K, talk, _ = flags(*picks, first_play=True)
                    end = ending(F, K)
                    code = route_code(picks, True)
                    cleared = "yes" if code == "1-1-1" else "no"
                    notes = (
                        f"初回（天使自動，不列入路線碼）。F={F}（slot 0x0A）、K={K}（slot 0x0B）。"
                        f"{mid_notes(F,K,talk)}。"
                        "二週目若選天使，對應 4 碼為 1-" + code + "（旗標相同）。"
                    )
                    rows.append(dict(
                        route_code=code, ending=end,
                        choice_seq=choice_seq(picks, True),
                        chapters=chapters(F, K, end),
                        choice_ids=choice_ids(picks, True),
                        cleared=cleared, notes=notes,
                        play_type="初回", F=F, K=K, talk=talk, picks=picks,
                    ))
    # NG+ 16 codes
    for a in (1, 2):
        for b in (1, 2):
            for c in (1, 2):
                for d in (1, 2):
                    picks = (a, b, c, d)
                    F, K, talk, _ = flags(*picks, first_play=False)
                    end = ending(F, K)
                    code = route_code(picks, False)
                    cleared = "yes" if code == "2-2-1-2" else "no"
                    extra = ""
                    if a == 1:
                        extra = f"與初回 {b}-{c}-{d} 旗標相同（皆走天使）。"
                    if end == "傘":
                        extra += "初回因自動天使 F≥1，走不到傘線；僅二週目選惡魔且後三選皆「不加分」項（旁觀、庶民、雖然難得）可進傘線。"
                    notes = (
                        f"二週目（通關雙見或此芽後重開，第一章出現天使／惡魔）。"
                        f"F={F}（slot 0x0A）、K={K}（slot 0x0B）。"
                        f"{mid_notes(F,K,talk)}。{extra}"
                    )
                    rows.append(dict(
                        route_code=code, ending=end,
                        choice_seq=choice_seq(picks, False),
                        chapters=chapters(F, K, end),
                        choice_ids=choice_ids(picks, False),
                        cleared=cleared, notes=notes.strip(),
                        play_type="二週目", F=F, K=K, talk=talk, picks=picks,
                    ))
    # special
    rows.append(dict(
        route_code="（特殊啟動 mode=2）",
        ending="《異ならぬ世の終わりより》（隱藏／神話篇）",
        choice_seq="（本篇四選項走不到；mainscript 以 $E1(0)==2 進入）",
        chapters="Scenario0185–0191（原初的鬥爭〜激怒的終焉）",
        choice_ids="mainscript $11A／$F1「異ならぬ世の終わりより」@0x43E0；ScenarioDB●185●–●191●",
        cleared="no",
        notes="標題／特殊啟動。解鎖如何在標題畫面點選，系統腳本多為圖片選單，本圖標為未完全解開；建議三條女主線通關後檢查標題或附贈是否出現新項目。內容為奧丁／『激怒』神話，不是愛愛或音的獨立女主線。",
        play_type="特殊", F="", K="", talk="", picks=None,
    ))
    rows.append(dict(
        route_code="（特殊啟動 mode=3）",
        ending="附贈劇本",
        choice_seq="（本篇四選項走不到；mainscript 以 $E1(0)==3 進入）",
        chapters="Scenario0193（附贈劇本）；Scenario0192 スタッフルーム為標題卡殘件",
        choice_ids="mainscript $F1「おまけしなりお」@0x47C4；ScenarioDB●193●",
        cleared="no",
        notes="標題／特殊啟動。如何從標題進入未完全從系統腳本解開。劇本開頭會勸玩家 ALT+F4，其後為平行世界搞笑後日談。",
        play_type="特殊", F="", K="", talk="", picks=None,
    ))
    return rows


def write_tsv(rows):
    cols = ["route_code", "ending", "choice_seq", "chapters", "choice_ids", "cleared", "notes"]
    # add helper cols
    cols2 = cols + ["play_type", "F", "K"]
    lines = ["\t".join(cols2)]
    for r in rows:
        lines.append("\t".join(str(r.get(c, "")) for c in cols2))
    (OUT / "routes.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_readme(rows):
    fp = [r for r in rows if r["play_type"] == "初回"]
    ng = [r for r in rows if r["play_type"] == "二週目"]
    def tbl(rs):
        out = ["| 路線碼 | 選項序列（簡） | F,K | 結尾 | 已測 |",
               "|---|---|---|---|---|"]
        for r in rs:
            picks = r["picks"]
            if r["play_type"] == "初回":
                short = "→".join([C2[picks[1]-1].rstrip("。"), "貴族" if picks[2]==1 else "庶民", "雖然難得" if picks[3]==1 else "回答提問"])
            else:
                short = "→".join([C1[picks[0]-1], C2[picks[1]-1].rstrip("。"), "貴族" if picks[2]==1 else "庶民", "雖然難得" if picks[3]==1 else "回答提問"])
            mark = "是（已通關）" if r["cleared"]=="yes" else "否"
            out.append(f"| **{r['route_code']}** | {short} | {r['F']},{r['K']} | {r['ending']} | {mark} |")
        return "\n".join(out)

    text = f"""# 《何時到達那片天空》路線選項圖（2026-11-14）

給實機測試用：照著選項碼走完全線。編號與已通關的 **1-1-1**、**2-2-1-2** 同一套。

本包不改 official tl／sys，也不編譯、不煙測、不動 EXE。全部選項與跳轉均從現譯繁中劇本與日文 `mainscript` 反組譯對回。

## 檔案

- `route_map_overview.png`／`.svg`：全覽（選項、旗標公式、三條女主結尾、二週目解鎖）
- `route_map_all_codes.png`／`.svg`：全部可玩路線碼一覽（已通關者以星號標出）
- `route_map_midflags.png`／`.svg`：共通線上「無選項、依旗標自動分枝」的走法
- `routes.tsv`：標準欄位清單
- `NOTE_route_map_20261114.md`：抽取方法與不確定點
- `MANIFEST`：檔名與 md5

另附 `route_map_overview.dot`／`.mmd` 源稿（本機套件庫當時無法安裝 graphviz，圖由 Python＋繁中 TTF 直接繪出，源稿可供日後用 dot／mermaid 重繪）。

## 編號規則

- **第 n 次出現在畫面上的選項**，選 **由上到下第 k 項**（從 1 起算），用連字號串成路線碼。
- 選項文與順序以 `mainscript` 的 `$160` 選擇陣列為準（不是 ScenarioDB 章序）。尤其第 4 次：**第 1 項是「雖然難得……」，第 2 項才是「回答櫻守姬的提問。」**（DB 裡 033／034 章號與此相反，不要依章號點選）。
- 本篇一共 **4 個玩家選項**（全部在共通線前段）。其後女主線分歧是旗標自動跳轉，不再出現 `$160` 選項。

### 初回＝3 碼

全新存檔（尚未通關雙見或此芽）**不會出現**「天使／惡魔」。腳本在「早晨・早安」（Scenario0007）之後**自動走「天使」**（並給 F+1），然後才出現後 3 個選項。因此初回路線碼是 3 位數，例如 **1-1-1**。

### 二週目＝4 碼（通關旗標解鎖）

通關 **雙見**（`$E2(0x0A,1)`）或 **此芽**（`$E2(0x0B,1)`）後，從標題重開新遊戲，第一章（「早晨・早安」之後、貳壹學園早晨）會出現：

1. 天使
2. 惡魔

此時路線碼改為 4 位數，第一碼就是這組。例如已通關的 **2-2-1-2**＝惡魔→在一旁觀望。→貴族派→回答櫻守姬的提問。

說明：

- 解鎖條件（mainscript @0x090C）：`$E3(0x0A)==1` **或** `$E3(0x0B)==1`（分別對應已通關雙見／此芽）。
- 腳本也讀取 `$E3(0x0C)`（傘通關旗），但**不用它來解鎖這組選項**。實務上傘線本身要先有二週目才能走，故先通關的一定是雙見或此芽。
- 選「天使」：與初回相同，F+1。選「惡魔」：F 不加。
- 若二週目選天使，後三碼與初回同碼時，旗標與結尾相同（例如二週目 `1-1-1-1` ≡ 初回 `1-1-1`）。

## 四次選項（畫面順序）

| 次 | 出現位置 | 第 1 項 | 第 2 項 | 旗標效果 |
|---|---|---|---|---|
| ① | 早晨・早安之後（Scenario0007 後）。**僅二週目顯示**；初回自動① | 天使（F+1，進 Scenario0008） | 惡魔（不加，進 Scenario0009） | 合流 Scenario0010 |
| ② | 學園・首位男性委員（Scenario0018）之後 | 出面制止。（F+1，Scenario0019） | 在一旁觀望。（不加，Scenario0020） | 合流 Scenario0021 |
| ③ | 學園・果然水火不容（Scenario0028）之後 | 「竟對公主如此無禮！」斥責的貴族派（K+1，Scenario0029） | 「什麼公主不公主的」自暴自棄的庶民派（不加，Scenario0030） | 合流 Scenario0031 |
| ④ | 放學後・金牛座的照陽菜準備（Scenario0032）之後 | 雖然難得……（不加，Scenario0034） | 回答櫻守姬的提問。（K+1，並記「此芽對話」slot 0x0D，Scenario0033） | 之後進入條件分歧 |

F＝變數 `var_0x38`，寫入 `$0E0(0x0A, F)`。K＝`var_0x34`，寫入 `$0E0(0x0B, K)`。此芽對話＝`$0E0(0x0D, 1)`，讀取為 `$E1(0x0D)==1`。

## 結尾怎麼決定（「假日・符合」之後）

共通線走到 Scenario0109「假日・符合」後：

1. 若 **K > F** → **此芽線**（Scenario0135–0163），通關時 `$E2(0x0B, 1)`
2. 否則先播「斜陽的心情／炎之子」（Scenario0111–0112）
   - 若 **F==0 且 K==0** → **傘線**（Scenario0165–0184），通關時 `$E2(0x0C, 1)`
   - 否則 → **雙見線**（Scenario0113–0133），通關時 `$E2(0x0A, 1)`

因此：

- **初回**自動天使使 F≥1，**走不到傘線**。初回 8 條碼裡，只有 **2-1-2**（旁觀→貴族→回答）是此芽，其餘 7 條都是雙見。
- **傘線**只在二週目選 **2-2-2-1**（惡魔→旁觀→庶民→雖然難得），F=0、K=0。

腳本中**沒有**愛愛、音、綠野、靜的獨立 `$F1` 結尾區塊。愛愛主要出現在雙見線（照顧愛愛等），音／透舞神社出現在傘線。不要按舊攻略去找不存在的愛愛／音獨立線。

另外兩條不是本篇選項走出來的：

- 《異ならぬ世の終わりより》（隱藏／神話篇，Scenario0185–0191）：起始模式 `$E1(0)==2`
- 附贈劇本（Scenario0193）：起始模式 `$E1(0)==3`

未發現獨立 Bad End 區塊（三條女主線都有後記／H）。

## 已測／未測

| 路線碼 | 性質 | 結尾（由旗標推算） | 狀態 |
|---|---|---|---|
| **1-1-1** | 初回：出面制止。→貴族派→雖然難得…… | 雙見（F=2, K=1） | **已通關** |
| **2-2-1-2** | 二週目：惡魔→在一旁觀望。→貴族派→回答提問 | 此芽（F=0, K=2） | **已通關** |
| 其餘初回 7 條、二週目 15 條、隱藏篇、附贈 | 見下表 | 見下表 | 未測 |

## 初回（3 碼）清單

{tbl(fp)}

## 二週目（4 碼）清單

{tbl(ng)}

## 共通線上的自動分枝（無新選項）

這些不改變路線碼，但劇情切片不同。觸發條件都是上面的 F、K、此芽對話。細節見 `route_map_midflags.png` 與 `routes.tsv` 的 notes。

- 朝・此芽的「誓言」（Scenario0037）：K > F
- 假日・有／未通過此芽對話（0039／0040）：此芽對話旗（回答④第 2 項）
- 明日起是「雙子座」〜雙見／〜其他（0043／0044）、對照陽菜的認識〜雙見、關於巽家〜雙見、雙子座最後一天〜雙見：F≥K 且並非兩者皆 0
- 照雪之戀〜傘、看家〜傘、食之王（傘的惡夢等）：F==0 且 K==0
- 放學後・櫻守姬的規矩、火災〜此芽、交錯的心意〜此芽：K > F

## 來源

- 現譯繁中：`/workspace/itsusora/tl/tc/mainscript.txt`、`ScenarioDB.txt`、`Scenario????.txt`
- 日文原稿（UTF-16 dump 與 bin）：`/workspace/itsusora/dump_v200/`、`/workspace/itsusora/att/x_v200/mainscript`（舊式無標頭 BGI，`$160`＝選項、`$F1`＝載入章標題、`$0E0`／`$E1`／`$E2`／`$E3`＝旗標）
- 章標題：`ScenarioDB.txt`
- 選項系統：`scrslct._bp` 只負責選項畫面繪製；選項文與跳轉在 `mainscript`

用語：雙見、愛愛、音、綠野、此芽、傘、靜（不用美美／萌萌／舊譯娜）。
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")


def write_note():
    text = """# NOTE　路線選項圖抽取方法（2026-11-14）

## 方法

1. 現譯繁中 `tl/tc/ScenarioDB.txt`、`mainscript.txt`、各 `Scenario????.txt` 先對出章標題與選項文（選項文同時存在於 mainscript 與作為獨立章的 Scenario0019／0020 等）。
2. 日文 `att/x_v200/mainscript`（360 349 位元組，舊式無 `BurikoCompiledScript` 標頭）以專案既有 `bgi_script_disasm.py` 反組譯。字串池起點 0x5607D，主函式約 0x0–0x5A08。
3. 全書只找到 **4 處** `$160`（選擇指令）：在選擇陣列寫入 2 條字串後 `nargs 2; $160`，回傳 0-based 索引到 `var_0x3C`。未在各章 Scenario 檔發現真正的 `$160`／`$0E0`（對齊掃描的命中經反組譯確認為假陽性）。
4. 跳轉以 `$F1_scenario_switch`＋章標題字串為準（154 處），並以 `$1B4(0, "NNN")` 的三位數對回 Scenario 編號（NNN+1，因 0000 為無題）。`$11A_scene_meta` 為日期／章題卡。
5. 旗標：`$0E0(slot, value)` 寫、`$E1(slot)` 讀（本週目計數，開新遊戲時從存檔／系統讀入後再累加）、`$E2(slot, 1)` 寫通關、`$E3(slot)` 讀通關。slot 0x0A＝雙見通關／F 計數、0x0B＝此芽通關／K 計數、0x0C＝傘通關、0x0D＝此芽對話。
6. 「天使／惡魔」解鎖：`($E3(0x0A)==1) || ($E3(0x0B)==1)` 為真才進入 `$160`；否則 `jz` 跳到自動「天使」（含 F+1）。這與使用者「通關後重開，第一章出現天使與惡魔」一致。條件出現在「朝・おはようございます」（Scenario0007）之後，屬貳壹學園第一日早晨，不是 Scenario0002 序章本文之內。
7. 未用網路攻略當準。網路若與腳本不符，以腳本為準。

## 計數

- 玩家選項點：4（其中 1 個僅二週目顯示）
- 初回可玩路線碼：8（3 碼）
- 二週目可玩路線碼：16（4 碼）
- 女主結尾：3（雙見／此芽／傘）
- 特殊結尾：2（隱藏神話篇《異ならぬ世の終わりより》、附贈劇本）
- 已標已測：2 條（1-1-1→雙見，2-2-1-2→此芽），皆由旗標公式推算結尾，通關當日未另外從存檔核對結尾名稱
- 自動分枝點（無 `$160`）：約 12 處（誓言、此芽對話、雙見切片、傘切片、此芽向切片、符合後三大分歧）

## 不確定／未完全解開

- **標題如何進入隱藏篇／附贈**：mainscript 以 `$E1(0)` 為啟動模式（0＝本篇、2＝異ならぬ世の終わりより、3＝おまけしなりお；另有 1、0x64、0x3E8 等模式，1 看起來像短程返回、0x3E8 像回想／H 重播）。`title._bp` 幾乎沒有可讀的日文選單字（多半是圖片按鈕），故「通關幾條線後標題出現哪一個按鈕」**未證**。建議三線通關後目視標題與附贈。
- **`$E1(0)==1`、Staff Room（Scenario0192）**：0192 只是標題卡殘件；mode 1 的路徑未掛 `$F1` 章，用途未證。
- **ScenarioDB 中若干題卡**（《哀しいほど優しきこの世界》●110●、《誇らしきその歩み》●134●、《背に負ったいしの重みは》●164●）在 mainscript **沒有**對應 `$F1`。可能未使用或由其他系統顯示，標為未證是否播放。
- **傘通關旗 `$E3(0x0C)`** 在開場被讀入 `var_0x24`，但主流程不用它解鎖天使／惡魔。後段 helper（約 0x4ED2C）有檢查此旗，可能與回想／流程圖解鎖有關，未完整追完。
- **本週目 F／K 是否在「繼續遊戲」時從 `$E1` 帶回**：開場確實 `var_38=$E1(0x0A)`、`var_34=$E1(0x0B)`。若中途存檔再讀，應延續當週目計數。跨週目是否清零，依引擎把 `$E1` 放在系統還是遊戲存檔而定；路線圖以「新遊戲從 0 起算再加本週目選擇」為準。若實機新遊戲卻看到非 0 的殘留，以實機為準並回報。
- **jz 極性**：以「K>F 才播此芽的誓言／才進此芽線」反推 `jz`＝條件為假才跳，前後一致。已用來對回 1-1-1→雙見、2-2-1-2→此芽。
- 未跑 EXE、未煙測。

## 繪圖

套件庫當時無法安裝 graphviz（debian 鏡像 500）。圖以 Python／Pillow 寫入 Resource Han Rounded TW 與（必要時）Noto Sans CJK TC，並抽查 cmap 與點陣墨水，避免豆腐字。同內容另存 SVG（字轉 path 或 text＋font-face）。
"""
    (OUT / "NOTE_route_map_20261114.md").write_text(text, encoding="utf-8")


# --------------- drawing ---------------

def load_font(size, bold=False):
    path = FONT_BD if bold and FONT_BD.exists() else FONT_REG
    if path.exists():
        return ImageFont.truetype(str(path), size=size)
    # TTC index 3 = Noto Sans CJK TC
    return ImageFont.truetype(str(FONT_FALLBACK), size=size, index=3)


def font_has_chars(s: str) -> list[str]:
    missing = []
    fonts = []
    if FONT_REG.exists():
        fonts.append(TTFont(str(FONT_REG)))
    fonts.append(TTFont(str(FONT_FALLBACK), fontNumber=3))
    cmaps = []
    for f in fonts:
        cmap = {}
        for t in f["cmap"].tables:
            cmap.update(t.cmap)
        cmaps.append(cmap)
    for ch in s:
        if ord(ch) < 32:
            continue
        if not any(ord(ch) in cmap for cmap in cmaps):
            missing.append(ch)
    for f in fonts:
        f.close()
    return missing


class Canvas:
    def __init__(self, w, h, bg="#F7F1E3"):
        self.w, self.h, self.bg = w, h, bg
        self.im = Image.new("RGB", (w, h), bg)
        self.dr = ImageDraw.Draw(self.im)
        self.svg_ops = []
        self._chars = set()

    def rect(self, x, y, w, h, fill, outline="#3A2F1B", width=2, radius=12):
        self.dr.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill, outline=outline, width=width)
        self.svg_ops.append(("rect", x, y, w, h, fill, outline, width, radius))

    def line(self, x1, y1, x2, y2, fill="#3A2F1B", width=3):
        self.dr.line((x1, y1, x2, y2), fill=fill, width=width)
        self.svg_ops.append(("line", x1, y1, x2, y2, fill, width))

    def polygon(self, pts, fill="#3A2F1B"):
        self.dr.polygon(pts, fill=fill)
        self.svg_ops.append(("poly", pts, fill))

    def arrow(self, x1, y1, x2, y2, fill="#3A2F1B", width=3):
        self.line(x1, y1, x2, y2, fill, width)
        # arrow head
        if x1 == x2 and y2 > y1:
            self.polygon([(x2, y2), (x2 - 7, y2 - 12), (x2 + 7, y2 - 12)], fill)
        elif x1 == x2 and y2 < y1:
            self.polygon([(x2, y2), (x2 - 7, y2 + 12), (x2 + 7, y2 + 12)], fill)
        elif y1 == y2 and x2 > x1:
            self.polygon([(x2, y2), (x2 - 12, y2 - 7), (x2 - 12, y2 + 7)], fill)
        elif y1 == y2 and x2 < x1:
            self.polygon([(x2, y2), (x2 + 12, y2 - 7), (x2 + 12, y2 + 7)], fill)

    def text(self, x, y, s, size=22, fill="#2B2114", bold=False, anchor="lt"):
        self._chars.update(s)
        font = load_font(size, bold)
        self.dr.text((x, y), s, font=font, fill=fill, anchor=anchor)
        self.svg_ops.append(("text", x, y, s, size, fill, bold, anchor))

    def wrap_text(self, x, y, s, size, fill, box_w, bold=False, line_h=None, center=False):
        font = load_font(size, bold)
        if line_h is None:
            line_h = int(size * 1.35)
        # greedy wrap
        lines, cur = [], ""
        for ch in s:
            trial = cur + ch
            bb = font.getbbox(trial)
            if bb[2] - bb[0] <= box_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
        for i, ln in enumerate(lines):
            if center:
                self.text(x + box_w / 2, y + i * line_h, ln, size, fill, bold, anchor="mt")
            else:
                self.text(x, y + i * line_h, ln, size, fill, bold, anchor="lt")
        return len(lines) * line_h

    def save_png(self, path: Path):
        self.im.save(path, "PNG", optimize=True)

    def save_svg(self, path: Path):
        # Render text as SVG text with font-family; also embed font file as base64 subset would be huge.
        # Convert glyphs to paths via fontTools for portability.
        from fontTools.ttLib import TTFont
        from fontTools.pens.svgPathPen import SVGPathPen
        from fontTools.pens.transformPen import TransformPen
        font_r = TTFont(str(FONT_REG))
        font_b = TTFont(str(FONT_BD)) if FONT_BD.exists() else font_r
        glyf_r, glyf_b = font_r["glyf"], font_b["glyf"]
        cmap_r, cmap_b = {}, {}
        for t in font_r["cmap"].tables:
            cmap_r.update(t.cmap)
        for t in font_b["cmap"].tables:
            cmap_b.update(t.cmap)
        upem_r = font_r["head"].unitsPerEm
        upem_b = font_b["head"].unitsPerEm
        hmtx_r, hmtx_b = font_r["hmtx"], font_b["hmtx"]

        def glyph_path(font, cmap, glyf, hmtx, upem, ch, size):
            gid = cmap.get(ord(ch))
            if gid is None:
                return "", 0
            pen = SVGPathPen(font.getGlyphSet())
            scale = size / upem
            tpen = TransformPen(pen, (scale, 0, 0, -scale, 0, 0))
            font.getGlyphSet()[gid].draw(tpen)
            adv = hmtx[gid][0] * scale
            return pen.getCommands(), adv

        parts = [
            f'<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">',
            f'<rect width="100%" height="100%" fill="{self.bg}"/>',
        ]
        for op in self.svg_ops:
            typ = op[0]
            if typ == "rect":
                _, x, y, w, h, fill, outline, width, radius = op
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" ry="{radius}" '
                    f'fill="{fill}" stroke="{outline}" stroke-width="{width}"/>'
                )
            elif typ == "line":
                _, x1, y1, x2, y2, fill, width = op
                parts.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{fill}" stroke-width="{width}" stroke-linecap="round"/>'
                )
            elif typ == "poly":
                _, pts, fill = op
                ps = " ".join(f"{px},{py}" for px, py in pts)
                parts.append(f'<polygon points="{ps}" fill="{fill}"/>')
            elif typ == "text":
                _, x, y, s, size, fill, bold, anchor = op
                font = font_b if bold else font_r
                cmap = cmap_b if bold else cmap_r
                glyf = glyf_b if bold else glyf_r
                hmtx = hmtx_b if bold else hmtx_r
                upem = upem_b if bold else upem_r
                # measure width for anchor
                width = 0
                cmds = []
                for ch in s:
                    d, adv = glyph_path(font, cmap, glyf, hmtx, upem, ch, size)
                    cmds.append((d, adv, ch))
                    width += adv
                # PIL anchor: lt = top-left of text bbox approx; mt = mid-top; lm mid-left
                # Pillow text anchor lt is at top-left of em-box-ish. We'll match using ascent.
                ascent = size * 0.8
                if anchor == "mt":
                    px = x - width / 2
                    py = y + ascent
                elif anchor == "mm":
                    px = x - width / 2
                    py = y + ascent / 2
                elif anchor == "lm":
                    px = x
                    py = y + ascent / 2
                else:  # lt
                    px = x
                    py = y + ascent
                parts.append(f'<g fill="{fill}">')
                cx = px
                for d, adv, ch in cmds:
                    if d:
                        parts.append(f'<path transform="translate({cx:.2f},{py:.2f})" d="{d}"/>')
                    cx += adv
                parts.append("</g>")
        parts.append("</svg>")
        path.write_text("\n".join(parts), encoding="utf-8")
        font_r.close()
        if font_b is not font_r:
            font_b.close()


# colors
INK = "#2B2114"
LINE = "#5A4A32"
GOLD = "#C9A227"
CREAM = "#FFF9EF"
PAPER = "#F7F1E3"
BOX = "#FFFDF7"
NG = "#F3E2C4"      # second-play highlight
OK = "#E7F3DA"      # cleared
END_F = "#F8E6D4"   # 雙見
END_K = "#E3EEF8"   # 此芽
END_S = "#EEE4F6"   # 傘
END_H = "#F5E8C8"   # hidden
MUTED = "#F0EAE0"
RED = "#8B2E1F"
GREEN = "#2E5A32"
BLUE = "#1E4A70"
PURPLE = "#4A2E6B"


def draw_overview(rows):
    cv = Canvas(3400, 2400)
    # title
    cv.rect(0, 0, 3400, 132, fill="#3A2F1B", outline="#3A2F1B", radius=0)
    cv.text(80, 28, "何時到達那片天空　路線選項圖", 44, "#FFF9EF", bold=True)
    cv.text(80, 84, "給實機測試　·　編號與已通關的 1-1-1、2-2-1-2 同一套　·　2026-11-14", 22, "#E8D9B0")
    cv.text(2480, 40, "已通關以 ★ 標出", 22, "#E8D9B0", bold=True)

    # numbering box
    cv.rect(60, 160, 3280, 150, fill=CREAM, outline=GOLD, width=3)
    cv.text(80, 172, "編號規則", 24, INK, bold=True)
    cv.text(80, 210, "第 n 次出現在畫面上的選項，選由上到下第 k 項（從 1 起算），用連字號連接。選項順序以 mainscript $160 陣列為準，不是 ScenarioDB 章號。", 20, INK)
    cv.text(80, 244, "初回（尚未通關雙見／此芽）：不出現「天使／惡魔」，系統自動走天使（F+1），路線碼為 3 碼。　例如 ★1-1-1＝出面制止。→貴族派→雖然難得……→雙見。", 20, INK)
    cv.text(80, 278, "二週目（通關雙見或此芽後從標題重開）：第一章「早晨・早安」之後解鎖「1 天使／2 惡魔」，路線碼為 4 碼。　例如 ★2-2-1-2＝惡魔→在一旁觀望。→貴族派→回答提問→此芽。", 20, INK)

    # flow columns
    # Start
    def box(x, y, w, h, fill, title, lines, title_color=INK, tw=22, bw=20):
        cv.rect(x, y, w, h, fill=fill, outline=LINE, width=2, radius=14)
        cv.text(x + 16, y + 10, title, tw, title_color, bold=True)
        yy = y + 42
        for ln, sz, col, bd in lines:
            cv.wrap_text(x + 16, yy, ln, sz, col, w - 32, bold=bd)
            yy += int(sz * 1.4) if len(ln) < 40 else int(sz * 1.4) * 2
        return x + w / 2, y + h

    # row 0 start
    cx, bottom = box(140, 340, 360, 110, BOX, "開始",
                     [("序章 Scenario0002，5 月 16 日前後", 18, INK, False),
                      ("經「和雙見在一起」進入貳壹學園", 18, INK, False)])

    # NG+ choice
    cv.arrow(cx, bottom, cx, 500)
    # two boxes: auto vs unlock
    box(80, 510, 420, 210, MUTED, "初回（自動，不列入路線碼）",
        [("早晨・早安（Scenario0007）之後", 17, INK, False),
         ("不顯示選項，直接走「天使」", 18, INK, False),
         ("F+1，進 Scenario0008，再合流 0010", 17, INK, False)], tw=20)
    box(560, 510, 560, 210, NG, "二週目解鎖　選項①（通關旗標）",
        [("條件：已通關雙見 $E3(0x0A) 或已通關此芽 $E3(0x0B)", 16, RED, True),
         ("1  天使　→ F+1　Scenario0008", 18, INK, False),
         ("2  惡魔　→ 不加　Scenario0009", 18, INK, False),
         ("合流：早晨・早安〜合流 Scenario0010", 16, INK, False)], tw=20, title_color=RED)

    cv.line(290, 720, 290, 760, LINE, 3)
    cv.line(840, 720, 840, 760, LINE, 3)
    cv.line(290, 760, 840, 760, LINE, 3)
    cv.arrow(565, 760, 565, 800)

    box(200, 800, 730, 170, BOX, "選項②　學園・首位男性委員（Scenario0018）之後",
        [("1  出面制止。　→ F+1　Scenario0019", 20, INK, False),
         ("2  在一旁觀望。　→ 不加　Scenario0020", 20, INK, False),
         ("合流 Scenario0021　→ 繼續共通線", 17, INK, False)], tw=20)
    cv.arrow(565, 970, 565, 1010)

    box(140, 1010, 850, 200, BOX, "選項③　學園・果然水火不容（Scenario0028）之後",
        [("1  「竟對公主如此無禮！」斥責的貴族派　→ K+1　Scenario0029", 18, INK, False),
         ("2  「什麼公主不公主的」自暴自棄的庶民派　→ 不加　Scenario0030", 18, INK, False),
         ("注意：以畫面上到下為準。合流 Scenario0031。", 16, LINE, False)], tw=20)
    cv.arrow(565, 1210, 565, 1250)

    box(140, 1250, 850, 200, BOX, "選項④　放學後・金牛座的照陽菜準備（Scenario0032）之後",
        [("1  雖然難得……　→ 不加　Scenario0034（注意：這是畫面上的第 1 項）", 17, INK, False),
         ("2  回答櫻守姬的提問。　→ K+1，並記「此芽對話」　Scenario0033", 17, INK, False),
         ("DB 章號 033／034 與畫面順序相反，測試時不要依章號點。", 16, RED, False)], tw=20)

    cv.arrow(565, 1450, 565, 1490)
    box(180, 1490, 770, 120, MUTED, "共通線走到「假日・符合」Scenario0109（約 6 月 22 日）",
        [("其間尚有依 F／K／此芽對話自動插入的切片，見 midflags 圖。無新的玩家選項。", 17, INK, False)], tw=20)

    # ending dispatch on the right
    cv.arrow(950, 1550, 1120, 1550)
    box(1120, 1480, 700, 160, CREAM, "結尾公式（符合之後）",
        [("若 K > F　→　此芽線", 22, BLUE, True),
         ("否則先播斜陽的心情／炎之子（0111–0112）", 18, INK, False),
         ("　F=0 且 K=0　→　傘線；否則　→　雙見線", 18, INK, False)], tw=22)

    # three ending boxes
    y_end = 1680
    box(80, y_end, 1000, 230, END_F, "雙見線　Scenario0113–0133",
        [("條件：不是（K>F），且不是（F=K=0）", 18, INK, False),
         ("★ 已通關 1-1-1（初回，F=2, K=1）", 20, GREEN, True),
         ("初回 8 碼中有 7 碼進這裡。含後記／H。通關寫 $E2(0x0A,1)。", 17, INK, False),
         ("日期約 6/22–6/29。愛愛戲份（照顧愛愛等）在此線。", 17, INK, False)], tw=24, title_color="#7A3E12")

    box(1140, y_end, 1060, 230, END_K, "此芽線　Scenario0135–0163",
        [("條件：K > F", 18, INK, False),
         ("★ 已通關 2-2-1-2（二週目，F=0, K=2）", 20, GREEN, True),
         ("初回唯一此芽碼：2-1-2（旁觀→貴族→回答）。通關寫 $E2(0x0B,1)。", 17, INK, False),
         ("日期約 6/22 起。含結婚式、此芽後記／H、過去的清算。", 17, INK, False)], tw=24, title_color=BLUE)

    box(2260, y_end, 1080, 230, END_S, "傘線　Scenario0165–0184",
        [("條件：F=0 且 K=0　→　僅二週目 2-2-2-1", 18, INK, False),
         ("惡魔→在一旁觀望。→庶民派→雖然難得……", 18, INK, True),
         ("初回自動天使使 F≥1，走不到。通關寫 $E2(0x0C,1)。", 17, INK, False),
         ("含透舞神社、傘姊後記／H。音的戲份多在此線。", 17, INK, False)], tw=24, title_color=PURPLE)

    # side column: flags + hidden
    box(1960, 340, 1380, 250, NG, "「天使／惡魔」解鎖（請務必測）",
        [("位置：第一章，貳壹學園早晨，「早晨・早安」Scenario0007 之後（不是序章 0002 本文內）。", 17, INK, False),
         ("解鎖：系統通關旗　已通關雙見或已通關此芽。與使用者「通關後重開就出現」一致。", 17, INK, False),
         ("未解鎖：不顯示選項，自動天使（F+1）。這就是初回只有 3 碼的原因。", 17, INK, False),
         ("跳轉：1→Scenario0008 天使；2→Scenario0009 惡魔；皆合流 Scenario0010。", 17, INK, False)], tw=22, title_color=RED)

    box(1960, 620, 1380, 280, BOX, "旗標速記（新遊戲從 0 起算）",
        [("F（slot 0x0A）：選「天使」或「出面制止。」各 +1", 18, INK, False),
         ("K（slot 0x0B）：選「貴族派」或「回答櫻守姬的提問。」各 +1", 18, INK, False),
         ("此芽對話（slot 0x0D）：只有「回答提問」會寫入，影響對話切片、不單獨決定結尾。", 17, INK, False),
         ("例：1-1-1 → 自動天使+制止+貴族+難得 ⇒ F=2,K=1 ⇒ 雙見", 17, INK, False),
         ("例：2-2-1-2 → 惡魔+旁觀+貴族+回答 ⇒ F=0,K=2 ⇒ 此芽", 17, INK, False)], tw=22)

    box(1960, 930, 1380, 280, END_H, "本篇選項走不到的兩條",
        [("《異ならぬ世の終わりより》　隱藏／神話篇　Scenario0185–0191", 18, INK, True),
         ("起始模式 $E1(0)==2。奧丁／『激怒』。不是愛愛或音的女主線。標題如何點選：未完全解開。", 16, INK, False),
         ("附贈劇本　Scenario0193　起始模式 $E1(0)==3。平行世界搞笑後日談。", 17, INK, False),
         ("腳本中沒有愛愛／音／綠野／靜的獨立結尾區塊，也未發現獨立 Bad End。", 16, INK, False)], tw=22)

    box(1960, 1240, 1380, 200, MUTED, "測試建議（尚未測的關鍵碼）",
        [("初回此芽：2-1-2。　二週目傘（唯一）：2-2-2-1。", 18, INK, True),
         ("二週目其他此芽：2-1-1-2、2-2-1-1、2-2-2-2 等（凡 K>F）。", 17, INK, False),
         ("隱藏篇／附贈：三條女主線通關後檢查標題畫面。", 17, INK, False)], tw=22)

    cv.text(80, 2240, "來源：tl/tc 現譯＋ att/x_v200/mainscript 反組譯（$160／$F1／$0E0／$E2／$E3）。用語：雙見、此芽、傘、愛愛、音、綠野、靜。不改 official tl／sys。", 16, LINE)
    cv.text(80, 2278, "亞洲／香港時間製作。", 16, LINE)

    return cv


def draw_all_codes(rows):
    cv = Canvas(3200, 2280)
    cv.rect(0, 0, 3200, 120, fill="#3A2F1B", outline="#3A2F1B", radius=0)
    cv.text(70, 24, "全部可玩路線碼　·　何時到達那片天空", 40, "#FFF9EF", bold=True)
    cv.text(70, 76, "★＝使用者已通關　·　F／K 為本週目計數　·　結尾由 mainscript 公式推算", 20, "#E8D9B0")

    def header(y, title, fill):
        cv.rect(60, y, 3080, 48, fill=fill, outline=LINE, width=2, radius=8)
        cv.text(80, y + 10, title, 24, INK, bold=True)
        return y + 58

    def row_line(y, cols, fills, bold=False, sizes=None):
        # cols: list of (x, w, text)
        h = 46
        x0 = cols[0][0]
        total_w = cols[-1][0] + cols[-1][1] - x0
        cv.rect(x0, y, total_w, h, fill=fills, outline="#D7CBB8", width=1, radius=6)
        for i, (x, w, t) in enumerate(cols):
            sz = (sizes[i] if sizes else 18)
            cv.text(x + 8, y + 12, t, sz, INK, bold=bold)
        return y + h + 4

    y = 150
    y = header(y, "初回（3 碼）　天使自動、不列入路線碼　　已通關：★1-1-1 → 雙見", END_F)
    # column heads
    heads = [(70, 200, "路線碼"), (270, 900, "選項（②→③→④）"), (1170, 160, "F,K"), (1330, 140, "結尾"), (1470, 1600, "備註")]
    y = row_line(y, heads, "#EDE4D4", True)

    for r in rows:
        if r["play_type"] != "初回":
            continue
        picks = r["picks"]
        short = "→".join([
            C2[picks[1]-1].rstrip("。"),
            "貴族派" if picks[2]==1 else "庶民派",
            "雖然難得……" if picks[3]==1 else "回答提問",
        ])
        code = r["route_code"]
        if r["cleared"] == "yes":
            code = "★ " + code
            fill = OK
        else:
            fill = END_K if r["ending"]=="此芽" else (END_S if r["ending"]=="傘" else BOX)
        note = "初回唯一此芽線" if r["ending"]=="此芽" else ("已通關" if r["cleared"]=="yes" else "")
        cols = [(70, 200, code), (270, 900, short), (1170, 160, f"{r['F']},{r['K']}"),
                (1330, 140, r["ending"]), (1470, 1600, note)]
        y = row_line(y, cols, fill, bold=(r["cleared"]=="yes"), sizes=[20, 16, 18, 18, 16])

    y += 24
    y = header(y, "二週目（4 碼）　通關雙見或此芽後重開，第一章出現天使／惡魔　　已通關：★2-2-1-2 → 此芽", NG)
    heads = [(70, 230, "路線碼"), (300, 1080, "選項（①→②→③→④）"), (1380, 160, "F,K"), (1540, 140, "結尾"), (1680, 1400, "備註")]
    y = row_line(y, heads, "#EDE4D4", True)

    for r in rows:
        if r["play_type"] != "二週目":
            continue
        picks = r["picks"]
        short = "→".join([C1[picks[0]-1], C2[picks[1]-1], "貴族派" if picks[2]==1 else "庶民派", "雖然難得" if picks[3]==1 else "回答提問"])
        code = r["route_code"]
        note = ""
        if r["cleared"] == "yes":
            code = "★ " + code
            fill = OK
            note = "已通關"
        elif r["ending"] == "傘":
            fill = END_S
            note = "唯一可進傘線的碼；初回走不到"
        elif r["ending"] == "此芽":
            fill = END_K
            note = "K>F"
        else:
            fill = BOX
            if picks[0] == 1:
                note = "≡ 初回 " + f"{picks[1]}-{picks[2]}-{picks[3]}"
        cols = [(70, 230, code), (300, 1080, short), (1380, 160, f"{r['F']},{r['K']}"),
                (1540, 140, r["ending"]), (1680, 1400, note)]
        y = row_line(y, cols, fill, bold=(r["cleared"]=="yes" or r["ending"]=="傘"), sizes=[20, 16, 18, 18, 16])

    y += 24
    y = header(y, "特殊啟動（本篇四選項走不到）", END_H)
    for r in rows:
        if r["play_type"] != "特殊":
            continue
        cols = [(70, 520, r["route_code"]), (590, 700, r["ending"][:24]), (1290, 1790, r["chapters"])]
        y = row_line(y, cols, END_H, sizes=[18, 18, 16])

    cv.text(70, 2200, "沒有愛愛／音／綠野／靜的獨立結尾。隱藏篇為奧丁神話。未發現獨立 Bad End。", 16, LINE)
    return cv


def draw_midflags():
    cv = Canvas(3200, 2200)
    cv.rect(0, 0, 3200, 120, fill="#3A2F1B", outline="#3A2F1B", radius=0)
    cv.text(70, 24, "共通線自動分枝（無新選項）　·　何時到達那片天空", 40, "#FFF9EF", bold=True)
    cv.text(70, 76, "這些切片不改變路線碼。條件只用 F、K、此芽對話。F／K 來自前面四次（或初回三次）選擇。", 20, "#E8D9B0")

    items = [
        ("朝・條件分岐前（0036）之後",
         "K > F", "朝・此芽的「誓言」Scenario0037", "略過誓言，直接假日・金牛座照陽菜失敗"),
        ("假日・金牛座照陽菜失敗（0038）之後",
         "已回答④第 2 項（此芽對話，$E1(0x0D)==1）", "假日・有通過此芽對話 Scenario0039", "假日・未通過此芽對話 Scenario0040；然後合流 0041"),
        ("假日・明天起是「雙子座」（0042）",
         "F==0 且 K==0　→　〜其他；否則 F≥K　→　〜雙見；其餘　→　〜其他",
         "〜雙見 Scenario0043　或　〜其他 Scenario0044", "之後仍會播「於桃色飛舞之園／雙見的照陽菜」"),
        ("放學後・對照陽菜的認識（0054）",
         "同上（兩者皆 0 或 F<K → 合流；F≥K 且非皆 0 → 〜雙見）",
         "〜雙見 Scenario0055", "〜合流 Scenario0056"),
        ("放學後・關於巽家（0067）",
         "同上", "〜雙見 Scenario0068", "〜合流 Scenario0069"),
        ("放學後・密碼？（0073）之後",
         "K > F", "放學後・櫻守姬的規矩 Scenario0074，然後跳過食之王區塊", "若 F=K=0：走食之王（傘的惡夢／和傘／四次元和傘 0075–0078）；否則直接櫻守姬的府邸 0079–"),
        ("放學後・照雪之戀（0087）",
         "F==0 且 K==0", "〜傘 Scenario0088", "〜其他 Scenario0089；皆合流 0090"),
        ("上學・看家（0094）",
         "F==0 且 K==0", "〜傘 Scenario0095", "直接合流 0096"),
        ("放學後・火災（0097）",
         "K > F", "〜此芽 Scenario0098", "〜其他 Scenario0099；皆合流 0100"),
        ("假日・交錯的心意（0102）",
         "K > F", "〜此芽 Scenario0103", "直接合流 0104"),
        ("假日・「雙子座」期間的最後一天（0105）",
         "兩者皆 0 → 合流；F≥K 且非皆 0 → 〜雙見；其餘 → 合流",
         "〜雙見 Scenario0106", "〜合流 Scenario0107"),
        ("假日・符合（0109）之後＝女主線分歧",
         "K>F → 此芽；否則 0111–0112 之後，F=K=0 → 傘，其餘 → 雙見",
         "見全覽圖", ""),
    ]

    y = 150
    cv.rect(60, y, 3080, 46, fill="#EDE4D4", outline=LINE, width=1, radius=8)
    for x, t in ((80, "時機"), (780, "條件"), (1680, "為真時走"), (2440, "否則")):
        cv.text(x, y + 10, t, 20, INK, bold=True)
    y += 56
    for i, (when, cond, yes, no) in enumerate(items):
        fill = CREAM if i % 2 == 0 else BOX
        cv.rect(60, y, 3080, 140, fill=fill, outline="#D7CBB8", width=1, radius=8)
        cv.wrap_text(80, y + 16, when, 18, INK, 680, bold=True)
        cv.wrap_text(780, y + 16, cond, 17, INK, 860)
        cv.wrap_text(1680, y + 16, yes, 17, GREEN, 740)
        cv.wrap_text(2440, y + 16, no, 17, LINE, 680)
        y += 148

    cv.text(70, 2120, "對回 mainscript 0x18A0–0x2FAC 的 jz／$F1。Scenario 編號為 ScenarioDB／$1B4+1。", 16, LINE)
    return cv


def write_dot_and_mmd():
    dot = r'''digraph itsusora_routes {
  graph [rankdir=TB, fontname="Noto Sans CJK TC", fontsize=14, bgcolor="#F7F1E3", label="何時到達那片天空 路線選項圖（2026-11-14）"];
  node [fontname="Noto Sans CJK TC", shape=box, style="rounded,filled", fillcolor="#FFFDF7", color="#5A4A32"];
  edge [fontname="Noto Sans CJK TC", color="#5A4A32"];

  start [label="開始（序章 Scenario0002）"];
  morning [label="早晨・早安\nScenario0007"];
  auto [label="初回：自動「天使」\n（不列入路線碼，F+1）" fillcolor="#F0EAE0"];
  c1 [label="二週目解鎖 選項①\n（通關雙見或此芽後重開）\n1 天使（F+1）\n2 惡魔（不加）" fillcolor="#F3E2C4"];
  merge1 [label="合流 Scenario0010"];
  c2 [label="選項② 學園・首位男性委員後\n1 出面制止。（F+1）\n2 在一旁觀望。（不加）"];
  c3 [label="選項③ 果然水火不容後\n1 貴族派（K+1）\n2 庶民派（不加）"];
  c4 [label="選項④ 照陽菜準備後\n1 雖然難得……（不加）\n2 回答櫻守姬的提問。（K+1，此芽對話）"];
  common [label="共通線 → 假日・符合\nScenario0109（其間有旗標切片）"];
  formula [label="K > F？" shape=diamond fillcolor="#FFF3CC"];
  konome [label="此芽線 0135–0163\n★已通關 2-2-1-2（F=0,K=2）\n初回僅 2-1-2" fillcolor="#E3EEF8"];
  fire [label="斜陽的心情／炎之子\n0111–0112"];
  zero [label="F=0 且 K=0？" shape=diamond fillcolor="#FFF3CC"];
  kasane [label="傘線 0165–0184\n僅二週目 2-2-2-1" fillcolor="#EEE4F6"];
  futami [label="雙見線 0113–0133\n★已通關 1-1-1（F=2,K=1）" fillcolor="#F8E6D4"];
  hidden [label="隱藏篇《異ならぬ世の終わりより》\n起始模式 2（本篇選項走不到）" fillcolor="#F5E8C8"];
  omake [label="附贈劇本\n起始模式 3" fillcolor="#F5E8C8"];

  start -> morning -> auto;
  morning -> c1 [label="已通關雙見或此芽"];
  auto -> merge1;
  c1 -> merge1;
  merge1 -> c2 -> c3 -> c4 -> common -> formula;
  formula -> konome [label="是"];
  formula -> fire [label="否"];
  fire -> zero;
  zero -> kasane [label="是"];
  zero -> futami [label="否"];
}
'''
    (OUT / "route_map_overview.dot").write_text(dot, encoding="utf-8")
    mmd = """flowchart TB
  start[開始 序章 Scenario0002] --> morning[早晨・早安 Scenario0007]
  morning -->|初回 自動天使 不列入路線碼 F+1| merge1[合流 0010]
  morning -->|二週目：已通關雙見或此芽| c1{選項①}
  c1 -->|1 天使 F+1| merge1
  c1 -->|2 惡魔 不加| merge1
  merge1 --> c2{選項② 首位男性委員後}
  c2 -->|1 出面制止。 F+1| c3
  c2 -->|2 在一旁觀望。 不加| c3
  c3{選項③ 果然水火不容後}
  c3 -->|1 貴族派 K+1| c4
  c3 -->|2 庶民派 不加| c4
  c4{選項④ 照陽菜準備後}
  c4 -->|1 雖然難得…… 不加| common
  c4 -->|2 回答提問 K+1 此芽對話| common
  common[共通線 → 假日・符合 0109] --> formula{K 大於 F？}
  formula -->|是| konome[此芽線 0135–0163<br/>已通關 2-2-1-2]
  formula -->|否| fire[斜陽的心情／炎之子 0111–0112]
  fire --> zero{F=0 且 K=0？}
  zero -->|是| kasane[傘線 0165–0184<br/>僅 2-2-2-1]
  zero -->|否| futami[雙見線 0113–0133<br/>已通關 1-1-1]
"""
    (OUT / "route_map_overview.mmd").write_text(mmd, encoding="utf-8")


def tofu_check(im: Image.Image, chars: set[str]) -> list[str]:
    """Rasterize each char; flag empty or tiny ink (possible .notdef/tofu)."""
    bad = []
    font = load_font(48, False)
    for ch in sorted(chars):
        if ch.isspace() or ord(ch) < 32:
            continue
        # skip punctuation that may be thin
        g = Image.new("L", (80, 80), 0)
        d = ImageDraw.Draw(g)
        d.text((8, 8), ch, font=font, fill=255)
        ink = sum(1 for p in g.getdata() if p > 20)
        if ink < 8:
            bad.append(f"{ch} U+{ord(ch):04X} ink={ink}")
    return bad


def write_manifest(files):
    lines = []
    for p in files:
        data = p.read_bytes()
        md5 = hashlib.md5(data).hexdigest()
        lines.append(f"{md5}  {p.stat().st_size:10d}  {p.name}")
    (OUT / "MANIFEST").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = all_routes()
    write_tsv(rows)
    write_readme(rows)
    write_note()
    write_dot_and_mmd()

    # gather all text for cmap check
    all_text = []
    for r in rows:
        all_text.extend([r["route_code"], r["ending"], r["choice_seq"], r["chapters"], r["notes"]])
    sample = "何時到達那片天空路線選項圖雙見此芽傘愛愛音綠野靜天使惡魔出面制止在一旁觀望雖然難得回答櫻守姬貴族庶民已通關二週目初回隱藏"
    missing = font_has_chars(sample + "".join(C1+C2+C3+C4))
    if missing:
        raise SystemExit(f"font missing glyphs: {missing}")

    ov = draw_overview(rows)
    ov.save_png(OUT / "route_map_overview.png")
    ov.save_svg(OUT / "route_map_overview.svg")
    bad = tofu_check(ov.im, ov._chars)
    if bad:
        raise SystemExit(f"overview tofu/empty glyphs: {bad}")

    ac = draw_all_codes(rows)
    ac.save_png(OUT / "route_map_all_codes.png")
    ac.save_svg(OUT / "route_map_all_codes.svg")
    bad = tofu_check(ac.im, ac._chars)
    if bad:
        raise SystemExit(f"all_codes tofu/empty glyphs: {bad}")

    mf = draw_midflags()
    mf.save_png(OUT / "route_map_midflags.png")
    mf.save_svg(OUT / "route_map_midflags.svg")
    bad = tofu_check(mf.im, mf._chars)
    if bad:
        raise SystemExit(f"midflags tofu/empty glyphs: {bad}")

    files = sorted([p for p in OUT.iterdir() if p.is_file() and p.name != "_generate.py"])
    write_manifest(files)
    print("OK", OUT)
    for p in sorted(OUT.iterdir()):
        print(p.name, p.stat().st_size)

if __name__ == "__main__":
    main()
