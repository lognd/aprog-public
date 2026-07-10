from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from aprog.constants import SCHEMA_VERSION


class ManifestAssignment(BaseModel):
    slug: str
    name: str
    author: str
    description: str


class ManifestClassification(BaseModel):
    language: str
    difficulty: str
    topics: list[str]
    course: Optional[str] = None


class ManifestTemplate(BaseModel):
    slug: str
    version: str = ""


class ManifestPaths(BaseModel):
    assignment_root: str
    readme: str
    visible_tests: str


class AssignmentManifest(BaseModel):
    schema_version: str = SCHEMA_VERSION
    assignment: ManifestAssignment
    classification: ManifestClassification
    template: ManifestTemplate
    paths: ManifestPaths
    state: str = "draft"
    source_hash: str = ""


class PrivateManifest(BaseModel):
    schema_version: str = SCHEMA_VERSION
    assignment_slug: str
    solution_path: str
    hidden_tests_path: str
    grader_path: str
    has_solution: bool
    has_hidden_tests: bool
    private_source_hash: str = ""
    verification_state: str = "unverified"


class PackageManifest(BaseModel):
    schema_version: str = SCHEMA_VERSION
    assignment_slug: str
    contains_solution: bool
    contains_hidden_tests: bool
    contains_grader: bool
    created_by: str = ""
