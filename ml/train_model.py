
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.ensemble import GradientBoostingRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/bikes_model_ready.csv")

print("Dataset loaded successfully!")
print("Total rows:", len(df))


# ==========================================
# 2. DEFINE FEATURES AND TARGET
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

target = "price"

X = df[features]
y = df[target]


# ==========================================
# 3. TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


print("\n==============================")
print("TRAIN / TEST SPLIT")
print("==============================")

print("Training rows:", len(X_train))
print("Testing rows :", len(X_test))


# ==========================================
# 4. DEFINE FEATURE TYPES
# ==========================================

categorical_features = [
    "brand",
    "model",
    "condition"
]

numerical_features = [
    "engine_cc",
    "age_months",
    "km_driven",
    "owners",
    "launch_price"
]


# ==========================================
# 5. CREATE PREPROCESSOR
# ==========================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            numerical_features
        ),
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


# ==========================================
# 6. CREATE GRADIENT BOOSTING MODEL
# ==========================================

model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=3,
    random_state=42
)


# ==========================================
# 7. CREATE COMPLETE PIPELINE
# ==========================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ==========================================
# 8. TRAIN MODEL
# ==========================================

print("\n==============================")
print("TRAINING GRADIENT BOOSTING")
print("==============================")

pipeline.fit(X_train, y_train)

print("Model training completed!")


# ==========================================
# 9. MAKE PREDICTIONS
# ==========================================

y_pred = pipeline.predict(X_test)


# ==========================================
# 10. CALCULATE PERFORMANCE
# ==========================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

mse = mean_squared_error(
    y_test,
    y_pred
)

rmse = mse ** 0.5

r2 = r2_score(
    y_test,
    y_pred
)


# ==========================================
# 11. DISPLAY PERFORMANCE
# ==========================================

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"MAE  : ₹{mae:,.2f}")
print(f"RMSE : ₹{rmse:,.2f}")
print(f"R²   : {r2:.4f}")


# ==========================================
# 12. SAMPLE PREDICTIONS
# ==========================================

comparison = pd.DataFrame({
    "Actual Price": y_test.values[:10],
    "Predicted Price": y_pred[:10].round().astype(int)
})

print("\n--- SAMPLE PREDICTIONS ---")

print(comparison.to_string(index=False))


# ==========================================
# 13. SAVE MODEL
# ==========================================

model_path = "models/bike_resale_model.pkl"

joblib.dump(
    pipeline,
    model_path
)

print("\n==============================")
print("MODEL SAVED")
print("==============================")

print("Saved model to:")
print(model_path)


# ==========================================
# 14. COMPLETE
# ==========================================

print("\n==============================")
print("GRADIENT BOOSTING TRAINING COMPLETE")
print("==============================")
