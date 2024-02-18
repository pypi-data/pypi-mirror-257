from __future__ import annotations

import importlib
import os
import sys
from functools import lru_cache
from typing import (
    Any,
    Type,
)



__all__ = ("settings",)

import os

# Получаем путь к текущему модулю



class Settings:
    SERVICE_MODULE = "src.config"

    @classmethod
    @lru_cache
    def load(cls) -> Any:

        # Переходим в родительский каталог
        sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
        settings_module = os.environ.get(
            cls.SERVICE_MODULE, "popug_legacy_sdk.config.global_settings"
        )
        module_path = os.path.abspath('../auth/src/config')
        settings_module = "src.config"
        print(os.getcwd())
        # path = os.path.dirname(os.getcwd()).replace("/", ".") + "." + settings_module
        # print(path)
        module = importlib.import_module(module_path)
        # print('s', module)
        # settings_class: Type[BaseSettings] = getattr(module, "Settings")
        # print(settings_class)
        # _settings = settings_class()
        #
        # return _settings


settings = Settings.load()
