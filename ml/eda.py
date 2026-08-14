import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv(
    "data/clean_sales.csv",
    encoding="latin1"
)

# Convert Order Date
df["Order Date"] = pd.to_datetime(df["Order Date"])

print("EDA started successfully!")
print("Rows:", len(df))


monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["Order Date"],
    monthly_sales["Sales"],
    marker="o"
)

plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("monthly_sales.png", dpi=300)

plt.show()


daily_sales = (
    df.groupby("Order Date")["Sales"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))

plt.plot(
    daily_sales["Order Date"],
    daily_sales["Sales"]
)

plt.title("Daily Sales")
plt.xlabel("Date")
plt.ylabel("Sales")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("daily_sales.png", dpi=300)

plt.show()


top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

top_products.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig("top_10_products.png", dpi=300)

plt.show()


category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 6))

category_sales.plot(
    kind="bar"
)

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("category_sales.png", dpi=300)

plt.show()


monthly_revenue = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_revenue["Order Date"] = (
    monthly_revenue["Order Date"].astype(str)
)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue["Order Date"],
    monthly_revenue["Sales"],
    marker="o"
)

plt.title("Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("revenue_trend.png", dpi=300)

plt.show()


print("\nAll 5 EDA charts created successfully!")