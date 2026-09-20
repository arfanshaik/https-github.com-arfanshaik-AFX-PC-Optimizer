import os
import platform

def _ram_gb():
    try:
        import psutil
        return round(psutil.virtual_memory().total / (1024 ** 3), 1)
    except Exception:
        if hasattr(os, "sysconf"):
            try:
                pages = os.sysconf("SC_PHYS_PAGES")
                page_size = os.sysconf("SC_PAGE_SIZE")
                return round((pages * page_size) / (1024 ** 3), 1)
            except Exception:
                pass
        return 0.0

def get_hardware_info():
    return {
        "os": f"{platform.system()} {platform.release()}",
        "cpu_cores": os.cpu_count() or 1,
        "ram_gb": _ram_gb(),
        "machine": platform.machine(),
        "processor": platform.processor() or "Unknown CPU",
    }
