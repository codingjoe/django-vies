#!/usr/bin/env python3
import glob
import subprocess
from pathlib import Path


def main():
    base_dir = Path(__file__).resolve().parent.parent
    pattern = base_dir / "vies/locale/*/LC_MESSAGES/django.po"

    for file in glob.glob(str(pattern)):
        mo_path = Path(file).with_suffix(".mo")
        mo_path.parent.mkdir(parents=True, exist_ok=True)

        # Ensure output directory exists
        mo_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = ["msgfmt", "-c", "-o", str(mo_path), file]
        print(f"Running: {' '.join(cmd)}")
        subprocess.check_call(cmd, cwd=base_dir)


if __name__ == "__main__":
    main()
