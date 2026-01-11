import shutil
from pathlib import Path
from datetime import datetime


formats = {"png", "jpg", "jpeg", "webp"}
directory = Path(__file__).resolve().parent.parent / "uploads"


def is_format_allowed(filename):
    if not filename:
        return False
    return Path(filename).suffix.lower().lstrip(".") in {f.lower() for f in formats}


def upload_image(
    source,
    filename,
):
    src = Path(source)
    if not src.exists():
        raise FileNotFoundError(f"File not found: {source}")

    if is_format_allowed(src.name) == False:
        raise ValueError("Image format not allowed")

    directory.mkdir(parents=True, exist_ok=True)
    name = f"{filename}-{datetime.now().strftime('%Y-%m-%d')}{src.suffix.lower()}"
    dest = directory / name
    shutil.copyfile(src, dest)
    return str(Path("uploads") / name)
