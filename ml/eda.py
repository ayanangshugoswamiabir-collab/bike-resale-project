import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# ==========================================
# 1. LOAD CLEAN DATASET
# ==========================================

df = pd.read_csv("data/bikes_model_ready.csv")

print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))


# ==========================================
# 2. CREATE PLOTS FOLDER
# ==========================================

os.makedirs("ml/plots", exist_ok=True)


# ==========================================
# 3. BASIC INFORMATION
# ==========================================

print("\n--- DATASET INFORMATION ---")
print(df.info())

print("\n--- NUMERICAL SUMMARY ---")
print(df.describe())


# ==========================================
# 4. PRICE DISTRIBUTION
# ==========================================

plt.figure(figsize=(10, 6))

sns.histplot(
    df["price"],
    bins=30,
    kde=True
)

plt.title("Distribution of Bike Resale Prices")
plt.xlabel("Resale Price (₹)")
plt.ylabel("Number of Bikes")

plt.tight_layout()

plt.savefig(
    "ml/plots/price_distribution.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 5. AGE VS RESALE PRICE
# ==========================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="age_months",
    y="price",
    alpha=0.6
)

plt.title("Bike Age vs Resale Price")
plt.xlabel("Bike Age (Months)")
plt.ylabel("Resale Price (₹)")

plt.tight_layout()

plt.savefig(
    "ml/plots/age_vs_price.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 6. KM DRIVEN VS RESALE PRICE
# ==========================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="km_driven",
    y="price",
    alpha=0.6
)

plt.title("Kilometers Driven vs Resale Price")
plt.xlabel("Kilometers Driven")
plt.ylabel("Resale Price (₹)")

plt.tight_layout()

plt.savefig(
    "ml/plots/km_vs_price.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 7. ENGINE CC VS RESALE PRICE
# ==========================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="engine_cc",
    y="price",
    alpha=0.6
)

plt.title("Engine Size vs Resale Price")
plt.xlabel("Engine Capacity (CC)")
plt.ylabel("Resale Price (₹)")

plt.tight_layout()

plt.savefig(
    "ml/plots/engine_cc_vs_price.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 8. CONDITION VS PRICE
# ==========================================

plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="condition",
    y="price"
)

plt.title("Bike Condition vs Resale Price")
plt.xlabel("Condition")
plt.ylabel("Resale Price (₹)")

plt.tight_layout()

plt.savefig(
    "ml/plots/condition_vs_price.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 9. BRAND VS PRICE
# ==========================================

plt.figure(figsize=(12, 6))

sns.boxplot(
    data=df,
    x="brand",
    y="price"
)

plt.title("Brand vs Resale Price")
plt.xlabel("Brand")
plt.ylabel("Resale Price (₹)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "ml/plots/brand_vs_price.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 10. CORRELATION MATRIX
# ==========================================

numeric_columns = [
    "engine_cc",
    "age_months",
    "km_driven",
    "owners",
    "launch_price",
    "price"
]

correlation = df[numeric_columns].corr()

print("\n--- CORRELATION MATRIX ---")
print(correlation)


plt.figure(figsize=(10, 7))

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm"
)

plt.title("Correlation Matrix")

plt.tight_layout()

plt.savefig(
    "ml/plots/correlation_matrix.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 11. AVERAGE PRICE BY CONDITION
# ==========================================

condition_prices = (
    df.groupby("condition")["price"]
    .mean()
    .sort_values(ascending=False)
)

print("\n--- AVERAGE PRICE BY CONDITION ---")
print(condition_prices)


# ==========================================
# 12. AVERAGE PRICE BY BRAND
# ==========================================

brand_prices = (
    df.groupby("brand")["price"]
    .mean()
    .sort_values(ascending=False)
)

print("\n--- AVERAGE PRICE BY BRAND ---")
print(brand_prices)


# ==========================================
# 13. AGE GROUP ANALYSIS
# ==========================================

df["age_group"] = pd.cut(
    df["age_months"],
    bins=[0, 12, 24, 36, 48, 60, 72, 84, 96],
    labels=[
        "0-1 Year",
        "1-2 Years",
        "2-3 Years",
        "3-4 Years",
        "4-5 Years",
        "5-6 Years",
        "6-7 Years",
        "7-8 Years"
    ]
)

age_prices = (
    df.groupby("age_group", observed=False)["price"]
    .mean()
)

print("\n--- AVERAGE PRICE BY AGE GROUP ---")
print(age_prices)


# ==========================================
# 14. DEPRECIATION CHART
# ==========================================

plt.figure(figsize=(10, 6))

plt.plot(
    age_prices.index.astype(str),
    age_prices.values,
    marker="o"
)

plt.title("Bike Depreciation Curve")
plt.xlabel("Bike Age")
plt.ylabel("Average Resale Price (₹)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "ml/plots/depreciation_curve.png",
    dpi=300
)

plt.show()
plt.close()


# ==========================================
# 15. COMPLETE
# ==========================================

print("\n==============================")
print("EDA COMPLETE")
print("==============================")

print("\nGraphs saved in:")
print("ml/plots/")