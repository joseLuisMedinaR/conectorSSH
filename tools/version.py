import os
import sys


def obtener_version():
    try:
        if getattr(sys, "frozen", False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.dirname(__file__))

        version_path = os.path.join(base_path, "VERSION")

        with open(version_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    except Exception:
        return "dev"