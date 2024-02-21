import copy
import os
from typing import Any, Dict, Generator, Optional
from unittest.mock import patch

import click
from click.testing import CliRunner
import pytest

from anyscale.commands.service_commands import deploy
from anyscale.service.models import ServiceConfig, ServiceStatus


MINIMAL_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "test_config_files", "minimal.yaml",
)
FULL_CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "test_config_files", "full.yaml",
)
MULTI_LINE_REQUIREMENTS_PATH = os.path.join(
    os.path.dirname(__file__), "test_requirements_files", "multi_line.txt",
)


class FakeServiceSDK:
    def __init__(self):
        self._deployed_config: Optional[ServiceConfig] = None
        self._deployed_kwargs: Dict[str, Any] = {}

    @property
    def deployed_config(self) -> Optional[ServiceConfig]:
        return self._deployed_config

    @property
    def deployed_kwargs(self) -> Dict[str, Any]:
        return copy.deepcopy(self._deployed_kwargs)

    def deploy(self, config: ServiceConfig, **kwargs):
        assert isinstance(config, ServiceConfig)
        self._deployed_config = config
        self._deployed_kwargs = kwargs

    def status(self) -> ServiceStatus:
        return ServiceStatus()


@pytest.fixture()
def fake_service_sdk() -> Generator[FakeServiceSDK, None, None]:
    fake_service_sdk = FakeServiceSDK()
    with patch(
        "anyscale.service.commands._LAZY_GLOBAL_SDK", new=fake_service_sdk,
    ):
        yield fake_service_sdk


def _assert_error_message(result: click.testing.Result, *, message: str):
    assert result.exit_code != 0
    assert message in result.stdout


class TestDeploy:
    def test_deploy_from_import_path(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(import_path="main:app")
        assert (
            fake_service_sdk.deployed_config.ray_serve_config
            == expected_config.ray_serve_config
        )

    def test_deploy_from_import_path_with_args(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", "arg1=val1", "arg2=val2"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            import_path="main:app", arguments={"arg1": "val1", "arg2": "val2"}
        )
        assert (
            fake_service_sdk.deployed_config.ray_serve_config
            == expected_config.ray_serve_config
        )

    def test_deploy_from_import_path_with_bad_arg(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", "bad_arg"])
        _assert_error_message(result, message="Invalid application argument 'bad_arg'")

    def test_deploy_from_file(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, [MINIMAL_CONFIG_PATH])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(import_path="main:app")
        assert (
            fake_service_sdk.deployed_config.ray_serve_config
            == expected_config.ray_serve_config
        )

    def test_deploy_from_file_with_args(self, fake_service_sdk):
        runner = CliRunner()
        os.path.join(
            os.path.dirname(__file__), "test_config_files", "minimal.yaml",
        )
        result = runner.invoke(deploy, [MINIMAL_CONFIG_PATH, "arg1=val1"])
        _assert_error_message(
            result,
            message="Application arguments can't be passed when deploying from a config file.",
        )

    @pytest.mark.parametrize("flag", ["--in-place", "-i"])
    def test_deploy_in_place(self, fake_service_sdk, flag: str):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", flag])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(import_path="main:app")
        assert (
            fake_service_sdk.deployed_config.ray_serve_config
            == expected_config.ray_serve_config
        )
        assert fake_service_sdk.deployed_kwargs == {
            "canary_percent": None,
            "in_place": True,
            "max_surge_percent": None,
        }

    def test_deploy_canary_percent(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", "--canary-percent", "50"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(import_path="main:app")
        assert (
            fake_service_sdk.deployed_config.ray_serve_config
            == expected_config.ray_serve_config
        )
        assert fake_service_sdk.deployed_kwargs == {
            "canary_percent": 50,
            "in_place": False,
            "max_surge_percent": None,
        }

    def test_deploy_max_surge_percent(self, fake_service_sdk):
        runner = CliRunner()
        result = runner.invoke(deploy, ["main:app", "--max-surge-percent", "50"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(import_path="main:app")
        assert (
            fake_service_sdk.deployed_config.ray_serve_config
            == expected_config.ray_serve_config
        )
        assert fake_service_sdk.deployed_kwargs == {
            "canary_percent": None,
            "in_place": False,
            "max_surge_percent": 50,
        }

    def test_deploy_from_file_override_options(self, fake_service_sdk):
        runner = CliRunner()

        # No overrides, should match the config in the file.
        result = runner.invoke(deploy, [FULL_CONFIG_PATH])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            import_path="main:app",
            name="test-name",
            image="test-image",
            working_dir="test-working-dir",
            requirements=["pip-install-test"],
        )
        assert fake_service_sdk.deployed_config == expected_config

        # Override name.
        result = runner.invoke(deploy, [FULL_CONFIG_PATH, "--name", "override-name"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            import_path="main:app",
            name="override-name",
            image="test-image",
            working_dir="test-working-dir",
            requirements=["pip-install-test"],
        )
        assert fake_service_sdk.deployed_config == expected_config

        # Override image.
        result = runner.invoke(deploy, [FULL_CONFIG_PATH, "--image", "override-image"])
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            import_path="main:app",
            name="test-name",
            image="override-image",
            working_dir="test-working-dir",
            requirements=["pip-install-test"],
        )
        assert fake_service_sdk.deployed_config == expected_config

        # Override working_dir.
        result = runner.invoke(
            deploy, [FULL_CONFIG_PATH, "--working-dir", "override-working-dir"]
        )
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            import_path="main:app",
            name="test-name",
            image="test-image",
            working_dir="override-working-dir",
            requirements=["pip-install-test"],
        )
        assert fake_service_sdk.deployed_config == expected_config

        # Override requirements.
        result = runner.invoke(
            deploy, [FULL_CONFIG_PATH, "--requirements", MULTI_LINE_REQUIREMENTS_PATH]
        )
        assert result.exit_code == 0
        assert fake_service_sdk.deployed_config is not None

        expected_config = ServiceConfig(
            import_path="main:app",
            name="test-name",
            image="test-image",
            working_dir="test-working-dir",
            requirements=["pip-install-test", "torch==1.10.1"],
        )
        assert fake_service_sdk.deployed_config == expected_config
