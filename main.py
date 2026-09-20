import argparse
from app.hardware import get_hardware_info
from app.profiles import recommend_profile
from app.emulator_finder import find_emulators

def diagnose():
    info = get_hardware_info()
    print("AFX Emulator Booster - Diagnostics")
    print("=" * 38)
    print(f"OS: {info['os']}")
    print(f"CPU cores: {info['cpu_cores']}")
    print(f"RAM: {info['ram_gb']} GB")
    print(f"Recommended profile: {recommend_profile(info)}")

    found = find_emulators()
    if found:
        print("Detected emulators:")
        for name, path in found:
            print(f"  - {name}: {path}")
    else:
        print("No supported emulator was auto-detected.")
        print("Use Browse in the app to select your emulator executable.")

def main():
    parser = argparse.ArgumentParser(description="AFX Emulator Booster")
    parser.add_argument("--diagnose", action="store_true", help="Run PC/emulator diagnostics")
    args = parser.parse_args()

    if args.diagnose:
        diagnose()
        return

    from app.ui import EmulatorBoosterApp
    EmulatorBoosterApp().run()

if __name__ == "__main__":
    main()
