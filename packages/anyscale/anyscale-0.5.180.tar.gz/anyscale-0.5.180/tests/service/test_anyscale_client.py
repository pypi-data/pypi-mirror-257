from dataclasses import dataclass
import os
from typing import Any, Generator, Tuple
from unittest.mock import Mock, patch

import pytest

from anyscale.client.openapi_client.configuration import Configuration
from anyscale.client.openapi_client.models import (
    CloudDataBucketFileType,
    CloudDataBucketPresignedUploadInfo,
    CloudDataBucketPresignedUploadRequest,
    Project,
)
from anyscale.service._private.anyscale_client import RealAnyscaleClient


def _get_test_working_dir_path(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), "test_working_dirs", name)


BASIC_WORKING_DIR = _get_test_working_dir_path("basic")
NESTED_WORKING_DIR = _get_test_working_dir_path("nested")
SYMLINK_WORKING_DIR = _get_test_working_dir_path("symlink_to_basic")
TEST_WORKING_DIRS = [BASIC_WORKING_DIR, NESTED_WORKING_DIR, SYMLINK_WORKING_DIR]

OPENAPI_NO_VALIDATION = Configuration()
OPENAPI_NO_VALIDATION.client_side_validation = False


class FakeServiceController:
    pass


@dataclass
class FakeClientResult:
    result: Any


class FakeInternalAPIClient:
    FAKE_FILE_URI = "s3://some-bucket/{file_name}"
    FAKE_UPLOAD_URL = "http://some-domain.com/upload-magic-file/{file_name}"
    DEFAULT_PROJECT_ID = "fake-default-project-id"

    def __init__(self):
        self._num_get_project_calls: int = 0

    @property
    def num_get_project_calls(self) -> int:
        return self._num_get_project_calls

    def get_default_project_api_v2_projects_default_project_get(
        self,
    ) -> FakeClientResult:
        self._num_get_project_calls += 1
        return FakeClientResult(
            result=Project(
                id=self.DEFAULT_PROJECT_ID,
                local_vars_configuration=OPENAPI_NO_VALIDATION,
            ),
        )

    def generate_cloud_data_bucket_presigned_upload_url_api_v2_clouds_cloud_id_generate_cloud_data_bucket_presigned_upload_url_post(
        self, cloud_id: str, request: CloudDataBucketPresignedUploadRequest
    ) -> FakeClientResult:
        assert request.file_type == CloudDataBucketFileType.RUNTIME_ENV_PACKAGES
        assert isinstance(request.file_name, str)
        return FakeClientResult(
            result=CloudDataBucketPresignedUploadInfo(
                upload_url=self.FAKE_UPLOAD_URL.format(file_name=request.file_name),
                file_uri=self.FAKE_FILE_URI.format(file_name=request.file_name),
            ),
        )


@pytest.fixture()
def setup_anyscale_client() -> Tuple[RealAnyscaleClient, FakeInternalAPIClient]:
    fake_internal_client = FakeInternalAPIClient()
    return (
        RealAnyscaleClient(
            controller=FakeServiceController(),
            internal_api_client=fake_internal_client,
        ),
        fake_internal_client,
    )


@pytest.fixture()
def mock_requests_put() -> Generator[Mock, None, None]:
    with patch("requests.put") as mock_requests_put:
        yield mock_requests_put


def test_get_default_project(
    setup_anyscale_client: Tuple[RealAnyscaleClient, FakeInternalAPIClient]
):
    anyscale_client, fake_internal_client = setup_anyscale_client

    # The project ID should be cached so we only make one API call.
    for _ in range(100):
        assert (
            anyscale_client.get_default_project_id()
            == FakeInternalAPIClient.DEFAULT_PROJECT_ID
        )
        assert fake_internal_client.num_get_project_calls == 1


class TestUploadLocalDirToCloudStorage:
    @pytest.mark.parametrize("working_dir", TEST_WORKING_DIRS)
    def test_basic(
        self,
        setup_anyscale_client: Tuple[RealAnyscaleClient, FakeInternalAPIClient],
        mock_requests_put: Mock,
        working_dir: str,
    ):
        anyscale_client, _ = setup_anyscale_client
        uri = anyscale_client.upload_local_dir_to_cloud_storage(
            working_dir, cloud_id="test-cloud-id",
        )
        assert isinstance(uri, str) and len(uri) > 0
        mock_requests_put.assert_called_once()
        mock_requests_put.reset_mock()

    def test_missing_dir(
        self,
        setup_anyscale_client: Tuple[RealAnyscaleClient, FakeInternalAPIClient],
        mock_requests_put: Mock,
    ):
        anyscale_client, _ = setup_anyscale_client
        with pytest.raises(
            RuntimeError, match="Path 'does_not_exist' is not a valid directory."
        ):
            anyscale_client.upload_local_dir_to_cloud_storage(
                "does_not_exist", cloud_id="test-cloud-id",
            )

    def test_uri_content_addressed(
        self,
        setup_anyscale_client: Tuple[RealAnyscaleClient, FakeInternalAPIClient],
        mock_requests_put: Mock,
    ):
        anyscale_client, _ = setup_anyscale_client

        # Uploading the same directory contents should result in the same content-addressed URI.
        uri1 = anyscale_client.upload_local_dir_to_cloud_storage(
            BASIC_WORKING_DIR, cloud_id="test-cloud-id",
        )
        uri2 = anyscale_client.upload_local_dir_to_cloud_storage(
            BASIC_WORKING_DIR, cloud_id="test-cloud-id",
        )
        assert uri1 == uri2

        # Uploading a different directory should not result in the same content-addressed URI.
        uri3 = anyscale_client.upload_local_dir_to_cloud_storage(
            NESTED_WORKING_DIR, cloud_id="test-cloud-id",
        )
        assert uri1 != uri3 and uri2 != uri3
