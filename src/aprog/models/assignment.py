from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from aprog.boundary import RESERVED_SLUGS, SLUG_RE

_VISIBILITY_VALUES = frozenset(
    {"visible", "hidden", "after_due_date", "after_published"}
)


class AssignmentSection(BaseModel):
    slug: str
    name: str
    author: str
    description: str
    version: str = "0.1.0"
    status: str = "draft"

    @field_validator("slug")
    @classmethod
    def slug_is_valid(cls, v: str) -> str:
        if not SLUG_RE.match(v):
            raise ValueError(f"slug must be kebab-case, got {v!r}")
        if v in RESERVED_SLUGS:
            raise ValueError(f"slug {v!r} is a reserved name")
        return v

    @field_validator("status")
    @classmethod
    def status_is_valid(cls, v: str) -> str:
        allowed = {"draft", "published"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}, got {v!r}")
        return v


class ClassificationSection(BaseModel):
    language: str
    difficulty: str
    topics: list[str] = Field(min_length=1)
    concepts: list[str] = Field(default_factory=list)
    labels: list[str] = Field(default_factory=list)
    course: Optional[str] = None
    module: Optional[str] = None


class TemplateSection(BaseModel):
    slug: str
    version: str = ""


class GraderDependencies(BaseModel):
    lograder: str = ""
    extra: list[str] = Field(default_factory=list)
    system: list[str] = Field(default_factory=list)


class GraderSection(BaseModel):
    visibility: str = "after_due_date"
    stdout_visibility: str = "after_due_date"
    dependencies: GraderDependencies = Field(default_factory=GraderDependencies)

    @field_validator("visibility", "stdout_visibility")
    @classmethod
    def visibility_is_valid(cls, v: str) -> str:
        if v not in _VISIBILITY_VALUES:
            raise ValueError(
                f"visibility must be one of {_VISIBILITY_VALUES}, got {v!r}"
            )
        return v


class AssignmentConfig(BaseModel):
    assignment: AssignmentSection
    classification: ClassificationSection
    template: TemplateSection
    grader: GraderSection = Field(default_factory=GraderSection)
