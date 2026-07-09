# quick_test.py, run once, then delete
from core.plugin_manager import PluginManager

pm = PluginManager()
print([p.name for p in pm.plugins])