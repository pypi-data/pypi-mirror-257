from typing import Any, Dict, Optional

from anyscale.service._private.anyscale_client import (
    AnyscaleClientWrapper,
    RealAnyscaleClient,
)
from anyscale.service.models import ServiceConfig, ServiceStatus


class ServiceSDK:
    def __init__(self, *, client: Optional[AnyscaleClientWrapper] = None):
        self._client = client or RealAnyscaleClient()

    def deploy(
        self,
        config: ServiceConfig,
        *,
        in_place: bool = False,
        canary_percent: Optional[int] = None,
        max_surge_percent: Optional[int] = None,
    ):
        if not isinstance(in_place, bool):
            raise TypeError("in_place must be a bool.")

        if canary_percent is not None:
            if not isinstance(canary_percent, int):
                raise TypeError("canary_percent must be an int.")
            if canary_percent < 0 or canary_percent > 100:
                raise ValueError("canary_percent must be between 0 and 100.")

        if max_surge_percent is not None:
            if not isinstance(max_surge_percent, int):
                raise TypeError("max_surge_percent must be an int.")

            if max_surge_percent < 0 or max_surge_percent > 100:
                raise ValueError("max_surge_percent must be between 0 and 100.")

        config = config.with_local_dirs_uploaded(self._client)
        config_dict: Dict[str, Any] = {
            "ray_serve_config": config.ray_serve_config,
            "rollout_strategy": "IN_PLACE" if in_place else "ROLLOUT",
            "project_id": self._client.get_default_project_id(),
        }
        if config.name is not None:
            config_dict["name"] = config.name
        if config.image is not None:
            config_dict["cluster_env"] = config.image
        if canary_percent is not None:
            config_dict["canary_percent"] = canary_percent
        if max_surge_percent is not None:
            config_dict["max_surge_percent"] = max_surge_percent

        self._client.roll_out_service(config_dict)

    def status(self, name: str) -> ServiceStatus:  # noqa: ARG002
        return ServiceStatus()
