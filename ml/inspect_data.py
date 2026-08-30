import pandas as pd

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/used_bikes_clean.csv")


# ==========================================
# 2. BASIC DATASET INFORMATION
# ==========================================

print("\n==============================")
print("BIKE RESALE DATASET INSPECTION")
print("==============================")


# First 5 rows
print("\n--- FIRST 5 ROWS ---")
print(df.head())


# Dataset shape
print("\n--- DATASET SHAPE ---")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")


# Column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())


# Data types
print("\n--- DATA TYPES ---")
print(df.dtypes)


# ==========================================
# 3. MISSING VALUES
# ==========================================

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())


# ==========================================
# 4. DUPLICATE ROWS
# ==========================================

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())


# ==========================================
# 5. UNIQUE VALUES
# ==========================================

# Brands
print("\n--- BRANDS ---")
print(df["brand"].unique())


# Number of brands
print("\n--- NUMBER OF BRANDS ---")
print(df["brand"].nunique())


# Models
print("\n--- NUMBER OF UNIQUE MODELS ---")
print(df["model"].nunique())


# Conditions
print("\n--- CONDITIONS ---")
print(df["condition"].unique())


# ==========================================
# 6. NUMERICAL STATISTICS
# ==========================================

print("\n--- NUMERICAL STATISTICS ---")
print(df.describe())


# ==========================================
# 7. PRICE INFORMATION
# ==========================================

print("\n--- PRICE RANGE ---")

print(f"Minimum price: ₹{df['price'].min():,}")
print(f"Maximum price: ₹{df['price'].max():,}")
print(f"Average price : ₹{df['price'].mean():,.2f}")
print(f"Median price  : ₹{df['price'].median():,.2f}")


# ==========================================
# 8. VALUE VALIDATION
# ==========================================

print("\n--- VALUE VALIDATION ---")


# Negative engine capacity
print(
    "Negative engine CC:",
    (df["engine_cc"] < 0).sum()
)


# Negative bike age
print(
    "Negative age:",
    (df["age_months"] < 0).sum()
)


# Negative kilometers
print(
    "Negative kilometers:",
    (df["km_driven"] < 0).sum()
)


# Invalid number of owners
print(
    "Invalid owners (less than 1):",
    (df["owners"] < 1).sum()
)


# Negative launch prices
print(
    "Negative launch prices:",
    (df["launch_price"] < 0).sum()
)


# Negative resale prices
print(
    "Negative resale prices:",
    (df["price"] < 0).sum()
)


# Resale price higher than launch price
print(
    "Resale price > launch price:",
    (df["price"] > df["launch_price"]).sum()
)


# ==========================================
# 9. RANGE CHECKS
# ==========================================

print("\n--- RANGE CHECKS ---")


print(
    "Age above 15 years:",
    (df["age_months"] > 180).sum()
)


print(
    "Owners above 5:",
    (df["owners"] > 5).sum()
)


print(
    "Kilometers above 200,000:",
    (df["km_driven"] > 200000).sum()
)


# ==========================================
# 10. DATASET SUMMARY
# ==========================================

print("\n==============================")
print("INSPECTION COMPLETE")
print("==============================")