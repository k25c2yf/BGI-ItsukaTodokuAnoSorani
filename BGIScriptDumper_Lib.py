# -*- coding: utf-8 -*-
# BGIScriptDumper_Lib (improved): works for both scenario chapters and
# library-type BGI scripts (Custom, Product, Framework, macro_*),
# and old headerless BGI scripts (no BurikoCompiledScript magic).
# Output format is identical to BGIScriptDumper-jp.py: ●address●text, UTF-16.
#
# Glyph codes 0xFF nn (Lump of Sugar special glyphs, e.g. heart): no sister
# project defined a dump convention, so we use reversible ASCII escapes
# "\xFFNN" (NN = uppercase hex). The UTF-8 engine keeps raw FF nn bytes in
# the string pool (0xFF never appears in UTF-8), so the importer writes them
# back as-is. See BGIScriptImporter.py.
import sys, struct, unicodedata, re

# Matches dump-side escapes produced below; also used as documentation.
FF_ESC_RE = re.compile(r'\\xFF([0-9A-Fa-f]{2})')

def _strip_ff_glyph_pairs(part):
    """Remove 0xFF nn glyph pairs so the rest can be checked as SJIS/cp932."""
    out = bytearray()
    i = 0
    while i < len(part):
        if part[i] == 0xFF and i + 1 < len(part):
            i += 2
            continue
        out.append(part[i]); i += 1
    return bytes(out)

def is_text_part(part):
    # 0xFF nn are engine glyph codes (not SJIS); ignore them for the check.
    cleaned = _strip_ff_glyph_pairs(part)
    if not cleaned:
        return True  # pure glyph-code string is still a pool string
    try:
        t = cleaned.decode('cp932')
    except UnicodeDecodeError:
        return False
    return not any(ord(c) < 0x20 and c not in '\r\n\t' for c in t)

def has_japanese(t):
    # same rule as BGIScriptDumper-jp.py: first char must not be narrow ASCII.
    # (this also skips function/label names such as __神気桜, _驚き)
    if t.startswith('<R') or t.startswith('<r'):
        return True   # line beginning with ruby, e.g. <Rやこたみちょう>矢古民町</R>
    # Date headers like #《５月１６日》: leading '#' is Na, but body is CJK.
    if t.startswith('#') and any(unicodedata.east_asian_width(c) != 'Na' for c in t[1:]):
        return True
    # Skip leading \xFFNN escapes when judging the first "real" character.
    s = t
    while True:
        m = re.match(r'\\xFF[0-9A-Fa-f]{2}', s)
        if not m:
            break
        s = s[m.end():]
    if not s:
        return True  # glyph-only line (e.g. face icons)
    return unicodedata.east_asian_width(s[0]) != 'Na'

def decode_script_string(raw):
    """Decode a pool string that may contain 0xFF nn glyph codes.

    Glyph pairs become reversible '\\xFFNN' tokens; the rest is Shift-JIS
    (cp932 fallback), identical to the old path when no FF is present.
    Returns None if the non-glyph bytes are not valid SJIS/cp932.
    """
    out = []
    i = 0
    chunk = bytearray()

    def flush():
        nonlocal chunk
        if not chunk:
            return True
        try:
            out.append(bytes(chunk).decode('shift_jis'))
        except UnicodeDecodeError:
            try:
                out.append(bytes(chunk).decode('cp932'))
            except UnicodeDecodeError:
                return False
        chunk = bytearray()
        return True

    while i < len(raw):
        if raw[i] == 0xFF and i + 1 < len(raw):
            if not flush():
                return None
            out.append('\\xFF%02X' % raw[i + 1])
            i += 2
            continue
        # Keep SJIS double-byte pairs intact inside the chunk.
        if (0x81 <= raw[i] <= 0x9F or 0xE0 <= raw[i] <= 0xFC) and i + 1 < len(raw):
            chunk.append(raw[i]); chunk.append(raw[i + 1]); i += 2
        else:
            chunk.append(raw[i]); i += 1
    if not flush():
        return None
    return ''.join(out)

def dump(SC, include_ascii=False):
    data = open(SC, 'rb').read()
    if data.startswith(b'BurikoCompiledScript'):
        # newer BGI: code start = 0x1C + header size
        offset = 0x1C + struct.unpack_from('<I', data, 0x1C)[0]
    else:
        # old headerless BGI (e.g. いつか、届く、あの空に。2007):
        # code starts at 0 and string operands are relative to file start
        offset = 0

    # 1) find where the trailing string pool begins: walk back from EOF over
    #    NUL-terminated printable strings until we hit code bytes.
    parts = data[offset:].split(b'\x00')
    pos = len(data)
    for part in reversed(parts):
        start = pos - len(part)
        if part and not is_text_part(part):
            break
        pos = start - 1          # skip the NUL before this part
    tail = pos + 1

    # 2) pool start = smallest push-string (03) operand pointing into the tail
    ops = []
    for p in range(offset, len(data) - 8, 4):
        if data[p:p+4] == b'\x03\x00\x00\x00':
            v = struct.unpack_from('<I', data, p + 4)[0]
            ops.append((p + 4, v))
    valid = [v for _, v in ops if tail <= offset + v < len(data)
             and data[offset + v - 1] == 0]
    if not valid:
        print(SC + "\tno strings."); open(SC + ".txt", 'w', encoding='utf-16').close(); return True
    pool = offset + min(valid)

    n = 0
    with open(SC + ".txt", 'w', 1, "UTF_16") as out:
        for address, v in ops:
            a = offset + v
            if address >= pool or not (pool <= a < len(data)) or data[a-1] != 0:
                continue
            raw = data[a:data.find(b'\x00', a)]
            t = decode_script_string(raw)
            if t is None:
                continue
            if not t or '\n' in t or '\r' in t:
                continue   # empty, or multi-line debug message (would break ●ID● lines)
            # Drop leftover C0 controls (e.g. mainscript junk 'ｵ\x01'); glyph
            # codes were already turned into \\xFFNN so they are not controls.
            if any(ord(c) < 0x20 and c not in '\t' for c in t):
                continue
            if include_ascii or has_japanese(t):
                out.write('●' + '%.6d' % address + '●' + t + '\n'); n += 1
    print(SC + "\t%d lines. Finished!" % n)
    return True

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if a != '--all']
    if not args:
        print("usage: " + sys.argv[0] + " [--all] <script> [script ...]"); sys.exit(1)
    for f in args:
        dump(f, '--all' in sys.argv)
