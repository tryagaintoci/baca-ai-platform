from app.models.crop import Crop
from app.repositories.base_repository import BaseRepository


class CropRepository(BaseRepository):

    model = Crop
