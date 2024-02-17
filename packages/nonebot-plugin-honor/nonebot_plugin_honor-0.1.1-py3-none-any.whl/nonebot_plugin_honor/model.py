from typing import List

from pydantic import BaseModel


class HonorDetail(BaseModel):
    id: int
    name: str
    img: str
    type: List[int]


class HonorInfo(BaseModel):
    rows: List[HonorDetail]


class HonorWinOrLooseDetail(BaseModel):
    banRate: List[str]
    bpRate: List[str]
    pickRate: List[str]
    winRate: List[str]
