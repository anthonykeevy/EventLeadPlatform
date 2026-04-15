from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class FormAiGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=4000)
    runtimeContext: Optional["FormAiRuntimeContext"] = None
    maxSystemCorrectionAttempts: Optional[int] = Field(
        default=None,
        ge=0,
        le=10,
        description=(
            "Cap on correction rounds after initial generation. "
            "None uses server default."
        ),
    )


class FormAiRuntimeComponentFootprint(BaseModel):
    componentType: str = Field(..., min_length=1)
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    recommendedGapAfter: Optional[float] = Field(default=None, ge=0)


class FormAiRuntimeCanvasContext(BaseModel):
    width: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    gridSize: Optional[float] = Field(default=None, gt=0)


class FormAiRuntimeTermsDefaults(BaseModel):
    companyId: Optional[int] = None
    hasCompanyTerms: Optional[bool] = None
    defaultTermsAssetId: Optional[int] = None
    source: Optional[Literal["form-existing", "company-default", "none"]] = None
    termsLinkText: Optional[str] = None
    termsUrl: Optional[str] = None
    termsDisplayMode: Optional[Literal["popup", "new_tab"]] = None
    preserveCompanyTermsLink: Optional[bool] = None


class FormAiRuntimeEventInformation(BaseModel):
    """Factual event metadata from the builder host form (optional UI toggle)."""

    eventId: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
    startDateTime: Optional[str] = None
    endDateTime: Optional[str] = None
    timezoneIdentifier: Optional[str] = None
    venueName: Optional[str] = None
    venueAddress: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    shortDescription: Optional[str] = None


class FormAiRuntimeContext(BaseModel):
    formId: Optional[str] = None
    canvasSettings: Optional[FormAiRuntimeCanvasContext] = None
    globalStylesLocked: Optional[bool] = True
    globalStyles: Optional[Dict[str, Any]] = None
    theme: Optional[Dict[str, Any]] = None
    termsDefaults: Optional[FormAiRuntimeTermsDefaults] = None
    componentFootprints: List[FormAiRuntimeComponentFootprint] = Field(default_factory=list)
    eventInformation: Optional[FormAiRuntimeEventInformation] = None


class AttemptValidationSummary(BaseModel):
    valid: bool
    schemaErrorCount: int
    boundaryViolationCount: int
    collisionCount: int
    errorCount: int


class PostProcessingComponentPositionDelta(BaseModel):
    componentId: str
    componentType: Optional[str] = None
    before: Dict[str, float]
    after: Dict[str, float]


class PostProcessingSummary(BaseModel):
    changedComponentCount: int = Field(default=0, ge=0)
    changedComponents: List[PostProcessingComponentPositionDelta] = Field(
        default_factory=list
    )
    canvasHeightBefore: Optional[float] = None
    canvasHeightAfter: Optional[float] = None
    canvasHeightChanged: bool = False


class AttemptTraceEntry(BaseModel):
    attemptNumber: int = Field(..., ge=1)
    phase: Literal["initial", "correction"]
    validation: AttemptValidationSummary
    correctionIssued: bool = False
    notes: Optional[str] = None
    postProcessing: Optional[PostProcessingSummary] = None


class GenerationTraceMetadata(BaseModel):
    attemptCount: int = Field(..., ge=0)
    maxSystemCorrectionAttempts: int = Field(..., ge=0)
    systemCorrectionAttemptsUsed: int = Field(..., ge=0)
    terminalReason: str
    attempts: List[AttemptTraceEntry]
    validationSummary: Optional[AttemptValidationSummary] = None
    postProcessingSummary: Optional[PostProcessingSummary] = None


class FormAiGenerateResponse(BaseModel):
    status: Literal["completed", "failed"]
    definitionJSON: Optional[Dict[str, Any]] = None
    trace: GenerationTraceMetadata
    userMessage: str
    draftHasValidationIssues: bool = False


FormAiGenerateRequest.model_rebuild()
