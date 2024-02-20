import dataclasses
from dataclasses import dataclass
from enum import Enum
from typing import Any
class TaskState(Enum):SUSPENDED=1;SCHEDULED=2;RUNNING=3
@dataclass
class Task:name:str;task_id:str;created_on:str='';state:TaskState=TaskState.SUSPENDED;warehouse:str='';database:str='';schema:str='';schedule:str='';definition:str='';properties:dict[str,Any]=dataclasses.field(default_factory=dict)