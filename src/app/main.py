from fastapi import FastAPI, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError

from src.app.api.assets import router as assets_router
from src.app.database.db import Base, SessionLocal, engine
from src.app.models.asset import Asset

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="InfraTrack API",
    description="API para gerenciamento de ativos de TI e monitoramento de infraestrutura",
    version="0.1.0-alpha",
)

app.mount(
    "/static",
    StaticFiles(directory="src/app/static"),
    name="static"
)

templates = Jinja2Templates(directory="src/app/templates")

app.include_router(assets_router)


@app.get("/")
def root():
    return {
        "project": "InfraTrack",
        "status": "running",
        "version": "0.1.0-alpha",
    }


@app.get("/dashboard")
@app.get("/dashboard")
def dashboard(
    request: Request,
    search: str | None = Query(default=None),
    status_filter: str | None = Query(default=None),
    sort_by: str = Query(default="id"),
    order: str = Query(default="asc"),
    error: str | None = Query(default=None),
    success: str | None = Query(default=None),
    
):
    db = SessionLocal()

    query = db.query(Asset)

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Asset.hostname.ilike(search_filter))
            | (Asset.ip_address.ilike(search_filter))
            | (Asset.operating_system.ilike(search_filter))
            | (Asset.asset_type.ilike(search_filter))
            | (Asset.status.ilike(search_filter))
        )

    if status_filter and status_filter != "Todos":
        query = query.filter(Asset.status == status_filter)

    allowed_sort_fields = {
        "id": Asset.id,
        "hostname": Asset.hostname,
        "ip_address": Asset.ip_address,
        "url": Asset.url,
        "operating_system": Asset.operating_system,
        "asset_type": Asset.asset_type,
        "status": Asset.status,
    }

    sort_column = allowed_sort_fields.get(sort_by, Asset.id)

    if order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    assets = query.all()
    all_assets = db.query(Asset).all()

    total_assets = len(all_assets)
    online_assets = len(
        [asset for asset in all_assets if asset.status.lower() == "online"]
    )
    offline_assets = len(
        [asset for asset in all_assets if asset.status.lower() == "offline"]
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
            "search": search or "",
            "sort_by": sort_by,
            "order": order,
            "error": error,
            "success": success,
            "status_filter": status_filter or "Todos",
        },
    )

@app.post("/dashboard/assets/create")
def create_asset_web(
    hostname: str = Form(...),
    ip_address: str = Form(...),
    url: str | None = Form(default=None),
    operating_system: str = Form(...),
    asset_type: str = Form(...),
    status: str = Form(...),
):
    db = SessionLocal()

    hostname = hostname.strip().upper()
    ip_address = ip_address.strip()

    existing_hostname = (
        db.query(Asset)
        .filter(Asset.hostname == hostname)
        .first()
    )

    if existing_hostname:
        db.close()
        return RedirectResponse(
            url="/dashboard?error=Já existe um ativo cadastrado com este nome.",
            status_code=303,
        )

    existing_ip = (
        db.query(Asset)
        .filter(Asset.ip_address == ip_address)
        .first()
    )

    if existing_ip:
        db.close()
        return RedirectResponse(
            url="/dashboard?error=Já existe um ativo cadastrado com este endereço IP.",
            status_code=303,
        )

    new_asset = Asset(
        hostname=hostname,
        ip_address=ip_address,
        url=url,
        operating_system=operating_system,
        asset_type=asset_type,
        status=status,
    )

    try:
        db.add(new_asset)
        db.commit()
    except IntegrityError:
        db.rollback()
        db.close()
        return RedirectResponse(
            url="/dashboard?error=Já existe um ativo cadastrado com este nome ou endereço IP.",
            status_code=303,
        )

    db.close()

    return RedirectResponse(
        url="/dashboard?success=Ativo cadastrado com sucesso.",
        status_code=303,
    )

@app.post("/dashboard/assets/update/{asset_id}")
def update_asset_web(
    asset_id: int,
    hostname: str = Form(...),
    ip_address: str = Form(...),
    url: str | None = Form(default=None),
    operating_system: str = Form(...),
    asset_type: str = Form(...),
    status: str = Form(...),
):
    db = SessionLocal()

    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if asset is None:
        db.close()
        raise HTTPException(status_code=404, detail="Ativo não encontrado")

    hostname = hostname.strip().upper()
    ip_address = ip_address.strip()

    asset.hostname = hostname
    asset.ip_address = ip_address
    asset.url = url
    asset.operating_system = operating_system
    asset.asset_type = asset_type
    asset.status = status

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        db.close()
        return RedirectResponse(
            url="/dashboard?error=Já existe um ativo cadastrado com este nome ou endereço IP.",
            status_code=303,
        )

    db.close()

    return RedirectResponse(
        url="/dashboard?success=Ativo atualizado com sucesso.",
        status_code=303,
    )

@app.post("/dashboard/assets/delete/{asset_id}")
def delete_asset_web(asset_id: int):
    db = SessionLocal()

    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if asset:
        db.delete(asset)
        db.commit()

    db.close()

    return RedirectResponse(
        url="/dashboard?success=Ativo excluído com sucesso.",
        status_code=303,
    )