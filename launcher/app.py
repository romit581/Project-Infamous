"""Minimal dark-themed Tkinter launcher shell.

This is a UI/configuration prototype. It does not run the PS3 EBOOT.BIN and
does not implement the native game runtime.
"""
from __future__ import annotations

import os
import shlex
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from .config import load_config, save_config

BG = "#100D10"
PANEL = "#191418"
PANEL_2 = "#21191E"
BORDER = "#38272E"
RED = "#8E2638"
RED_HI = "#B33A4C"
TEXT = "#F2E9E9"
MUTED = "#B2A3A8"
GREEN = "#79C49A"
YELLOW = "#E5BB72"


class Launcher(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("inFAMOUS PC — Launcher")
        self.geometry("1080x700")
        self.minsize(900, 600)
        self.configure(bg=BG)
        self.config_data = load_config()
        self.vars: dict[str, tk.Variable] = {}
        self.active_tab = "HOME"
        self._build_shell()
        self.show_tab("HOME")

    def _build_shell(self) -> None:
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=24, pady=(18, 12))

        brand = tk.Frame(header, bg=BG)
        brand.pack(side="left")
        tk.Label(
            brand, text="inFAMOUS", bg=BG, fg=TEXT,
            font=("Arial", 25, "bold"),
        ).pack(anchor="w")
        tk.Label(
            brand, text="NATIVE PC PROJECT  /  LAUNCHER",
            bg=BG, fg=RED_HI, font=("Consolas", 9, "bold"),
        ).pack(anchor="w", pady=(2, 0))

        self.runtime_badge = tk.Label(
            header, text="RUNTIME NOT CONFIGURED", bg=PANEL_2,
            fg=YELLOW, padx=12, pady=8, font=("Consolas", 9, "bold"),
        )
        self.runtime_badge.pack(side="right", pady=8)

        tk.Frame(self, bg=RED, height=2).pack(fill="x", padx=24)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=24, pady=18)

        sidebar = tk.Frame(
            body, bg=PANEL, width=200,
            highlightbackground=BORDER, highlightthickness=1,
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="CONTROL DECK", bg=PANEL, fg=MUTED,
            font=("Consolas", 9, "bold"),
        ).pack(anchor="w", padx=16, pady=(20, 12))

        self.nav_buttons: dict[str, tk.Button] = {}
        for name, symbol in (
            ("HOME", "⌂"), ("GRAPHICS", "▧"), ("PERFORMANCE", "◴"),
            ("GAME", "▶"), ("ADVANCED", "⚙"),
        ):
            button = tk.Button(
                sidebar, text=f"  {symbol}   {name}", anchor="w",
                command=lambda n=name: self.show_tab(n),
                bg=PANEL, fg=MUTED, activebackground=RED,
                activeforeground=TEXT, bd=0, padx=12, pady=13,
                font=("Consolas", 10, "bold"), cursor="hand2",
            )
            button.pack(fill="x", padx=8, pady=2)
            self.nav_buttons[name] = button

        tk.Frame(sidebar, bg=BORDER, height=1).pack(
            fill="x", padx=16, pady=(18, 12)
        )
        tk.Label(
            sidebar, text="PROJECT STATUS", bg=PANEL, fg=MUTED,
            font=("Consolas", 9, "bold"),
        ).pack(anchor="w", padx=16, pady=(0, 8))
        tk.Label(
            sidebar, text="Launcher  •  Prototype", bg=PANEL, fg=TEXT,
            font=("Arial", 10),
        ).pack(anchor="w", padx=16, pady=3)
        tk.Label(
            sidebar, text="Game runtime  •  Pending", bg=PANEL, fg=YELLOW,
            font=("Arial", 10),
        ).pack(anchor="w", padx=16, pady=3)

        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True, padx=(18, 0))

        footer = tk.Frame(self, bg="#0B090B", height=32)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)
        self.status = tk.Label(
            footer, text="READY  //  Configure game files and runtime when available.",
            bg="#0B090B", fg=MUTED, anchor="w",
            font=("Consolas", 9), padx=24,
        )
        self.status.pack(fill="both", expand=True)

    def _clear(self) -> None:
        for child in self.content.winfo_children():
            child.destroy()

    def _title(self, title: str, subtitle: str) -> None:
        tk.Label(
            self.content, text=title, bg=BG, fg=TEXT,
            font=("Arial", 23, "bold"),
        ).pack(anchor="w")
        tk.Label(
            self.content, text=subtitle, bg=BG, fg=MUTED,
            font=("Arial", 10),
        ).pack(anchor="w", pady=(4, 18))

    def _card(self, parent: tk.Widget | None = None) -> tk.Frame:
        parent = parent or self.content
        outer = tk.Frame(
            parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1
        )
        outer.pack(fill="x", pady=(0, 12))
        inner = tk.Frame(outer, bg=PANEL)
        inner.pack(fill="x", padx=18, pady=16)
        return inner

    def show_tab(self, tab: str) -> None:
        self.active_tab = tab
        for name, button in self.nav_buttons.items():
            button.configure(
                bg=RED if name == tab else PANEL,
                fg=TEXT if name == tab else MUTED,
            )
        self._clear()
        getattr(self, f"_page_{tab.lower()}")()
        self._refresh_runtime_badge()

    def _refresh_runtime_badge(self) -> None:
        runtime = self.config_data.get("runtime_exe", "")
        if runtime and Path(runtime).is_file():
            self.runtime_badge.configure(text="RUNTIME READY", fg=GREEN)
        else:
            self.runtime_badge.configure(text="RUNTIME NOT CONFIGURED", fg=YELLOW)

    def _status(self, message: str, color: str = MUTED) -> None:
        self.status.configure(text=message, fg=color)

    def _button(
        self, parent: tk.Widget, text: str, command, primary: bool = True
    ) -> tk.Button:
        return tk.Button(
            parent, text=text, command=command,
            bg=RED if primary else PANEL_2, fg=TEXT,
            activebackground=RED_HI if primary else BORDER,
            activeforeground=TEXT, bd=0, padx=15, pady=10,
            font=("Arial", 9, "bold"), cursor="hand2",
        )

    def _page_home(self) -> None:
        self._title("Welcome back, Cole.", "EMPIRE CITY  /  NATIVE PC PORT")
        hero = tk.Frame(
            self.content, bg="#25151B",
            highlightbackground=RED, highlightthickness=1,
        )
        hero.pack(fill="x", pady=(0, 14))
        inside = tk.Frame(hero, bg="#25151B")
        inside.pack(fill="x", padx=24, pady=24)
        tk.Label(
            inside, text="THE CITY IS YOURS TO RECLAIM",
            bg="#25151B", fg=TEXT, font=("Arial", 21, "bold"),
        ).pack(anchor="w")
        tk.Label(
            inside, text="A community-driven native PC port research project.",
            bg="#25151B", fg=MUTED, font=("Arial", 11),
        ).pack(anchor="w", pady=(6, 18))
        actions = tk.Frame(inside, bg="#25151B")
        actions.pack(fill="x")
        self._button(actions, "▶   PLAY", self.launch_game).pack(side="left")
        self._button(
            actions, "CONFIGURE GAME FILES",
            lambda: self.show_tab("GAME"), primary=False,
        ).pack(side="left", padx=(10, 0))

        card = self._card()
        tk.Label(
            card, text="SYSTEM CHECK", bg=PANEL, fg=MUTED,
            font=("Consolas", 9, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        game_dir = self.config_data.get("game_dir", "")
        runtime = self.config_data.get("runtime_exe", "")
        checks = (
            ("Game files", "Directory selected" if game_dir and Path(game_dir).is_dir() else "Not configured",
             GREEN if game_dir and Path(game_dir).is_dir() else YELLOW),
            ("Native runtime", "Executable found" if runtime and Path(runtime).is_file() else "Not available yet",
             GREEN if runtime and Path(runtime).is_file() else YELLOW),
            ("Settings", "infamous_launcher.json", MUTED),
        )
        for row, (label, value, color) in enumerate(checks, start=1):
            tk.Label(card, text=label, bg=PANEL, fg=TEXT, font=("Arial", 10)).grid(
                row=row, column=0, sticky="w", pady=5
            )
            tk.Label(card, text=value, bg=PANEL, fg=color, font=("Consolas", 10)).grid(
                row=row, column=1, sticky="e", padx=(24, 0), pady=5
            )
        card.columnconfigure(1, weight=1)

        note = self._card()
        tk.Label(note, text="PROTOTYPE NOTICE", bg=PANEL, fg=RED_HI,
                 font=("Consolas", 9, "bold")).pack(anchor="w")
        tk.Label(
            note,
            text="The launcher does not itself make the PS3 game executable on PC. A compatible native runtime must be developed separately. Graphics settings are saved locally but do not affect gameplay until the runtime implements them.",
            bg=PANEL, fg=MUTED, wraplength=690, justify="left",
            font=("Arial", 10),
        ).pack(anchor="w", pady=(7, 0))

    def _var(self, key: str, default=None) -> tk.Variable:
        if key not in self.vars:
            value = self.config_data.get(key, default if default is not None else "")
            self.vars[key] = tk.StringVar(value=str(value))
        return self.vars[key]

    def _option(
        self, parent: tk.Widget, label: str, key: str, values: list[str],
        note: str = "",
    ) -> None:
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", pady=8)
        left = tk.Frame(row, bg=PANEL)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text=label, bg=PANEL, fg=TEXT,
                 font=("Arial", 10, "bold")).pack(anchor="w")
        if note:
            tk.Label(left, text=note, bg=PANEL, fg=MUTED,
                     font=("Arial", 9)).pack(anchor="w", pady=(3, 0))
        var = self._var(key)
        menu = tk.OptionMenu(row, var, *values)
        menu.configure(
            bg=PANEL_2, fg=TEXT, activebackground=RED, activeforeground=TEXT,
            bd=0, highlightthickness=0, font=("Consolas", 10), width=14,
        )
        menu["menu"].configure(bg=PANEL_2, fg=TEXT)
        menu.pack(side="right")

    def _check(self, parent: tk.Widget, label: str, key: str, note: str) -> None:
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", pady=8)
        left = tk.Frame(row, bg=PANEL)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text=label, bg=PANEL, fg=TEXT,
                 font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(left, text=note, bg=PANEL, fg=MUTED,
                 font=("Arial", 9)).pack(anchor="w", pady=(3, 0))
        var = self._var(key)
        # Use a BooleanVar to keep checkbox values unambiguous.
        bool_var = tk.BooleanVar(value=str(var.get()).lower() in ("true", "1", "yes"))
        self.vars[key] = bool_var
        tk.Checkbutton(
            row, text="Enabled", variable=bool_var, bg=PANEL, fg=TEXT,
            selectcolor=PANEL_2, activebackground=PANEL, activeforeground=TEXT,
            font=("Arial", 10),
        ).pack(side="right")

    def _save(self) -> None:
        for key, var in self.vars.items():
            value = var.get()
            if isinstance(var, tk.BooleanVar):
                value = bool(value)
            self.config_data[key] = value
        save_config(self.config_data)
        self._status("SETTINGS SAVED  //  infamous_launcher.json", GREEN)

    def _page_graphics(self) -> None:
        self._title("Graphics", "DISPLAY CONFIGURATION  /  LOCAL SETTINGS")
        card = self._card()
        self._option(card, "Resolution", "resolution",
                     ["1280x720", "1600x900", "1920x1080", "2560x1440", "3840x2160"],
                     "Output resolution, subject to runtime support.")
        self._check(card, "Fullscreen", "fullscreen", "Use fullscreen mode when supported.")
        self._check(card, "Vertical sync", "vsync", "May reduce tearing; requires renderer support.")
        self._option(card, "Render scale", "render_scale",
                     ["50%", "67%", "75%", "83%", "100%", "125%", "150%"],
                     "Placeholder until the runtime exposes render scaling.")
        self._button(self.content, "SAVE GRAPHICS SETTINGS", self._save).pack(anchor="e")

    def _page_performance(self) -> None:
        self._title("Performance", "FRAME PACING  /  EXPERIMENTAL OPTIONS")
        card = self._card()
        self._option(card, "Target frame rate", "target_fps",
                     ["30", "60", "90", "120", "Uncapped"],
                     "Target only; actual frame pacing must be implemented by the runtime.")
        row = tk.Frame(card, bg=PANEL)
        row.pack(fill="x", pady=8)
        tk.Label(row, text="Launch arguments", bg=PANEL, fg=TEXT,
                 font=("Arial", 10, "bold")).pack(anchor="w")
        var = self._var("launch_args")
        tk.Entry(row, textvariable=var, bg=PANEL_2, fg=TEXT,
                 insertbackground=TEXT, relief="flat", width=35).pack(
                     anchor="e", ipady=7, pady=(5, 0)
                 )
        warning = self._card()
        tk.Label(warning, text="NOT IMPLEMENTED YET", bg=PANEL, fg=YELLOW,
                 font=("Consolas", 9, "bold")).pack(anchor="w")
        tk.Label(
            warning,
            text="Upscaling, frame generation, shader cache management and GPU selection must remain unavailable until a compatible renderer supports them.",
            bg=PANEL, fg=MUTED, wraplength=690, justify="left",
            font=("Arial", 10),
        ).pack(anchor="w", pady=(6, 0))
        self._button(self.content, "SAVE PERFORMANCE SETTINGS", self._save).pack(anchor="e")

    def _choose_dir(self, key: str) -> None:
        path = filedialog.askdirectory(title="Select folder")
        if path:
            self.config_data[key] = path
            self._save()
            self.show_tab("GAME")

    def _choose_runtime(self) -> None:
        path = filedialog.askopenfilename(
            title="Select compatible native runtime executable",
            filetypes=[("Windows executable", "*.exe"), ("All files", "*.*")],
        )
        if path:
            self.config_data["runtime_exe"] = path
            self._save()
            self.show_tab("GAME")

    def _path_row(self, parent: tk.Widget, label: str, key: str, command,
                  button_label: str = "BROWSE") -> None:
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", pady=9)
        tk.Label(row, text=label, bg=PANEL, fg=TEXT,
                 font=("Arial", 10, "bold")).pack(anchor="w")
        lower = tk.Frame(row, bg=PANEL)
        lower.pack(fill="x", pady=(6, 0))
        value = self.config_data.get(key, "") or "Not selected"
        tk.Label(
            lower, text=value, bg=PANEL_2, fg=MUTED, anchor="w",
            padx=10, pady=9, font=("Consolas", 9), wraplength=480,
            justify="left",
        ).pack(side="left", fill="x", expand=True)
        self._button(lower, button_label, command).pack(side="right", padx=(8, 0))

    def _page_game(self) -> None:
        self._title("Game", "GAME DATA  /  RUNTIME PATHS")
        card = self._card()
        self._path_row(card, "Game data directory", "game_dir",
                       lambda: self._choose_dir("game_dir"))
        self._path_row(card, "Native runtime executable", "runtime_exe",
                       self._choose_runtime, "SELECT EXE")
        self._path_row(card, "Save directory", "save_dir",
                       lambda: self._choose_dir("save_dir"))
        self._path_row(card, "Log directory", "log_dir",
                       lambda: self._choose_dir("log_dir"))
        tk.Label(
            self.content,
            text="Select a future compatible native runtime executable — not the PS3 EBOOT.BIN.",
            bg=BG, fg=YELLOW, font=("Arial", 9),
        ).pack(anchor="w", pady=(0, 10))
        self._button(self.content, "SAVE PATHS", self._save).pack(anchor="e")

    def _page_advanced(self) -> None:
        self._title("Advanced", "DIAGNOSTICS  /  PROJECT UTILITIES")
        card = self._card()
        tk.Label(card, text="Local configuration file", bg=PANEL, fg=TEXT,
                 font=("Arial", 10, "bold")).pack(anchor="w")
        tk.Label(card, text=str(__import__("launcher.config", fromlist=["CONFIG_PATH"]).CONFIG_PATH),
                 bg=PANEL, fg=MUTED, font=("Consolas", 9),
                 wraplength=690, justify="left").pack(anchor="w", pady=(5, 10))
        self._button(card, "SAVE ALL SETTINGS", self._save).pack(anchor="w")
        log = self._card()
        tk.Label(log, text="CURRENT CAPABILITIES", bg=PANEL, fg=MUTED,
                 font=("Consolas", 9, "bold")).pack(anchor="w")
        tk.Label(
            log,
            text="Launcher UI: available\nLocal settings: available\nNative runtime: not included\nPS3 executable compatibility: not implemented\nGraphics backend: not connected",
            bg=PANEL, fg=TEXT, justify="left", font=("Consolas", 10),
        ).pack(anchor="w", pady=(8, 0))

    def launch_game(self) -> None:
        self._save()
        runtime = str(self.config_data.get("runtime_exe", "")).strip()
        if not runtime or not Path(runtime).is_file():
            messagebox.showinfo(
                "Native runtime not configured",
                "No compatible native inFAMOUS runtime is configured yet. "
                "Choose a runtime executable under Game when one becomes available. "
                "The original PS3 EBOOT.BIN cannot be launched directly by Windows.",
            )
            self.show_tab("GAME")
            return
        args_text = str(self.config_data.get("launch_args", ""))
        try:
            args = shlex.split(args_text, posix=(os.name != "nt"))
            subprocess.Popen([runtime, *args], cwd=str(Path(runtime).parent))
            self._status("RUNTIME PROCESS STARTED", GREEN)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Launch failed", f"Could not start runtime:\n{exc}")
            self._status("LAUNCH FAILED", RED_HI)
