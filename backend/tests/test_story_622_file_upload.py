"""Story 6.2.2 — public attachment upload, submit binding, session checks, download ACL."""
import json
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from common.database import DATABASE_URL
from models.submission_attachment import SubmissionAttachment


def _mssql_without_submission_attachment_table() -> bool:
    """True → skip integration tests until revision 051 is applied on SQL Server."""
    url = (os.getenv("DATABASE_URL") or DATABASE_URL or "").strip().lower()
    if not url.startswith("mssql"):
        return False
    try:
        from sqlalchemy import inspect
        from common.database import engine

        insp = inspect(engine)
        return not insp.has_table("SubmissionAttachment", schema="dbo")
    except Exception:
        return True


skip_if_sqlserver_pending_migration = pytest.mark.skipif(
    _mssql_without_submission_attachment_table(),
    reason="SQL Server: create dbo.SubmissionAttachment with `cd backend` then `alembic upgrade head` (revision 051).",
)


def _def_with_file_upload(comp_id="fu1"):
    return {
        "schemaVersion": "1.0",
        "formId": "622-form",
        "theme": {"primaryColor": "#0055FF", "backgroundColor": "#FFFFFF", "fontFamily": "Inter"},
        "canvasSettings": {"width": 500, "height": 400, "gridSize": 8},
        "pages": [
            {
                "id": "page-1",
                "title": "Page 1",
                "components": [
                    {
                        "id": comp_id,
                        "type": "file-upload",
                        "props": {
                            "label": "Doc",
                            "maxFileSizeBytes": 5 * 1024 * 1024,
                            "allowMultiple": False,
                            "acceptedFileTypes": [".txt", "text/plain"],
                        },
                        "position": {"x": 20, "y": 20},
                        "style": {"width": 200, "height": 60},
                    }
                ],
            }
        ],
    }


@pytest.fixture
def asset_tmp(monkeypatch, tmp_path):
    monkeypatch.setenv("ASSET_STORAGE_PROVIDER", "local")
    monkeypatch.setenv("ASSET_STORAGE_LOCAL_DIR", str(tmp_path / "assets"))


def _submission_payload(*, att_id: str, session: str = "sess-a", idem: str = "idem-622-1"):
    return {
        "idempotencyKey": idem,
        "submittedAtClient": "2026-03-31T12:00:00Z",
        "answersByComponentId": {"fu1": att_id},
        "context": {
            "clientDeviceId": "dev-1",
            "clientSessionId": session,
            "submitAttemptId": "att-1",
        },
    }


def test_story_622_form_validate_accepts_file_upload(client: TestClient):
    from tests.test_story_6_1_form_validate import _valid_definition_payload

    payload = _valid_definition_payload()
    comps = payload["definition"]["pages"][0]["components"]
    comps.append(
        {
            "id": "fu-val",
            "type": "file-upload",
            "props": {"label": "Upload"},
            "position": {"x": 300, "y": 20},
            "style": {"width": 120, "height": 60},
        }
    )
    r = client.post("/api/form-validate", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["valid"] is True


@skip_if_sqlserver_pending_migration
def test_story_622_upload_submit_bind_and_download(
    client: TestClient, test_db: Session, mock_published_form, asset_tmp, admin_token_headers
):
    from models.form_version import FormVersion

    form_id = int(mock_published_form["form_id"])
    token = mock_published_form["token"]
    fv = test_db.query(FormVersion).filter(FormVersion.FormID == form_id).first()
    fv.DefinitionJSON = json.dumps(_def_with_file_upload())
    test_db.commit()

    files = {"file": ("hello.txt", b"hello-bytes-622", "text/plain")}
    data = {"componentId": "fu1", "clientSessionId": "sess-a"}
    up = client.post(f"/api/public/forms/{token}/attachments", files=files, data=data)
    assert up.status_code == 201, up.text
    att_id = up.json()["attachmentId"]
    assert up.json().get("duplicateOfExisting") is False

    sub = client.post(
        f"/api/public/forms/{token}/submissions",
        json=_submission_payload(att_id=att_id),
    )
    assert sub.status_code == 200, sub.text
    sid = sub.json()["submissionId"]

    row = test_db.query(SubmissionAttachment).filter_by(PublicAttachmentId=att_id).first()
    assert row is not None
    assert row.FormSubmissionID == sid

    dl = client.get(
        f"/api/forms/{form_id}/attachments/{att_id}/content",
        headers=admin_token_headers,
    )
    assert dl.status_code == 200
    assert dl.content == b"hello-bytes-622"


@skip_if_sqlserver_pending_migration
def test_story_622_reject_cross_session_attachment(client: TestClient, test_db: Session, mock_published_form, asset_tmp):
    from models.form_version import FormVersion

    token = mock_published_form["token"]
    form_id = int(mock_published_form["form_id"])
    fv = test_db.query(FormVersion).filter(FormVersion.FormID == form_id).first()
    fv.DefinitionJSON = json.dumps(_def_with_file_upload())
    test_db.commit()

    up = client.post(
        f"/api/public/forms/{token}/attachments",
        files={"file": ("a.txt", b"a", "text/plain")},
        data={"componentId": "fu1", "clientSessionId": "session-alpha"},
    )
    assert up.status_code == 201
    att_id = up.json()["attachmentId"]

    sub = client.post(
        f"/api/public/forms/{token}/submissions",
        json=_submission_payload(att_id=att_id, session="session-beta", idem="idem-cross"),
    )
    assert sub.status_code == 422


@skip_if_sqlserver_pending_migration
def test_story_622_dedupe_same_session_same_hash(
    client: TestClient, test_db: Session, mock_published_form, asset_tmp
):
    from models.form_version import FormVersion

    form_id = int(mock_published_form["form_id"])
    token = mock_published_form["token"]
    fv = test_db.query(FormVersion).filter(FormVersion.FormID == form_id).first()
    fv.DefinitionJSON = json.dumps(_def_with_file_upload())
    test_db.commit()

    body = b"same-content"
    data = {"componentId": "fu1", "clientSessionId": "sess-dedupe"}
    r1 = client.post(
        f"/api/public/forms/{token}/attachments",
        files={"file": ("1.txt", body, "text/plain")},
        data=data,
    )
    r2 = client.post(
        f"/api/public/forms/{token}/attachments",
        files={"file": ("2.txt", body, "text/plain")},
        data=data,
    )
    assert r1.status_code == 201 and r2.status_code == 201
    id1 = r1.json()["attachmentId"]
    id2 = r2.json()["attachmentId"]
    assert id1 == id2
    assert r2.json().get("duplicateOfExisting") is True


@skip_if_sqlserver_pending_migration
def test_story_622_reject_fake_attachment_id_on_submit(
    client: TestClient, test_db: Session, mock_published_form, asset_tmp
):
    """UAT 3.3: submit referencing a UUID that was never uploaded for this link → 422."""
    from models.form_version import FormVersion

    form_id = int(mock_published_form["form_id"])
    token = mock_published_form["token"]
    fv = test_db.query(FormVersion).filter(FormVersion.FormID == form_id).first()
    fv.DefinitionJSON = json.dumps(_def_with_file_upload())
    test_db.commit()

    fake_id = "11111111-1111-4111-8111-111111111111"
    sub = client.post(
        f"/api/public/forms/{token}/submissions",
        json=_submission_payload(att_id=fake_id, idem="idem-fake-uuid"),
    )
    assert sub.status_code == 422


@skip_if_sqlserver_pending_migration
def test_story_622_download_404_unknown_attachment(client: TestClient, mock_published_form, admin_token_headers):
    form_id = int(mock_published_form["form_id"])
    r = client.get(
        f"/api/forms/{form_id}/attachments/00000000-0000-4000-8000-000000000099/content",
        headers=admin_token_headers,
    )
    assert r.status_code == 404
