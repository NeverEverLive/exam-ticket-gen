from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src import models
from src.exceptions.authentication import AuthenticationException
from src.views.health import router as health_router
from src.views.user import router as user_router
from src.views.subject import router as subject_router
from src.views.module import router as module_router
from src.views.question import router as question_router
from src.views.ticket import router as ticket_router
from src.main import router as main_router

def create_app():
    app = FastAPI(title="Studing ticket", debug=False)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(Exception)
    async def unicorn_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(exc)},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"success": False, "message": str(exc)},
        )

    @app.exception_handler(AuthenticationException)
    async def validation_exception_handler(request: Request, exc: AuthenticationException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message},
        )

    app.include_router(
        health_router,
        prefix="/api",
        tags=["Health check"]
    )

    app.include_router(
        user_router,
        prefix="/api",
        tags=["User"]
    )

    app.include_router(
        subject_router,
        prefix="/api",
        tags=["Subject"]
    )

    app.include_router(
        module_router,
        prefix="/api",
        tags=["Module"]
    )

    app.include_router(
        question_router,
        prefix="/api",
        tags=["Question"]
    )

    app.include_router(
        ticket_router,
        prefix="/api",
        tags=["Ticket"]
    )

    app.include_router(
        main_router,
        prefix="",
        tags=["MAIN"]
    )

    return app
