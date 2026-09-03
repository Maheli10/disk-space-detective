from pathlib import Path

from core.scanner import scan_filesystem


def test_scanner_returns_results():
    test_folder = Path(".")

    result = scan_filesystem(test_folder)

    assert isinstance(result, dict)

    assert "root" in result
    assert "total_size" in result
    assert "files" in result
    assert "folder_sizes" in result
    assert "top_level_folders" in result
    assert "large_files" in result
    assert "old_files" in result
    assert "categories" in result
    assert "special_folders" in result
    assert "cache_folders" in result
    assert "duplicate_candidates" in result


def test_scanner_total_size():
    test_folder = Path(".")

    result = scan_filesystem(test_folder)

    assert result["total_size"] >= 0


def test_scanner_lists_are_valid():
    test_folder = Path(".")

    result = scan_filesystem(test_folder)

    assert isinstance(result["files"], list)
    assert isinstance(result["large_files"], list)
    assert isinstance(result["old_files"], list)
    assert isinstance(result["categories"], list)
    assert isinstance(result["special_folders"], list)
    assert isinstance(result["cache_folders"], list)
    assert isinstance(result["duplicate_candidates"], dict)