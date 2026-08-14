import pandas as pd
import joblib


model = joblib.load(
    "ml/sales_model.pkl"
)

print("Model loaded successfully!")


input_data = pd.DataFrame({
    "day": [13],
    "month": [8],
    "day_of_week": [3],

    "lag_1": [4],
    "lag_7": [5],
    "lag_14": [6],

    "rolling_mean_7": [4.5],
    "rolling_mean_14": [4.8]
})


prediction = model.predict(
    input_data
)


predicted_quantity = max(
    0,
    prediction[0]
)

print()
print("==============================")
print("SALES FORECAST")
print("==============================")

print(
    "Predicted Quantity:",
    round(predicted_quantity, 2)
)

print("==============================")