# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

# mypy: disable-error-code="import-untyped"
import functools
import io
from typing import Optional

from dyff.schema.platform import Artifact, StorageSignedURL
from dyff.storage import dynamic_import, paths
from dyff.storage.backend.base.storage import StorageBackend
from dyff.storage.config import config


@functools.lru_cache()
def _get_backend() -> StorageBackend:
    return dynamic_import.instantiate(config.storage.backend)


def storage_size(path: str) -> int:
    return _get_backend().storage_size(path)


def list_dir(path: str) -> list[str]:
    return _get_backend().list_dir(path)


def download_recursive(source: str, destination: str) -> None:
    return _get_backend().download_recursive(source, destination)


def upload_recursive(source: str, destination: str) -> None:
    return _get_backend().upload_recursive(source, destination)


def put_object(data: io.BytesIO, destination: str) -> None:
    return _get_backend().put_object(data, destination)


def get_object(source: str) -> io.BytesIO:
    return _get_backend().get_object(source)


def signed_url_for_dataset_upload(
    dataset_id: str,
    artifact: Artifact,
    *,
    size_limit_bytes: Optional[int] = None,
    storage_path: Optional[str] = None,
) -> StorageSignedURL:
    return _get_backend().signed_url_for_dataset_upload(
        dataset_id,
        artifact,
        size_limit_bytes=size_limit_bytes,
        storage_path=storage_path,
    )


def dataset_artifact_md5hash(
    dataset_id: str, artifact_path: str, *, storage_path: Optional[str] = None
) -> bytes:
    return _get_backend().dataset_artifact_md5hash(
        dataset_id, artifact_path, storage_path=storage_path
    )


__all__ = [
    "paths",
    "dataset_artifact_md5hash",
    "download_recursive",
    "list_dir",
    "signed_url_for_dataset_upload",
    "storage_size",
]
