# mypy: ignore-errors
from __future__ import annotations

import pytest
from pydantic import ValidationError

from aprog.models.assignment import (
    AssignmentConfig,
)


def _valid_data() -> dict:
    return {
        "assignment": {
            "slug": "linked-list-insertion",
            "name": "Linked List Insertion",
            "author": "handle",
            "description": "Insert into a linked list.",
        },
        "classification": {
            "language": "python",
            "difficulty": "medium",
            "topics": ["data-structures"],
        },
        "template": {"slug": "python-function"},
    }


def test_valid_assignment_parses() -> None:
    cfg = AssignmentConfig.model_validate(_valid_data())
    assert cfg.assignment.slug == "linked-list-insertion"
    assert cfg.classification.language == "python"
    assert cfg.grader.visibility == "after_due_date"


def test_slug_must_be_kebab_case() -> None:
    data = _valid_data()
    data["assignment"]["slug"] = "LinkedList"
    with pytest.raises(ValidationError, match="kebab-case"):
        AssignmentConfig.model_validate(data)


def test_slug_rejects_reserved_word() -> None:
    data = _valid_data()
    data["assignment"]["slug"] = "solution"
    with pytest.raises(ValidationError, match="reserved"):
        AssignmentConfig.model_validate(data)


def test_status_default_is_draft() -> None:
    cfg = AssignmentConfig.model_validate(_valid_data())
    assert cfg.assignment.status == "draft"


def test_invalid_status_rejected() -> None:
    data = _valid_data()
    data["assignment"]["status"] = "live"
    with pytest.raises(ValidationError):
        AssignmentConfig.model_validate(data)


def test_topics_must_be_nonempty() -> None:
    data = _valid_data()
    data["classification"]["topics"] = []
    with pytest.raises(ValidationError):
        AssignmentConfig.model_validate(data)


def test_grader_defaults() -> None:
    cfg = AssignmentConfig.model_validate(_valid_data())
    assert cfg.grader.visibility == "after_due_date"
    assert cfg.grader.stdout_visibility == "after_due_date"


def test_grader_visibility_values() -> None:
    for v in ("visible", "hidden", "after_due_date", "after_published"):
        data = _valid_data()
        data["grader"] = {"visibility": v}
        cfg = AssignmentConfig.model_validate(data)
        assert cfg.grader.visibility == v


def test_grader_invalid_visibility_rejected() -> None:
    data = _valid_data()
    data["grader"] = {"visibility": "never"}
    with pytest.raises(ValidationError):
        AssignmentConfig.model_validate(data)


def test_optional_fields_default_empty() -> None:
    cfg = AssignmentConfig.model_validate(_valid_data())
    assert cfg.classification.concepts == []
    assert cfg.classification.labels == []
    assert cfg.classification.course is None
    assert cfg.classification.module is None


def test_slug_with_numbers_valid() -> None:
    data = _valid_data()
    data["assignment"]["slug"] = "lab1-intro"
    cfg = AssignmentConfig.model_validate(data)
    assert cfg.assignment.slug == "lab1-intro"
