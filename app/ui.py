import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from app.hardware import get_hardware_info
from app.profiles import PROFILES, recommend_profile, get_profile
from app.emulator_finder import find_emulators
from app.launcher import launch_emulator, set_power_plan
from app.settings import load_settings, save_settings

class EmulatorBoosterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AFX Emulator Booster")
        self.root.geometry("780x570")
        self.root.minsize(720, 520)

        self.settings = load_settings()
        self.hardware = get_hardware_info()
        self.detected = find_emulators()

        default_profile = self.settings.get("profile") or recommend_profile(self.hardware)
        self.profile_var = tk.StringVar(value=default_profile)
        self.emulator_var = tk.StringVar(value=self.settings.get("emulator_path", ""))
        self.power_var = tk.BooleanVar(
            value=self.settings.get("enable_high_performance_power_plan", False)
        )
        self.priority_var = tk.BooleanVar(
            value=self.settings.get("auto_raise_priority", True)
        )
        self.status_var = tk.StringVar(value="Ready.")

        self._build()
        self._populate()
        self._show_profile()

    def _build(self):
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        page = ttk.Frame(self.root, padding=20)
        page.pack(fill="both", expand=True)

        ttk.Label(page, text="AFX Emulator Booster", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(
            page,
            text="Emulator launcher + safe performance profiles for Windows PCs",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(0, 16))

        system = ttk.LabelFrame(page, text="PC Detection", padding=12)
        system.pack(fill="x")
        ttk.Label(
            system,
            text=(
                f"OS: {self.hardware['os']}   "
                f"CPU: {self.hardware['cpu_cores']} cores   "
                f"RAM: {self.hardware['ram_gb']} GB   "
                f"Suggested: {recommend_profile(self.hardware)}"
            )
        ).pack(anchor="w")

        emu = ttk.LabelFrame(page, text="Choose Emulator", padding=12)
        emu.pack(fill="x", pady=12)
        row = ttk.Frame(emu)
        row.pack(fill="x")
        self.combo = ttk.Combobox(row, textvariable=self.emulator_var)
        self.combo.pack(side="left", fill="x", expand=True)
        ttk.Button(row, text="Browse", command=self._browse).pack(side="left", padx=(8, 0))
        ttk.Button(row, text="Scan", command=self._scan).pack(side="left", padx=(8, 0))

        perf = ttk.LabelFrame(page, text="Performance Profile", padding=12)
        perf.pack(fill="x")
        p_row = ttk.Frame(perf)
        p_row.pack(fill="x")
        ttk.Label(p_row, text="Profile").pack(side="left")
        p_combo = ttk.Combobox(
            p_row,
            textvariable=self.profile_var,
            values=list(PROFILES.keys()),
            state="readonly",
            width=16
        )
        p_combo.pack(side="left", padx=8)
        p_combo.bind("<<ComboboxSelected>>", lambda _e: self._show_profile())

        self.profile_text = ttk.Label(perf, wraplength=700)
        self.profile_text.pack(anchor="w", pady=(10, 0))

        opts = ttk.LabelFrame(page, text="Boost Options", padding=12)
        opts.pack(fill="x", pady=12)
        ttk.Checkbutton(
            opts,
            text="Raise emulator process priority",
            variable=self.priority_var
        ).pack(anchor="w")
        ttk.Checkbutton(
            opts,
            text="Use Windows High Performance power plan",
            variable=self.power_var
        ).pack(anchor="w", pady=(5, 0))

        buttons = ttk.Frame(page)
        buttons.pack(fill="x")
        ttk.Button(buttons, text="BOOST & LAUNCH", command=self._launch).pack(side="left")
        ttk.Button(buttons, text="Restore Balanced Power", command=self._restore).pack(side="left", padx=8)
        ttk.Button(buttons, text="Save", command=self._save).pack(side="left")

        ttk.Separator(page).pack(fill="x", pady=15)
        ttk.Label(page, textvariable=self.status_var, wraplength=700).pack(anchor="w")
        ttk.Label(
            page,
            text="FPS is hardware/game dependent. This tool avoids destructive system tweaks.",
            wraplength=700
        ).pack(anchor="w", pady=(14, 0))

    def _populate(self):
        values = [f"{name} | {path}" for name, path in self.detected]
        self.combo["values"] = values
        if not self.emulator_var.get() and self.detected:
            self.emulator_var.set(self.detected[0][1])

    def _scan(self):
        self.detected = find_emulators()
        self._populate()
        self.status_var.set(f"Scan complete: {len(self.detected)} supported emulator(s) detected.")

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Select emulator executable",
            filetypes=[("Executable", "*.exe"), ("All files", "*.*")]
        )
        if path:
            self.emulator_var.set(path)

    def _path(self):
        raw = self.emulator_var.get().strip()
        return raw.split(" | ", 1)[1].strip() if " | " in raw else raw

    def _show_profile(self):
        profile = get_profile(self.profile_var.get())
        self.profile_text.config(
            text=(
                f"{profile['description']} "
                f"FPS guidance: {profile['target_fps']}. "
                f"Resource guidance: {profile['recommended_ram_gb']} GB RAM / "
                f"{profile['recommended_cpu_cores']} CPU cores."
            )
        )

    def _save(self):
        save_settings({
            "profile": self.profile_var.get(),
            "emulator_path": self._path(),
            "enable_high_performance_power_plan": self.power_var.get(),
            "auto_raise_priority": self.priority_var.get()
        })
        self.status_var.set("Settings saved.")

    def _launch(self):
        path = self._path()
        if not path:
            messagebox.showwarning("AFX Emulator Booster", "Select an emulator first.")
            return

        self._save()
        ok, msg = launch_emulator(
            path,
            get_profile(self.profile_var.get()),
            enable_power_plan=self.power_var.get(),
            auto_priority=self.priority_var.get()
        )
        self.status_var.set(msg)
        if not ok:
            messagebox.showerror("Launch failed", msg)

    def _restore(self):
        ok, msg = set_power_plan(False)
        self.status_var.set(msg)
        if not ok:
            messagebox.showwarning("Power plan", msg)

    def run(self):
        self.root.mainloop()
