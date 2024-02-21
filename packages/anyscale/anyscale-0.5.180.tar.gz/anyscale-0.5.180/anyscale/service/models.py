import copy
from typing import Any, Dict, List, Optional, Union

import yaml

from anyscale.cli_logger import BlockLogger
from anyscale.service._private.anyscale_client import AnyscaleClientWrapper
from anyscale.utils.runtime_env import is_dir_remote_uri, parse_requirements_file


logger = BlockLogger()


class ServiceConfig:
    def __init__(
        self,
        *,
        import_path: Optional[str] = None,
        arguments: Optional[Dict[str, Any]] = None,
        ray_serve_config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        image: Optional[str] = None,
        working_dir: Optional[str] = None,
        requirements: Optional[Union[str, List[str]]] = None,
        **kwargs,
    ):
        if len(kwargs) > 0:
            raise ValueError(f"Unrecognized options: {list(kwargs.keys())}.")

        if name is not None and not isinstance(name, str):
            raise TypeError("name must be a string.")

        if image is not None and not isinstance(image, str):
            raise TypeError("image must be a string.")

        self._name = name
        self._image = image
        self._ray_serve_config = self._populate_ray_serve_config(
            import_path=import_path,
            arguments=arguments,
            ray_serve_config=ray_serve_config,
            working_dir=working_dir,
            requirements=self._parse_requirements(requirements),
        )

    def _populate_ray_serve_config(
        self,
        import_path: Optional[str] = None,
        arguments: Optional[Dict[str, str]] = None,
        ray_serve_config: Optional[Dict[str, Any]] = None,
        working_dir: Optional[str] = None,
        requirements: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        # Generate a minimal ray_serve_config from the import_path and arguments if needed.
        if ray_serve_config is not None:
            if import_path is not None or arguments is not None:
                raise ValueError(
                    "import_path and arguments cannot be provided with ray_serve_config."
                )

            # Copy to avoid modifying arguments passed directly from user code.
            ray_serve_config = copy.deepcopy(ray_serve_config)
        elif import_path is not None:
            ray_serve_config = {
                "applications": [{"import_path": import_path,}],
            }
            if arguments is not None:
                if not isinstance(arguments, dict):
                    raise TypeError("Application arguments must be a dictionary.")
                ray_serve_config["applications"][0]["arguments"] = arguments
        else:
            raise ValueError("Either import_path or ray_serve_config must be provided.")

        applications = ray_serve_config.get("applications", None)
        if not applications:
            raise ValueError("ray_serve_config must contain a list of applications.")

        ray_serve_config["applications"] = self._override_application_runtime_envs(
            applications, working_dir=working_dir, requirements=requirements,
        )

        return ray_serve_config

    def _parse_requirements(
        self, requirements: Optional[Union[str, List[str]]] = None
    ) -> Optional[List[str]]:
        parsed_requirements = None
        if isinstance(requirements, str):
            parsed_requirements = parse_requirements_file(requirements)
            if parsed_requirements is None:
                raise ValueError(f"Requirements file {requirements} does not exist.")
        elif isinstance(requirements, list):
            # Copy to avoid modifying arguments passed directly from user code.
            parsed_requirements = copy.deepcopy(requirements)

        return parsed_requirements

    def _override_application_runtime_envs(
        self,
        applications: List[Dict[str, Any]],
        *,
        working_dir: Optional[str],
        requirements: Optional[List[str]],
    ):
        """Override the runtime_env field of the provided applications.

        Only the working_dir and requirements fields will be modified.
        """
        applications = copy.deepcopy(applications)
        for application in applications:
            runtime_env = application.get("runtime_env", {})
            if working_dir is not None:
                runtime_env["working_dir"] = working_dir

            if requirements is not None:
                runtime_env["pip"] = requirements

            if runtime_env:
                application["runtime_env"] = runtime_env

        return applications

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(**d)

    @classmethod
    def from_yaml(cls, path: str):
        with open(path) as f:
            return cls.from_dict(yaml.safe_load(f))

    @property
    def name(self) -> Optional[str]:
        # TODO(edoakes): in the future, this should get populated from workspace
        # or default immediately and never be None here.
        return self._name

    @property
    def image(self) -> Optional[str]:
        # TODO(edoakes): in the future, this should get populated from workspace
        # or default immediately and never be None here.
        return self._image

    @property
    def ray_serve_config(self) -> Dict[str, Any]:
        return self._ray_serve_config

    def options(
        self,
        ray_serve_config: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        image: Optional[str] = None,
        working_dir: Optional[str] = None,
        requirements: Optional[Union[str, List[str]]] = None,
    ) -> "ServiceConfig":
        return ServiceConfig(
            ray_serve_config=ray_serve_config or self.ray_serve_config,
            name=name or self.name,
            image=image or self.image,
            working_dir=working_dir,
            requirements=requirements,
        )

    def with_local_dirs_uploaded(
        self, client: AnyscaleClientWrapper
    ) -> "ServiceConfig":
        """Returns a copy of the config with all local dirs converted to remote URIs.

        Local dirs can be specified in the working_dir or py_modules fields of the runtime_env.

        Each unique local directory across these fields will be uploaded once to cloud storage,
        then all occurrences of it in the config will be replaced with the corresponding remote URI.
        """
        cloud_id = client.get_cloud_id()
        new_ray_serve_config = copy.deepcopy(self.ray_serve_config)

        local_path_to_uri: Dict[str, str] = {}

        def _upload_dir_memoized(target: str) -> str:
            if is_dir_remote_uri(target):
                return target
            if target in local_path_to_uri:
                return local_path_to_uri[target]

            logger.info(f"Uploading local dir '{target}' to cloud storage.")
            uri = client.upload_local_dir_to_cloud_storage(target, cloud_id=cloud_id)
            local_path_to_uri[target] = uri
            return uri

        for application in new_ray_serve_config["applications"]:
            working_dir = application.get("runtime_env", {}).get("working_dir", None)
            if working_dir is not None:
                application["runtime_env"]["working_dir"] = _upload_dir_memoized(
                    working_dir
                )

            py_modules = application.get("runtime_env", {}).get("py_modules", None)
            if py_modules is not None:
                new_py_modules = []
                for py_module in py_modules:
                    new_py_modules.append(_upload_dir_memoized(py_module))

                application["runtime_env"]["py_modules"] = new_py_modules

        return self.options(ray_serve_config=new_ray_serve_config)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ServiceConfig):
            return all(
                [
                    self.ray_serve_config == other.ray_serve_config,
                    self.image == other.image,
                    self.name == other.name,
                ]
            )

        return False


class ServiceStatus:
    # TODO: implement __str__ and __repr__.
    def __init__(self):
        pass

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError
