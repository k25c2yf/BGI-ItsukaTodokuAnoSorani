#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply voice-variant speaker-dword alignment to compiled BGI chapter bins.

Only rewrites the speaker pair (n0, n1) at listed file offsets: unnamed
(0, 0) becomes (3, pointer-to-Chinese-name-in-THIS-bin's-string-pool).
Does not copy pointer values from another compile. Does not change
dialogue, V, ruby, or line count, and does not use Ｚ.

Usage:
  python3 apply_voice_align.py --input <compiled_dir> --sites sites.tsv --output <out_dir>
  python3 apply_voice_align.py --input <compiled_dir> --sites sites.tsv --dry-run
  python3 apply_voice_align.py --input <compiled_dir> --sites sites.tsv --in-place
"""
from __future__ import annotations

import argparse
import shutil
import struct
import sys
from collections import defaultdict
from pathlib import Path


def read_u32(buf: bytes, off: int) -> int:
    return struct.unpack_from("<I", buf, off)[0]


def decode_cstr(buf: bytes, ptr: int):
    if ptr <= 0 or ptr >= len(buf):
        return None
    end = buf.find(b"\x00", ptr)
    if end < 0:
        return None
    raw = buf[ptr:end]
    for enc in ("utf-8", "cp932"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return None


def whole_string_offsets(data: bytes, name: str) -> list[int]:
    """Offsets of NUL-terminated UTF-8 `name` that are not mid-string."""
    needle = name.encode("utf-8") + b"\x00"
    hits = []
    start = 0
    while True:
        i = data.find(needle, start)
        if i < 0:
            break
        if i == 0 or data[i - 1] == 0:
            hits.append(i)
        start = i + 1
    return hits


def parse_msgs(data: bytes):
    """Minimal parse of call 0x3F / argc=5 message trailers (headerless BGI)."""
    pat = b"\x3f\x00\x00\x00\x05\x00\x00\x00"
    calls = []
    i = 0
    while True:
        j = data.find(pat, i)
        if j < 0:
            break
        calls.append(j)
        i = j + 1
    msgs = []
    for call_at in calls:
        trailer_start = call_at - 8 * 4
        if trailer_start < 0 or trailer_start + 8 > len(data):
            continue
        n0 = read_u32(data, trailer_start)
        n1 = read_u32(data, trailer_start + 4)
        if n0 == 0 and n1 == 0:
            name = 0
        elif n0 == 3:
            name = decode_cstr(data, n1) or f"ptr:{n1}"
        else:
            name = f"op{n0}:{n1}"
        msgs.append({"idx": len(msgs), "name_at": trailer_start, "n0": n0, "n1": n1, "name": name})
    return msgs


def used_speaker_ptrs(data: bytes, name: str) -> list[int]:
    """Distinct name-pool pointers already used by (type=3) slots for `name`."""
    seen = []
    for m in parse_msgs(data):
        if m["n0"] == 3 and m["name"] == name and m["n1"] not in seen:
            seen.append(m["n1"])
    return seen


def resolve_name_ptr(data: bytes, name: str) -> tuple[int, str]:
    """Pick the pool address of `name` in this bin. Never reuse a foreign pointer.

    Prefer the pointer already used by existing (type=3) speaker slots for this
    name. Importer string-dedup can point a short name into the suffix of a
    longer pool string (e.g. 傘 inside 和傘\0); that is still the address the
    engine uses, so we reuse it. Raw-byte fallback only accepts a whole
    NUL-terminated string (preceded by NUL or start of file) so we do not
    invent a mid-string cut.
    """
    used = []
    for p in used_speaker_ptrs(data, name):
        if not (0 < p < len(data)):
            continue
        if decode_cstr(data, p) != name:
            continue
        end = p + len(name.encode("utf-8"))
        if end >= len(data) or data[end] != 0:
            continue
        if p not in used:
            used.append(p)
    if used:
        return used[0], "existing-speaker-slot"
    hits = whole_string_offsets(data, name)
    if len(hits) == 1:
        return hits[0], "unique-pool-string"
    if len(hits) > 1:
        # Importer appends a new UTF-8 pool at EOF; the last whole-string match
        # is the one that belongs to this compile.
        return hits[-1], "last-of-multiple-pool-strings"
    raise ValueError(
        f"Chinese name {name!r} not found as an existing speaker pointer or "
        f"a NUL-terminated whole string in the bin"
    )


def slot_state(data: bytes, off: int, name: str) -> str:
    if off < 0 or off + 8 > len(data):
        return "oob"
    n0 = read_u32(data, off)
    n1 = read_u32(data, off + 4)
    if n0 == 0 and n1 == 0:
        return "unnamed"
    if n0 == 3 and decode_cstr(data, n1) == name:
        return "already"
    return f"unexpected({n0},{n1})"


def load_sites(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines:
        raise SystemExit(f"empty sites file: {path}")
    header = lines[0].lstrip("#").strip().split("\t")
    required = {"chapter", "offset", "name"}
    if not required.issubset(set(header)):
        raise SystemExit(f"{path}: header must include chapter, offset, name (got {header})")
    col = {h: i for i, h in enumerate(header)}
    sites = []
    for lineno, line in enumerate(lines[1:], start=2):
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        try:
            chapter = parts[col["chapter"]].strip()
            offset = int(parts[col["offset"]].strip(), 0)
            name = parts[col["name"]].strip()
        except (IndexError, ValueError) as e:
            raise SystemExit(f"{path}:{lineno}: bad row: {e}") from e
        if not chapter or not name:
            raise SystemExit(f"{path}:{lineno}: empty chapter or name")
        rec = {"chapter": chapter, "offset": offset, "name": name, "line": lineno}
        for opt in ("idx", "prefix", "source", "V", "jp_seq"):
            if opt in col and col[opt] < len(parts):
                rec[opt] = parts[col[opt]]
        sites.append(rec)
    return sites


def find_bin(input_dir: Path, chapter: str) -> Path | None:
    candidates = [
        input_dir / chapter,
        input_dir / "tc" / chapter,
        input_dir / f"{chapter}.bin",
        input_dir / "tc" / f"{chapter}.bin",
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def apply_chapter(data: bytes, sites: list[dict], dry: bool):
    """Return (new_bytes_or_None, n_applied, n_skipped, errors)."""
    errors = []
    n_applied = 0
    n_skipped = 0
    planned = []  # (offset, ptr, name)
    name_ptr_cache: dict[str, int] = {}

    for s in sites:
        off = s["offset"]
        name = s["name"]
        label = f"{s['chapter']} offset={off} name={name!r}"
        if "idx" in s and s["idx"] != "":
            label += f" idx={s['idx']}"
        st = slot_state(data, off, name)
        if st == "oob":
            errors.append(f"{label}: offset is past end of file (size={len(data)})")
            continue
        if st == "already":
            n_skipped += 1
            continue
        if st != "unnamed":
            errors.append(f"{label}: slot is {st}, expected (0,0) or already {name!r}")
            continue
        if name not in name_ptr_cache:
            try:
                ptr, _how = resolve_name_ptr(data, name)
            except ValueError as e:
                errors.append(f"{label}: {e}")
                continue
            name_ptr_cache[name] = ptr
        ptr = name_ptr_cache[name]
        if ptr + len(name.encode("utf-8")) + 1 > len(data):
            errors.append(f"{label}: resolved pointer {ptr} would run past end of file")
            continue
        planned.append((off, ptr, name, label))

    if errors:
        return None, 0, n_skipped, errors

    buf = bytearray(data)
    if not dry:
        for off, ptr, name, label in planned:
            if read_u32(bytes(buf), off) != 0 or read_u32(bytes(buf), off + 4) != 0:
                errors.append(f"{label}: slot changed under us, aborting chapter")
                return None, 0, n_skipped, errors
            struct.pack_into("<I", buf, off, 3)
            struct.pack_into("<I", buf, off + 4, ptr)
            n_applied += 1
    else:
        n_applied = len(planned)
    return (bytes(buf) if not dry else data), n_applied, n_skipped, errors


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, type=Path, help="directory of compiled chapter bins")
    ap.add_argument("--sites", type=Path, default=None, help="sites.tsv (default: next to this script)")
    ap.add_argument("--output", type=Path, default=None, help="directory to write patched bins")
    ap.add_argument("--dry-run", action="store_true", help="report only, do not write files")
    ap.add_argument("--in-place", action="store_true", help="patch input files in place (writes <file>.bak first)")
    args = ap.parse_args(argv)

    if not args.dry_run and not args.in_place and args.output is None:
        ap.error("provide --output, or --in-place, or --dry-run")
    if args.in_place and args.output is not None:
        ap.error("use either --in-place or --output, not both")

    sites_path = args.sites
    if sites_path is None:
        sites_path = Path(__file__).resolve().parent / "sites.tsv"
    if not sites_path.is_file():
        raise SystemExit(f"sites file not found: {sites_path}")
    if not args.input.is_dir():
        raise SystemExit(f"input directory not found: {args.input}")

    sites = load_sites(sites_path)
    by_ch = defaultdict(list)
    for s in sites:
        by_ch[s["chapter"]].append(s)

    if args.output and not args.dry_run:
        args.output.mkdir(parents=True, exist_ok=True)

    total_applied = total_skipped = total_failed = 0
    chapters_ok = chapters_fail = 0

    for chapter in sorted(by_ch):
        src = find_bin(args.input, chapter)
        if src is None:
            print(f"FAIL {chapter}: not found under {args.input}", file=sys.stderr)
            total_failed += len(by_ch[chapter])
            chapters_fail += 1
            continue
        data = src.read_bytes()
        new_data, n_app, n_skip, errors = apply_chapter(data, by_ch[chapter], dry=args.dry_run)
        if errors:
            print(f"FAIL {chapter}: {len(errors)} site error(s)", file=sys.stderr)
            for e in errors:
                print(f"  {e}", file=sys.stderr)
            total_failed += len(errors)
            total_skipped += n_skip
            chapters_fail += 1
            continue
        total_applied += n_app
        total_skipped += n_skip
        chapters_ok += 1
        action = "DRY" if args.dry_run else "OK"
        print(f"{action} {chapter}: applied={n_app} skipped={n_skip} from {src}")
        if args.dry_run:
            continue
        if args.in_place:
            bak = src.with_name(src.name + ".bak")
            if not bak.exists():
                shutil.copy2(src, bak)
            if new_data != data:
                src.write_bytes(new_data)
        else:
            dst = args.output / src.name
            # If the source used a .bin suffix, keep the game-style name when possible
            if src.name.endswith(".bin") and not chapter.endswith(".bin"):
                dst = args.output / chapter
            dst.write_bytes(new_data)

    print(
        f"done applied={total_applied} skipped={total_skipped} failed={total_failed} "
        f"chapters_ok={chapters_ok} chapters_fail={chapters_fail}"
    )
    return 1 if total_failed or chapters_fail else 0


if __name__ == "__main__":
    sys.exit(main())
