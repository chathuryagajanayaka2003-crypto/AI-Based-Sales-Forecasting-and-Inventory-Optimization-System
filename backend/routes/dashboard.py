from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from ..models import Product, Sale, Inventory, Forecast


router = APIRouter()


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):

    total_products = db.query(Product).count()

    total_sales = db.query(Sale).count()

    total_inventory = db.query(
        func.coalesce(
            func.sum(Inventory.current_stock),
            0
        )
    ).scalar()

    total_forecasts = db.query(Forecast).count()

    return {
        "total_products": total_products,
        "total_sales": total_sales,
        "total_inventory": total_inventory,
        "total_forecasts": total_forecasts
    }
