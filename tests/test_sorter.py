import os
import pytest

from core.sorter import sort_files


extensions = [
    "png", "jpg", "md", "txt",
    "py", "pdf", "docx", "doc",
    "pptx", "odt", "wpd", "msg",
    "eml", "rtf"
]


@pytest.mark.parametrize("extension", extensions)
def test_sort_files_ext(tmp_path, extension):
    file = tmp_path / f"test_file.{extension}"
    file.write_text("test data")

    moves, created_folders, count = sort_files(
        tmp_path,
        "ext",
        False,
        False
    )

    expected_file = tmp_path / extension / file.name

    assert expected_file.exists()
    assert count == 1
    assert len(moves) == 1


@pytest.mark.parametrize("extension", extensions)
def test_sort_files_date(tmp_path, extension):
    file = tmp_path / f"test_file.{extension}"
    file.write_text("test data")

    os.utime(file, (1757808000, 1757808000))

    moves, created_folders, count = sort_files(
        tmp_path,
        "date",
        False,
        False
    )

    expected_folder = tmp_path / "2025-09"
    expected_file = expected_folder / file.name

    assert expected_file.exists()
    assert count == 1
    assert len(moves) == 1


def test_sort_files_all_creates_nested_folders(tmp_path):
    file = tmp_path / "test_file.pdf"
    file.write_text("test data")

    os.utime(file, (1757808000, 1757808000))

    moves, created_folders, count = sort_files(
        tmp_path,
        "all",
        False,
        False
    )

    expected_folder = tmp_path / "pdf" / "2025-09"
    expected_file = expected_folder / file.name

    assert expected_file.exists()
    assert count == 1
    assert len(moves) == 1

    assert str(tmp_path / "pdf") in created_folders
    assert str(expected_folder) in created_folders
