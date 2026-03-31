"""
Story 6.2.2: public upload + submit binding for SubmissionAttachment.
"""
from __future__ import annotations

import hashlib
import os
import re
import uuid
from typing import Any, Dict, List, Mapping, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import select

from models.submission_attachment import SubmissionAttachment
from models.form_version import FormVersion
from models.form_public_link import FormPublicLink
from modules.assets.storage import get_storage_provider, load_storage_config

DEFAULT_MAX_BYTES = 10 * 1024 * 1024
SUBMISSION_STORAGE_PREFIX = "submissions"

SAFE_EXT_RE = re.compile(r"^[a-z0-9.]{1,12}$")


def _walk_file_upload_targets(nodes: Any, out: List[Tuple[str, Mapping[str, Any]]]) -> None:
    if not nodes:
        return
    for node in nodes:
        if not isinstance(node, dict):
            continue
        if node.get("type") == "file-upload":
            cid = node.get("id")
            if isinstance(cid, str) and cid:
                props = node.get("props") or {}
                out.append((cid, props if isinstance(props, dict) else {}))
        children = node.get("children")
        if isinstance(children, list):
            _walk_file_upload_targets(children, out)


def collect_file_upload_specs(definition: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    specs: Dict[str, Mapping[str, Any]] = {}
    for key in ("desktopPages", "tabletPages", "mobilePages", "pages"):
        pages = definition.get(key)
        if not isinstance(pages, list):
            continue
        for page in pages:
            if not isinstance(page, dict):
                continue
            components = page.get("components")
            if not isinstance(components, list):
                continue
            found: List[Tuple[str, Mapping[str, Any]]] = []
            _walk_file_upload_targets(components, found)
            for cid, props in found:
                specs[cid] = props
    return specs


def _max_bytes_for_props(props: Mapping[str, Any]) -> int:
    raw = props.get("maxFileSizeBytes")
    if isinstance(raw, int) and raw > 0:
        return raw
    mb = props.get("maxFileSizeMb")
    if isinstance(mb, (int, float)) and mb > 0:
        return int(mb * 1024 * 1024)
    return DEFAULT_MAX_BYTES


def _accepted_list(props: Mapping[str, Any]) -> Optional[List[str]]:
    acc = props.get("acceptedFileTypes") or props.get("accept")
    if acc is None:
        return None
    if isinstance(acc, str):
        parts = [p.strip() for p in acc.split(",") if p.strip()]
        return parts if parts else None
    if isinstance(acc, list):
        out = [str(x).strip() for x in acc if str(x).strip()]
        return out if out else None
    return None


def mime_or_extension_allowed(content_type: str, filename: str, accepted: Optional[List[str]]) -> bool:
    if not accepted:
        return True
    ct = (content_type or "").strip().lower()
    fn = (filename or "").strip().lower()
    for rule in accepted:
        r = rule.strip().lower()
        if not r:
            continue
        if r.startswith("."):
            if fn.endswith(r):
                return True
        elif r.endswith("/*") and "/" in r:
            prefix = r[:-2]
            if ct.startswith(prefix + "/"):
                return True
        elif "/" in r and not r.endswith("*"):
            if ct == r:
                return True
    return False


def _safe_extension(filename: str, content_type: str) -> str:
    base, ext = os.path.splitext((filename or "").strip())
    ext = (ext or "").lower()
    if ext and SAFE_EXT_RE.match(ext) and ext != ".":
        return ext[:12]
    ct = (content_type or "").lower()
    simple = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "application/pdf": ".pdf",
        "text/plain": ".txt",
    }
    return simple.get(ct, ".bin")


def _component_props_for_id(definition: Mapping[str, Any], component_id: str) -> Optional[Mapping[str, Any]]:
    specs = collect_file_upload_specs(definition)
    return specs.get(component_id)


