import types
from typing import Optional

from modules.form_ai import service
from modules.form_ai.schemas import (
    AttemptTraceEntry,
    AttemptValidationSummary,
    FormAiGenerateResponse,
    GenerationTraceMetadata,
)


class _FakeResult:
    def __init__(self, *, first=None, all_rows=None, scalar_one=None, scalar_one_or_none=None):
        self._first = first
        self._all_rows = all_rows if all_rows is not None else []
        self._scalar_one = scalar_one
        self._scalar_one_or_none = scalar_one_or_none

    def mappings(self):
        return self

    def first(self):
        return self._first

    def all(self):
        return self._all_rows

    def scalar_one(self):
        return self._scalar_one

    def scalar_one_or_none(self):
        return self._scalar_one_or_none


class _FakeSession:
    def __init__(self):
        self.run_insert_params = None
        self.artifact_insert_params = []
        self.committed = False
        self.rolled_back = False

    def execute(self, statement, params=None):
        sql = " ".join(str(statement).split())

        if "FROM config.PromptTemplateVersion" in sql:
            return _FakeResult(
                first={
                    "PromptTemplateVersionID": 7,
                    "PromptTemplateID": 3,
                    "VersionNumber": 2,
                }
            )
        if "FROM config.PromptAssemblyProfile" in sql:
            return _FakeResult(
                first={
                    "PromptAssemblyProfileID": 12,
                    "ProfileKey": "default",
                    "StepName": "semantic-plan",
                }
            )
        if "FROM config.CapabilityPolicyVersion" in sql:
            return _FakeResult(
                first={
                    "CapabilityPolicyVersionID": 21,
                    "PolicyKey": "baseline",
                    "VersionNumber": 5,
                }
            )
        if "FROM config.ComponentCapabilitySnapshot" in sql:
            return _FakeResult(
                first={
                    "ComponentCapabilitySnapshotID": 33,
                    "SnapshotVersion": "snapshot-v1",
                }
            )
        if "FROM config.WidthClassPolicyVersion" in sql:
            return _FakeResult(
                first={
                    "WidthClassPolicyVersionID": 44,
                    "PolicyKey": "default-width",
                    "VersionNumber": 3,
                }
            )
        if "FROM config.ComponentValidationContract" in sql:
            return _FakeResult(
                all_rows=[
                    {"ComponentType": "text", "ContractVersion": "v1"},
                    {"ComponentType": "email", "ContractVersion": "v1"},
                ]
            )

        if "SELECT TOP 1 FormID FROM dbo.Form" in sql:
            return _FakeResult(scalar_one_or_none=None)
        if "SELECT TOP 1 CompanyID FROM dbo.Company" in sql:
            return _FakeResult(scalar_one_or_none=None)
        if "INSERT INTO dbo.GenerationRun" in sql:
            self.run_insert_params = dict(params or {})
            return _FakeResult(scalar_one=9001)
        if "INSERT INTO dbo.GenerationArtifact" in sql:
            self.artifact_insert_params.append(dict(params or {}))
            return _FakeResult()

        raise AssertionError(f"Unexpected SQL in test fake: {sql}")

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


def _sample_response() -> FormAiGenerateResponse:
    trace = GenerationTraceMetadata(
        attemptCount=1,
        maxSystemCorrectionAttempts=0,
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
    )
    return FormAiGenerateResponse(
        status="completed",
        definitionJSON={"schemaVersion": "1.0", "pages": [{"components": []}]},
        trace=trace,
        userMessage="ok",
        draftHasValidationIssues=False,
    )


def test_story_631_resolves_active_governance_versions_from_db():
    fake_session = _FakeSession()

    resolved = service._resolve_runtime_governance_versions(fake_session)

    assert resolved["governanceResolutionSource"] == "db-active"
    assert resolved["promptTemplateVersionId"] == 7
    assert resolved["promptTemplateVersionRef"] == "3:v2"
    assert resolved["promptAssemblyProfileId"] == 12
    assert resolved["capabilityPolicyVersionId"] == 21
    assert resolved["componentCapabilitySnapshotId"] == 33
    assert resolved["widthClassPolicyVersionId"] == 44
    assert resolved["validationContractVersion"] is not None
    assert resolved["validationContractVersion"].startswith("contracts-")


