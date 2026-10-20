# Development roadmap

## Milestone 1 — Launcher foundation
- [x] Repository layout
- [x] Tkinter application shell
- [x] Local JSON settings
- [x] Game and runtime path selectors
- [x] Safe launch failure when no runtime is configured

## Milestone 2 — Launcher/runtime contract
- [ ] Document config schema and command-line arguments
- [ ] Runtime capability detection
- [ ] Standard log location and exit-code reporting
- [ ] Add automated config tests

## Milestone 3 — Integration
- [ ] Connect supported settings to a real runtime
- [ ] Controller configuration
- [ ] Runtime logs and diagnostics
- [ ] Windows packaging

## Scope note
The launcher is not a PS3 emulator and does not itself port the game. A compatible native runtime is a separate, substantial reverse-engineering project.
