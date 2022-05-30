import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from filealchemy import FileAlchemy

FIXTURES_DIR = "./tests/fixtures"


class TestList:
    def test_non_recursively(self):
        files = FileAlchemy(FIXTURES_DIR)

        assert list(files) == [
            Path(f"{FIXTURES_DIR}/a"),
            Path(f"{FIXTURES_DIR}/b"),
        ]

    def test_recursively(self):
        files = FileAlchemy(FIXTURES_DIR, recursive=True)

        assert list(files) == [
            Path(f"{FIXTURES_DIR}/a"),
            Path(f"{FIXTURES_DIR}/b"),
            Path(f"{FIXTURES_DIR}/b/c"),
        ]


class TestFilter:
    def test_extension(self):
        temp_file = NamedTemporaryFile(suffix=".txt", dir=FIXTURES_DIR)

        files = FileAlchemy(FIXTURES_DIR).filter(extension="txt")

        assert list(files) == [
            Path(os.path.relpath(temp_file.name)),
        ]

    def test_multiple_extensions(self):
        temp_txt_file = NamedTemporaryFile(suffix=".txt", dir=FIXTURES_DIR)
        temp_py_file = NamedTemporaryFile(suffix=".py", dir=FIXTURES_DIR)

        files = FileAlchemy(FIXTURES_DIR).filter(extension=["txt", "py"])

        assert list(files) == [
            Path(os.path.relpath(temp_txt_file.name)),
            Path(os.path.relpath(temp_py_file.name)),
        ]


class TestDelete:
    def test_default(self):
        _ = NamedTemporaryFile(suffix=".txt", dir=FIXTURES_DIR)

        files = FileAlchemy(FIXTURES_DIR).filter(extension="txt")
        files = files.delete()

        assert list(files) == []


class TestMove:
    def test_default(self):
        temp_file = NamedTemporaryFile(suffix=".txt", dir=FIXTURES_DIR)

        files = FileAlchemy(FIXTURES_DIR).filter(extension="txt")
        files = files.move("./tests/fixtures/b")

        # TODO: fix tempfile path after moving
        assert list(files) == [
            Path(FIXTURES_DIR) / "b" / Path(temp_file.name).name,
        ]

        # TODO: fix tempfile cleanup after moving
        files.delete()
