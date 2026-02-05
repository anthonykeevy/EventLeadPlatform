"""
Public Submission Schemas (Story 3.11)

Contracts only (Task T01):
- POST /api/public/forms/{token}/submissions
- POST /api/public/forms/{token}/telemetry/validation

Routers / persistence are implemented in later tasks (T03, T07).
"""

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Literal, Optional, Union


class PublicSchemaBase(BaseModel):
    class Config:
        populate_by_name = True


class PublicClientScreen(PublicSchemaBase):
    width: int
    height: int
    dpr: Optional[float] = None


class PublicClientViewport(PublicSchemaBase):
    width: int
    height: int


class PublicSubmissionContext(PublicSchemaBase):
    client_device_id: str = Field(..., alias="clientDeviceId")
    client_session_id: str = Field(..., alias="clientSessionId")
    submit_attempt_id: str = Field(..., alias="submitAttemptId")
    client_timezone: Optional[str] = Field(None, alias="clientTimezone")
    client_locale: Optional[str] = Field(None, alias="clientLocale")
    client_user_agent: Optional[str] = Field(None, alias="clientUserAgent")
    client_screen: Optional[PublicClientScreen] = Field(None, alias="clientScreen")
    client_viewport: Optional[PublicClientViewport] = Field(None, alias="clientViewport")
    render_canvas_width: Optional[int] = Field(None, alias="renderCanvasWidth")
    render_canvas_height: Optional[int] = Field(None, alias="renderCanvasHeight")
    render_scale_at_submit: Optional[float] = Field(None, alias="renderScaleAtSubmit")
    client_online_at_submit: Optional[bool] = Field(None, alias="clientOnlineAtSubmit")
    effective_connection_type: Optional[str] = Field(None, alias="effectiveConnectionType")
    max_touch_points: Optional[int] = Field(None, alias="maxTouchPoints")
    client_orientation: Optional[str] = Field(None, alias="clientOrientation")
    prefers_color_scheme: Optional[str] = Field(None, alias="prefersColorScheme")
    prefers_reduced_motion: Optional[bool] = Field(None, alias="prefersReducedMotion")
    device_memory_gb: Optional[float] = Field(None, alias="deviceMemoryGb")
    hardware_concurrency: Optional[int] = Field(None, alias="hardwareConcurrency")
    supports_indexed_db: Optional[bool] = Field(None, alias="supportsIndexedDB")
    supports_service_worker: Optional[bool] = Field(None, alias="supportsServiceWorker")
    storage_quota_mb: Optional[float] = Field(None, alias="storageQuotaMb")
    storage_usage_mb: Optional[float] = Field(None, alias="storageUsageMb")
    app_version: Optional[str] = Field(None, alias="appVersion")
    build_sha: Optional[str] = Field(None, alias="buildSha")
    ip_country_code: Optional[str] = Field(None, alias="ipCountryCode")


class PublicFormSubmissionRequest(PublicSchemaBase):
    idempotency_key: str = Field(..., alias="idempotencyKey")
    submitted_at_client: str = Field(..., alias="submittedAtClient")
    answers_by_component_id: Dict[str, Any] = Field(..., alias="answersByComponentId")
    context: PublicSubmissionContext


class PublicFormSubmissionResponse(PublicSchemaBase):
    submission_id: Union[int, str] = Field(..., alias="submissionId")
    status: Literal["ACCEPTED", "DUPLICATE"]


PublicSubmissionLinkType = Literal["PREVIEW", "PRODUCTION"]

ValueDiagnosticsType = Literal["null", "string", "number", "boolean", "array", "object", "unknown"]
DigitCountBucket = Literal["0", "1-3", "4-7", "8-12", "13+"]


class PublicValueDiagnosticsFlags(PublicSchemaBase):
    has_whitespace: Optional[bool] = Field(None, alias="hasWhitespace")
    has_plus: Optional[bool] = Field(None, alias="hasPlus")
    digit_count_bucket: Optional[DigitCountBucket] = Field(None, alias="digitCountBucket")


class PublicValueDiagnostics(PublicSchemaBase):
    value_type: ValueDiagnosticsType = Field(..., alias="type")
    length: Optional[int] = None
    trimmed_length: Optional[int] = Field(None, alias="trimmedLength")
    flags: Optional[PublicValueDiagnosticsFlags] = None


PublicValidationErrorCategory = Literal[
    "required",
    "min",
    "max",
    "pattern",
    "range",
    "custom",
    "unknown",
]


class PublicValidationFailure(PublicSchemaBase):
    component_id: str = Field(..., alias="componentId")
    component_type: str = Field(..., alias="componentType")
    rule_id: Optional[str] = Field(None, alias="ruleId")
    rule_type: Optional[str] = Field(None, alias="ruleType")
    rule_code: Optional[str] = Field(None, alias="ruleCode")
    error_category: Optional[PublicValidationErrorCategory] = Field(None, alias="errorCategory")
    value_diagnostics: Optional[PublicValueDiagnostics] = Field(None, alias="valueDiagnostics")


class PublicValidationEventRequest(PublicSchemaBase):
    event_type: Literal["validation_failed_submit"] = Field(..., alias="eventType")
    occurred_at_client: str = Field(..., alias="occurredAtClient")
    link_type: Optional[PublicSubmissionLinkType] = Field(None, alias="linkType")
    client_device_id: str = Field(..., alias="clientDeviceId")
    client_session_id: str = Field(..., alias="clientSessionId")
    submit_attempt_id: str = Field(..., alias="submitAttemptId")
    failures: List[PublicValidationFailure]
