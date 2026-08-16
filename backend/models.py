from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    ForeignKey,
    DateTime,
    func,
)

from .database import Base


# ============================================================
# PRODUCT
# ============================================================

class Product(Base):
    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True
    )

    product_name = Column(
        String(255),
        nullable=False
    )

    category = Column(
        String(100)
    )

    sub_category = Column(
        String(100)
    )


# ============================================================
# SALES
# ============================================================

class Sale(Base):
    __tablename__ = "sales"

    id = Column(
        Integer,
        primary_key=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    sale_date = Column(
        Date,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    sales_amount = Column(
        Numeric(12, 2)
    )

    profit = Column(
        Numeric(12, 2)
    )


# ============================================================
# INVENTORY
# ============================================================

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(
        Integer,
        primary_key=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    current_stock = Column(
        Integer,
        nullable=False
    )

    reorder_level = Column(
        Integer
    )

    safety_stock = Column(
        Integer
    )


# ============================================================
# FORECAST
# ============================================================

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(
        Integer,
        primary_key=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    forecast_date = Column(
        Date,
        nullable=False
    )

    predicted_quantity = Column(
        Numeric(10, 2),
        nullable=False
    )

    model_name = Column(
        String(100)
    )


# ============================================================
# USER
# ============================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        nullable=False,
        default="STAFF"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )