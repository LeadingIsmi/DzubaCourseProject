from fastapi import APIRouter, HTTPException, Depends
from models.cart_model import Cart
from carts_handler.carts_handler import CartsHandler
from bson.errors import InvalidId
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
router = APIRouter()


@router.get("/get_cart")
async def get_cart(cart_id: str):
    cart = await CartsHandler.get_cart(cart_id=cart_id)
    if cart:
        return cart
    else:
        raise HTTPException(status_code=404, detail="Cart not found")


@router.get("/show_part_of_carts")
async def show_part_of_carts(limit: int, offset: int):
    carts = await CartsHandler.get_carts(limit=limit, offset=offset)
    if limit <= 0 or offset < 0:
        raise HTTPException(
            status_code=400, detail="Offset must be greater than or equal to a zero and limit must be greater than zero")
    if carts:
        return carts
    else:
        raise HTTPException(status_code=404, detail="Carts not found")


@router.post("/add_cart")
async def add_message(cart: Cart):
    try:
        cart_id = await CartsHandler.add_cart(cart=cart)
        return {"message": f"Cart {cart_id} added successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Problems with adding")


@router.put("/change_cart")
async def change_cart(cart_id: str, cart: Cart, security: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        is_cart_updated = await CartsHandler.change_cart(cart_id, cart, security)
        if is_cart_updated:
            return {"Message": "Cart was updated successfully"}
        else:
            return {"Message": "Cart before and after update is same, so we didn't change it"}
    except InvalidId as e:
        raise e
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Check data please")


@router.delete("/delete_cart")
async def change_cart(cart_id: str):
    try:
        is_cart_deleted = await CartsHandler.delete_cart(cart_id)
        if is_cart_deleted:
            return {"Message": "Cart was successfully deleted"}
        else:
            return {"Message": "Cart can't be deleted"}
    except InvalidId as e:
        raise e
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Check data please")
