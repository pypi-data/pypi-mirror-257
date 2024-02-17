from pathlib import Path
from typing import BinaryIO


@classmethod  # type: ignore[misc, no-untyped-def]
def from_file(
    cls,
    file_or_path: Path | BinaryIO,
) -> 'File':  # type: ignore[name-defined]  # noqa: F821
    if isinstance(file_or_path, Path):
        if file_or_path.is_dir():
            msg = f'{file_or_path} is a directory'
            raise ValueError(msg)

        data = file_or_path.read_bytes()
        filename = file_or_path.name
    else:
        file_or_path.seek(0)
        data = file_or_path.read()
        filename = Path(file_or_path.name).name

    return cls(data=data, filename=filename)
