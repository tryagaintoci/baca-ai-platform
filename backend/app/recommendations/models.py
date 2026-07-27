from dataclasses import dataclass


@dataclass(slots=True)
class Recommendation:

    category: str
    priority: str
    title: str
    description: str
    action: str
