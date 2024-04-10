from bson import ObjectId
from connector.mongo_conn import MongoConnector
from models.cart_model import Cart
from bson.errors import InvalidId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorCollection
import requests


class CartsHandler:
    _collection = None

    def __new__(cls):
        if cls._collection is None:
            cls._collection: AsyncIOMotorCollection = MongoConnector.get_collection()
        return cls._instance

    @classmethod
    async def get_cart(cls, cart_id: str):
        try:
            if cls._collection is None:
                cls._collection = MongoConnector.get_collection()
            cart = await cls._collection.find_one({"_id": ObjectId(cart_id)})
            if cart:
                cart["_id"] = str(cart["_id"])
                cart["products"] = list(map(str, cart["products"]))
            return cart
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ID")

    @classmethod
    async def get_carts(cls, limit: int, offset: int):
        try:
            if cls._collection is None:
                cls._collection = MongoConnector.get_collection()
            carts = await cls._collection.find().skip(offset).limit(limit).to_list(length=None)
            print(carts)
            for cart in carts:
                cart["_id"] = str(cart["_id"])
                cart["products"] = list(map(str, cart["products"]))
            return carts
        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Mongo error")

    @classmethod
    async def add_cart(cls, cart: Cart):
        if cls._collection is None:
            cls._collection = MongoConnector.get_collection()
        for product_id in cart.products:
            if requests.get(f"http://products_api:8080/products/get_product?product_id={product_id}").status_code != 200:
                raise HTTPException(
                    status_code=404, detail=f"Product with id {product_id} not found. Check your cart data and try again")
        if await cls._collection.find_one(filter={"user_id": cart.user_id}):
            raise HTTPException(
                status_code=400, detail="Cart of this user already exists")
        result = await cls._collection.insert_one(cart.model_dump())
        inserted_id = str(result.inserted_id)
        return inserted_id

    @classmethod
    async def change_cart(cls, cart_id: str, cart: Cart):
        try:
            if cls._collection is None:
                cls._collection = MongoConnector.get_collection()
            find_exist = await cls._collection.find_one(filter={"_id": ObjectId(cart_id)})
            if not find_exist:
                raise HTTPException(
                    status_code=404, detail="Cart not found")
            find_with_same_that_updated_name = await cls._collection.find_one(filter={"user_id": cart.user_id})
            if find_with_same_that_updated_name and \
                    "_id" in find_with_same_that_updated_name and \
                    find_with_same_that_updated_name["_id"] != find_exist["_id"]:
                raise HTTPException(
                    status_code=400, detail="Cart with this user id already exists")
            for product_id in cart.products:
                if requests.get(f"http://products_api:8080/products/get_product?product_id={product_id}").status_code != 200:
                    raise HTTPException(
                        status_code=404, detail=f"Product with id {product_id} not found. Check your cart data and try again")
            result = await cls._collection.update_one(filter={"_id": ObjectId(cart_id)}, update={"$set": cart.model_dump()})
            if result.modified_count == 1:
                return True
            elif result.matched_count == 1 and result.modified_count == 0:
                return False
            else:
                raise HTTPException(
                    status_code=404, detail="Cart with this id not found")
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ID")

    @classmethod
    async def delete_cart(cls, cart_id: str):
        try:
            if cls._collection is None:
                cls._collection = MongoConnector.get_collection()
            result = await cls._collection.delete_one(filter={"_id": ObjectId(cart_id)})
            if result.deleted_count == 1:
                return True
            else:
                raise HTTPException(
                    status_code=404, detail="Cart with this id not found")
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid ID")
