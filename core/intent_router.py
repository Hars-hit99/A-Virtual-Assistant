from plugins.base import Plugin
from core.plugin_manager import PluginManager


class IntentRouter:
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager

    def route(self, command: str) -> Plugin:
        plugin = self.plugin_manager.find(command)
        if plugin is None:
            raise RuntimeError(f"No plugin matched command: {command!r}")
        return plugin