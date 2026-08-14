from fastapi import FastAPI

from .routes import products
from .routes import sales
from .routes import inventory
from .routes import forecast
from .routes import dashboard


app = FastAPI(
    title="AI Sales Forecasting API",
    description="Sales Forecasting and Inventory Optimization System",
    version="1.0.0"
)


app.include_router(products.router)
app.include_router(sales.router)
app.include_router(inventory.router)
app.include_router(forecast.router)
app.include_router(dashboard.router)


@app.get("/")
def home():

    return {
        "message": "AI Sales Forecasting API is running!"
    }
