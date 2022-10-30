from pydantic import BaseModel
from typing import List


class Item(BaseModel):
    name: str
    width: float
    height: float
    depth: float
    weight: float
    rotation_type: int
    position: list
    number_of_decimals: int


class Bin(BaseModel):
    name: str
    width: float
    height: float
    depth:  float
    max_weight: float
    items: List
    unfitted_items: List
    number_of_decimals: int
    efficacy: float
    packer_owner: None
