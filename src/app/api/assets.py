from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.app.database.db import get_db
from src.app.models.asset import Asset
from src.app.schemas.asset import AssetCreate, AssetResponse

router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
)


@router.post("/", response_model=AssetResponse)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    new_asset = Asset(**asset.model_dump())

    try:
        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="IP address already registered",
        )

    return new_asset


@router.get("/", response_model=list[AssetResponse])
def list_assets(db: Session = Depends(get_db)):
    return db.query(Asset).all()


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    return asset


@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    db.delete(asset)
    db.commit()

    return {
        "message": "Asset deleted successfully",
        "asset_id": asset_id,
    }