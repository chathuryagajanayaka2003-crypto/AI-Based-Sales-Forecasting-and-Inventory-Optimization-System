from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Sale
from ..schemas import SaleResponse


router = APIRouter()


@router.get("/sales", response_model=list[SaleResponse])
def get_sales(db: Session = Depends(get_db)):

    sales = db.query(Sale).all()

    return sales
