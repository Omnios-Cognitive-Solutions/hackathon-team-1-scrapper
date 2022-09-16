import os
from configparser import ConfigParser

from dotenv import load_dotenv

from src.utils.toolbox import get_path

load_dotenv()


class Config:
    def __init__(self) -> None:
        self.prefix = "env:"
        self.extension = ".conf"
        self.config = None
        self.path = get_path(__file__, "../config")

    def load(self) -> None:
        if self.config is None:
            self.reload()

    def reload(self) -> None:
        self.config = ConfigParser()

        for file in os.listdir(self.path):
            if file.endswith(self.extension):
                self.config.read(self.path + os.path.sep + file)

    def get(self, section: str, key: str) -> str:
        self.load()

        value = self.config[section][key]

        if value.startswith(self.prefix):
            real_value = os.getenv(value.lstrip(self.prefix))
        else:
            real_value = value

        return real_value

    def set(self, section: str, key: str, value: str) -> None:
        self.load()

        self.config[section][key] = value


config = Config()
