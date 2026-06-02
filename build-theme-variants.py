#!/usr/bin/env python3

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
BASE_FILE = BASE_DIR / "index.html"
DIST_DIR = BASE_DIR / "dist"
OUTPUT_FILE = DIST_DIR / "index.html"


def main() -> None:
    DIST_DIR.mkdir(exist_ok=True)

    for path in DIST_DIR.iterdir():
        if path.is_file():
            path.unlink()

    OUTPUT_FILE.write_text(BASE_FILE.read_text())


if __name__ == "__main__":
    main()
