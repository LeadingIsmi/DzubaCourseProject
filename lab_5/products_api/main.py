from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from routers.products_router import router as product_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

app.include_router(product_router, tags=["Products"], prefix="/products")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    modified_details = []
    for error in details:
        if error["msg"] == "Field required":
            modified_details.append(
                {
                    "message": f"{error["loc"][1]} is absent. Check your data, please",
                }
            )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": modified_details}),
    )
