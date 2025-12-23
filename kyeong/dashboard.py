import platform
import sys
import os

def get_dashboard_text():
    lines = []
    lines.append("=" * 40)
    lines.append(" Terminal Helper")
    lines.append(" Version: v0.1.0")
    lines.append("=" * 40)
    lines.append(f"OS: {platform.system()} {platform.release()}")
    lines.append(f"Python: {sys.version.split()[0]}")
    lines.append(f"Current Directory: {os.getcwd()}")
    return "\n".join(lines)

def show_dashboard():
    print(get_dashboard_text())

if __name__ == "__main__":
    show_dashboard()