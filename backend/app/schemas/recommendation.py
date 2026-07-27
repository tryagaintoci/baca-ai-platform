from pydantic import BaseModel


class Recommendation(BaseModel):

    category: str
    priority: str

    title: str

    description: str

    action: str
