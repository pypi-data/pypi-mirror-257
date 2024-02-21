from dataclasses import dataclass
import os
import re
from typing import List, Optional

import pytest

from anyscale.service._private.anyscale_client import FakeAnyscaleClient
from anyscale.service.models import ServiceConfig


@dataclass
class ConfigFile:
    name: str
    expected_config: Optional[ServiceConfig] = None
    expected_error: Optional[str] = None

    def get_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "test_config_files", self.name)


TEST_CONFIG_FILES = [
    ConfigFile("minimal.yaml", expected_config=ServiceConfig(import_path="main:app")),
    ConfigFile(
        "full.yaml",
        expected_config=ServiceConfig(
            import_path="main:app",
            name="test-name",
            image="test-image",
            working_dir="test-working-dir",
            requirements=["pip-install-test"],
        ),
    ),
    ConfigFile(
        "arguments.yaml",
        expected_config=ServiceConfig(
            import_path="main:app", arguments={"abc": "def", "nested": {"key": "val"}}
        ),
    ),
    ConfigFile(
        "unrecognized_option.yaml",
        expected_error=re.escape("Unrecognized options: ['bad_option']."),
    ),
    ConfigFile(
        "import_path_and_ray_serve_config.yaml",
        expected_error=re.escape(
            "import_path and arguments cannot be provided with ray_serve_config."
        ),
    ),
    ConfigFile(
        "ray_serve_config.yaml",
        expected_config=ServiceConfig(
            ray_serve_config={
                "applications": [
                    {
                        "import_path": "main:app",
                        "runtime_env": {"env_vars": {"abc": "def"}},
                        "arguments": {"abc": "def", "nested": {"key": "val"}},
                    }
                ],
            },
        ),
    ),
]


@dataclass
class RequirementsFile:
    name: str
    expected_pip_list: Optional[List[str]]

    def get_path(self) -> str:
        return os.path.join(
            os.path.dirname(__file__), "test_requirements_files", self.name,
        )


TEST_REQUIREMENTS_FILES = [
    RequirementsFile("does_not_exist.txt", None),
    RequirementsFile("empty.txt", []),
    RequirementsFile("single_line.txt", ["pip-install-test"]),
    RequirementsFile("multi_line.txt", ["pip-install-test", "torch==1.10.1"]),
    RequirementsFile(
        "multi_line_with_whitespace.txt",
        ["pip-install-test", "torch==1.10.1", "something-else"],
    ),
    RequirementsFile("comments.txt", ["pip-install-test", "torch==1.10.1"]),
]


