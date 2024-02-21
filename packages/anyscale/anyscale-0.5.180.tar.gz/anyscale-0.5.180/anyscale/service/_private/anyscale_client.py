from abc import ABC, abstractmethod
import pathlib
from typing import Any, Dict, Optional
import uuid

import requests

from anyscale.client.openapi_client.api.default_api import DefaultApi as InternalApi
from anyscale.client.openapi_client.models import (
    CloudDataBucketFileType,
    CloudDataBucketPresignedUploadInfo,
    CloudDataBucketPresignedUploadRequest,
    Project,
)
from anyscale.controllers.service_controller import ServiceController
from anyscale.utils.cloud_utils import get_default_cloud
from anyscale.utils.runtime_env import zip_local_dir


RUNTIME_ENV_PACKAGE_FORMAT = "pkg_{content_hash}.zip"


class AnyscaleClientWrapper(ABC):
    @abstractmethod
    def get_default_project_id(self) -> str:
        """Get the default project ID for this user."""
        raise NotImplementedError

    @abstractmethod
    def get_cloud_id(self, cloud_name: Optional[str] = None) -> str:
        """Get the cloud ID for the provided cloud name.

        If cloud name is None, gets the default cloud for this user.
        """
        raise NotImplementedError

    @abstractmethod
    def roll_out_service(self, config_dict: Dict[str, Any]):
        """Deploy or update the service to use the provided config."""
        # NOTE(edoakes): using the untyped dictionary is temporary and this will be updated
        # to directly call the SDK with the ApplyServiceModel.
        raise NotImplementedError

    @abstractmethod
    def upload_local_dir_to_cloud_storage(
        self, local_dir: str, *, cloud_id: str
    ) -> str:
        """Upload the provided directory to cloud storage and return a URI for it.

        The directory will be zipped and the resulting URI can be in a Ray runtime_env.

        The upload is preformed using a pre-signed URL fetched from Anyscale, so no
        local cloud provider authentication is required.
        """
        raise NotImplementedError


class FakeAnyscaleClient(AnyscaleClientWrapper):
    CLOUD_BUCKET = "s3://fake-bucket/{cloud_id}"
    DEFAULT_CLOUD_ID = "fake-default-cloud-id"
    DEFAULT_PROJECT_ID = "fake-default-project-id"

    def __init__(self):
        self._rolled_out_config: Optional[Dict[str, Any]] = None

    def get_default_project_id(self) -> str:
        return self.DEFAULT_PROJECT_ID

    def get_cloud_id(self, cloud_name: Optional[str] = None) -> str:
        if cloud_name is None:
            return self.DEFAULT_CLOUD_ID

        return f"{cloud_name}-fake-id"

    @property
    def rolled_out_service(self) -> Optional[Dict[str, Any]]:
        return self._rolled_out_config

    def roll_out_service(self, config_dict: Dict[str, Any]):
        self._rolled_out_config = config_dict

    def upload_local_dir_to_cloud_storage(
        self, local_dir: str, *, cloud_id: str  # noqa: ARG002
    ) -> str:
        bucket = self.CLOUD_BUCKET.format(cloud_id=cloud_id)
        return f"{bucket}/fake_pkg_{uuid.uuid4()}.zip"


class RealAnyscaleClient(AnyscaleClientWrapper):
    def __init__(
        self,
        *,
        controller: Optional[ServiceController] = None,
        internal_api_client: Optional[InternalApi] = None,
    ):
        # NOTE(edoakes): this is an incremental path, eventually the logic in the
        # service controller will be moved here.
        self._controller = controller or ServiceController()
        self._internal_api_client = (
            internal_api_client or self._controller.internal_api_client
        )

        # Cached IDs to avoid duplicate lookups.
        self._default_project_id: Optional[str] = None
        self._cloud_id_cache: Dict[Optional[str], str] = {}

    def get_default_project_id(self) -> str:
        if self._default_project_id is None:
            default_project: Project = self._internal_api_client.get_default_project_api_v2_projects_default_project_get().result
            self._default_project_id = default_project.id

        return self._default_project_id

    def get_cloud_id(self, cloud_name: Optional[str] = None) -> str:
        if cloud_name in self._cloud_id_cache:
            return self._cloud_id_cache[cloud_name]

        # TODO(edoakes): this fetch path requires multiple RTTs which seems unnecessary.
        # We should consider adding a better backend endpoint to hit.
        cloud_id, _ = get_default_cloud(self._internal_api_client, cloud_name)
        self._cloud_id_cache[cloud_name] = cloud_id
        return cloud_id

    def roll_out_service(self, config_dict: Dict[str, Any]):
        self._controller.rollout(config_dict, auto_complete_rollout=True)

    def upload_local_dir_to_cloud_storage(
        self, local_dir: str, *, cloud_id: str
    ) -> str:
        if not pathlib.Path(local_dir).is_dir():
            raise RuntimeError(f"Path '{local_dir}' is not a valid directory.")

        with zip_local_dir(local_dir) as (_, zip_file_bytes, content_hash):
            request = CloudDataBucketPresignedUploadRequest(
                file_type=CloudDataBucketFileType.RUNTIME_ENV_PACKAGES,
                file_name=RUNTIME_ENV_PACKAGE_FORMAT.format(content_hash=content_hash),
            )
            info: CloudDataBucketPresignedUploadInfo = self._internal_api_client.generate_cloud_data_bucket_presigned_upload_url_api_v2_clouds_cloud_id_generate_cloud_data_bucket_presigned_upload_url_post(
                cloud_id, request
            ).result
            requests.put(info.upload_url, data=zip_file_bytes).raise_for_status()

        return info.file_uri
