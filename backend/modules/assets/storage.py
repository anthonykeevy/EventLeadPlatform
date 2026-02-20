"""
Asset storage providers (local filesystem + Azure Blob).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os

from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.core.exceptions import ResourceExistsError


@dataclass(frozen=True)
class AssetStorageConfig:
    provider: str
    local_dir: str
    azure_connection_string: Optional[str]
    azure_container: str


def load_storage_config() -> AssetStorageConfig:
    provider = os.getenv("ASSET_STORAGE_PROVIDER", "local").strip().lower()
    backend_root = Path(__file__).resolve().parents[2]
    local_dir = os.getenv(
        "ASSET_STORAGE_LOCAL_DIR",
        str(backend_root / "storage" / "assets"),
    )
    azure_connection_string = os.getenv("ASSET_STORAGE_AZURE_CONNECTION_STRING") or os.getenv(
        "AZURE_STORAGE_CONNECTION_STRING"
    )
    azure_container = os.getenv("ASSET_STORAGE_AZURE_CONTAINER", "background-assets")
    return AssetStorageConfig(
        provider=provider,
        local_dir=local_dir,
        azure_connection_string=azure_connection_string,
        azure_container=azure_container,
    )


class AssetStorageProvider:
    provider_code: str

    def save(self, *, storage_key: str, data: bytes, content_type: str) -> None:
        raise NotImplementedError

    def exists(self, storage_key: str) -> bool:
        """Check if the file/blob exists at the given storage key."""
        raise NotImplementedError

    def get_public_url(self, *, storage_key: str, request_base: Optional[str], asset_id: Optional[int]) -> str:
        raise NotImplementedError


class LocalAssetStorageProvider(AssetStorageProvider):
    provider_code = "local"

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)

    def resolve_path(self, storage_key: str) -> Path:
        return (self.base_dir / storage_key).resolve()

    def save(self, *, storage_key: str, data: bytes, content_type: str) -> None:
        path = self.resolve_path(storage_key)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(data)

    def exists(self, storage_key: str) -> bool:
        path = self.resolve_path(storage_key)
        return path.exists()

    def get_public_url(self, *, storage_key: str, request_base: Optional[str], asset_id: Optional[int]) -> str:
        if not request_base or asset_id is None:
            raise ValueError("request_base and asset_id are required for local asset URLs")
        base = request_base.rstrip("/")
        return f"{base}/api/assets/{asset_id}/content"


class AzureBlobAssetStorageProvider(AssetStorageProvider):
    provider_code = "azure"

    def __init__(self, *, connection_string: str, container_name: str):
        self.container_name = container_name
        self.service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.service_client.get_container_client(container_name)
        try:
            self.container_client.create_container()
        except ResourceExistsError:
            pass

    def save(self, *, storage_key: str, data: bytes, content_type: str) -> None:
        blob_client = self.container_client.get_blob_client(storage_key)
        blob_client.upload_blob(
            data,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type),
        )

    def exists(self, storage_key: str) -> bool:
        blob_client = self.container_client.get_blob_client(storage_key)
        return blob_client.exists()

    def get_public_url(self, *, storage_key: str, request_base: Optional[str], asset_id: Optional[int]) -> str:
        blob_client = self.container_client.get_blob_client(storage_key)
        return blob_client.url


def get_storage_provider(config: AssetStorageConfig) -> AssetStorageProvider:
    if config.provider == "azure":
        if not config.azure_connection_string:
            raise ValueError("Azure storage provider requires ASSET_STORAGE_AZURE_CONNECTION_STRING")
        return AzureBlobAssetStorageProvider(
            connection_string=config.azure_connection_string,
            container_name=config.azure_container,
        )
    return LocalAssetStorageProvider(config.local_dir)
