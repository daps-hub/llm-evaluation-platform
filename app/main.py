from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.admin import router as admin_router
app = FastAPI(
    title="LLM Evaluation Platform",
    version="0.1.0",
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(admin_router)

@app.get("/health")
async def health():
    return {"status": "healthy"}