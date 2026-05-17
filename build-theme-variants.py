#!/usr/bin/env python3

from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parent
BASE_FILE = BASE_DIR / "index.html"
DIST_DIR = BASE_DIR / "dist"
OUTPUT_FILES = [
    "index.html",
    "sandstone.html",
    "harbor.html",
    "forest.html",
    "claret.html",
    "slate.html",
]


THEMES = [
    (
        "Sandstone",
        "sandstone.html",
        """
        --page-columns: minmax(0, 1.55fr) minmax(0, 0.92fr);
        --paper: #fffdf8;
        --line: #d8cabc;
        --ink: #14202b;
        --muted: #52606b;
        --accent: #b15528;
        --accent-mid: #d58955;
        --accent-end: #f0d2b8;
        --accent-soft: #f1dece;
        --chip: #f5eadf;
        --chip-line: rgba(177, 85, 40, 0.18);
        --page-wash: rgba(247, 240, 228, 0.72);
        --panel-bg: rgba(255, 255, 255, 0.45);
        --screen-bg: #ece3d8;
        --screen-glow-1: rgba(177, 85, 40, 0.14);
        --screen-glow-2: rgba(20, 32, 43, 0.12);
        --shadow: rgba(20, 32, 43, 0.12);
        """.strip(),
    ),
    (
        "Harbor",
        "harbor.html",
        """
        --page-columns: minmax(0, 1.55fr) minmax(0, 0.92fr);
        --paper: #fbfcfe;
        --line: #c7d4df;
        --ink: #102030;
        --muted: #50677a;
        --accent: #0c6f8b;
        --accent-mid: #3d9db8;
        --accent-end: #c6e1ed;
        --accent-soft: #dcecf3;
        --chip: #e8f4f9;
        --chip-line: rgba(12, 111, 139, 0.2);
        --page-wash: rgba(228, 240, 247, 0.78);
        --panel-bg: rgba(255, 255, 255, 0.56);
        --screen-bg: #dde8ef;
        --screen-glow-1: rgba(12, 111, 139, 0.15);
        --screen-glow-2: rgba(16, 32, 48, 0.12);
        --shadow: rgba(16, 32, 48, 0.14);
        """.strip(),
    ),
    (
        "Forest",
        "forest.html",
        """
        --page-columns: minmax(0, 1.55fr) minmax(0, 0.92fr);
        --paper: #fcfcf6;
        --line: #cfd7c2;
        --ink: #17211b;
        --muted: #5a685d;
        --accent: #40633a;
        --accent-mid: #789a59;
        --accent-end: #dce7cb;
        --accent-soft: #e4edd8;
        --chip: #eef3e4;
        --chip-line: rgba(64, 99, 58, 0.18);
        --page-wash: rgba(236, 243, 227, 0.82);
        --panel-bg: rgba(255, 255, 255, 0.5);
        --screen-bg: #e5eadf;
        --screen-glow-1: rgba(120, 154, 89, 0.16);
        --screen-glow-2: rgba(23, 33, 27, 0.1);
        --shadow: rgba(23, 33, 27, 0.12);
        """.strip(),
    ),
    (
        "Claret",
        "claret.html",
        """
        --page-columns: minmax(0, 1.55fr) minmax(0, 0.92fr);
        --paper: #fffafb;
        --line: #dcc7ce;
        --ink: #221720;
        --muted: #6b5761;
        --accent: #9a304d;
        --accent-mid: #c5667d;
        --accent-end: #f1cbd5;
        --accent-soft: #f2dbe1;
        --chip: #f7eaee;
        --chip-line: rgba(154, 48, 77, 0.18);
        --page-wash: rgba(248, 235, 239, 0.76);
        --panel-bg: rgba(255, 255, 255, 0.52);
        --screen-bg: #eee1e5;
        --screen-glow-1: rgba(154, 48, 77, 0.14);
        --screen-glow-2: rgba(34, 23, 32, 0.12);
        --shadow: rgba(34, 23, 32, 0.12);
        """.strip(),
    ),
    (
        "Slate",
        "slate.html",
        """
        --page-columns: minmax(0, 1.55fr) minmax(0, 0.92fr);
        --paper: #fafcfb;
        --line: #c5d2cf;
        --ink: #142324;
        --muted: #56696b;
        --accent: #1f7a72;
        --accent-mid: #48a99f;
        --accent-end: #c7e9e2;
        --accent-soft: #d9efeb;
        --chip: #e6f3f0;
        --chip-line: rgba(31, 122, 114, 0.2);
        --page-wash: rgba(230, 244, 240, 0.76);
        --panel-bg: rgba(255, 255, 255, 0.54);
        --screen-bg: #dde8e5;
        --screen-glow-1: rgba(31, 122, 114, 0.15);
        --screen-glow-2: rgba(20, 35, 36, 0.12);
        --shadow: rgba(20, 35, 36, 0.12);
        """.strip(),
    ),
]


def replace_root_vars(source: str, theme_vars: str) -> str:
    return re.sub(
        r":root\s*\{.*?\n\s*\}",
        ":root {\n" + "\n".join(f"        {line.strip()}" for line in theme_vars.splitlines()) + "\n      }",
        source,
        count=1,
        flags=re.S,
    )


def replace_title(source: str, theme_name: str) -> str:
    return re.sub(
        r"<title>.*?</title>",
        f"<title>Peter Assi Resume - {theme_name}</title>",
        source,
        count=1,
    )


def main() -> None:
    source = BASE_FILE.read_text()
    DIST_DIR.mkdir(exist_ok=True)

    for filename in OUTPUT_FILES + ["resume.pdf"]:
        path = DIST_DIR / filename
        if path.exists():
            path.unlink()

    (DIST_DIR / "index.html").write_text(source)

    for theme_name, filename, theme_vars in THEMES:
        themed_html = replace_root_vars(source, theme_vars)
        themed_html = replace_title(themed_html, theme_name)
        (DIST_DIR / filename).write_text(themed_html)


if __name__ == "__main__":
    main()
