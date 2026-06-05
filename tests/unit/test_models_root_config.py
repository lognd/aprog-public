# mypy: ignore-errors
from __future__ import annotations

import pytest
from pydantic import ValidationError

from aprog.models.root_config import ClassificationConfig, DifficultyEntry, LanguageEntry, RootConfig


def _sample_root() -> dict:
    return {
        "classification": {
            "languages": {"python": {"name": "Python"}, "cpp": {"name": "C++"}},
            "difficulties": {
                "easy": {"name": "Easy", "rank": 1},
                "medium": {"name": "Medium", "rank": 2},
                "hard": {"name": "Hard", "rank": 3},
            },
            "topics": {"data-structures": {"name": "Data Structures"}},
            "concepts": {"recursion": {"name": "Recursion"}},
        },
        "labels": {
            "requires-filesystem": {
                "name": "Requires filesystem access",
                "description": "...",
            }
        },
        "organization": {
            "require_encryption": False,
            "require_hidden_tests": True,
            "default_grader_visibility": "after_due_date",
        },
    }


def test_root_config_parses() -> None:
    cfg = RootConfig.model_validate(_sample_root())
    assert "python" in cfg.classification.languages
    assert "medium" in cfg.classification.difficulties
    assert cfg.organization.require_hidden_tests is True


def test_language_entry_has_name() -> None:
    cfg = RootConfig.model_validate(_sample_root())
    assert cfg.classification.languages["python"].name == "Python"


def test_difficulty_entry_has_rank() -> None:
    cfg = RootConfig.model_validate(_sample_root())
    assert cfg.classification.difficulties["hard"].rank == 3


def test_empty_root_config_has_defaults() -> None:
    cfg = RootConfig.model_validate({})
    assert cfg.classification.languages == {}
    assert cfg.labels == {}
    assert cfg.organization.require_encryption is False


def test_label_description_defaults_empty() -> None:
    cfg = RootConfig.model_validate(
        {"labels": {"unit-tests": {"name": "Unit Tests"}}}
    )
    assert cfg.labels["unit-tests"].description == ""
