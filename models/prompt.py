from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Prompt:
    """
    Represents one prompt flowing through the AgenticAI system.
    """

    id: int

    template: str

    text: str

    strategy: str

    generation: int

    parent_id: Optional[int] = None

    created_at: datetime = field(default_factory=datetime.now)

    score: float = 0.0

    label: str = "Unknown"