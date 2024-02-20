import json
import logging
import uuid


class Base:
    def __init__(self):
        data = json.loads(open("config.json", "r").read())
        logging.info(f"config info {data}")
        self.username = data["username"]
        self.password = data["password"]
        self.host = data["host"]
        self.__config = data
        self.tmp_dir = "/tmp"

    # 生成一个临时文件
    def generate_file(self, extend: str) -> str:
        return f"{self.tmp_dir}/{str(uuid.uuid4())}.{extend}"

    # 根据路径生成一个新的同名文件
    def generate_file_with_path(self, path: str) -> str:
        return self.generate_file(path.split(".")[-1])

    # 从参数中提取文件路径
    @staticmethod
    def get_path_from_params(data: dict) -> str:
        return json.loads(data['param_data'])['path']

    # 从参数中提取耗时信息
    @staticmethod
    def get_duration_from_params(data: dict) -> float:
        return json.loads(data['param_data'])['duration']

    # 从参数中获取大小信息
    @staticmethod
    def get_size_from_params(data: dict) -> int:
        return json.loads(data['param_data'])['size']

    # 获取配置文件
    def get_config_data(self, key: str):
        return self.__config[key]
