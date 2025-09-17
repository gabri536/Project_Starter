from fastapi import FastAPI

app = FastAPI(title="Project Starter API")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Server is up. Try /healthz or /docs"}


@app.get("/healthz")
async def healthz() -> dict[str, bool]:
    return {"ok": True}
