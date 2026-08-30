import pandas as pd

from sklearn.model_selection import train_test_split


# ==========================================
# 1. LOAD CLEAN DATASET
# ==========================================

df = pd.read_csv("data/bikes_model_ready.csv")

print("Dataset loaded successfully!")
print("Total rows:", len(df))


# ==========================================
# 2. DEFINE FEATURES
# ==========================================

features = [
    "brand",
    "model",
    "engine_cc",
    "age_months",
    "km_driven",
    "owners",
    "condition",
    "launch_price"
]


# ==========================================
# 3. DEFINE TARGET
# ==========================================

target = "price"


# ==========================================
# 4. CREATE X AND y
# ==========================================

X = df[features]
y = df[target]


# ==========================================
# 5. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ==========================================
# 6. DISPLAY DATASET SIZES
# ==========================================

print("\n==============================")
print("TRAIN / TEST SPLIT")
print("==============================")

print("\nOriginal dataset:")
print(f"X: {X.shape}")
print(f"y: {y.shape}")

print("\nTraining data:")
print(f"X_train: {X_train.shape}")
print(f"y_train: {y_train.shape}")

print("\nTesting data:")
print(f"X_test: {X_test.shape}")
print(f"y_test: {y_test.shape}")


# ==========================================
# 7. DISPLAY SAMPLE
# ==========================================

print("\n--- X TRAIN SAMPLE ---")
print(X_train.head())

print("\n--- Y TRAIN SAMPLE ---")
print(y_train.head())


# ==========================================
# 8. COMPLETE
# ==========================================

print("\n==============================")
print("TRAIN / TEST SPLIT COMPLETE")
print("==============================")