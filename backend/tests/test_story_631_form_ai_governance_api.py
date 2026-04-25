from modules.form_ai import router as form_ai_router
from modules.form_ai.schemas import (
    AttemptTraceEntry,
    AttemptValidationSummary,
    FormAiGenerateResponse,
    GenerationTraceMetadata,
)


def _build_response_with_governance_source(source: str, status: str = "completed") -> FormAiGenerateResponse:
    has_definition = status == "completed"
    return FormAiGenerateResponse(
        status=status,
        definitionJSON=(
            {"schemaVersion": "1.0", "pages": [{"components": []}]}
            if has_definition
            else None
        ),
        trace=GenerationTraceMetadata(
            attemptCount=1,
            maxSystemCorrectionAttempts=3,
            systemCorrectionAttemptsUsed=0,
            terminalReason=(
                "validated-success"
                if status == "completed"
                else "retry-cap-exhausted"
            ),
            attempts=[
                AttemptTraceEntry(
                    attemptNumber=1,
                    phase="initial",
                    validation=AttemptValidationSummary(
                        valid=(status == "completed"),
                        schemaErrorCount=0 if status == "completed" else 1,
                        boundaryViolationCount=0,
                        collisionCount=0,
                        errorCount=0 if status == "completed" else 1,
                    ),
                )
            ],
            validationSummary=AttemptValidationSummary(
                valid=(status == "completed"),
                schemaErrorCount=0 if status == "completed" else 1,
                boundaryViolationCount=0,
                collisionCount=0,
                errorCount=0 if status == "completed" else 1,
            ),
            resolvedOpenaiTransport="sync",
            promptTemplateVersionId=None,
            promptTemplateVersionRef=None,
            promptAssemblyProfileId=None,
            promptAssemblyProfileRef=None,
            capabilityPolicyVersionId=None,
            capabilityPolicyVersionRef=None,
            componentCapabilitySnapshotId=None,
            componentCapabilitySnapshotRef=None,
            widthClassPolicyVersionId=None,
            widthClassPolicyVersionRef=None,
            validationContractVersion=None,
            governanceResolutionSource=source,
        ),
        userMessage="ok",
        draftHasValidationIssues=(status != "completed"),
    )


def test_story_631_generate_endpoint_returns_governance_trace_fields(client, auth_headers, monkeypatch):
    captured = {}

    def fake_generate(
        prompt,
        model_override=None,
        runtime_context=None,
        openai_transport="auto",
        *,
        max_system_correction_attempts=None,
        system_prompt_addendum=None,
        db_session=None,
        actor_user_id=None,
        actor_company_id=None,
    ):
        captured["prompt"] = prompt
        captured["runtime_context"] = runtime_context
        captured["db_session"] = db_session
        captured["actor_user_id"] = actor_user_id
        captured["actor_company_id"] = actor_company_id
        captured["openai_transport"] = openai_transport
        captured["max_system_correction_attempts"] = max_system_correction_attempts
        captured["system_prompt_addendum"] = system_prompt_addendum

        return FormAiGenerateResponse(
            status="completed",
            definitionJSON={"schemaVersion": "1.0", "pages": [{"components": []}]},
            trace=GenerationTraceMetadata(
                attemptCount=1,
                maxSystemCorrectionAttempts=3,
                systemCorrectionAttemptsUsed=0,
                terminalReason="validated-success",
                attempts=[
                    AttemptTraceEntry(
                        attemptNumber=1,
                        phase="initial",
                        validation=AttemptValidationSummary(
                            valid=True,
                            schemaErrorCount=0,
                            boundaryViolationCount=0,
                            collisionCount=0,
                            errorCount=0,
                        ),
                    )
                ],
                validationSummary=AttemptValidationSummary(
                    valid=True,
                    schemaErrorCount=0,
                    boundaryViolationCount=0,
                    collisionCount=0,
                    errorCount=0,
                ),
                resolvedOpenaiTransport="sync",
                promptTemplateVersionId=1,
                promptTemplateVersionRef="1:v1",
                promptAssemblyProfileId=2,
                promptAssemblyProfileRef="default:semantic-plan",
                capabilityPolicyVersionId=3,
                capabilityPolicyVersionRef="baseline:v1",
                componentCapabilitySnapshotId=4,
                componentCapabilitySnapshotRef="snapshot-v1",
                widthClassPolicyVersionId=5,
                widthClassPolicyVersionRef="default-width:v1",
                validationContractVersion="contracts-abc123-16",
                governanceResolutionSource="db-active",
            ),
            userMessage="ok",
            draftHasValidationIssues=False,
        )

    monkeypatch.setattr(form_ai_router, "generate_form_definition", fake_generate)
    response = client.post(
        "/api/form-ai/generate",
        headers=auth_headers,
        json={
            "prompt": "Generate a lead capture form",
            "runtimeContext": {"formId": "42"},
            "openaiTransport": "sync",
            "maxSystemCorrectionAttempts": 1,
            "systemPromptAddendum": "extra guardrails",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    trace = payload["trace"]

    assert trace["governanceResolutionSource"] == "db-active"
    assert trace["promptTemplateVersionId"] == 1
    assert trace["promptAssemblyProfileId"] == 2
    assert trace["capabilityPolicyVersionId"] == 3
    assert trace["componentCapabilitySnapshotId"] == 4
    assert trace["widthClassPolicyVersionId"] == 5
    assert trace["validationContractVersion"] == "contracts-abc123-16"

    assert captured["prompt"] == "Generate a lead capture form"
    assert captured["runtime_context"] == {"formId": "42", "canvas": None, "lockedGlobals": None, "termsDefaults": None, "componentFootprints": []}
    assert captured["db_session"] is not None
    assert isinstance(captured["actor_user_id"], int)
    assert captured["actor_user_id"] > 0
    assert captured["actor_company_id"] is None
    assert captured["openai_transport"] == "sync"
    # Story 6.4 moved retry budget ownership to config.AppSetting; the request
    # field is kept for compatibility but is intentionally ignored by router.py.
    assert captured["max_system_correction_attempts"] is None
    assert captured["system_prompt_addendum"] == "extra guardrails"


def test_story_631_generate_endpoint_handles_db_empty_governance(client, auth_headers, monkeypatch):
    monkeypatch.setattr(
        form_ai_router,
        "generate_form_definition",
        lambda *args, **kwargs: _build_response_with_governance_source("db-empty", "completed"),
    )

    response = client.post(
        "/api/form-ai/generate",
        headers=auth_headers,
        json={"prompt": "Generate a form"},
    )

    assert response.status_code == 200
    trace = response.json()["trace"]
    assert trace["governanceResolutionSource"] == "db-empty"
    assert trace["promptTemplateVersionId"] is None
    assert trace["validationContractVersion"] is None


def test_story_631_generate_endpoint_handles_db_resolution_error_governance(
    client, auth_headers, monkeypatch
):
    monkeypatch.setattr(
        form_ai_router,
        "generate_form_definition",
        lambda *args, **kwargs: _build_response_with_governance_source(
            "db-resolution-error", "failed"
        ),
    )

    response = client.post(
        "/api/form-ai/generate",
        headers=auth_headers,
        json={"prompt": "Generate a form"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "failed"
    assert payload["draftHasValidationIssues"] is True
    trace = payload["trace"]
    assert trace["governanceResolutionSource"] == "db-resolution-error"
    assert trace["promptTemplateVersionId"] is None
    assert trace["validationContractVersion"] is None
