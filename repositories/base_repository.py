from datetime import datetime
from enum import Enum
from typing import TypeVar, Generic, Type, List

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

    async def create(self, data_create: dict, raise_exception: bool = True, session=None) -> DBModel:
        print("Creating instance in database")
        created_instance = self._entity_model.model_validate(data_create)
        instance = self.convert_enum_values(created_instance.model_dump())
        instance["_id"] = instance.pop("id")
        await self.collection.insert_one(instance, session=session)
        if not created_instance and raise_exception:
            raise ValueError("Instance not created")
        print("Instance created successfully in database")
        return created_instance

    async def get_by_id(self, _id: str, raise_exception: bool = True) -> DBModel | None:
        print("Getting instance from database")
        instance_found = await self.collection.find_one({"_id": _id, "is_deleted": False})
        if not instance_found and raise_exception:
            raise ValueError("Instance not found")
        print("Instance found successfully in database")
        return self._entity_model.model_validate(instance_found)

    async def get_all(self, raise_exception: bool = True) -> List[DBModel] | None:
        print("Getting all instances from database")
        instances_found = self.collection.find({"is_deleted": False})
        list_instances = await instances_found.to_list()
        if not list_instances and raise_exception:
            raise ValueError("there are no instances")
        instances = []
        for instance in list_instances:
            instances.append(self._entity_model.model_validate(instance))
        print("Instances found successfully in database")
        return instances

    async def patch(self, _id: str, data_update: BaseModel) -> DBModel:
        print("Patching instance in database")
        instance_found = await self.get_by_id(_id)
        data = data_update.model_dump(exclude_unset=True)
        data_copy = instance_found.model_copy(update=data)
        updated_instance = await self.update(_id, data_copy.model_dump())
        print("Instance updated successfully in database")
        return self._entity_model.model_validate(updated_instance)

    async def update(self, _id: str, data_update: dict, raise_exception: bool = True) -> DBModel:
        print("Updating instance in database")
        data_update["updated_at"] = datetime.utcnow()
        data_update["_id"] = data_update.pop("id")
        update = await self.collection.update_one({"_id": _id}, {"$set": data_update})
        if not update and raise_exception:
            raise ValueError("Non updated instance")
        updated_instance = await self.collection.find_one({"_id": _id})
        return self._entity_model.model_validate(updated_instance)

    async def delete(self, _id: str, raise_exception: bool = True) -> None:
        print("Deleting instance from database")
        instance = await self.collection.find_one_and_delete({"_id": _id})
        if not instance and raise_exception:
            raise ValueError("Non deleted instance")
        print("Instance deleted successfully in database")
        return
