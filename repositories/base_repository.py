from enum import Enum
from typing import TypeVar, Generic, Type, List

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from pydantic import BaseModel

DBModel = TypeVar('DBModel', bound=BaseModel)


class BaseRepository(Generic[DBModel]):
    _entity_model = Type[DBModel]

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection: AsyncIOMotorCollection = db.get_collection(self._entity_model._collection_name.default)

    @staticmethod
    def convert_enum_values(data):
        if isinstance(data, dict):
            return {k: BaseRepository.convert_enum_values(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [BaseRepository.convert_enum_values(item) for item in data]
        elif isinstance(data, Enum):
            return data.value
        else:
            return data

    async def create(self, data: dict, raise_exception: bool = True, session=None) -> DBModel:
        print("Creating instance in database")
        created_instance = self._entity_model.model_validate(data)
        instance = self.convert_enum_values(created_instance.model_dump())
        instance["_id"] = instance.pop("id")
        await self.collection.insert_one(instance, session=session)
        if not created_instance and raise_exception:
            raise ValueError("Instance not created")
        print("Instance created successfully in database")
        return created_instance

    async def get_by_id(self, _id: str, raise_exception: bool = True) -> DBModel | None:
        print("Getting instance from database")
        instance_found = await self.collection.find_one({"_id": _id, "deleted": False})
        if not instance_found and raise_exception:
            raise ValueError("Instance not found")
        print("Instance found successfully in database")
        return self._entity_model.model_validate(instance_found)

    async def get_all(self) -> List[DBModel] | None:
        print("Getting all instances from database")
        instances_found = self.collection.find({"deleted": False})
        list_instances = await instances_found.to_list()
        if not list_instances:
            raise ValueError("there are no instances")
        instances = []
        for instance in list_instances:
            instances.append(self._entity_model.model_validate(instance))
        print("Instances found successfully in database")
        return instances
