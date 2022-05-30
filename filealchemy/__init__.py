from pathlib import Path
from typing import List, Union


class FileAlchemy:
    def __init__(
        self, root=".", recursive=False, extension: Union[str, List] = ""
    ) -> None:
        self.root = Path(root)
        self.recursive = recursive
        self.extension = extension if isinstance(extension, list) else [extension]

    def __iter__(self):
        pattern = "*"

        if self.recursive:
            pattern = "**/" + pattern

        for extension in self.extension:
            glob_pattern = pattern
            if extension:
                glob_pattern = f"{pattern}.{extension}"

            for path in self.root.glob(glob_pattern):
                yield path

    def filter(self, extension: Union[str, List] = ""):
        return FileAlchemy(self.root, self.recursive, extension)

    def delete(self):
        for path in self:
            path.unlink()

        return self

    def move(self, destination: str):
        # make sure destination exists
        Path(destination).mkdir(parents=True, exist_ok=True)

        for path in self:
            path.replace(Path(destination) / path.name)

        return FileAlchemy(destination, self.recursive, self.extension)
