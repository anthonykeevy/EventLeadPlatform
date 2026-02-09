"""
Tests for background asset upload endpoint.
"""
from __future__ import annotations

import io
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from PIL import Image

from jose import jwt

from common.constants import DEFAULT_ASSET_IMAGE_MAX_UPLOAD_BYTES
from config.jwt import get_secret_key, get_algorithm
from models.asset import Asset
from models.ref.asset_type import AssetType


def _make_auth_headers() -> dict:
    now = datetime.utcnow()
    payload = {
        "sub": "1",
        "email": "test@example.com",
        "role": "company_admin",
        "company_id": 1,
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=15),
    }
    token = jwt.encode(payload, get_secret_key(), algorithm=get_algorithm())
    return {"Authorization": f"Bearer {token}"}


def _seed_asset_type(db) -> None:
    existing = db.query(AssetType).filter_by(TypeCode="IMAGE").first()
    if existing:
        return
    asset_type = AssetType(
        AssetTypeID=1,
        TypeCode="IMAGE",
        TypeName="Image",
        Description="Image asset type",
        IsActive=True,
        SortOrder=1,
        IsDeleted=False,
        CreatedDate=datetime.utcnow(),
    )
    db.add(asset_type)
    db.commit()


def _make_png_bytes() -> bytes:
    image = Image.new("RGB", (16, 16), (255, 0, 0))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _seed_asset(db, asset_id: int = 1) -> None:
    existing = db.query(Asset).filter_by(AssetID=asset_id).first()
    if existing:
        return
    asset = Asset(
        AssetID=asset_id,
        CompanyID=1,
        AssetTypeID=1,
        Sha256="testsha256",
        MimeType="image/png",
        SizeBytes=123,
        WidthPx=16,
        HeightPx=16,
        StorageProvider="local",
        StorageKey="1/test.png",
        OriginalFileName="test.png",
        DisplayName="Test Asset",
        CreatedDate=datetime.utcnow(),
        UpdatedDate=datetime.utcnow(),
        CreatedBy=1,
        UpdatedBy=1,
        IsDeleted=False,
    )
    db.add(asset)
    db.commit()


def test_upload_background_image_success(client: TestClient, test_db, monkeypatch, tmp_path):
    monkeypatch.setenv("ASSET_STORAGE_PROVIDER", "local")
    monkeypatch.setenv("ASSET_STORAGE_LOCAL_DIR", str(tmp_path))
    _seed_asset_type(test_db)

    response = client.post(
        "/api/assets/backgrounds/upload",
        files={"file": ("test.png", _make_png_bytes(), "image/png")},
        headers=_make_auth_headers(),
    )
    assert response.status_code == 201
    payload = response.json()
    assert payload["asset"]["mimeType"] == "image/png"
    assert payload["asset"]["assetId"] > 0
    assert payload["asset"]["assetKey"].startswith("asset:")


def test_upload_background_rejects_oversize(client: TestClient, test_db, monkeypatch, tmp_path):
    monkeypatch.setenv("ASSET_STORAGE_PROVIDER", "local")
    monkeypatch.setenv("ASSET_STORAGE_LOCAL_DIR", str(tmp_path))
    _seed_asset_type(test_db)

    too_large = b"x" * (DEFAULT_ASSET_IMAGE_MAX_UPLOAD_BYTES + 1)
    response = client.post(
        "/api/assets/backgrounds/upload",
        files={"file": ("big.png", too_large, "image/png")},
        headers=_make_auth_headers(),
    )
    assert response.status_code == 413


def test_upload_background_rejects_invalid_mime(client: TestClient, test_db, monkeypatch, tmp_path):
    monkeypatch.setenv("ASSET_STORAGE_PROVIDER", "local")
    monkeypatch.setenv("ASSET_STORAGE_LOCAL_DIR", str(tmp_path))
    _seed_asset_type(test_db)

    response = client.post(
        "/api/assets/backgrounds/upload",
        files={"file": ("note.txt", b"not an image", "text/plain")},
        headers=_make_auth_headers(),
    )
    assert response.status_code == 400


def test_resolve_asset_url_builds_runtime_url(client: TestClient, test_db, monkeypatch, tmp_path):
    monkeypatch.setenv("ASSET_STORAGE_PROVIDER", "local")
    monkeypatch.setenv("ASSET_STORAGE_LOCAL_DIR", str(tmp_path))
    _seed_asset_type(test_db)
    _seed_asset(test_db, asset_id=1)

    response = client.get(
        "/api/assets/1/resolve",
        headers=_make_auth_headers(),
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["url"].endswith("/api/assets/1/content")
