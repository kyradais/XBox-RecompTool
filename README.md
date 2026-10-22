# XBox-RecompTool

Standalone project for static recompilation of Xbox `.xbe` binaries to C++ source code.

## Goal
- Convert original Xbox game image (`default.xbe` or similar) into portable C++.
- Produce build artifacts ready for Android, Windows, Linux or other platforms.
- Keep minimal dependencies: only the XboxXBE‑Recomp toolchain and a C++20 compiler.

## High‑level workflow
1. **Extract** `.xbe` from disc/ISO (use `tools/xdvdfs.py` or similar).
2. **Run** `xbe_recomp` with a configuration TOML (see `example_game.toml`).
3. **Generate** C++ sources under `generated/`.
4. **Compile** sources with desired toolchain (Android NDK, MSVC, GCC, …).
5. **Link** against the portable Xbox runtime SDK (vendored in original repo).

## Dependencies
- Python 3.8+ (for extraction script).
- CMake ≥ 3.20.
- A C++20 compiler (MSVC 2022, clang‑cl, gcc ≥ 11).
- Vulkan SDK if you plan to build the Android host.
- SDL3 for input/audio when targeting Android.

## Directory layout (initial)
```
XBox-RecompTool/
├─ docs/               # additional design/architecture docs
├─ example_game.toml   # sample recompilation config
├─ generated/          # output of xbe_recomp (git‑ignored)
├─ tools/              # helper scripts (extractor, symbol dumper)
└─ README.md           # this file
```

## Next steps
- Add `example_game.toml` based on `config/game.toml` from ShaolinMonks.
- Write a quick start script `run_recomp.sh`.
- Create `.gitignore` to exclude generated sources.

---
*This directory is intended to be split out into its own repository later.*