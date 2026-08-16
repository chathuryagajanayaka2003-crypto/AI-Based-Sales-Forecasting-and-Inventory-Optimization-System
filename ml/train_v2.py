import os
import warnings

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBRegressor


warnings.filterwarnings("ignore")


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "stores_sales_forecasting.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "sales_model_v2.pkl"
)

RESULT_PATH = os.path.join(
    BASE_DIR,
    "ml",
    "model_comparison_v2.csv"
)


# ============================================================
# TRAINING FUNCTION
# ============================================================

def train_all_products(df):

    print()
    print("=" * 60)
    print("              ML MODEL V2")
    print("=" * 60)
    print()

    df = df.copy()

    # ========================================================
    # 1. Validate required columns
    # ========================================================

    required_columns = [
        "Product ID",
        "Order Date",
        "Category",
        "Sub-Category",
        "Sales",
        "Quantity",
        "Discount"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # ========================================================
    # 2. Convert date
    # ========================================================

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "Order Date",
            "Product ID",
            "Quantity"
        ]
    )

    print("Original rows:", len(df))

    # ========================================================
    # 3. Product + Date aggregation
    # ========================================================

    daily = (
        df.groupby(
            [
                "Product ID",
                "Order Date"
            ]
        )
        .agg(
            {
                "Quantity": "sum",
                "Sales": "sum",
                "Discount": "mean",
                "Category": "first",
                "Sub-Category": "first"
            }
        )
        .reset_index()
    )

    daily = daily.sort_values(
        [
            "Product ID",
            "Order Date"
        ]
    ).reset_index(drop=True)

    print(
        "Daily product rows:",
        len(daily)
    )

    # ========================================================
    # 4. Time features
    # ========================================================

    daily["day"] = (
        daily["Order Date"].dt.day
    )

    daily["month"] = (
        daily["Order Date"].dt.month
    )

    daily["day_of_week"] = (
        daily["Order Date"].dt.dayofweek
    )

    daily["quarter"] = (
        daily["Order Date"].dt.quarter
    )

    daily["year"] = (
        daily["Order Date"].dt.year
    )

    daily["is_weekend"] = (
        daily["day_of_week"] >= 5
    ).astype(int)

    # ========================================================
    # 5. Encode categories
    # ========================================================

    category_encoder = LabelEncoder()

    subcategory_encoder = LabelEncoder()

    daily["cat_encoded"] = (
        category_encoder.fit_transform(
            daily["Category"].astype(str)
        )
    )

    daily["sub_cat_encoded"] = (
        subcategory_encoder.fit_transform(
            daily["Sub-Category"].astype(str)
        )
    )

    # ========================================================
    # 6. Product history features
    #
    # IMPORTANT:
    # We use product history separately.
    # ========================================================

    product_group = (
        daily.groupby("Product ID")["Quantity"]
    )

    # Previous observed quantity
    daily["lag_1"] = (
        product_group.shift(1)
    )

    daily["lag_3"] = (
        product_group.shift(3)
    )

    daily["lag_7"] = (
        product_group.shift(7)
    )

    # ========================================================
    # 7. Rolling features
    # ========================================================

    daily["rolling_mean_3"] = (
        daily
        .groupby("Product ID")["Quantity"]
        .transform(
            lambda x:
            x.shift(1)
            .rolling(
                window=3,
                min_periods=2
            )
            .mean()
        )
    )

    daily["rolling_mean_7"] = (
        daily
        .groupby("Product ID")["Quantity"]
        .transform(
            lambda x:
            x.shift(1)
            .rolling(
                window=7,
                min_periods=3
            )
            .mean()
        )
    )

    daily["rolling_std_7"] = (
        daily
        .groupby("Product ID")["Quantity"]
        .transform(
            lambda x:
            x.shift(1)
            .rolling(
                window=7,
                min_periods=3
            )
            .std()
        )
    )

    # ========================================================
    # 8. Remove invalid rows
    # ========================================================

    feature_cols = [
        "day",
        "month",
        "day_of_week",
        "quarter",
        "year",
        "is_weekend",
        "cat_encoded",
        "sub_cat_encoded",
        "Sales",
        "Discount",
        "lag_1",
        "lag_3",
        "lag_7",
        "rolling_mean_3",
        "rolling_mean_7",
        "rolling_std_7"
    ]

    daily = daily.dropna(
        subset=feature_cols + ["Quantity"]
    ).reset_index(drop=True)

    print(
        "Rows after feature engineering:",
        len(daily)
    )

    # ========================================================
    # 9. Safety check
    # ========================================================

    if len(daily) < 50:

        raise ValueError(
            "Not enough rows after feature engineering. "
            f"Only {len(daily)} rows available."
        )

    # ========================================================
    # 10. Sort by date
    # ========================================================

    daily = daily.sort_values(
        "Order Date"
    ).reset_index(drop=True)

    # ========================================================
    # 11. Features + target
    # ========================================================

    X = daily[feature_cols]

    y = daily["Quantity"]

    # ========================================================
    # 12. Time-based train/test split
    # ========================================================

    split_index = int(
        len(daily) * 0.80
    )

    X_train = X.iloc[:split_index]

    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]

    y_test = y.iloc[split_index:]

    print()
    print("=" * 60)
    print("              TRAIN / TEST")
    print("=" * 60)

    print(
        "Training rows:",
        len(X_train)
    )

    print(
        "Testing rows :",
        len(X_test)
    )

    # ========================================================
    # 13. Models
    # ========================================================

    models = {

        "Random Forest":

        RandomForestRegressor(
            n_estimators=200,
            max_depth=12,
            min_samples_split=3,
            random_state=42,
            n_jobs=-1
        ),

        "XGBoost":

        XGBRegressor(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            objective="reg:squarederror"
        )
    }

    # ========================================================
    # 14. Train + evaluate
    # ========================================================

    results = {}

    best_model = None

    best_model_name = None

    best_mae = float("inf")

    print()
    print("=" * 60)
    print("              MODEL RESULTS")
    print("=" * 60)

    for name, model in models.items():

        print()
        print(
            f"Training {name}..."
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        # ----------------------------------------------------
        # MAE
        # ----------------------------------------------------

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        # ----------------------------------------------------
        # RMSE
        # ----------------------------------------------------

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions
            )
        )

        # ----------------------------------------------------
        # R2
        # ----------------------------------------------------

        r2 = r2_score(
            y_test,
            predictions
        )

        results[name] = {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        }

        print()
        print(
            f"{name} Results:"
        )

        print(
            f"MAE  : {mae:.4f}"
        )

        print(
            f"RMSE : {rmse:.4f}"
        )

        print(
            f"R2   : {r2:.4f}"
        )

        # ----------------------------------------------------
        # Best model
        # ----------------------------------------------------

        if mae < best_mae:

            best_mae = mae

            best_model = model

            best_model_name = name

    # ========================================================
    # 15. Save best model
    # ========================================================

    print()
    print("=" * 60)
    print("              BEST MODEL")
    print("=" * 60)

    print(
        "Best Model:",
        best_model_name
    )

    print(
        f"Best MAE  : {best_mae:.4f}"
    )

    model_package = {

        "model": best_model,

        "model_name": best_model_name,

        "feature_cols": feature_cols,

        "label_encoders": {

            "category":
            category_encoder,

            "sub_category":
            subcategory_encoder
        }
    }

    joblib.dump(
        model_package,
        MODEL_PATH
    )

    # ========================================================
    # 16. Save comparison results
    # ========================================================

    results_df = (
        pd.DataFrame(results)
        .T
    )

    results_df.to_csv(
        RESULT_PATH
    )

    # ========================================================
    # 17. Final output
    # ========================================================

    print()
    print("=" * 60)
    print("              TRAINING COMPLETE")
    print("=" * 60)

    print()
    print(
        "Model saved:"
    )

    print(
        MODEL_PATH
    )

    print()
    print(
        "Comparison saved:"
    )

    print(
        RESULT_PATH
    )

    print()
    print("=" * 60)

    return results, best_model


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("Loading dataset...")

    # --------------------------------------------------------
    # Try UTF-8 first
    # --------------------------------------------------------

    try:

        df = pd.read_csv(
            DATA_PATH,
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        print(
            "UTF-8 failed. Trying cp1252..."
        )

        df = pd.read_csv(
            DATA_PATH,
            encoding="cp1252"
        )

    # --------------------------------------------------------
    # Dataset information
    # --------------------------------------------------------

    print(
        "Dataset loaded successfully!"
    )

    print(
        "Dataset Shape:",
        df.shape
    )

    print()

    print(
        "Columns:"
    )

    print(
        df.columns.tolist()
    )

    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    train_all_products(df)