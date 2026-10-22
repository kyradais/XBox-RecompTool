# Build Pipeline Overview

The build process requires a Windows environment to run `xbe_recomp` (compiled with Visual Studio's clang-cl), but the resulting code can be cross-compiled or compiled for other OSes.

## Stages

### Stage 1: Tools
Build the `xbe_recomp` and `xbe_symbols` host tools.
- **Tool**: CMake + clang-cl.
- **Source**: Pulled from `XboxXBE-Recomp` GitHub.
- **Dependencies**: Zydis (disassembler), toml++ (config parser).
- **Output**: `xbe_recomp.exe`, `xbe_symbols.exe`.

### Stage 2: Symbol Discovery
Run `xbe_symbols.exe <path-to-xbe> <path-to-xdk>`.
- Scans the binary and the SDK's known signature database.
- Generates the `[symbols]` table if missing.
- If a symbol is missing, the runtime cannot link that function. You will need to either:
  1. Add the address manually.
  2. Implement the missing function in the SDK.

### Stage 3: Recompilation
Run `xbe_recomp.exe config/game.toml --xdk <path-to-xdk>`.
- Translates x86 instructions in `default.xbe` to C++.
- Splits output into partitions (default 128) for parallel compilation.
- Generated files: `x86_recomp.{0..N}.cpp` and `x86_func_mapping.cpp`.

### Stage 4: Android Compilation
- Use Gradle + Android NDK.
- CMake compiles the generated C++ plus the host code.
- **Time**: 30-90 minutes for the first build (release mode).
- **Optimization**: Must use `-O2`; debug builds are too slow to run.
- **Output**: `libmain.so` packaged inside the APK.

## Commands Quick Reference
```bash
# 1. Build tools
cmake -S tools -B out/build/android-tools -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build out/build/android-tools

# 2. Find symbols
out/build/android-tools/xbe_symbols.exe assets/default.xbe sdk/xdk --out config/game.toml

# 3. Recompile
out/build/android-tools/xbe_recomp.exe config/game.toml --xdk sdk/xdk

# 4. Build APK
gradlew.bat assembleRelease
```
