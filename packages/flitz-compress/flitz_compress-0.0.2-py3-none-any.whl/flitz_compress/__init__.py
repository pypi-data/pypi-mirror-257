__version__ = "0.0.2"

from flitz.context_menu import ContextMenuItem

from pathlib import Path
import zipfile

def get_target(path: Path, extension: str = "zip") -> Path:
    """Given a directory name, return a name that doesn't exist yet."""
    if not path.is_dir():
        raise ValueError(f"{path} is not a directory")
    tmp_path = path / f"archive.{extension}"
    suffix = None
    while tmp_path.exists():
        if suffix is None:
            suffix = 1
        else:
            suffix += 1
        tmp_path = path / f"archive-{suffix}.{extension}"
    return tmp_path


def compress_selection(selection: list[Path]):
    print(f"Compressing {selection}...")
    if len(selection) == 0:
        raise ValueError("No selection")
    target = get_target(selection[0].parent)
    with zipfile.ZipFile(target, "w") as archive:
        for path in selection:
            archive.write(path, path.name)

def is_active(selection: list[Path]) -> bool:
    return len(selection) > 0

context_menu_item = ContextMenuItem(
    name = "COMPRESS",
    label="Compress selection",
    action=compress_selection,
    is_active=is_active,
)

