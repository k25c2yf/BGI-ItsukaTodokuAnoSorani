# apply_voice_align：繁／簡人名變體（2026-11-25）

原腳本只在 bin 裡找 `sites.tsv` 的繁中人名（UTF-8 整串＋NUL）。簡體編譯（`gbk/` 或 `tl/sc`，講者為「双见／静／爱爱／绿野」）會令 119 處失敗，連帶整章另外 155 處也不會寫入。本目錄為修補副本，**未覆寫**正式包裡的原檔。

- 修補檔：`apply_voice_align.py`
- 對照用原檔：`apply_voice_align.orig.py`（與 2026-11-23 包相同）
- 用法不變：`python apply_voice_align.py --input ./temp/ --sites sites.tsv --output ./outputgbk`
- 不必改 `sites.tsv`。指標會指向 bin 裡實際存在的簡體（或繁中）字串。
- 不會把日文暱稱（メメ／ふたみ／みどの）對到中文名。若 temp 仍是日文講者，應先用中文劇本重編，不要用 jpname 回寫。

本機用 2026-11-23 `prebuilt_outputbig5` 還原站位並把四個人名換成簡體後：原腳本重現 `applied=73 skipped=0 failed=119 chapters_ok=9 chapters_fail=14`；修補後繁簡皆 `applied=347 failed=0`。
