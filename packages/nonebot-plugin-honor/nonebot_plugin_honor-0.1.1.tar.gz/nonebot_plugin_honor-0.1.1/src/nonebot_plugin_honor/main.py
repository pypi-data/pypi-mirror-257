from nonebot import on_command, require
from nonebot.adapters import Bot, Event, Message
from nonebot.params import CommandArg

from .draw import draw
from .model import HonorWinOrLooseDetail
from .utils import get_honor_info

require("nonebot_plugin_saa")
from nonebot_plugin_saa import Image, MessageFactory, Text  # noqa: E402

honor = on_command("honor", priority=5, block=True, aliases={"查胜率", "英雄胜率"})


@honor.handle()
async def _(ev: Event, bot: Bot, arg: Message = CommandArg()):  # noqa: B008
    honor_name = arg.extract_plain_text().strip()
    wrong_msg_builder = MessageFactory([Text("数据获取失败")])
    try:
        info = await get_honor_info(honor_name)
        if info:
            info = HonorWinOrLooseDetail.parse_obj(info["data"]["cardInfo"])
            msg = MessageFactory(
                [
                    Text(f"{honor_name}的胜率如下，数据来自苏苏的荣耀助手"),
                    Image(draw(info, honor_name)),
                ]
            )
            await msg.send()
        else:
            await wrong_msg_builder.send()
    except Exception:
        await wrong_msg_builder.send()
    finally:
        await honor.finish()
