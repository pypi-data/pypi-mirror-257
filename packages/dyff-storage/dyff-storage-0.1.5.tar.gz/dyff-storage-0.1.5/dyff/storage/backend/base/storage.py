# SPDX-FileCopyrightText: 2024 UL Research Institutes
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import abc
from typing import IO, Optional

from dyff.schema.platform import Artifact, StorageSignedURL


class StorageBackend(abc.ABC):
    @abc.abstractmethod
    def storage_size(self, path: str) -> int:
        """Get the total size, in bytes, of all objects stored under the
        ``path`` prefix.
        """

    @abc.abstractmethod
    def list_dir(self, path: str) -> list[str]:
        """Get the absolute paths of all objects that are immediate
        "children" of ``path``.
        """

    @abc.abstractmethod
    def download_recursive(self, source: str, destination: str) -> None:
        """Download all objects stored under the path ``source`` to under the
        local directory ``destination``. The directory structure is preserved.
        """

    @abc.abstractmethod
    def upload_recursive(self, source: str, destination: str) -> None:
        """Upload all files stored under the local directory ``source`` to
        under the storage path ``destination``. The directory structure is
        preserved.
        """

    @abc.abstractmethod
    def put_object(self, data: bytes | IO[bytes], destination: str) -> None:
        """Upload a single object in memory."""

    @abc.abstractmethod
    def get_object(self, source: str) -> IO[bytes]:
        """Download a single object."""

    @abc.abstractmethod
    def signed_url_for_dataset_upload(
        self,
        dataset_id: str,
        artifact: Artifact,
        *,
        size_limit_bytes: Optional[int] = None,
        storage_path: Optional[str] = None,
    ) -> StorageSignedURL:
        """Create a temporary signed URL that can be used in a PUT request
        to upload an ``Artifact`` directly to storage.
        """

    @abc.abstractmethod
    def dataset_artifact_md5hash(
        self, dataset_id: str, artifact_path: str, *, storage_path: Optional[str] = None
    ) -> bytes:
        """Compute the MD5 hash of a dataset artifact in storage."""
