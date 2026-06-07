from fastapi import FastAPI
from fastapi import Request
from src.app.database.db import SessionLocal
from src.app.models.asset import Asset
from fastapi.templating import Jinja2Templates
from src.app.api.assets import router as assets_router
from src.app.database.db import Base, engine
from fastapi.responses import RedirectResponse


templates = Jinja2Templates(directory="src/app/templates")

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IT-IMRT API",
    description="API for IT infrastructure monitoring and asset reporting.",
    version="0.1.0-alpha",
)

app.include_router(assets_router)


@app.get("/")
def root():
    return {
        "project": "IT Infrastructure Monitoring & Asset Reporting Tool",
        "status": "running",
        "version": "0.1.0-alpha",
    }

@app.get("/dashboard")
def dashboard(request: Request):

    db = SessionLocal()

    assets = db.query(Asset).all()

    total_assets = len(assets)

    online_assets = len(
        [asset for asset in assets if asset.status.lower() == "online"]
    )

    offline_assets = len(
        [asset for asset in assets if asset.status.lower() == "offline"]
    )

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "assets": assets,
            "total_assets": total_assets,
            "online_assets": online_assets,
            "offline_assets": offline_assets,
        },
    )

@app.get("/assets/delete/{asset_id}")
def delete_asset_web(asset_id: int):

    db = SessionLocal()

    asset = db.query(Asset).filter(
        Asset.id == asset_id
    ).first()

    if asset:
        db.delete(asset)
        db.commit()

    db.close()

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )