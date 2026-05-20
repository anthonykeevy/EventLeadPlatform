"""ACS email provider configuration wiring (unit, no outbound calls)."""
import pytest

from config.email import EmailConfig
from services.email_providers.acs import ACSEmailProvider
from services.email_service import get_email_service


def test_email_config_acs_requires_connection_string(monkeypatch):
    monkeypatch.setenv("EMAIL_PROVIDER", "acs")
    monkeypatch.delenv("AZURE_COMMUNICATION_CONNECTION_STRING", raising=False)
    monkeypatch.delenv("ACS_CONNECTION_STRING", raising=False)
    with pytest.raises(ValueError, match="ACS email provider requires"):
        EmailConfig.from_env()


def test_email_config_acs_accepts_az_comm_env(monkeypatch):
    monkeypatch.setenv("EMAIL_PROVIDER", "acs")
    monkeypatch.setenv(
        "AZURE_COMMUNICATION_CONNECTION_STRING",
        "endpoint=https://sample.australia.communication.azure.com/;accesskey=dummykey",
    )
    cfg = EmailConfig.from_env()
    assert cfg.provider == "acs"
    assert cfg.azure_communication_connection_string is not None
    assert "endpoint=https://" in cfg.azure_communication_connection_string


def test_email_config_acs_accepts_legacy_acs_alias(monkeypatch):
    monkeypatch.setenv("EMAIL_PROVIDER", "acs")
    monkeypatch.delenv("AZURE_COMMUNICATION_CONNECTION_STRING", raising=False)
    monkeypatch.setenv(
        "ACS_CONNECTION_STRING",
        "endpoint=https://sample.australia.communication.azure.com/;accesskey=other",
    )
    cfg = EmailConfig.from_env()
    assert cfg.azure_communication_connection_string.endswith("accesskey=other")


def test_get_email_service_acs_provider(monkeypatch):
    monkeypatch.setenv("EMAIL_PROVIDER", "acs")
    monkeypatch.setenv(
        "AZURE_COMMUNICATION_CONNECTION_STRING",
        "endpoint=https://sample.australia.communication.azure.com/;accesskey=zz",
    )
    monkeypatch.setenv("EMAIL_FROM", "noreply@example.com")
    svc = get_email_service()
    assert isinstance(svc.provider, ACSEmailProvider)


def test_acs_provider_rejects_blank_connection():
    with pytest.raises(ValueError, match="AZURE_COMMUNICATION_CONNECTION_STRING"):
        ACSEmailProvider("")


async def test_acs_send_does_not_misapply_from_name_to_recipient(monkeypatch):
    """Regression for the 2026-05-19 bug: from_name is the SENDER's display name
    (matches MailHog and SMTP), and ACS does NOT support a per-message sender display
    name. Previously this code applied from_name to recipients.to[0].displayName, which
    is the RECIPIENT's display name -- causing inboxes to render the recipient as the
    sender's name. Pins the corrected message shape.
    """

    captured: dict = {}

    class _FakePoller:
        async def result(self):
            return {"status": "Succeeded"}

    class _FakeClient:
        async def begin_send(self, message):
            captured["message"] = message
            return _FakePoller()

        async def close(self):
            pass

    provider = ACSEmailProvider(
        "endpoint=https://sample.australia.communication.azure.com/;accesskey=dummy"
    )
    # Bypass _get_client so no real ACS HTTP traffic happens
    provider._client = _FakeClient()

    ok = await provider.send(
        to="recipient@example.com",
        subject="Test",
        html_body="<p>hello</p>",
        from_email="noreply@signalplatforms.com.au",
        from_name="Signal Platforms Notifications",
    )

    assert ok is True
    msg = captured["message"]

    # senderAddress is the bare email (ACS limitation; display name lives in
    # MailFrom resource config, not per-message)
    assert msg["senderAddress"] == "noreply@signalplatforms.com.au"

    # recipients.to[0] must carry ONLY the recipient address, NOT the sender's
    # from_name leaking in as the recipient's displayName.
    recipient = msg["recipients"]["to"][0]
    assert recipient["address"] == "recipient@example.com"
    assert "displayName" not in recipient, (
        "from_name (sender's display name) must NOT be applied to recipient.displayName "
        "(regression from the 2026-05-19 bug). If you intend to set a RECIPIENT display "
        "name in future, extend the cross-provider send() signature first; do not reuse "
        "from_name for that purpose."
    )


async def test_acs_send_works_when_from_name_is_omitted(monkeypatch):
    """Smoke: omitting from_name is the dominant call path today; ensure that path
    still produces a well-formed message (senderAddress + recipient address only)."""

    captured: dict = {}

    class _FakePoller:
        async def result(self):
            return {"status": "Succeeded"}

    class _FakeClient:
        async def begin_send(self, message):
            captured["message"] = message
            return _FakePoller()

        async def close(self):
            pass

    provider = ACSEmailProvider(
        "endpoint=https://sample.australia.communication.azure.com/;accesskey=dummy"
    )
    provider._client = _FakeClient()

    ok = await provider.send(
        to="recipient@example.com",
        subject="Test",
        html_body="<p>hello</p>",
        from_email="noreply@signalplatforms.com.au",
    )

    assert ok is True
    msg = captured["message"]
    assert msg["senderAddress"] == "noreply@signalplatforms.com.au"
    recipient = msg["recipients"]["to"][0]
    assert recipient == {"address": "recipient@example.com"}

