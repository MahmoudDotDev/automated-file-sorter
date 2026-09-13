import pytest
import pytest_check as check
import random
import tempfile
from pathlib import Path 
import os

from core.sorter import sort_files

tmp_dir = Path(tempfile.mkdtemp())
extensions = ["png", "jpg", "md", "txt", "py", "pdf", "docx", "doc", "pptx", "odt", "wpd", "msg", "eml", "rtf"]
@pytest.mark.parametrize("i", range(100))

def test_sort_files_ext(i):
    files = [tmp_dir / f"file{i}.{extensions[i % 4]}"]
    
    for file in files:
        file.write_text("test data")
    
    moves, count = sort_files(tmp_dir, "ext", False, False)
    
    for file in files:
        expected_folder = tmp_dir / file.suffix[1:]
        expected_file = expected_folder / file.name 
        
        check.is_true(expected_file.exists(), f"{file.name} was not moved to {expected_file.parent}")
    
def test_sort_files_date(i):
    files = [tmp_dir / f"file{i}.{extetions[i % 4]}"]
    for file in files:
        path = tmp_dir / file.suffix[1:] / file.name
        os.utime(path, random.randrange(10000, 20000), random.randrange(20000, 30000))
