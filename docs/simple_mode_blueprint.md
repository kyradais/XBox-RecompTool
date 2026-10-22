# Development Blueprint: Simple-Mode Recompiler

The goal is to make the tool usable "out-of-the-box" by allowing it to analyze a disc image (ISO) and automatically generate the necessary `game.toml` using the SDK's known signatures.

## 1. Proposed "Simple Mode" Workflow
Instead of manual TOML creation, the user provides an ISO:
`./xbe_recomp_tool --auto <game.iso> --xdk <sdk_path>`

**Internal logic:**
1. **Automatic Extraction**: Use `tools/extract_iso.py` to find and extract `default.xbe`.
2. **Symbol Discovery**: Internally call `xbe_symbols` logic.
   - Compare `.xbe` against SDK's known API signatures.
   - Identify `title_id` and `entry_point` from the XBE header.
3. **Dynamic TOML Generation**:
   - Generate a temporary `game.toml` with discovered symbols, title, and entry point.
   - Set default `partitions = 128` and standard `code_sections`.
4. **Static Recompilation**:
   - Pass the generated TOML to the recompiler core (`Analysis` $\rightarrow$ `CodeGen`).
5. **Output**: Save the generated C++ code and the final `game.toml` for future manual tuning (hooks/patches).

## 2. Required Implementation Steps

### A. Integration of `xbe_symbols`
Currently, `xbe_symbols` is a separate tool. To simplify, we should wrap its logic into a library:
- `SymbolAnalyzer::findSymbols(Image& img, SDK& sdk) -> SymbolTable`

### B. ISO-to-C++ Bridge
Create a wrapper (e.g., `main_simple.cpp`) that orchestrates:
`ISO` $\rightarrow$ `XBE` $\rightarrow$ `SymbolTable` $\rightarrow$ `TOML` $\rightarrow$ `C++ Sources`.

### C. Header Analysis
Extract basic metadata from the XBE header automatically:
- `title_id`
- `entry_point`
- `kernel_thunk`

## 3. User Experience (UX)
- **Zero-Config**: User only needs the ISO and the SDK.
- **Transparency**: The tool prints "Found 180/200 symbols" so the user knows if the game is well-supported by the SDK.
- **Tuning**: The generated `game.toml` is saved so the user can add `[[hook]]` entries later without re-running the auto-analysis.

## 4. Technical Constraints
- **SDK Dependency**: The tool still depends on the XDK signature database in the SDK.
- **Build Env**: Needs a Windows host to run the recompiler core (unless the core is ported to Linux).
