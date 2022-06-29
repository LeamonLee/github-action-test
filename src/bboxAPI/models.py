# from pydantic import BaseModel
# from typing import List

# class generalParam(BaseModel):
#     payload: dict

from enum import Enum, auto

class RFMode(Enum):
    TX      = 0
    RX      = auto()