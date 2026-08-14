from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Inventory
from ..schemas import InventoryResponse


router = APIRouter()


@router.get("/inventory", response_model=list[InventoryResponse])
def get_inventory(db: Session = Depends(get_db)):

    inventory = db.query(Inventory).all()

    return inventory