class TestServiceConfig:
    def test_no_ray_serve_config_fields(self):
        with pytest.raises(
            ValueError, match="Either import_path or ray_serve_config must be provided."
        ):
            ServiceConfig(
                import_path=None, ray_serve_config=None,
            )

    def test_reject_import_path_and_config(self):
        with pytest.raises(
            ValueError,
            match="import_path and arguments cannot be provided with ray_serve_config.",
        ):
            ServiceConfig(
                import_path="main:app", ray_serve_config={"test": "123"},
            )

    def test_reject_arguments_and_config(self):
        with pytest.raises(
            ValueError,
            match="import_path and arguments cannot be provided with ray_serve_config.",
        ):
            ServiceConfig(
                ray_serve_config={"test": "123"}, arguments={"abc": "def"},
            )

    def test_import_path(self):
        config = ServiceConfig(import_path="main:app")
        assert config.ray_serve_config == {
            "applications": [{"import_path": "main:app",},],
        }

    def test_import_path_with_arguments(self):
        config = ServiceConfig(import_path="main:app", arguments={"hello": "world"})
        assert config.ray_serve_config == {
            "applications": [
                {"import_path": "main:app", "arguments": {"hello": "world"},},
            ],
        }

    def test_import_path_with_nested_arguments(self):
        config = ServiceConfig(
            import_path="main:app",
            arguments={"hello": "world", "nested": {"hi": "there"}, "list": [1]},
        )
        assert config.ray_serve_config == {
            "applications": [
                {
                    "import_path": "main:app",
                    "arguments": {
                        "hello": "world",
                        "nested": {"hi": "there"},
                        "list": [1],
                    },
                },
            ],
        }

    def test_import_path_with_bad_arguments(self):
        err_msg = "Application arguments must be a dictionary."
        with pytest.raises(TypeError, match=err_msg):
            ServiceConfig(
                import_path="main:app", arguments=["a", "b", "c"],
            )

    def test_passed_ray_serve_config(self):
        ray_serve_config = {
            "applications": [{"import_path": "main:app",},],
        }
        config = ServiceConfig(ray_serve_config=ray_serve_config)
        assert config.ray_serve_config == ray_serve_config

    def test_name(self):
        config = ServiceConfig(import_path="main:app")
        assert config.name is None

        config = ServiceConfig(import_path="main:app", name="my-custom-name")
        assert config.name == "my-custom-name"

        with pytest.raises(TypeError, match="name must be a string"):
            ServiceConfig(import_path="main:app", name=123)

    def test_image(self):
        config = ServiceConfig(import_path="main:app")
        assert config.image is None

        config = ServiceConfig(import_path="main:app", image="my-custom-image:1")
        assert config.image == "my-custom-image:1"

        with pytest.raises(TypeError, match="image must be a string"):
            ServiceConfig(import_path="main:app", image=123)

    def test_options(self):
        config = ServiceConfig(import_path="main:app", arguments={"hello": "world"})

        options = {
            "name": "test-name",
            "image": "test-image",
            "requirements": ["pip-install-test"],
            "working_dir": ".",
        }

        # Test setting fields one at a time.
        for option, val in options.items():
            assert config.options(**{option: val}) == ServiceConfig(
                import_path="main:app", arguments={"hello": "world"}, **{option: val}
            )

            assert config.options(**{option: val}) == ServiceConfig(
                import_path="main:app", arguments={"hello": "world"}, **{option: val}
            )

        # Test setting fields all at once.
        assert config.options(**options) == ServiceConfig(
            import_path="main:app", arguments={"hello": "world"}, **options
        )

    @pytest.mark.parametrize("working_dir", [None, ".", "s3://path.zip"])
    def test_override_working_dir_import_path(self, working_dir: Optional[str]):
        config = ServiceConfig(
            import_path="main:app", arguments={"foo": "bar"}, working_dir=working_dir,
        )

        if working_dir is None:
            assert "runtime_env" not in config.ray_serve_config["applications"][0]
        else:
            config.ray_serve_config["applications"][0]["runtime_env"] = {
                "working_dir": working_dir,
            }

    @pytest.mark.parametrize("working_dir", [None, ".", "s3://path.zip"])
    def test_override_working_dir_ray_serve_config(self, working_dir: Optional[str]):
        ray_serve_config = {
            "applications": [
                {"name": "no_runtime_env", "import_path": "main:app",},
                {
                    "name": "empty_runtime_env",
                    "import_path": "main:app",
                    "runtime_env": {},
                },
                {
                    "name": "has_runtime_env",
                    "import_path": "main:app",
                    "runtime_env": {
                        "working_dir": "s3://somewhere.zip",
                        "env_vars": {"abc": "123"},
                    },
                },
            ],
        }

        config = ServiceConfig(
            ray_serve_config=ray_serve_config, working_dir=working_dir,
        )

        if working_dir is None:
            assert config.ray_serve_config == ray_serve_config
        else:
            assert len(config.ray_serve_config["applications"]) == 3
            assert config.ray_serve_config["applications"][0] == {
                "name": "no_runtime_env",
                "import_path": "main:app",
                "runtime_env": {"working_dir": working_dir,},
            }

            assert config.ray_serve_config["applications"][1] == {
                "name": "empty_runtime_env",
                "import_path": "main:app",
                "runtime_env": {"working_dir": working_dir,},
            }
            assert config.ray_serve_config["applications"][2] == {
                "name": "has_runtime_env",
                "import_path": "main:app",
                "runtime_env": {
                    "working_dir": working_dir,
                    "env_vars": {"abc": "123"},
                },
            }

    @pytest.mark.parametrize("requirements", [None, *TEST_REQUIREMENTS_FILES])
    def test_override_requirements_file(self, requirements: Optional[RequirementsFile]):
        ray_serve_config = {
            "applications": [
                {"name": "no_runtime_env", "import_path": "main:app",},
                {
                    "name": "empty_runtime_env",
                    "import_path": "main:app",
                    "runtime_env": {},
                },
                {
                    "name": "has_runtime_env",
                    "import_path": "main:app",
                    "runtime_env": {
                        "env_vars": {"abc": "123"},
                        "working_dir": "s3://somewhere.zip",
                    },
                },
            ],
        }

        if requirements is not None and requirements.expected_pip_list is None:
            with pytest.raises(ValueError):
                ServiceConfig(
                    ray_serve_config=ray_serve_config,
                    requirements=requirements.get_path(),
                )

            return

        config = ServiceConfig(
            ray_serve_config=ray_serve_config,
            requirements=requirements.get_path() if requirements else None,
        )
        if requirements is None:
            assert config.ray_serve_config == ray_serve_config
        else:
            assert len(config.ray_serve_config["applications"]) == 3
            assert config.ray_serve_config["applications"][0] == {
                "name": "no_runtime_env",
                "import_path": "main:app",
                "runtime_env": {"pip": requirements.expected_pip_list,},
            }

            assert config.ray_serve_config["applications"][1] == {
                "name": "empty_runtime_env",
                "import_path": "main:app",
                "runtime_env": {"pip": requirements.expected_pip_list,},
            }
            assert config.ray_serve_config["applications"][2] == {
                "name": "has_runtime_env",
                "import_path": "main:app",
                "runtime_env": {
                    "env_vars": {"abc": "123"},
                    "working_dir": "s3://somewhere.zip",
                    "pip": requirements.expected_pip_list,
                },
            }

    @pytest.mark.parametrize("config_file", TEST_CONFIG_FILES)
    def test_from_config_file(self, config_file: ConfigFile):
        if config_file.expected_error is not None:
            with pytest.raises(Exception, match=config_file.expected_error):
                ServiceConfig.from_yaml(config_file.get_path())

            return

        assert config_file.expected_config == ServiceConfig.from_yaml(
            config_file.get_path()
        )

    def test_upload_local_working_dir(self):
        client = FakeAnyscaleClient()
        config = ServiceConfig(import_path="main:app", working_dir=".",)
        new_config = config.with_local_dirs_uploaded(client)

        # The original config should not be modified.
        assert config != new_config

        applications = new_config.ray_serve_config["applications"]
        assert len(applications) == 1
        assert applications[0]["runtime_env"]["working_dir"].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.DEFAULT_CLOUD_ID
            )
        )

    def test_upload_with_no_local_dirs(self):
        """Configs should be left unchanged if there are no local dirs."""
        client = FakeAnyscaleClient()

        basic_config = ServiceConfig(import_path="main:app",)
        assert basic_config == basic_config.with_local_dirs_uploaded(client)

        config_with_requirements = ServiceConfig(
            import_path="main:app", requirements=TEST_REQUIREMENTS_FILES[2],
        )
        assert (
            config_with_requirements
            == config_with_requirements.with_local_dirs_uploaded(client)
        )

        complex_config = ServiceConfig(
            ray_serve_config={
                "applications": [
                    {"name": "app1", "import_path": "main:app",},
                    {
                        "name": "app2",
                        "import_path": "main:app",
                        "runtime_env": {"env_vars": {"foo": "bar",},},
                    },
                ],
            },
        )
        assert complex_config == complex_config.with_local_dirs_uploaded(client)

    def test_no_upload_remote_working_dir(self):
        client = FakeAnyscaleClient()
        config = ServiceConfig(
            import_path="main:app", working_dir="s3://some-remote-uri.zip",
        )
        config = config.with_local_dirs_uploaded(client)

        applications = config.ray_serve_config["applications"]
        assert len(applications) == 1
        assert (
            applications[0]["runtime_env"]["working_dir"] == "s3://some-remote-uri.zip"
        )

    def test_upload_local_py_modules(self):
        client = FakeAnyscaleClient()
        config = ServiceConfig(
            ray_serve_config={
                "applications": [
                    {
                        "import_path": "main:app",
                        "runtime_env": {
                            "py_modules": [
                                # Should be left alone.
                                "s3://some-remote-uri.zip",
                                # Should be uploaded.
                                "local-path",
                            ],
                        },
                    },
                ],
            },
        )
        config = config.with_local_dirs_uploaded(client)
        applications = config.ray_serve_config["applications"]
        assert len(applications) == 1
        assert (
            applications[0]["runtime_env"]["py_modules"][0]
            == "s3://some-remote-uri.zip"
        )
        assert applications[0]["runtime_env"]["py_modules"][1].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.DEFAULT_CLOUD_ID
            )
        )

    def test_upload_caching(self):
        """The same directory should only by uploaded once."""
        client = FakeAnyscaleClient()
        config = ServiceConfig(import_path="main:app", working_dir=".",)
        config = ServiceConfig(
            ray_serve_config={
                "applications": [
                    {
                        "name": "app1",
                        "import_path": "main:app",
                        "runtime_env": {"working_dir": ".",},
                    },
                    {
                        "name": "app2",
                        "import_path": "main:app",
                        "runtime_env": {
                            "working_dir": ".",
                            "py_modules": [".", "other-dir",],
                        },
                    },
                ],
            },
        )
        config = config.with_local_dirs_uploaded(client)

        applications = config.ray_serve_config["applications"]
        assert len(applications) == 2
        assert applications[0]["runtime_env"]["working_dir"].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.DEFAULT_CLOUD_ID
            )
        )
        common_uri = applications[0]["runtime_env"]["working_dir"]

        assert applications[1]["runtime_env"]["working_dir"] == common_uri
        assert applications[1]["runtime_env"]["py_modules"][0] == common_uri
        assert applications[1]["runtime_env"]["py_modules"][1] != common_uri
        assert applications[1]["runtime_env"]["py_modules"][1].startswith(
            FakeAnyscaleClient.CLOUD_BUCKET.format(
                cloud_id=FakeAnyscaleClient.DEFAULT_CLOUD_ID
            )
        )
