from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from .main import honor  # noqa: F401

__version__ = "0.1.1"
__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_honor",
    description="简易查询王者荣耀英雄胜率",
    usage="honor [英雄名]",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_saa"),
    type="application",
    homepage="https://github.com/forchannot/nonebot_plugin_honor",
    extra={
        "author": "forchannot",
        "version": __version__,
    },
)
