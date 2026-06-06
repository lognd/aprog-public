# mypy: ignore-errors
from __future__ import annotations

from pathlib import Path

from aprog.utils.hashing import hash_file, hash_paths


def test_hash_file_returns_sha256_hex(tmp_path: Path) -> None:
    f = tmp_path / "test.txt"
    f.write_text("hello")
    result = hash_file(f)
    assert isinstance(result, str)
    assert len(result) == 64  # hex sha256
    assert all(c in "0123456789abcdef" for c in result)


def test_hash_file_same_content_same_hash(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("same")
    b.write_text("same")
    assert hash_file(a) == hash_file(b)


def test_hash_file_different_content_different_hash(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("hello")
    b.write_text("world")
    assert hash_file(a) != hash_file(b)


def test_hash_paths_starts_with_sha256(tmp_path: Path) -> None:
    f = tmp_path / "file.txt"
    f.write_text("data")
    result = hash_paths([f])
    assert result.startswith("sha256:")


def test_hash_paths_empty_list_is_stable() -> None:
    h1 = hash_paths([])
    h2 = hash_paths([])
    assert h1 == h2


def test_hash_paths_order_independent(tmp_path: Path) -> None:
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("aaa")
    b.write_text("bbb")
    assert hash_paths([a, b]) == hash_paths([b, a])


def test_hash_paths_changes_when_content_changes(tmp_path: Path) -> None:
    f = tmp_path / "file.txt"
    f.write_text("v1")
    h1 = hash_paths([f])
    f.write_text("v2")
    h2 = hash_paths([f])
    assert h1 != h2
