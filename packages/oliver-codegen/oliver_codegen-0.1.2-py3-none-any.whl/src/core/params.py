import logging
import tomllib
from pathlib import Path

# 项目根目录路径
PROJECT_ROOT_PATH: Path = Path(__file__).parent.parent.parent

# pyproject.toml 默认路径
PYPROJECT_TOML_PATH: Path = PROJECT_ROOT_PATH.joinpath("pyproject.toml")


class PyprojectTomlParams:
    """
    解析 pyproject.toml 配置文件内容, 并将必要的参数定义在类中
    """
    def __init__(self, pyproject_toml_path: str | Path = PYPROJECT_TOML_PATH):
        self.pyproject_toml_path: str | Path = pyproject_toml_path
        self.project_name: str = ""
        self.description: str = ""
        self.version: str = ""
        self.debug: bool = False
        self.pyproject_toml_dict: dict | None = None
        self.init()

    def init(self):
        with open(self.pyproject_toml_path, 'rb') as fb:
            self.pyproject_toml_dict = tomllib.load(fb)
            try:
                self.project_name = self.pyproject_toml_dict.get("tool").get("poetry").get("name", "")
                self.description = self.pyproject_toml_dict.get("tool").get("poetry").get("description", "")
                self.version = self.pyproject_toml_dict.get("tool").get("poetry").get("version", "")
                self.debug = self.pyproject_toml_dict.get("project", {}).get("debug", False)
            except KeyError as e:
                logging.warning("解析 pyproject.toml 参数失败, 将使用默认值.", e)


# 实例化 PyprojectTomlParams 让其他模块能直接访问.
pyproject_toml_params: PyprojectTomlParams = PyprojectTomlParams()



