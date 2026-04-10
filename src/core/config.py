from pathlib import Path
from typing import Any

import yaml

class YamlConfig:
    def __init__(self) -> None:
        self.config = self._load_config()

    def _load_config(self, path: Path = "config.yaml") -> dict[str, Any]:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)

        return config

    def get_app_version(self) -> float:
        return self.config.get("app").get("version")

    def get_outputs_path(self) -> Path:
        return self.config.get("app").get("output_path")

    def get_proxies_list_path(self) -> str:
        return self.config.get("app").get("proxies_list_path")
