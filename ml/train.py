import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor

import joblib


df = pd.read_csv(
    "data/clean_sales.csv",
    encoding="latin1"
)

df["Order Date"] = pd.to_datetime(df["Order Date"])

print("Dataset loaded successfully!")


daily_sales = (
    df.groupby(
        ["Order Date", "Product Name"]
    )["Quantity"]
    .sum()
    .reset_index()
)

print("Daily sales created!")


products = daily_sales["Product Name"].unique()

start_date = daily_sales["Order Date"].min()
end_date = daily_sales["Order Date"].max()

dates = pd.date_range(
    start=start_date,
    end=end_date,
    freq="D"
)

all_combinations = pd.MultiIndex.from_product(
    [products, dates],
    names=["Product Name", "Order Date"]
)

full_data = all_combinations.to_frame(index=False)

daily_sales = full_data.merge(
    daily_sales,
    on=["Product Name", "Order Date"],
    how="left"
)

daily_sales["Quantity"] = (
    daily_sales["Quantity"]
    .fillna(0)
)

daily_sales = daily_sales.sort_values(
    ["Product Name", "Order Date"]
)


print("Complete daily dataset created!")
print("Rows:", len(daily_sales))


daily_sales["day"] = (
    daily_sales["Order Date"].dt.day
)

daily_sales["month"] = (
    daily_sales["Order Date"].dt.month
)

daily_sales["day_of_week"] = (
    daily_sales["Order Date"].dt.dayofweek
)


daily_sales["lag_1"] = (
    daily_sales
    .groupby("Product Name")["Quantity"]
    .shift(1)
)

daily_sales["lag_7"] = (
    daily_sales
    .groupby("Product Name")["Quantity"]
    .shift(7)
)

daily_sales["lag_14"] = (
    daily_sales
    .groupby("Product Name")["Quantity"]
    .shift(14)
)


daily_sales["rolling_mean_7"] = (
    daily_sales
    .groupby("Product Name")["Quantity"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(7)
        .mean()
    )
)

daily_sales["rolling_mean_14"] = (
    daily_sales
    .groupby("Product Name")["Quantity"]
    .transform(
        lambda x:
        x.shift(1)
        .rolling(14)
        .mean()
    )
)


daily_sales = daily_sales.dropna()


print("Feature engineering completed!")

print(
    daily_sales[
        [
            "Order Date",
            "Product Name",
            "Quantity",
            "lag_1",
            "lag_7",
            "lag_14",
            "rolling_mean_7",
            "rolling_mean_14"
        ]
    ].head()
)


features = [
    "day",
    "month",
    "day_of_week",
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_mean_7",
    "rolling_mean_14"
]

X = daily_sales[features]

y = daily_sales["Quantity"]


split_index = int(
    len(daily_sales) * 0.8
)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print()
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))


print()
print("Training Random Forest...")

rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=15,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(
    X_train,
    y_train
)

rf_prediction = rf_model.predict(
    X_test
)


rf_mae = mean_absolute_error(
    y_test,
    rf_prediction
)

rf_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        rf_prediction
    )
)

rf_r2 = r2_score(
    y_test,
    rf_prediction
)


print()
print("===== RANDOM FOREST =====")

print("MAE :", rf_mae)
print("RMSE:", rf_rmse)
print("R2  :", rf_r2)


print()
print("Training XGBoost...")

xgb_model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.03,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    objective="reg:squarederror"
)

xgb_model.fit(
    X_train,
    y_train
)

xgb_prediction = xgb_model.predict(
    X_test
)


xgb_mae = mean_absolute_error(
    y_test,
    xgb_prediction
)

xgb_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        xgb_prediction
    )
)

xgb_r2 = r2_score(
    y_test,
    xgb_prediction
)


print()
print("===== XGBOOST =====")

print("MAE :", xgb_mae)
print("RMSE:", xgb_rmse)
print("R2  :", xgb_r2)


results = pd.DataFrame({

    "Model": [
        "Random Forest",
        "XGBoost"
    ],

    "MAE": [
        rf_mae,
        xgb_mae
    ],

    "RMSE": [
        rf_rmse,
        xgb_rmse
    ],

    "R2": [
        rf_r2,
        xgb_r2
    ]
})


print()
print("==============================")
print("MODEL COMPARISON")
print("==============================")

print(results)


if rf_mae <= xgb_mae:

    best_model = rf_model
    best_model_name = "Random Forest"

else:

    best_model = xgb_model
    best_model_name = "XGBoost"


print()
print("Best Model:", best_model_name)


joblib.dump(
    best_model,
    "ml/sales_model.pkl"
)

print("Best model saved to ml/sales_model.pkl")

print()
print("Best model saved successfully!")

results.to_csv(
    "ml/model_comparison.csv",
    index=False
)

print("Model comparison saved!")