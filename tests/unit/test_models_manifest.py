# mypy: ignore-errors
from __future__ import annotations

from aprog.models.manifest import (
    AssignmentManifest,
    ManifestAssignment,
    ManifestClassification,
    ManifestPaths,
    ManifestTemplate,
    PackageManifest,
    PrivateManifest,
)


def _sample_manifest() -> AssignmentManifest:
    return AssignmentManifest(
        assignment=ManifestAssignment(
            slug="linked-list-insertion",
            name="Linked List Insertion",
            author="handle",
            description="Insert into a linked list.",
        ),
        classification=ManifestClassification(
            language="python",
            difficulty="medium",
            topics=["data-structures"],
        ),
        template=ManifestTemplate(slug="python-function", version="0.1"),
        paths=ManifestPaths(
            assignment_root="assignments/linked-list-insertion",
            readme="assignments/linked-list-insertion/README.md",
            visible_tests="assignments/linked-list-insertion/visible-tests",
        ),
        state="draft",
        source_hash="sha256:abc123",
    )


def test_manifest_roundtrip() -> None:
    m = _sample_manifest()
    data = m.model_dump()
    m2 = AssignmentManifest.model_validate(data)
    assert m2.assignment.slug == m.assignment.slug
    assert m2.source_hash == m.source_hash


def test_manifest_schema_version_default() -> None:
    m = _sample_manifest()
    assert m.schema_version == "0.1"


def test_package_manifest_fields() -> None:
    pm = PackageManifest(
        assignment_slug="linked-list-insertion",
        contains_solution=True,
        contains_hidden_tests=True,
        contains_grader=True,
        created_by="handle",
    )
    assert pm.schema_version == "0.1"
    assert pm.contains_grader is True


def test_private_manifest_verification_state_default() -> None:
    pm = PrivateManifest(
        assignment_slug="linked-list-insertion",
        solution_path="solutions/linked-list-insertion",
        hidden_tests_path="hidden-tests/linked-list-insertion",
        grader_path="grader/linked-list-insertion",
        has_solution=True,
        has_hidden_tests=False,
    )
    assert pm.verification_state == "unverified"


def test_manifest_course_is_optional() -> None:
    m = _sample_manifest()
    assert m.classification.course is None
