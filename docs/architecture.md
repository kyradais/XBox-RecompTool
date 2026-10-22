# Architecture Guide for Static Recompilation

This guide describes how to port an Xbox game using the `XboxXBE-Recomp` toolchain.

## 1. The Pipeline
The process is a "Static Recompilation" chain:
`Original .xbe` $\rightarrow$ `C++ Source` $\rightarrow$ `Native ARM64 Binary`.

### A. Extraction
The `.xbe` (executable) is the brain of the game. If you have an ISO, use `tools/xdvdfs.py` to extract `default.xbe`.

### B. The Recompiler (`xbe_recomp`)
This tool analyzes the x86 assembly and translates it into equivalent C++ code.
- **Inputs**: `.xbe` file + `game.toml` configuration.
- **Output**: A set of C++ files (`x86_recomp.0.cpp`, `x86_recomp.1.cpp`, etc.) and a mapping file.

### C. The Runtime (SDK)
Recompiled code doesn't run in a vacuum; it calls Xbox system functions (XDK). You need a **Portable Runtime** that implements these functions for your target OS (Android/Linux/Windows).
- This SDK mimics the Xbox Kernel and Direct3D 8 behavior.

## 2. Key Configuration (`game.toml`)
The `.toml` file is the most critical part of the design:
- `entry`: Where the game starts.
- `partitions`: Number of code chunks (prevents huge files that crash compilers).
- `[symbols]`: Mapping of Xbox API functions to their addresses in the binary.
- `[[hook]]`: Points where you can "intercept" game logic to inject custom C++ code (e.g., for widescreen, cheats, or Android-specific fixes).

## 3. Handling Incompatibilities
Not every function is automatically recompiled.
- **Missing Symbols**: If `xbe_symbols` can't find a function, you must find its address manually and add it to `[symbols]`.
- **Hardware-Specific Code**: Some x86 instructions might not map 1:1 to ARM64. The SDK handles most, but some require manual patching via `[[hook]]`.

## 4. Android Integration (The Host)
To make it a game on Android, you need a "Host" app:
- **Vulkan Backend**: Translates Direct3D 8 calls from the SDK into Vulkan for the GPU.
- **SDL3**: Handles the Android Activity, Touch Input, and Audio output.
- **ImGui**: Used for the settings panel (Render resolution, V-Sync, etc.).

## 5. Memory & Types
- **Signed Chars**: Xbox x86 uses signed chars. Ensure your compiler uses `-fsigned-char`.
- **Alignment**: Use 16KB page alignment for Android 15+ compatibility.
- **Strict Aliasing**: Use `-fno-strict-aliasing` to match x86 memory behavior.