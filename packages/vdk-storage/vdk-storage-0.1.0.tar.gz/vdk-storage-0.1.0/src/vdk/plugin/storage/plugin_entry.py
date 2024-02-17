from typing import List

from vdk.api.plugin.hook_markers import hookimpl
from vdk.api.plugin.plugin_registry import IPluginRegistry

@hookimpl
def vdk_start(plugin_registry: IPluginRegistry, command_line_args: List):
    pass



