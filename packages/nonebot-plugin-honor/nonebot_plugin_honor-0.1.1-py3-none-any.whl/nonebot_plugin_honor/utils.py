from datetime import datetime

import httpx

from .constant import HEADERS, HONOR_API, HONOR_DETAIL_API
from .model import HonorInfo


async def get_honor_info(name: str):
    time = datetime.now().strftime("%Y-%m-%d")
    async with httpx.AsyncClient(http2=True) as client:
        r = await client.post(
            HONOR_API,
            headers=HEADERS,
            data={"t": time, "openId": "", "accessToken": ""},
        )
    return await __get_honor_win_or_loose_detail(
        HonorInfo.parse_obj(r.json()["data"]["result"]), name
    )


async def __get_honor_win_or_loose_detail(honor_info: HonorInfo, name: str):
    id = next((i.id for i in honor_info.rows if i.name == name), None)
    if not id:
        return
    async with httpx.AsyncClient(http2=True) as client:
        r = await client.post(
            HONOR_DETAIL_API,
            headers=HEADERS,
            data={"openId": "", "accessToken": "", "q": id},
        )
        return r.json()
