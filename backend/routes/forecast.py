from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Forecast
from ..schemas import ForecastResponse


router = APIRouter()


@router.get(
    "/forecast/{product_id}",
    response_model=list[ForecastResponse]
)
def get_forecast(
    product_id: int,
    db: Session = Depends(get_db)
):

    forecasts = (
        db.query(Forecast)
        .filter(Forecast.product_id == product_id)
        .all()
    )

    return forecasts
