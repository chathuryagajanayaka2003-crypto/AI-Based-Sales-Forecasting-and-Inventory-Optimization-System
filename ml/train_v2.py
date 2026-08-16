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


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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


def train_all_products(df):

    print("\n========== ML MODEL V2 ==========\n")

    df = df.copy()

    # ---------------------------------
    # 1. Convert date
    # ---------------------------------

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df = df.dropna(subset=["Order Date"])

    print("Original rows:", len(df))

    # ---------------------------------
    # 2. Product-level daily aggregation
    # ---------------------------------

    daily = (
        df.groupby(
            ["Product ID", "Order Date"]
        )
        .agg({
            "Quantity": "sum",
            "Sales": "sum",
            "Discount": "mean",
            "Category": "first",
            "Sub-Category": "first"
        })
        .reset_index()
    )

    daily = daily.sort_values(
        ["Product ID", "Order Date"]
    )

    print("Daily product rows:", len(daily))

    # ---------------------------------
    # 3. Time features
    # ---------------------------------

    daily["day"] = daily["Order Date"].dt.day

    daily["month"] = daily["Order Date"].dt.month

    daily["day_of_week"] = (
        daily["Order Date"].dt.dayofweek
    )

    daily["quarter"] = (
        daily["Order Date"].dt.quarter
    )

    daily["is_weekend"] = (
        daily["day_of_week"] >= 5
    ).astype(int)

    # ---------------------------------
    # 4. Encode categories
    # ---------------------------------

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

    

    daily["lag_1"] = (
    daily.groupby("Product ID")["Quantity"]
    .shift(1)
    )

    daily["lag_3"] = (
    daily.groupby("Product ID")["Quantity"]
    .shift(3)
    )

    

    daily["rolling_mean_7"] = (
        daily.groupby("Product ID")["Quantity"]
        .transform(
            lambda x:
            x.shift(1).rolling(7).mean()
        )
    )

    daily["rolling_mean_14"] = (
        daily.groupby("Product ID")["Quantity"]
        .transform(
            lambda x:
            x.shift(1).rolling(14).mean()
        )
    )

    daily["rolling_std_7"] = (
        daily.groupby("Product ID")["Quantity"]
        .transform(
            lambda x:
            x.shift(1).rolling(7).std()
        )
    )

    # ---------------------------------
    # 7. Remove NaN
    # ---------------------------------

    daily = daily.dropna()

    print(
        "Rows after feature engineering:",
        len(daily)
    )

    if len(daily) < 50:

        raise ValueError(
            "Not enough rows after feature engineering."
        )

    # ---------------------------------
    # 8. Feature columns
    # ---------------------------------

    feature_cols = [
        "day",
        "month",
        "day_of_week",
        "quarter",
        "is_weekend",
        "cat_encoded",
        "sub_cat_encoded",
        "Discount",
        "lag_1",
        "lag_7",
        "lag_14",
        "rolling_mean_7",
        "rolling_mean_14",
        "rolling_std_7"
    ]

    X = daily[feature_cols]

    y = daily["Quantity"]

    # ---------------------------------
    # 9. Time-based split
    # ---------------------------------

    daily = daily.sort_values(
        "Order Date"
    )

    split_idx = int(
        len(daily) * 0.8
    )

    X = daily[feature_cols]

    y = daily["Quantity"]

    X_train = X.iloc[:split_idx]

    X_test = X.iloc[split_idx:]

    y_train = y.iloc[:split_idx]

    y_test = y.iloc[split_idx:]

    print("\nTraining rows:", len(X_train))

    print("Testing rows:", len(X_test))

    # ---------------------------------
    # 10. Models
    # ---------------------------------

    models = {

        "Random Forest":
            RandomForestRegressor(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ),

        "XGBoost":
            XGBRegressor(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42
            )
    }

    # ---------------------------------
    # 11. Train + evaluate
    # ---------------------------------

    results = {}

    best_model = None

    best_name = None

    best_mae = float("inf")

    for name, model in models.items():

        print(
            f"\nTraining {name}..."
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                predictions
            )
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        results[name] = {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2
        }

        print(
            f"{name}"
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

        if mae < best_mae:

            best_mae = mae

            best_model = model

            best_name = name

    # ---------------------------------
    # 12. Save best model
    # ---------------------------------

    model_package = {

        "model": best_model,

        "model_name": best_name,

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

    # ---------------------------------
    # 13. Save comparison
    # ---------------------------------

    results_df = (
        pd.DataFrame(results)
        .T
    )

    results_df.to_csv(
        RESULT_PATH
    )

    print(
        "\n================================"
    )

    print(
        "BEST MODEL:",
        best_name
    )

    print(
        "Model saved:",
        MODEL_PATH
    )

    print(
        "Results saved:",
        RESULT_PATH
    )

    print(
        "================================\n"
    )

    return results, best_model


if __name__ == "__main__":

    print(
        "Loading dataset..."
    )

    # Encoding fallback for problematic CSV
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

    print(
        "Dataset loaded successfully!"
    )

    print(
        "Dataset Shape:",
        df.shape
    )

    print(
        "\nColumns:"
    )

    print(
        list(df.columns)
    )

    train_all_products(df)