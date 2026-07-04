"""Core MVP domain models.

These models intentionally follow the founding docs' narrow MVP contract:
window-scoped artifacts, evidence, claims, warrants, contradictions, abstentions,
and open questions. Broader ontology can be admitted later when construction
rules and query value are proven.
"""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CodeLoreModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class WindowType(StrEnum):
    RELEASE = "release"
    COMMIT_RANGE = "commit_range"
    DATE_RANGE = "date_range"


class ScopeType(StrEnum):
    CANONICAL = "canonical"
    WINDOW = "window"


class ArtifactType(StrEnum):
    RELEASE = "release"
    TAG = "tag"
    COMMIT = "commit"
    DIFF = "diff"
    PULL_REQUEST = "pull_request"
    ISSUE = "issue"
    COMMENT = "comment"
    RELEASE_NOTE = "release_note"
    DOC_CHANGE = "doc_change"
    TEST_CHANGE = "test_change"
    ADR = "adr"


class LocatorType(StrEnum):
    GIT_COMMIT = "git_commit"
    GIT_COMMIT_MESSAGE = "git_commit_message"
    DIFF_HUNK = "diff_hunk"
    PR_BODY = "pr_body"
    ISSUE_BODY = "issue_body"
    COMMENT_BODY = "comment_body"
    MARKDOWN_SECTION = "markdown_section"
    ADR_SECTION = "adr_section"
    RELEASE_NOTE_SECTION = "release_note_section"
    FILE_PATH = "file_path"
    TAG_REF = "tag_ref"


class EvidenceType(StrEnum):
    TEXT_SPAN = "text_span"
    STRUCTURAL_RELATION = "structural_relation"
    DIFF_HUNK = "diff_hunk"
    ARTIFACT_REFERENCE = "artifact_reference"


class ClaimType(StrEnum):
    ARTIFACT_LINK = "artifact_link"
    CHANGE_FACT = "change_fact"
    EXPLICIT_PROBLEM = "explicit_problem"
    EXPLICIT_DECISION = "explicit_decision"
    NARROW_INFERENCE = "narrow_inference"


class ClaimStatus(StrEnum):
    SUPPORTED = "supported"
    CONTESTED = "contested"
    INSUFFICIENT = "insufficient"
    ABSTAINED = "abstained"


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class WarrantType(StrEnum):
    EXPLICIT_STATEMENT = "explicit_statement"
    STRUCTURAL_MEMBERSHIP = "structural_membership"
    CROSS_ARTIFACT_CORROBORATION = "cross_artifact_corroboration"
    BEHAVIOR_GUARD_INFERENCE = "behavior_guard_inference"
    RELEASE_INCLUSION = "release_inclusion"


class AbstentionReason(StrEnum):
    NO_EVIDENCE = "no_evidence"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    UNSUPPORTED_INFERENCE = "unsupported_inference"


class SubjectRef(CodeLoreModel):
    subject_kind: Literal["window", "artifact", "file", "module", "test", "release"]
    subject_id: str


class Project(CodeLoreModel):
    project_id: str
    name: str
    repo_url: str | None = None
    default_branch: str | None = None
    hosting_provider: str | None = None


class ChangeWindow(CodeLoreModel):
    window_id: str
    window_type: WindowType
    label: str
    project_id: str
    start_ref: str | None = None
    end_ref: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    build_status: str | None = None


class ArtifactRecord(CodeLoreModel):
    artifact_record_id: str
    scope_type: ScopeType = ScopeType.WINDOW
    artifact_type: ArtifactType
    locator_type: LocatorType
    source_locator: str
    window_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_system: str | None = None
    native_id: str | None = None
    captured_at: datetime | None = None
    normalized_by: str | None = None
    checksum: str | None = None
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)


class Evidence(CodeLoreModel):
    evidence_id: str
    scope_type: ScopeType = ScopeType.WINDOW
    evidence_type: EvidenceType
    artifact_record_id: str
    window_id: str
    source_ref: str | None = None
    span_start: int | None = None
    span_end: int | None = None
    excerpt: str | None = None
    capture_method: str | None = None
    evidence_role: str | None = None


class Warrant(CodeLoreModel):
    warrant_id: str
    scope_type: ScopeType = ScopeType.WINDOW
    warrant_type: WarrantType
    claim_id: str
    rule_name: str
    rule_text: str
    supporting_artifact_ids: tuple[str, ...]
    counterevidence_ids: tuple[str, ...] = Field(default_factory=tuple)
    limitations: str | None = None


class Claim(CodeLoreModel):
    claim_id: str
    scope_type: ScopeType = ScopeType.WINDOW
    window_id: str
    claim_type: ClaimType
    statement: str
    subject_refs: tuple[SubjectRef, ...]
    evidence_ids: tuple[str, ...]
    warrant_ids: tuple[str, ...]
    confidence: Confidence
    status: ClaimStatus
    claim_priority: int | None = None


class Contradiction(CodeLoreModel):
    contradiction_id: str
    scope_type: ScopeType = ScopeType.WINDOW
    window_id: str
    summary: str
    evidence_ids: tuple[str, ...]
    severity: str | None = None


class Abstention(CodeLoreModel):
    abstention_id: str
    scope_type: ScopeType = ScopeType.WINDOW
    window_id: str
    reason_code: AbstentionReason
    summary: str
    evidence_ids: tuple[str, ...] = Field(default_factory=tuple)


class OpenQuestion(CodeLoreModel):
    question_id: str
    scope_type: ScopeType = ScopeType.WINDOW
    window_id: str
    question_text: str
    question_type: str | None = None
    priority: int | None = None


class EvidencePack(CodeLoreModel):
    project: Project
    window: ChangeWindow
    artifacts: tuple[ArtifactRecord, ...] = Field(default_factory=tuple)
    evidence: tuple[Evidence, ...] = Field(default_factory=tuple)
    claims: tuple[Claim, ...] = Field(default_factory=tuple)
    warrants: tuple[Warrant, ...] = Field(default_factory=tuple)
    contradictions: tuple[Contradiction, ...] = Field(default_factory=tuple)
    abstentions: tuple[Abstention, ...] = Field(default_factory=tuple)
    open_questions: tuple[OpenQuestion, ...] = Field(default_factory=tuple)
