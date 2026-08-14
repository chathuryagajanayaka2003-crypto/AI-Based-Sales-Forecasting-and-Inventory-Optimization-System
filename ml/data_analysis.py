import pandas as pd

df = pd.read_csv(
    "data/stores_sales_forecasting.csv",
    encoding="latin1"
)

print("Dataset loaded successfully!")
print()

print("First 5 rows:")
print(df.head())

print()

print("Columns:")
print(df.columns.tolist())

print()

print("Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())


print("\nDuplicate Rows:")
print(df.duplicated().sum())

df = df.drop_duplicates()


df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    errors="coerce"
)

print("\nInvalid Order Dates:")
print(df["Order Date"].isnull().sum())

df = df.dropna(subset=["Order Date"])


print("\nNegative Quantity:")
print((df["Quantity"] < 0).sum())


print("\nNegative Sales:")
print((df["Sales"] < 0).sum())


print("\nSales Statistics:")
print(df["Sales"].describe())

print("\nQuantity Statistics:")
print(df["Quantity"].describe())

print("\nProfit Statistics:")
print(df["Profit"].describe())



print("\nNumber of Products:")
print(df["Product Name"].nunique())


print("\nCategories:")
print(df["Category"].value_counts())

df.to_csv(
    "data/clean_sales.csv",
    index=False
)

print("\nClean dataset saved successfully!")

print("\nFinal Shape:")
print(df.shape)