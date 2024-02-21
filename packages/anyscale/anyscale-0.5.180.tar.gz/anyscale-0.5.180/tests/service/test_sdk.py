from typing import Tuple

import pytest

from anyscale.service._private.anyscale_client import FakeAnyscaleClient
from anyscale.service._private.sdk import ServiceSDK
from anyscale.service.models import ServiceConfig


@pytest.fixture()
def sdk_with_fake_client() -> Tuple[ServiceSDK, FakeAnyscaleClient]:
    fake_client = FakeAnyscaleClient()
    return ServiceSDK(client=fake_client), fake_client


class TestDeploy:
    def test_validation(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, client = sdk_with_fake_client

        config = ServiceConfig(import_path="main:app")

        with pytest.raises(TypeError):
            sdk.deploy(config, name=123)

        with pytest.raises(TypeError):
            sdk.deploy(config, in_place="in_place")

        with pytest.raises(TypeError):
            sdk.deploy(config, canary_percent="10")

        with pytest.raises(ValueError):
            sdk.deploy(config, canary_percent=-1)

        with pytest.raises(ValueError):
            sdk.deploy(config, canary_percent=101)

        with pytest.raises(TypeError):
            sdk.deploy(config, max_surge_percent="10")

        with pytest.raises(ValueError):
            sdk.deploy(config, max_surge_percent=-1)

        with pytest.raises(ValueError):
            sdk.deploy(config, max_surge_percent=101)

    def test_basic(self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]):
        sdk, client = sdk_with_fake_client

        config = ServiceConfig(import_path="main:app")
        sdk.deploy(config)
        assert client.rolled_out_service == {
            "project_id": client.DEFAULT_PROJECT_ID,
            "ray_serve_config": config.ray_serve_config,
            "rollout_strategy": "ROLLOUT",
        }

    def test_in_place(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, client = sdk_with_fake_client

        config = ServiceConfig(import_path="main:app")
        sdk.deploy(config, in_place=True)
        assert client.rolled_out_service == {
            "project_id": client.DEFAULT_PROJECT_ID,
            "ray_serve_config": config.ray_serve_config,
            "rollout_strategy": "IN_PLACE",
        }

    def test_canary_percent(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, client = sdk_with_fake_client

        config = ServiceConfig(import_path="main:app")
        sdk.deploy(config, canary_percent=50)
        assert client.rolled_out_service == {
            "project_id": client.DEFAULT_PROJECT_ID,
            "ray_serve_config": config.ray_serve_config,
            "rollout_strategy": "ROLLOUT",
            "canary_percent": 50,
        }

    def test_max_surge_percent(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, client = sdk_with_fake_client

        config = ServiceConfig(import_path="main:app")
        sdk.deploy(config, max_surge_percent=50)
        assert client.rolled_out_service == {
            "project_id": client.DEFAULT_PROJECT_ID,
            "ray_serve_config": config.ray_serve_config,
            "rollout_strategy": "ROLLOUT",
            "max_surge_percent": 50,
        }

    def test_upload_local_dirs(
        self, sdk_with_fake_client: Tuple[ServiceSDK, FakeAnyscaleClient]
    ):
        sdk, client = sdk_with_fake_client

        config = ServiceConfig(import_path="main:app", working_dir=".")
        sdk.deploy(config)
        [application] = client.rolled_out_service["ray_serve_config"]["applications"]
        assert application["import_path"] == "main:app"
        assert application["runtime_env"]["working_dir"].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.DEFAULT_CLOUD_ID
            )
        )