def test_story_631_persists_generation_artifacts_with_fk_fallbacks(monkeypatch):
    fake_session = _FakeSession()
    monkeypatch.setattr(
        service,
        "get_current_request_context",
        lambda: types.SimpleNamespace(request_id="req-123", company_id=888),
    )

    governance_versions = service._resolve_runtime_governance_versions(fake_session)
    response = _sample_response()

    service._persist_generation_run_and_artifacts(
        db_session=fake_session,
        actor_user_id=1234,
        company_id=None,
        prompt="Generate a lead form",
        runtime_context={"formId": "42"},
        response=response,
        raw_attempt_payloads=[{"attemptNumber": 1, "payload": {"raw": True}}],
        semantic_attempt_payloads=[{"attemptNumber": 1, "semanticPlan": {"ok": True}}],
        compiled_attempt_payloads=[{"attemptNumber": 1, "definition": {"ok": True}}],
        governance_versions=governance_versions,
        brand_posture="local",
        brand_heritage_origin=None,
    )

    assert fake_session.run_insert_params is not None
    assert fake_session.run_insert_params["request_id"] == "req-123"
    assert fake_session.run_insert_params["form_id"] is None
    assert fake_session.run_insert_params["company_id"] is None
    assert fake_session.run_insert_params["prompt_template_version_id"] == 7
    assert fake_session.run_insert_params["attempt_count"] == 1
    assert fake_session.run_insert_params["first_shot_valid"] is True
    assert fake_session.run_insert_params["brand_posture"] == "local"
    assert fake_session.run_insert_params["brand_heritage_origin"] is None

    assert fake_session.committed is True
    assert fake_session.rolled_back is False
    assert len(fake_session.artifact_insert_params) == 5
    assert {row["artifact_type"] for row in fake_session.artifact_insert_params} == {
        "raw-semantic-attempt",
        "semantic-plan-attempt",
        "compiled-definition-attempt",
        "trace-metadata",
        "final-definition",
    }


# Story 6.3.1 UAT round 5 — remeasure (render-then-measure) service tests.


import json as _json  # noqa: E402  (intentional late import to keep module top tidy)

from modules.form_ai.schemas import (  # noqa: E402
    FormAiComponentMeasurement,
    FormAiRemeasureRequest,
    FormSemanticPlan,
)


class _FakeRemeasureSession(_FakeSession):
    """Extends _FakeSession with the SQL surface ``remeasure_form_definition``
    needs: loading the persisted ``compile-input-plan`` artifact and
    counting prior ``remeasure-output`` rows for sequence numbering.
    """

    def __init__(self, *, compile_input_plan_envelope: Optional[dict] = None,
                 prior_remeasure_count: int = 0):
        super().__init__()
        self._compile_input_plan_envelope = compile_input_plan_envelope
        self._prior_remeasure_count = prior_remeasure_count

    def execute(self, statement, params=None):  # noqa: C901
        sql = " ".join(str(statement).split())

        # Load compile-input-plan artifact for the remeasure target run.
        if (
            "FROM dbo.GenerationArtifact" in sql
            and "compile-input-plan" in sql
        ):
            if self._compile_input_plan_envelope is None:
                return _FakeResult(first=None)
            return _FakeResult(
                first={
                    "ArtifactJson": _json.dumps(self._compile_input_plan_envelope),
                }
            )

        # Sequence number lookup for remeasure-output.
        if (
            "FROM dbo.GenerationArtifact" in sql
            and "remeasure-output" in sql
            and "COUNT(" in sql
        ):
            return _FakeResult(scalar_one=self._prior_remeasure_count)

        # Everything else (governance lookups, artifact inserts) is identical
        # to the /generate path, so reuse the parent fake.
        return super().execute(statement, params)


def _baseline_compile_input_plan_envelope() -> dict:
    """Mirror what /generate persists as a ``compile-input-plan`` artifact:
    the post-heading-filter semantic plan plus envelope metadata."""
    plan = FormSemanticPlan.model_validate(
        {
            "semanticPlanVersion": "1.0",
            "formId": "remeasure-svc-1",
            "title": "Remeasure svc test",
            "components": [
                {
                    "componentType": "header",
                    "label": "Hi",
                    "widthIntent": "full",
                    "componentId": "header-1",
                },
                {
                    "componentType": "textarea",
                    "label": "Tell us more",
                    "widthIntent": "full",
                    "componentId": "textarea-1",
                },
                {
                    "componentType": "submit-button",
                    "label": "Submit",
                    "widthIntent": "compact",
                    "actionAlignment": "center",
                    "componentId": "submit-1",
                },
            ],
        }
    )
    return {
        "attemptNumber": 1,
        "phase": "initial",
        "plan": plan.model_dump(),
        "headingsDropped": [],
    }


