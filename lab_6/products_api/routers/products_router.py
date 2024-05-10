from fastapi import APIRouter, HTTPException
from models.product_model import Product
from products_handler.products_handler import ProductsHandler
from bson.errors import InvalidId
router = APIRouter()


@router.get("/get_product")
async def get_product(product_id: str):
    product = await ProductsHandler.get_product(product_id=product_id)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Product not found")


@router.get("/show_part_of_products")
async def show_part_of_products(limit: int, offset: int):
    products = await ProductsHandler.get_products(limit=limit, offset=offset)
    if limit <= 0 or offset < 0:
        raise HTTPException(
            status_code=400, detail="Offset must be greater than or equal to a zero and limit must be greater than zero")
    if products:
        return products
    else:
        raise HTTPException(status_code=404, detail="Products not found")


@router.post("/add_product")
async def add_message(product: Product):
    try:
        product_id = await ProductsHandler.add_product(product=product)
        return {"message": f"Product {product_id} added successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Problems with adding")


@router.put("/change_product")
async def change_product(product_id: str, product: Product):
    try:
        is_product_updated = await ProductsHandler.change_product(product_id, product)
        if is_product_updated:
            return {"Message": "Product was updated successfully"}
        else:
            return {"Message": "Product before and after update is same, so we didn't change it"}
    except InvalidId as e:
        raise e
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Check data please")


@router.delete("/delete_product")
async def change_product(product_id: str):
    try:
        is_product_deleted = await ProductsHandler.delete_product(product_id)
        if is_product_deleted:
            return {"Message": "Product was successfully deleted"}
        else:
            return {"Message": "Product can't be deleted"}
    except InvalidId as e:
        raise e
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Check data please")
