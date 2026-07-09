import importlib
import inspect
import pkgutil
from typing import Optional

import plugins as plugins_pkg
from plugins.base import Plugin


class PluginManager:
    def __init__(self):
        self.plugins: list[Plugin] = []
        self._discover()

    def _discover(self) -> None:
        for _, module_name, _ in pkgutil.iter_modules(plugins_pkg.__path__):
            if module_name == "base":
                continue
            module = importlib.import_module(f"plugins.{module_name}")
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Plugin) and obj is not Plugin and obj.__module__ == module.__name__:
                    self.plugins.append(obj())
        self.plugins.sort(key=lambda p: p.priority)

    def find(self, command: str) -> Optional[Plugin]:
        for plugin in self.plugins:
            if plugin.matches(command):
                return plugin
        return None