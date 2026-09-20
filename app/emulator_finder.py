from pathlib import Path
import os

COMMON_PATHS = {
    "BlueStacks 5": [
        r"C:\Program Files\BlueStacks_nxt\HD-Player.exe",
        r"C:\Program Files\BlueStacks\HD-Player.exe",
    ],
    "LDPlayer": [
        r"C:\LDPlayer\LDPlayer9\dnplayer.exe",
        r"C:\Program Files\LDPlayer\LDPlayer9\dnplayer.exe",
    ],
    "GameLoop": [
        r"C:\Program Files\TxGameAssistant\AppMarket\AppMarket.exe",
        r"C:\Program Files (x86)\TxGameAssistant\AppMarket\AppMarket.exe",
    ],
    "NoxPlayer": [
        r"C:\Program Files\Nox\bin\Nox.exe",
        r"C:\Program Files (x86)\Nox\bin\Nox.exe",
    ],
    "MuMu Player": [
        r"C:\Program Files\Netease\MuMuPlayer-12.0\shell\MuMuPlayer.exe",
        r"C:\Program Files\MuMu\emulator\nemu\MuMuPlayer.exe",
    ],
}

def find_emulators():
    found = []
    seen = set()
    for name, paths in COMMON_PATHS.items():
        for raw in paths:
            path = Path(os.path.expandvars(raw))
            if path.exists():
                key = str(path).lower()
                if key not in seen:
                    found.append((name, str(path)))
                    seen.add(key)
                break
    return found
