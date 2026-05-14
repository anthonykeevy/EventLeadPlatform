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

