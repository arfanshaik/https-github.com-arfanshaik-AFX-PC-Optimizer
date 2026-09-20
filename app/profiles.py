PROFILES = {
    "Low": {
        "description": "For lower-end PCs. Conservative resource use.",
        "priority": "above_normal",
        "recommended_ram_gb": 4,
        "recommended_cpu_cores": 2,
        "target_fps": "30-45",
    },
    "Balanced": {
        "description": "Best default for most PCs.",
        "priority": "high",
        "recommended_ram_gb": 8,
        "recommended_cpu_cores": 4,
        "target_fps": "45-60",
    },
    "High": {
        "description": "For stronger gaming PCs.",
        "priority": "high",
        "recommended_ram_gb": 16,
        "recommended_cpu_cores": 8,
        "target_fps": "60+ hardware/game dependent",
    },
}

def recommend_profile(info):
    ram = float(info.get("ram_gb", 0))
    cores = int(info.get("cpu_cores", 1))
    if ram >= 16 and cores >= 8:
        return "High"
    if ram >= 8 and cores >= 4:
        return "Balanced"
    return "Low"

def get_profile(name):
    return PROFILES.get(name, PROFILES["Balanced"])
