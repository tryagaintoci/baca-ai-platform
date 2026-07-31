from pydantic import BaseModel, ConfigDict


class FarmBase(BaseModel):
    name: str
    location: str


class FarmCreate(FarmBase):
    pass


class FarmUpdate(BaseModel):
    name: str | None = None
    location: str | None = None


class FarmRead(FarmBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)
