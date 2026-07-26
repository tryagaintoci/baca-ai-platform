from fastapi import HTTPException, status


class BaseService:
    """
    Service de base contenant les opérations CRUD communes.
    Les repositories doivent hériter de BaseRepository.
    """

    object_name = "Object"

    def __init__(self, repository):
        self.repository = repository

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, object_id: int):
        obj = self.repository.get_by_id(object_id)

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.object_name} not found",
            )

        return obj

    def create(self, obj):
        return self.repository.create(obj)

    def update(self, obj):
        return self.repository.update(obj)

    def delete(self, obj):
        return self.repository.delete(obj)
