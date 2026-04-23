from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class FormAiGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=4000)
    runtimeContext: Optional["FormAiRuntimeContext"] = None
    openaiTransport: Literal["auto", "sync", "stream"] = Field(
        default="auto",
        description=(
            "How outbound OpenAI calls are made: sync (single HTTP response), "
            "stream (SSE), or auto (FORM_AI_OPENAI_TRANSPORT env, default sync)."
        ),
    )
    maxSystemCorrectionAttempts: Optional[int] = Field(
        default=None,
        ge=0,
        le=10,
        description=(
            "Cap on validator-driven correction rounds after the initial model response. "
            "None = server default (3). Use 0 to evaluate only the first model reply."
        ),
    )
    systemPromptAddendum: Optional[str] = Field(
        default=None,
        max_length=12000,
        description=(
            "Extra instructions appended to the system message (context pack + runtime). "
            "Does not change the user message. For first-shot tuning experiments."
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


class SemanticPlanViolation(BaseModel):
    """One rule violation surfaced by the pre-compile semantic-validation gate.

    Story 6.3.1 (failure-mode separation): violations here are LLM-fault and
    are converted into a correction message the LLM is expected to act on.
    """

    code: Literal[
        "empty-plan",
        "unknown-component-type",
        "width-intent-not-allowed",
        "missing-options-for-choice",
        "invalid-validation-rule",
        "duplicate-component-id",
    ]
    componentIndex: Optional[int] = Field(
        default=None,
        ge=0,
        description="0-based index into FormSemanticPlan.components when the violation is component-scoped.",
    )
    componentId: Optional[str] = None
    componentType: Optional[str] = None
    message: str
    suggestion: Optional[str] = Field(
        default=None,
        description="Concrete corrective hint the LLM can act on (e.g. allowed widthIntents).",
    )


class AttemptTraceEntry(BaseModel):
    attemptNumber: int = Field(..., ge=1)
    phase: Literal["initial", "correction"]
    validation: AttemptValidationSummary
    correctionIssued: bool = False
    notes: Optional[str] = None
    collisionDeltaFromPrevious: Optional[int] = Field(
        default=None,
        description=(
            "This attempt's collisionCount minus the previous attempt's; "
            "None on the first attempt. Negative means fewer collisions (improvement)."
        ),
    )
    collisionTrendVsPrevious: Optional[Literal["improved", "worse", "unchanged", "n_a"]] = Field(
        default=None,
        description="Compared to the prior attempt's collision count; n_a on the first attempt.",
    )
    compileDiagnostics: Optional[Dict[str, Any]] = None
    failedAt: Optional[
        Literal[
            "json-parse",
            "semantic-plan",
            "semantic-rules",
            "compile",
            "compile-validation",
            "none",
        ]
    ] = Field(
        default="none",
        description=(
            "Which pipeline stage rejected this attempt. 'none' for successful attempts. "
            "Story 6.3.1 (failure-mode separation): lets dashboards distinguish "
            "LLM-fault stages (json-parse, semantic-plan, semantic-rules) from "
            "compiler-fault stages (compile, compile-validation)."
        ),
    )


class GenerationTraceMetadata(BaseModel):
    attemptCount: int = Field(..., ge=0)
    maxSystemCorrectionAttempts: int = Field(..., ge=0)
    systemCorrectionAttemptsUsed: int = Field(..., ge=0)
    terminalReason: str
    attempts: List[AttemptTraceEntry]
    validationSummary: Optional[AttemptValidationSummary] = None
    resolvedOpenaiTransport: Optional[Literal["sync", "stream"]] = Field(
        default=None,
        description="Resolved transport after applying request + FORM_AI_OPENAI_TRANSPORT.",
    )
    promptTemplateVersionId: Optional[int] = None
    promptTemplateVersionRef: Optional[str] = None
    promptAssemblyProfileId: Optional[int] = None
    promptAssemblyProfileRef: Optional[str] = None
    capabilityPolicyVersionId: Optional[int] = None
    capabilityPolicyVersionRef: Optional[str] = None
    componentCapabilitySnapshotId: Optional[int] = None
    componentCapabilitySnapshotRef: Optional[str] = None
    widthClassPolicyVersionId: Optional[int] = None
    widthClassPolicyVersionRef: Optional[str] = None
    validationContractVersion: Optional[str] = None
    governanceResolutionSource: Optional[str] = None
    compilerMode: Optional[Literal["deterministic-grid"]] = None
    compileSummary: Optional[Dict[str, Any]] = None
    failureClass: Optional[
        Literal[
            "none",
            "llm-fault",
            "compiler-fault",
            "provider-fault",
            "infrastructure-fault",
        ]
    ] = Field(
        default=None,
        description=(
            "Story 6.3.1 (failure-mode separation): coarse classification of the "
            "terminal outcome derived from terminalReason. 'none' for successful "
            "runs. LLM-fault means the model emitted something we asked it to fix; "
            "compiler-fault means our deterministic pipeline produced an invalid "
            "definition (not the user's prompt's fault)."
        ),
    )
    semanticValidationViolations: Optional[List[SemanticPlanViolation]] = Field(
        default=None,
        description=(
            "Last attempt's semantic-validation gate violations, surfaced for triage. "
            "None when the last attempt did not exercise the gate."
        ),
    )


class FormAiGenerateResponse(BaseModel):
    status: Literal["completed", "failed"]
    definitionJSON: Optional[Dict[str, Any]] = None
    trace: GenerationTraceMetadata
    userMessage: str
    draftHasValidationIssues: bool = False
    # Story 6.3.1 UAT round 5 — render-then-measure handle. Frontends that
    # support the second pass POST to ``/remeasure`` with this run id + DOM
    # heights to receive a refined definition. Older frontends ignore it
    # entirely and keep using ``definitionJSON`` from the first pass.
    generationRunId: Optional[int] = Field(
        default=None,
        description=(
            "Server-side id of the GenerationRun row that produced this "
            "response. Required for the second-pass /remeasure call."
        ),
    )


# --- Story 6.3.1 UAT round 5 — render-then-measure schemas ----------------


class FormAiComponentMeasurement(BaseModel):
    """One DOM-measured component height collected by the frontend after it
    rendered the first-pass ``definitionJSON``.

    The frontend only sends ``height`` because the deterministic compiler
    owns ``width`` (canvas-relative tier widths it picked itself); width
    measurements would just round-trip the same number. Heights, by contrast,
    depend on rendered text wrapping, option counts, validation chrome, and
    custom themes — all things the compiler cannot predict perfectly from
    the semantic plan alone.
    """

    componentId: str = Field(..., min_length=1)
    height: float = Field(
        ...,
        gt=0,
        description=(
            "Rendered height in CSS pixels measured from the live canvas DOM "
            "(e.g. ``element.getBoundingClientRect().height`` divided by the "
            "current zoom scale). Compiler ceil()s to the nearest integer."
        ),
    )


class FormAiRemeasureRequest(BaseModel):
    """POST body for ``/api/form-ai/remeasure``.

    The endpoint re-runs the deterministic compiler against the same semantic
    plan + governance that produced ``generationRunId`` (loaded from the
    persisted artifacts), but this time forces each measured component to
    use the supplied DOM-rendered height. The output is a refined
    ``DefinitionJSON`` that exactly matches what the renderer is going to
    paint — eliminating compiler-vs-validator height mismatches that today
    surface as "1 collision detected" failures on otherwise-clean forms.
    """

    generationRunId: int = Field(
        ...,
        gt=0,
        description=(
            "GenerationRunID returned by the original /generate response. "
            "Used to load the original semantic plan + governance snapshot."
        ),
    )
    measurements: List[FormAiComponentMeasurement] = Field(
        ...,
        min_length=1,
        description=(
            "DOM heights for every component the frontend rendered. "
            "Components missing from the list fall back to the per-type "
            "estimate (so partial measurements still produce a usable "
            "definition — see compileSummary.heightsSource = \"mixed\")."
        ),
    )
    runtimeContext: Optional["FormAiRuntimeContext"] = Field(
        default=None,
        description=(
            "Same canvas / footprint / theme runtime context the frontend "
            "supplied to /generate. Re-sending it (rather than persisting "
            "and reloading from the run row) keeps the second pass aligned "
            "with the *current* canvas size, which matters when the user "
            "switches between desktop/tablet/mobile preview modes after "
            "generating but before the measurement pass completes."
        ),
    )


class FormAiRemeasureResponse(BaseModel):
    """Response envelope for ``/api/form-ai/remeasure``.

    Mirrors the shape of ``FormAiGenerateResponse`` so the frontend can swap
    the painted definition with no extra branching, but trace metadata is
    intentionally lighter — there's no LLM call on this path so retries,
    semantic violations, and provider transport are all N/A.
    """

    status: Literal["completed", "failed"]
    definitionJSON: Optional[Dict[str, Any]] = None
    compileSummary: Optional[Dict[str, Any]] = None
    validationSummary: Optional[AttemptValidationSummary] = None
    userMessage: str
    # Same generationRunId the request came in with, echoed back so the
    # frontend can correlate logs.
    generationRunId: int


_VALIDATION_TAG_ALIASES = {
    "required": "required",
    "is_required": "required",
    "isrequired": "required",
    "mandatory": "required",
    "email": "email",
    "isemail": "email",
    "is_email": "email",
    "phone": "phone",
    "telephone": "phone",
    "isphone": "phone",
    "is_phone": "phone",
    "url": "url",
    "link": "url",
    "isurl": "url",
    "is_url": "url",
}


class SemanticValidationIntent(BaseModel):
    required: Optional[bool] = None
    email: Optional[bool] = None
    phone: Optional[bool] = None
    url: Optional[bool] = None
    minLength: Optional[int] = None
    maxLength: Optional[int] = None
    min: Optional[float] = None
    max: Optional[float] = None
    pattern: Optional[str] = None

    model_config = {"extra": "allow"}

    @model_validator(mode="before")
    @classmethod
    def _coerce_loose_shapes(cls, value: Any) -> Any:
        # Tolerate the two shapes the LLM commonly emits:
        #   ["required", "email"]                    -> {"required": True, "email": True}
        #   {"required": true, "format": "email"}    -> also map format alias to email/url/phone
        if isinstance(value, list):
            coerced: Dict[str, Any] = {}
            for item in value:
                if not isinstance(item, str):
                    continue
                key = _VALIDATION_TAG_ALIASES.get(item.strip().lower())
                if key:
                    coerced[key] = True
            return coerced
        if isinstance(value, str):
            key = _VALIDATION_TAG_ALIASES.get(value.strip().lower())
            return {key: True} if key else {}
        if isinstance(value, dict):
            coerced = dict(value)
            fmt = coerced.pop("format", None)
            if isinstance(fmt, str):
                key = _VALIDATION_TAG_ALIASES.get(fmt.strip().lower())
                if key and key not in coerced:
                    coerced[key] = True
            return coerced
        return value


class SemanticComponentIntent(BaseModel):
    componentType: str = Field(..., min_length=1)
    label: Optional[str] = None
    placeholder: Optional[str] = None
    helpText: Optional[str] = None
    section: Optional[str] = None
    rowGroup: Optional[str] = None
    widthIntent: Optional[Literal["compact", "half", "full"]] = None
    actionAlignment: Optional[Literal["left", "center", "right"]] = None
    options: Optional[List[Dict[str, Any]]] = None
    validationIntent: Optional[SemanticValidationIntent] = None
    componentId: Optional[str] = None

    model_config = {"extra": "allow"}

    @field_validator("rowGroup", "section", mode="before")
    @classmethod
    def _coerce_grouping_token_to_string(cls, value: Any) -> Any:
        """Lenient coercion for ``rowGroup``/``section`` grouping tokens.

        Background: UAT round 5 (run 41) wasted attempt 1 of 3 because the LLM
        emitted ``"rowGroup": 1`` (an integer) for every component. The strict
        ``Optional[str]`` schema rejected the whole plan and forced a full
        correction round trip. The role of these fields is purely to *group*
        components — the literal value is opaque, only equality matters — so
        accepting integer/float tokens (and stringifying them) costs us nothing
        and saves a retry on a very common LLM type-juggling mistake.

        Coercion rules:
          * ``None`` -> ``None`` (untouched; the field is optional).
          * ``str``  -> stripped; empty string becomes ``None``.
          * ``int`` / ``float`` -> stringified (``1`` -> ``"1"``,
            ``1.0`` -> ``"1.0"``); ``bool`` is intentionally rejected because
            ``isinstance(True, int)`` would otherwise turn ``rowGroup: true``
            into ``"True"`` which is almost certainly not what the LLM meant.
          * Anything else -> returned unchanged so Pydantic raises the
            normal validation error (lists/dicts are real bugs we want to see).
        """
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            stripped = value.strip()
            return stripped or None
        if isinstance(value, (int, float)):
            return str(value)
        return value


class FormSemanticPlan(BaseModel):
    semanticPlanVersion: Literal["1.0"] = "1.0"
    formId: Optional[str] = None
    title: Optional[str] = None
    components: List[SemanticComponentIntent] = Field(default_factory=list)
    notes: Optional[str] = None

    model_config = {"extra": "ignore"}

    @model_validator(mode="before")
    @classmethod
    def _normalise_root(cls, value: Any) -> Any:
        # Be tolerant of LLM drift: any non-"1.0" semanticPlanVersion (e.g. "6.3.1",
        # the story number it copied from the system prompt) is normalised to "1.0".
        # Also accept legacy keys: "fields" / "items" as aliases for "components".
        if not isinstance(value, dict):
            return value
        normalised = dict(value)
        version = normalised.get("semanticPlanVersion")
        if version is None or (isinstance(version, str) and version.strip() != "1.0"):
            normalised["semanticPlanVersion"] = "1.0"
        if "components" not in normalised:
            for alias in ("fields", "items", "elements"):
                if alias in normalised and isinstance(normalised[alias], list):
                    normalised["components"] = normalised.pop(alias)
                    break
        return normalised


# Resolve forward references after all models are declared. ``FormAiRuntime*``
# classes are defined below ``FormAiGenerateRequest`` / ``FormAiRemeasureRequest``
# in source order, so the forward refs need to be re-resolved here.
FormAiGenerateRequest.model_rebuild()
FormAiRemeasureRequest.model_rebuild()
