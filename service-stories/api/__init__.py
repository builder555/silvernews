from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import humps

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8001",
    "http://localhost:8001",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    ers = exc.errors()
    errors = []
    for e in ers:
        field_name = humps.decamelize(" > ".join(map(str, e["loc"][1:]))).replace("_", " ")
        err_str = f"{e['msg']}"
        if field_name:
            err_str += f": '{field_name}'"
        errors.append(err_str)
    return JSONResponse(
        status_code=418,
        content=jsonable_encoder({"detail": "; ".join(errors)}),
    )
