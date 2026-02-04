"""
Public Form Submission Schemas (Story 3.11)
Public endpoint: POST /api/public/forms/{token}/submissions
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, Literal


class PublicSubmissionContext(BaseModel):
    client_device_id: str = Field(..., alias="clientDeviceId")
    client_session_id: str = Field(..., alias="clientSessionId")
    submit_attempt_id: str = Field(..., alias="submitAttemptId")

    class Config:
        populate_by_name = True
        extra = "allow"


class PublicFormSubmissionRequest(BaseModel):
    idempotency_key: str = Field(..., alias="idempotencyKey")
    submitted_at_client: str = Field(..., alias="submittedAtClient")
    answers_by_component_id: Dict[str, Any] = Field(..., alias="answersByComponentId")
    context: PublicSubmissionContext = Field(..., alias="context")

    class Config:
        populate_by_name = True


class PublicFormSubmissionResponse(BaseModel):
    submission_id: int = Field(..., alias="submissionId")
    status: Literal["ACCEPTED", "DUPLICATE"] = Field(..., alias="status")

    class Config:
        populate_by_name = True
