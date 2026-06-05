from __future__ import annotations

from pydantic import BaseModel, Field


class TemplateClassification(BaseModel):
    language: str
    default_difficulty: str = "medium"
    recommended_topics: list[str] = Field(default_factory=list)


class PublicOutputs(BaseModel):
    assignment_toml: bool = True
    readme: bool = True
    visible_tests: bool = True
    expected: bool = True
    assets: bool = True


class PrivateOutputs(BaseModel):
    solution: bool = True
    hidden_tests: bool = True
    grader: bool = True


class Outputs(BaseModel):
    public: PublicOutputs = Field(default_factory=PublicOutputs)
    private: PrivateOutputs = Field(default_factory=PrivateOutputs)


class TemplateVariables(BaseModel):
    requires_problem_statement: bool = True
    requires_examples: bool = True


class TemplateConfig(BaseModel):
    template: "TemplateSection"
    classification: TemplateClassification
    outputs: Outputs = Field(default_factory=Outputs)
    variables: TemplateVariables = Field(default_factory=TemplateVariables)


class TemplateSection(BaseModel):
    slug: str
    name: str
    version: str = "0.1"
    description: str = ""
