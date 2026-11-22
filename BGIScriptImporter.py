# -*- coding: utf-8 -*-
# For Windows OS Only....
# 支援用"\r"符號取代為換行符，解決換行截斷問題
# 支援無 BurikoCompiledScript 檔頭的舊版 BGI 腳本（offset = 0）
# 支援 dump 端的 "\xFFNN" 圖示碼跳脫（還原為引擎字串池內的原始 FF nn 位元組；
# UTF-8 位元流不會出現 0xFF，故引擎可照舊辨識特殊字形）


import sys
import os
import struct
import codecs
import unicodedata
import re

FF_ESC_RE = re.compile(r'\\xFF([0-9A-Fa-f]{2})')

def transcode(uni):
    """Encode to UTF-8 with \\xFFNN glyph escapes restored to raw FF nn bytes."""
    parts = []
    pos = 0
    for m in FF_ESC_RE.finditer(uni):
        before = uni[pos:m.start()]
        if before:
            parts.append(_utf8_safe(before))
        parts.append(bytes([0xFF, int(m.group(1), 16)]))
        pos = m.end()
    if pos < len(uni):
        parts.append(_utf8_safe(uni[pos:]))
    return b"".join(parts)

def _utf8_safe(uni):
    tran = u""
    for ch in uni:
        try:
            ch.encode("utf-8")
        except:
            tran += u"·"
        else:
            tran += ch
    return tran.encode("utf-8")

def open_txt_lines(path):
    """Accept UTF-16 (BOM) or UTF-8 (BOM); return lines without newlines."""
    raw = open(path, "rb").read()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16").splitlines()
    return raw.decode("utf-8-sig").splitlines()


if len(sys.argv) < 4:
    print("error\n")
    print(sys.argv[0] + " <script> <txt> <out>")
    quit()

SC = sys.argv[1]
TX = sys.argv[2]
CN = sys.argv[3]

try:
    SCFile = open(SC, 'rb')
except FileNotFoundError:
    print(SC + " Error!\tCan't find file!")
    exit()
except:
    print("Error!")
    exit()
try:
    lines = open_txt_lines(TX)
except FileNotFoundError:
    print(TX + " Error!\tCan't find file!")
    exit()
except Exception as e:
    print(TX + " Error!\t" + str(e))
    exit()


SCFile.seek(0)
test = SCFile.read(20)
if test == b'BurikoCompiledScript':
    SCFile.seek(0x1C)
    offset = 0x1C + struct.unpack('<L', SCFile.read(4))[0]  # Lib: code start = 0x1C + header size (was: scan for 01 00 00 00)
else:
    # old headerless BGI (e.g. いつか、届く、あの空に。2007):
    # code starts at 0 and string operands are relative to file start
    offset = 0

SCFile.seek(0)
CNFile = open(CN, 'wb')
CNFile.write(SCFile.read())
SCFile.close()
newOffset = CNFile.tell()

textToFile = b""
for TXTemp in lines:
    if TXTemp == "":
        continue
    if TXTemp[0] == u'●':
        # ●AAAAAA●text  — address is 6 decimal digits
        text = TXTemp[8:].replace("\\r", b'\x0A'.decode())
        textGBK = transcode(text) + b'\x00'
        address = int(TXTemp[1:7])
        if textToFile.find(textGBK) >= 0:
            locate = textToFile.find(textGBK) + newOffset - offset
        else:
            locate = len(textToFile) + newOffset - offset
            textToFile = textToFile + textGBK
        CNFile.seek(address)
        CNFile.write(struct.pack('<L', locate))

CNTemp = textToFile
CNFile.seek(newOffset)
CNFile.write(CNTemp)

CNFile.close()
print("Finished!")
