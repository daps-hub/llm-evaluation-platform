from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import experiments
from app.api.routes.admin import router as admin_router
from app.api.routes.auth import router as auth_router
from app.api.routes.datasets import router as datasets_router
from app.api.routes.evaluations import router as evaluations_router
from app.api.routes.users import router as users_router


app = FastAPI(
    title="LLM Evaluation Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(evaluations_router)
app.include_router(datasets_router)
app.include_router(experiments.router)


@app.get("/health")
async def health():
    return {"status": "healthy"}