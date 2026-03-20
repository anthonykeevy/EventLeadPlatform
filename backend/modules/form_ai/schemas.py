from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class FormAiGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=4000)
    runtimeContext: Optional["FormAiRuntimeContext"] = None


class FormAiRuntimeComponentFootprint(BaseModel):
    componentType: str = Field(..., min_length=1)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    recommendedGapAfter: Optional[float] = Field(default=None, ge=0)


class FormAiRuntimeCanvasContext(BaseModel):
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    gridSize: Optional[float] = Field(default=None, gt=0)


class FormAiRuntimeLockedGlobals(BaseModel):
    theme: Optional[Dict[str, Any]] = None
    globalStyles: Optional[Dict[str, Any]] = None
    canvasSettings: Optional[Dict[str, Any]] = None


class FormAiRuntimeTermsDefaults(BaseModel):
    companyId: Optional[int] = None
    hasCompanyTerms: Optional[bool] = None
    defaultTermsAssetId: Optional[int] = None
    source: Optional[Literal["form-existing", "company-default", "none"]] = None
    termsLinkText: Optional[str] = None
    termsUrl: Optional[str] = None
    termsDisplayMode: Optional[Literal["popup", "new_tab"]] = None
    preserveCompanyTermsLink: Optional[bool] = None


class FormAiRuntimeContext(BaseModel):
    formId: Optional[str] = None
    canvas: Optional[FormAiRuntimeCanvasContext] = None
    lockedGlobals: Optional[FormAiRuntimeLockedGlobals] = None
    termsDefaults: Optional[FormAiRuntimeTermsDefaults] = None
    componentFootprints: List[FormAiRuntimeComponentFootprint] = Field(default_factory=list)


class AttemptValidationSummary(BaseModel):
    valid: bool
    schemaErrorCount: int
    boundaryViolationCount: int
    collisionCount: int
    errorCount: int


class AttemptTraceEntry(BaseModel):
    attemptNumber: int = Field(..., ge=1)
    phase: Literal["initial", "correction"]
    validation: AttemptValidationSummary
    correctionIssued: bool = False
    notes: Optional[str] = None


class GenerationTraceMetadata(BaseModel):
    attemptCount: int = Field(..., ge=0)
    maxSystemCorrectionAttempts: int = Field(..., ge=0)
    systemCorrectionAttemptsUsed: int = Field(..., ge=0)
    terminalReason: str
    attempts: List[AttemptTraceEntry]
    validationSummary: Optional[AttemptValidationSummary] = None


class FormAiGenerateResponse(BaseModel):
    status: Literal["completed", "failed"]
    definitionJSON: Optional[Dict[str, Any]] = None
    trace: GenerationTraceMetadata
    userMessage: str


FormAiGenerateRequest.model_rebuild()
