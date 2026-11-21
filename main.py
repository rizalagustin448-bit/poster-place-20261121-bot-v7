"""make.fun entrypoint: copy the pre-rendered poster to the output dir.

The poster image is drawn at build time by draw_poster.py (Pillow) and
committed as poster.png. This entrypoint uses only the standard library
and validates the PNG magic bytes and the 1 MiB size cap before copying.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "poster.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = SRC.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("poster.png is not a valid PNG")
    if len(data) > 1048576:
        raise SystemExit("poster.png exceeds the 1 MiB limit")
    out = out_dir / "entry.png"
    shutil.copyfile(SRC, out)
    print(f"wrote {out} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
