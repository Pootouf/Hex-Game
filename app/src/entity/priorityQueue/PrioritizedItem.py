from dataclasses import dataclass, field
from typing import Any

from src.entity.priorityQueue.CustomFloat import CustomFloat


@dataclass(order=True)
class PrioritizedItem:
    priority: CustomFloat
    item: Any=field(compare=False)