def create_pending_attachment(
    db: Session,
    *,
    link: FormPublicLink,
    version: FormVersion,
    component_id: str,
    file_body: bytes,
    original_filename: str,
    content_type: str,
    client_session_key: str,
) -> Tuple[str, bool]:
    """
    Writes blob via AssetStorageProvider and inserts SubmissionAttachment (pending).
    Returns (public_attachment_id, reused_existing_blob).
    """
    definition = version.definition
    if not isinstance(definition, dict):
        definition = {}
    props = _component_props_for_id(definition, component_id)
    if props is None:
        raise ValueError("Invalid or unknown file-upload component for this form.")

    max_bytes = _max_bytes_for_props(props)
    if len(file_body) > max_bytes:
        raise ValueError(f"File exceeds maximum size of {max_bytes} bytes.")

    accepted = _accepted_list(props)
    if not mime_or_extension_allowed(content_type, original_filename, accepted):
        raise ValueError("File type is not allowed for this field.")

    digest = hashlib.sha256(file_body).hexdigest()

    if client_session_key:
        existing = db.execute(
            select(SubmissionAttachment).where(
                SubmissionAttachment.FormPublicLinkID == link.FormPublicLinkID,
                SubmissionAttachment.ClientUploadSessionKey == client_session_key,
                SubmissionAttachment.Sha256 == digest,
                SubmissionAttachment.FormSubmissionID.is_(None),
            )
        ).scalars().first()
        if existing:
            return str(existing.PublicAttachmentId), True

    public_id = str(uuid.uuid4())
    ext = _safe_extension(original_filename, content_type)
    storage_key = f"{SUBMISSION_STORAGE_PREFIX}/{link.FormPublicLinkID}/{public_id}{ext}"

    config = load_storage_config()
    provider = get_storage_provider(config)
    provider.save(storage_key=storage_key, data=file_body, content_type=content_type or "application/octet-stream")

    row = SubmissionAttachment(
        FormPublicLinkID=link.FormPublicLinkID,
        FormSubmissionID=None,
        PublicAttachmentId=public_id,
        OriginalFileName=original_filename or "upload",
        ContentType=content_type or "application/octet-stream",
        SizeBytes=len(file_body),
        Sha256=digest,
        StorageProvider=provider.provider_code,
        StorageKey=storage_key,
        ClientUploadSessionKey=client_session_key or None,
    )
    db.add(row)
    db.flush()
    return public_id, False


def validate_and_bind_attachments_for_submission(
    db: Session,
    *,
    link: FormPublicLink,
    client_session_key: str,
    answers_by_component_id: Mapping[str, Any],
    definition_raw: Any,
    submission_id: int,
) -> None:
    if not isinstance(definition_raw, dict):
        definition_raw = {}
    specs = collect_file_upload_specs(definition_raw)
    if not specs:
        return

    to_bind: List[SubmissionAttachment] = []

    for comp_id, props in specs.items():
        answer = answers_by_component_id.get(comp_id)
        allow_multi = bool(props.get("allowMultiple"))
        max_files = props.get("maxFiles")
        max_n = int(max_files) if isinstance(max_files, int) and max_files > 0 else 8

        id_list: List[str] = []
        if allow_multi:
            if answer is None:
                continue
            if isinstance(answer, list):
                id_list = [str(x).strip() for x in answer if str(x).strip()]
            else:
                raise ValueError(f"Attachment answer for {comp_id} must be a list when allowMultiple is true.")
            if len(id_list) > max_n:
                raise ValueError(f"Too many files for field {comp_id}.")
        else:
            if answer is None or answer == "":
                continue
            if isinstance(answer, list):
                raise ValueError(f"Attachment answer for {comp_id} must be a single id when allowMultiple is false.")
            id_list = [str(answer).strip()]

        for att_id in id_list:
            row = db.execute(
                select(SubmissionAttachment).where(
                    SubmissionAttachment.PublicAttachmentId == att_id,
                    SubmissionAttachment.FormPublicLinkID == link.FormPublicLinkID,
                    SubmissionAttachment.FormSubmissionID.is_(None),
                )
            ).scalars().first()
            if not row:
                raise ValueError("Invalid or expired attachment reference.")
            if row.ClientUploadSessionKey != client_session_key:
                raise ValueError("Attachment does not belong to this session.")
            to_bind.append(row)

    for row in to_bind:
        row.FormSubmissionID = submission_id


def load_attachment_bytes(row: SubmissionAttachment) -> bytes:
    """Reads bytes using the currently configured storage provider (same env as upload)."""
    provider = get_storage_provider(load_storage_config())
    return provider.read_bytes(storage_key=row.StorageKey)
