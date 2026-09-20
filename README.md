# AFX Emulator Booster

A clean, lightweight Windows utility for launching supported Android emulators with practical performance presets.

> **Purpose:** make emulator setup easier on low-end, mid-range, and high-end PCs without unsafe tweaks or fake FPS promises.

## Features

- Detects CPU core count and RAM
- Recommends **Low**, **Balanced**, or **High** mode
- Searches common locations for:
  - BlueStacks
  - LDPlayer
  - GameLoop
  - NoxPlayer
  - MuMu Player
- Manual `.exe` selection for other emulators
- One-click **Boost & Launch**
- Raises emulator process priority when possible
- Optional Windows **High Performance** power plan
- One-click restore to **Balanced** power mode
- Diagnostic command
- Clean separated source files
- GitHub Actions test workflow

## Important

This is an **emulator booster/launcher**, not a complete Android virtualization engine.

Real FPS depends on your CPU, GPU, RAM, game settings, emulator, graphics driver, temperatures, refresh rate, and virtualization support.

## Recommended profiles

| PC | Profile |
|---|---|
| 4 GB RAM / 2–4 cores | Low |
| 8–16 GB RAM / 4–8 cores | Balanced |
| 16+ GB RAM / 8+ cores | High |

## Install

### 1. Install Python

Use Python 3.10 or newer.

### 2. Install dependency

```bash
pip install -r requirements.txt
```

### 3. Start the app

```bash
python main.py
```

Or on Windows, double-click:

```text
scripts/run_windows.bat
```

## Diagnostics

```bash
python main.py --diagnose
```

## Repository structure

```text
AFX-Emulator-Booster-Repo/
├── README.md
├── main.py
├── requirements.txt
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── .gitignore
├── app/
│   ├── __init__.py
│   ├── ui.py
│   ├── hardware.py
│   ├── emulator_finder.py
│   ├── profiles.py
│   ├── launcher.py
│   └── settings.py
├── config/
│   └── settings.json
├── docs/
│   └── PERFORMANCE_GUIDE.md
├── scripts/
│   └── run_windows.bat
├── tests/
│   ├── test_profiles.py
│   └── test_settings.py
└── .github/
    └── workflows/
        └── python-tests.yml
```

## Safe optimization approach

AFX Emulator Booster avoids destructive tweaks such as disabling security, deleting system files, editing critical registry values, or killing random Windows processes.

It focuses on emulator launching, sensible profiles, process priority, optional power mode, and diagnostics.

## License

MIT
