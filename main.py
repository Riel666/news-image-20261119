#!/usr/bin/env python3
"""news-image-20261119 entry: copy the artwork to /output/entry.png.

The artwork is entry.png beside this file: a one-page newspaper front
page summing up Thursday 19 November 2026 in four stories (GTA VI begins
its global rollout, Iran hits a US base in Kuwait, Trump/Xi/Putin trilateral
talks in Shenzhen, Voyager 1 reaches one light-day out). Standard library
only, no network, deterministic: the same bytes are written on every run.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The gate reads exactly the bytes written: refuse a partial copy.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy incomplete")


if __name__ == "__main__":
    main()
