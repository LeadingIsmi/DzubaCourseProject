from fastapi import FastAPI, HTTPException, Query, Depends, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials, HTTPBasic, HTTPAuthorizationCredentials, HTTPBearer
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import pybreaker
from datetime import datetime
app = FastAPI()


security: HTTPBasicCredentials = HTTPBasic()
security_bearer = HTTPBearer()

circuit_breaker = pybreaker.CircuitBreaker(fail_max=5, reset_timeout=10)


class Cart(BaseModel):
    user_id: int
    products: list[str]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        if error["msg"] == "Field required" or error["msg"] == "missing":
            modified_details.append(
                {
                    "message": f"The field {error["loc"][1]} absent in your request",
                }
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )


def get_token(credentials: HTTPBasicCredentials):
    try:
        response = circuit_breaker.call(
            requests.post,
            "http://users_api:8080/api/users/login",
            auth=(credentials.username, credentials.password)
        )
        if response.status_code >= 500:
            response.raise_for_status()
        return response.json()["access_token"]
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="User service unavailable due to Circuit Breaker")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=400, detail="Check token and try again")


@app.put("/add_product_to_cart")
def get_report(cart_id: str, cart: Cart, credentials: HTTPBasicCredentials = Depends(security)):
    token = get_token(credentials=credentials)
    headers = {"Authorization": f"Bearer {token}"}
    cart_dict = cart.model_dump()
    try:
        response = circuit_breaker.call(
            requests.put,
            f"http://carts_api:8080/carts/change_cart?cart_id={cart_id}",
            headers=headers,
            json=cart_dict
        )
        print(response.json())
        if response.status_code >= 500:
            response.raise_for_status()
        if response.status_code >= 400:
            raise HTTPException(
                status_code=response.status_code, detail=response.json())
        return response.json()
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Reports service unavailable due to Circuit Breaker")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
