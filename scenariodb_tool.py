#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ScenarioDB dump / apply / align for BGI《何時到達那片天空》.

Binary layout (verified on att/x_v200/ScenarioDB, 12420 bytes):
  uint32 LE count
  count × 64-byte records: NUL-terminated name at start, zero-padded.
  Optional metadata in last 16 bytes as 4×uint32 LE. When present, name
  must fit in the first 48 bytes (max 47 + NUL); otherwise max 63 + NUL.

Original names are CP932. UTF8_FIX expects UTF-8 names in slots;
BIG5_FIX expects CP950 (same policy as BGIScriptImporter_big5.py).
"""

from __future__ import annotations

import argparse
import struct
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REC_SIZE = 64
META_OFF = 48
META_SIZE = 16


def _read_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16")
    return raw.decode("utf-8-sig")


def _wave_variants(s: str) -> List[str]:
    """Return s plus ～ (U+FF5E) ↔ 〜 (U+301C) swaps."""
    out = [s]
    a = s.replace("\uff5e", "\u301c")
    b = s.replace("\u301c", "\uff5e")
    for v in (a, b):
        if v not in out:
            out.append(v)
    return out


def _detect_has_meta(name_cp932: bytes, rec: bytes) -> bool:
    meta = struct.unpack_from("<4I", rec, META_OFF)
    return len(name_cp932) <= META_OFF and any(meta)


def _max_name_bytes(has_meta: bool) -> int:
    return META_OFF - 1 if has_meta else REC_SIZE - 1


def load_db(path: Path) -> Tuple[int, List[dict]]:
    data = path.read_bytes()
    if len(data) < 4:
        raise SystemExit(f"{path}: too small")
    count = struct.unpack_from("<I", data, 0)[0]
    expect = 4 + count * REC_SIZE
    if len(data) != expect:
        raise SystemExit(
            f"{path}: size {len(data)} != expected {expect} (count={count})"
        )
    records = []
    for i in range(count):
        off = 4 + i * REC_SIZE
        rec = bytearray(data[off : off + REC_SIZE])
        name_b = bytes(rec).split(b"\x00", 1)[0]
        # UTF-8 first (patched DB / ASCII). Original JP CP932 is rarely
        # valid UTF-8, so it falls through. Preferring CP932 first would
        # mojibake many UTF-8 CJK names (false-success decode).
        try:
            name = name_b.decode("utf-8")
        except UnicodeDecodeError:
            name = name_b.decode("cp932")
        has_meta = _detect_has_meta(name_b, bytes(rec))
        meta = struct.unpack_from("<4I", rec, META_OFF) if has_meta else None
        records.append(
            {
                "index": i,
                "name": name,
                "name_bytes": name_b,
                "has_meta": has_meta,
                "meta": meta,
                "raw": rec,
            }
        )
    return count, records


def write_db(path: Path, records: List[dict], encoding: str = "utf-8") -> None:
    count = len(records)
    out = bytearray(struct.pack("<I", count))
    for r in records:
        name_utf8 = r["name"].encode(encoding)
        max_b = _max_name_bytes(r["has_meta"])
        if len(name_utf8) > max_b:
            raise SystemExit(
                f"overflow index {r['index']:03d}: "
                f"{len(name_utf8)} > {max_b} for {r['name']!r} enc={encoding}"
            )
        slot = bytearray(REC_SIZE)
        slot[: len(name_utf8)] = name_utf8
        # NUL already present via zero init
        if r["has_meta"]:
            # preserve original meta bytes from raw
            slot[META_OFF:REC_SIZE] = r["raw"][META_OFF:REC_SIZE]
        out.extend(slot)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(bytes(out))


def cmd_dump(db_path: Path, out_txt: Path) -> None:
    count, records = load_db(db_path)
    lines = []
    for r in records:
        line = f"●{r['index']:03d}●{r['name']}"
        if r["has_meta"] and r["meta"] is not None:
            a, b, c, d = r["meta"]
            line += f" # meta={a},{b},{c},{d}"
        lines.append(line)
    out_txt.parent.mkdir(parents=True, exist_ok=True)
    out_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"dump: {count} records -> {out_txt}")


def _parse_tl_txt(path: Path) -> Dict[int, str]:
    """Parse ●INDEX●NAME lines; INDEX is decimal (zero-padded ok)."""
    text = _read_text(path)
    mapping: Dict[int, str] = {}
    for lineno, line in enumerate(text.splitlines(), 1):
        s = line.strip().lstrip("\ufeff")
        if not s or s.startswith("#"):
            continue
        # strip trailing comment
        if " #" in s:
            s = s.split(" #", 1)[0].rstrip()
        if not s.startswith("●"):
            raise SystemExit(f"{path}:{lineno}: expected ●INDEX●NAME, got {line!r}")
        parts = s.split("●")
        # '', index, name...
        if len(parts) < 3 or parts[1] == "":
            raise SystemExit(f"{path}:{lineno}: bad line {line!r}")
        try:
            idx = int(parts[1])
        except ValueError as e:
            raise SystemExit(f"{path}:{lineno}: bad index {parts[1]!r}") from e
        name = "●".join(parts[2:])
        mapping[idx] = name
    return mapping


def cmd_apply(db_path: Path, tl_txt: Path, out_db: Path, encoding: str = "utf-8") -> None:
    count, records = load_db(db_path)
    mapping = _parse_tl_txt(tl_txt)
    overflows = []
    applied = 0
    for r in records:
        if r["index"] not in mapping:
            continue
        new_name = mapping[r["index"]]
        max_b = _max_name_bytes(r["has_meta"])
        nb = len(new_name.encode(encoding))
        if nb > max_b:
            overflows.append((r["index"], r["name"], new_name, nb, max_b, r["has_meta"]))
            continue
        if new_name != r["name"]:
            applied += 1
        r["name"] = new_name
    if overflows:
        print("OVERFLOW (left unchanged):")
        for idx, old, new, nb, max_b, hm in overflows:
            print(
                f"  ●{idx:03d}● {old!r} -> {new!r} "
                f"{encoding}={nb}>{max_b} has_meta={hm}"
            )
    write_db(out_db, records, encoding=encoding)
    print(
        f"apply: wrote {out_db} enc={encoding} "
        f"(changed={applied}, overflow={len(overflows)}, total={count})"
    )


def _parse_mainscript_ids(path: Path) -> Dict[str, str]:
    """Return {id_str: content} from ●ID●content lines."""
    text = _read_text(path)
    out: Dict[str, str] = {}
    for line in text.splitlines():
        s = line.strip().lstrip("\ufeff")
        if not s.startswith("●"):
            continue
        parts = s.split("●")
        if len(parts) < 3 or parts[1] == "":
            continue
        out[parts[1]] = "●".join(parts[2:])
    return out


def _build_jp_to_cn(jp_map: Dict[str, str], cn_map: Dict[str, str]) -> Dict[str, str]:
    """Match by shared ●ID●; expand keys with wave-dash variants."""
    base: Dict[str, str] = {}
    conflicts = []
    for iid, jp in jp_map.items():
        if iid not in cn_map:
            continue
        cn = cn_map[iid]
        if jp in base and base[jp] != cn:
            conflicts.append((iid, jp, base[jp], cn))
        else:
            base[jp] = cn
    if conflicts:
        print(f"warning: {len(conflicts)} JP→CN conflicts (keeping first):")
        for iid, jp, a, b in conflicts[:20]:
            print(f"  id={iid} {jp!r}: {a!r} vs {b!r}")
    expanded: Dict[str, str] = {}
    for jp, cn in base.items():
        for v in _wave_variants(jp):
            expanded.setdefault(v, cn)
    return expanded


def cmd_align(
    db_path: Path,
    jp_mainscript: Path,
    cn_mainscript: Path,
    out_db: Path,
    out_map: Optional[Path] = None,
    encoding: str = "utf-8",
) -> None:
    count, records = load_db(db_path)
    jp_ids = _parse_mainscript_ids(jp_mainscript)
    cn_ids = _parse_mainscript_ids(cn_mainscript)
    jp2cn = _build_jp_to_cn(jp_ids, cn_ids)

    translated = unchanged = missing = overflow = 0
    map_rows: List[Tuple[str, str, str]] = []
    overflows: List[str] = []

    for r in records:
        jp_name = r["name"]
        cn_name = None
        for cand in _wave_variants(jp_name):
            if cand in jp2cn:
                cn_name = jp2cn[cand]
                break
        if cn_name is None:
            missing += 1
            map_rows.append((jp_name, jp_name, "missing"))
            continue
        if cn_name == jp_name:
            unchanged += 1
            map_rows.append((jp_name, cn_name, "unchanged"))
            continue
        max_b = _max_name_bytes(r["has_meta"])
        nb = len(cn_name.encode(encoding))
        if nb > max_b:
            overflow += 1
            overflows.append(
                f"●{r['index']:03d}● {jp_name!r} -> {cn_name!r} "
                f"{encoding}={nb}>{max_b} has_meta={r['has_meta']}"
            )
            map_rows.append((jp_name, jp_name, "overflow"))
            continue
        r["name"] = cn_name
        translated += 1
        map_rows.append((jp_name, cn_name, "translated"))

    write_db(out_db, records, encoding=encoding)
    if out_map is not None:
        out_map.parent.mkdir(parents=True, exist_ok=True)
        lines = ["jp\tcn\tstatus"]
        for jp, cn, st in map_rows:
            lines.append(f"{jp}\t{cn}\t{st}")
        out_map.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"align: total={count} translated={translated} unchanged={unchanged} "
        f"missing={missing} overflow={overflow}"
    )
    print(f"  wrote {out_db}")
    if out_map is not None:
        print(f"  map   {out_map}")
    if overflows:
        print("OVERFLOW (left JP):")
        for line in overflows:
            print(" ", line)


def main(argv: Optional[List[str]] = None) -> None:
    p = argparse.ArgumentParser(description="ScenarioDB dump/apply/align tool")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("dump", help="Export ScenarioDB names to UTF-8 text")
    d.add_argument("scenariodb")
    d.add_argument("out_txt")

    a = sub.add_parser("apply", help="Apply ●INDEX●NAME text back to ScenarioDB")
    a.add_argument("scenariodb")
    a.add_argument("tl_txt")
    a.add_argument("out_scenariodb")
    a.add_argument("--enc", default="utf-8", help="name encoding: utf-8 or cp950")

    g = sub.add_parser(
        "align",
        help="Align ScenarioDB names using JP/CN mainscript ●ID● pairs",
    )
    g.add_argument("scenariodb")
    g.add_argument("jp_mainscript")
    g.add_argument("cn_mainscript")
    g.add_argument("out_scenariodb")
    g.add_argument("--out-map", default=None, help="Write jp\\tcn\\tstatus TSV")
    g.add_argument("--enc", default="utf-8", help="name encoding: utf-8 or cp950")

    args = p.parse_args(argv)
    if args.cmd == "dump":
        cmd_dump(Path(args.scenariodb), Path(args.out_txt))
    elif args.cmd == "apply":
        cmd_apply(Path(args.scenariodb), Path(args.tl_txt), Path(args.out_scenariodb), encoding=args.enc)
    elif args.cmd == "align":
        cmd_align(
            Path(args.scenariodb),
            Path(args.jp_mainscript),
            Path(args.cn_mainscript),
            Path(args.out_scenariodb),
            Path(args.out_map) if args.out_map else None,
            encoding=args.enc,
        )
    else:
        p.error("unknown command")


if __name__ == "__main__":
    main()
