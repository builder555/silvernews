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
    errors_by_field = {}
    for e in ers:
        field_name = humps.decamelize(" > ".join(e["loc"][1:])).replace("_", " ")
        errors.append(f"{e['msg']}: '{field_name}'")
        errors_by_field[field_name] = e["msg"]
    return JSONResponse(
        status_code=418,
        content=jsonable_encoder({"detail": "; ".join(errors), "errors": errors_by_field}),
    )
