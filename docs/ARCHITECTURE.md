# Architecture

- `main.py`: application entry point
- `launcher/app.py`: Tkinter screens and user interactions
- `launcher/config.py`: local JSON settings persistence
- `docs/`: project documentation

## Local configuration
The launcher stores machine-specific paths in `infamous_launcher.json` next to the project. This file is excluded from version control.

## Runtime boundary
The launcher launches only a user-selected compatible native executable. It must not attempt to launch the PS3 `EBOOT.BIN` as a Windows application. Graphics/performance options are currently configuration values only; they do not affect gameplay until a runtime reads and implements them.
