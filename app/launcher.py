import platform
import subprocess
import time
from pathlib import Path

HIGH_PERFORMANCE = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
BALANCED = "381b4222-f694-41f0-9685-ff5bb260df2e"

def set_power_plan(high_performance=True):
    if platform.system() != "Windows":
        return False, "Power plan control is available only on Windows."

    guid = HIGH_PERFORMANCE if high_performance else BALANCED
    try:
        result = subprocess.run(
            ["powercfg", "/setactive", guid],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return True, "Windows power plan updated."
        return False, (result.stderr or result.stdout or "Power plan change failed.").strip()
    except Exception as exc:
        return False, str(exc)

def raise_priority(pid, priority_name):
    try:
        import psutil
        process = psutil.Process(pid)
        if platform.system() != "Windows":
            return False, "Priority optimization skipped on non-Windows."

        if priority_name == "high":
            process.nice(psutil.HIGH_PRIORITY_CLASS)
        else:
            process.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
        return True, "Emulator priority optimized."
    except Exception as exc:
        return False, f"Priority optimization skipped: {exc}"

def launch_emulator(executable, profile, enable_power_plan=False, auto_priority=True):
    exe = Path(executable)
    if not exe.exists():
        return False, f"Emulator executable not found: {exe}"

    notes = []
    if enable_power_plan:
        _, msg = set_power_plan(True)
        notes.append(msg)

    try:
        process = subprocess.Popen([str(exe)], cwd=str(exe.parent))
    except Exception as exc:
        return False, f"Could not launch emulator: {exc}"

    if auto_priority:
        time.sleep(0.8)
        _, msg = raise_priority(process.pid, profile.get("priority", "high"))
        notes.append(msg)

    return True, "\n".join([f"Launched {exe.name}."] + notes)
