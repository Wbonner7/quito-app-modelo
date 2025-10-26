from fastapi import FastAPI

from app.api import router as api_router

app = FastAPI(
    title="Quito Advertiser Platform",
    description="API do MVP do Quito para corretores, imobiliárias e incorporadoras",
    version="0.1.0",
)

app.include_router(api_router)


@app.get("/")
def read_root():
    return {"message": "Quito API"}
