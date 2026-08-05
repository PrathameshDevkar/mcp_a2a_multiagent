from pathlib import Path
from datetime import datetime
import pprint


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "trace.log"


def debug_log(component: str, message: str, obj=None):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write("=" * 100 + "\n")
        f.write(f"{timestamp}\n")
        f.write(f"[{component}]\n")
        f.write(f"{message}\n")

        if obj is not None:
            f.write(pprint.pformat(obj))
            f.write("\n")

        f.write("=" * 100 + "\n\n")