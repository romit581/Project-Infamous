"""Local JSON configuration for the launcher."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

APP_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = APP_ROOT / "infamous_launcher.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "game_dir": "",
    "runtime_exe": "",
    "resolution": "1920x1080",
    "fullscreen": True,
    "vsync": True,
    "render_scale": "100%",
    "target_fps": "60",
    "launch_args": "",
    "save_dir": str(APP_ROOT / "user" / "saves"),
    "log_dir": str(APP_ROOT / "user" / "logs"),
}


def load_config() -> dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    if CONFIG_PATH.exists():
        try:
            saved = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            if isinstance(saved, dict):
                config.update(saved)
        except (OSError, json.JSONDecodeError):
            # Keep defaults if the local config is unreadable.
            pass
    return config


def save_config(config: dict[str, Any]) -> None:
    CONFIG_PATH.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
