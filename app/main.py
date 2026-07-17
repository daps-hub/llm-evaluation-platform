from fastapi import FastAPI

from app.api.routes.auth import router as auth_router

app = FastAPI(
    title="LLM Evaluation Platform",
    version="0.1.0",
)

app.include_router(auth_router)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}