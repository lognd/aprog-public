from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class LanguageEntry(BaseModel):
    name: str


class DifficultyEntry(BaseModel):
    name: str
    rank: int


class TopicEntry(BaseModel):
    name: str


class ConceptEntry(BaseModel):
    name: str


class LabelEntry(BaseModel):
    name: str
    description: str = ""


class ClassificationConfig(BaseModel):
    languages: dict[str, LanguageEntry] = Field(default_factory=dict)
    difficulties: dict[str, DifficultyEntry] = Field(default_factory=dict)
    topics: dict[str, TopicEntry] = Field(default_factory=dict)
    concepts: dict[str, ConceptEntry] = Field(default_factory=dict)


class OrganizationConfig(BaseModel):
    require_encryption: bool = False
    require_hidden_tests: bool = True
    default_grader_visibility: str = "after_due_date"


class RootConfig(BaseModel):
    classification: ClassificationConfig = Field(default_factory=ClassificationConfig)
    labels: dict[str, LabelEntry] = Field(default_factory=dict)
    organization: OrganizationConfig = Field(default_factory=OrganizationConfig)
