from bson import ObjectId
from connector.mongo_conn import MongoConnector
from models.product_model import Product
from bson.errors import InvalidId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection


class ProductsHandler:
    _collection = None

    def __new__(cls):
        if cls._collection is None:
            cls._collection: AsyncIOMotorCollection = MongoConnector.get_collection()
        return cls._instance

    @classmethod
    async def get_product(cls, product_id: str):
        try:
            if cls._collection is None:
                cls._collection = MongoConnector.get_collection()
            product = await cls._collection.find_one({"_id": ObjectId(product_id)})
            if product:
                product["_id"] = str(product["_id"])
            return product
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ID")

    @classmethod
    async def get_products(cls, limit: int, offset: int):
        try:
            if cls._collection is None:
                cls._collection = MongoConnector.get_collection()
            products = await cls._collection.find().skip(offset).limit(limit).to_list(length=None)
            for product in products:
                product["_id"] = str(product["_id"])
            return products
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Mongo error")

    @classmethod
    async def add_product(cls, product: Product):
        if cls._collection is None:
            cls._collection = MongoConnector.get_collection()
        if await cls._collection.find_one(filter={"name": product.name}):
            raise HTTPException(
                status_code=400, detail="Product with this name already exists")
        result = await cls._collection.insert_one(product.model_dump())
        inserted_id = str(result.inserted_id)
        return inserted_id

    @classmethod
    async def change_product(cls, product_id: str, product: Product):
        try:
            if cls._collection is None:
                cls._collection = MongoConnector.get_collection()
            find_exist = await cls._collection.find_one(filter={"_id": ObjectId(product_id)})
            if not find_exist:
                raise HTTPException(
                    status_code=404, detail="Product not found")
            find_with_same_that_updated_name = await cls._collection.find_one(filter={"name": product.name})
            if find_with_same_that_updated_name and \
                    "_id" in find_with_same_that_updated_name and \
                    find_with_same_that_updated_name["_id"] != find_exist["_id"]:
                raise HTTPException(
                    status_code=400, detail="Product with this name already exists")
            result = await cls._collection.update_one(filter={"_id": ObjectId(product_id)}, update={"$set": product.model_dump()})
            if result.modified_count == 1:
                return True
            elif result.matched_count == 1 and result.modified_count == 0:
                return False
            else:
                raise HTTPException(
                    status_code=404, detail="Product with this id not found")
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ID")

    @classmethod
    async def delete_product(cls, product_id: str):
        try:
            if cls._collection is None:
                cls._collection = MongoConnector.get_collection()
            result = await cls._collection.delete_one(filter={"_id": ObjectId(product_id)})
            if result.deleted_count == 1:
                return True
            else:
                raise HTTPException(
                    status_code=404, detail="Product with this id not found")
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ID")