# Avoid the test running against the real OpenAI key path: we never call /generate,
# we hit ``remeasure_form_definition`` directly.
def test_story_631_remeasure_recompiles_with_measured_heights_and_persists_artifacts(
    monkeypatch,
):
    """Full happy path for ``remeasure_form_definition``:

      * Loads compile-input-plan envelope from the fake DB.
      * Recompiles with caller-supplied measured heights (textarea: 350px).
      * Returns a ``completed`` response carrying the refined definition.
      * Reports ``heightsSource = "mixed"`` (textarea measured, others estimated).
      * Persists exactly one ``remeasure-input`` + one ``remeasure-output``
        artifact at the next sequence number.
    """
    envelope = _baseline_compile_input_plan_envelope()
    fake_session = _FakeRemeasureSession(
        compile_input_plan_envelope=envelope, prior_remeasure_count=2
    )
    monkeypatch.setattr(
        service,
        "get_current_request_context",
        lambda: types.SimpleNamespace(request_id="req-remeasure", company_id=42),
    )

    body = FormAiRemeasureRequest(
        generationRunId=9001,
        measurements=[
            FormAiComponentMeasurement(componentId="textarea-1", height=350.0),
        ],
    )

    response = service.remeasure_form_definition(
        body,
        runtime_context={"canvas": {"width": 1200, "height": 800, "gridSize": 8}},
        db_session=fake_session,
        actor_user_id=4321,
    )

    assert response.status == "completed", response.userMessage
    assert response.definitionJSON is not None
    assert response.compileSummary is not None
    # Only the textarea was measured; header/submit fall back to estimates.
    assert response.compileSummary["heightsSource"] == "mixed"
    assert response.compileSummary["measuredComponentCount"] == 1
    assert response.compileSummary["estimatedComponentCount"] >= 2

    # Definition geometry sanity: the textarea got the measured height.
    components = response.definitionJSON["pages"][0]["components"]
    textarea = next(c for c in components if c["type"] == "textarea")
    assert textarea["style"]["height"] == 350

    # Persistence: exactly two artifacts inserted (input + output) at seq=3
    # (prior_remeasure_count=2 → next sequence is 3).
    artifact_types = [row["artifact_type"] for row in fake_session.artifact_insert_params]
    assert artifact_types == ["remeasure-input", "remeasure-output"]
    assert all(row["sequence_number"] == 3 for row in fake_session.artifact_insert_params)
    assert all(
        row["generation_run_id"] == 9001
        for row in fake_session.artifact_insert_params
    )
    assert fake_session.committed is True


def test_story_631_remeasure_returns_failed_when_no_compile_input_plan(monkeypatch):
    """Legacy runs (created before round 5 shipped) have no
    ``compile-input-plan`` artifact. ``remeasure_form_definition`` must
    return ``failed`` cleanly so the frontend keeps the first-pass
    definition — never throw, never insert anything.
    """
    fake_session = _FakeRemeasureSession(
        compile_input_plan_envelope=None, prior_remeasure_count=0
    )
    monkeypatch.setattr(
        service,
        "get_current_request_context",
        lambda: types.SimpleNamespace(request_id="req-noplan", company_id=42),
    )

    body = FormAiRemeasureRequest(
        generationRunId=8888,
        measurements=[
            FormAiComponentMeasurement(componentId="textarea-1", height=350.0),
        ],
    )

    response = service.remeasure_form_definition(
        body,
        runtime_context={"canvas": {"width": 1200, "height": 800, "gridSize": 8}},
        db_session=fake_session,
        actor_user_id=None,
    )

    assert response.status == "failed"
    assert response.definitionJSON is None
    assert response.generationRunId == 8888
    assert "first-pass layout" in response.userMessage.lower()
    # No artifacts persisted on the legacy-run fast-path.
    assert fake_session.artifact_insert_params == []
    assert fake_session.committed is False
