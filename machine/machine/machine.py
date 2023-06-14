from dataclasses import dataclass

@dataclass
class Machine:
    id:int=None
    name:str=None
    program:str=None
    rpm:int=None
    x:int=None
    y:int=None
    z:int=None