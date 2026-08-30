import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

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
# 6. DEFINE MODELS
# ==========================================

models = {
    "Linear Regression": LinearRegression(),

    "Decision Tree": DecisionTreeRegressor(
        random_state=42
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )
}


# ==========================================
# 7. TRAIN AND EVALUATE MODELS
# ==========================================

results = []

print("\n==============================")
print("MODEL COMPARISON")
print("==============================")


for name, model in models.items():

    print(f"\nTraining {name}...")

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    # Train
    pipeline.fit(X_train, y_train)

    # Predict
    y_pred = pipeline.predict(X_test)

    # Metrics
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

    results.append([
        name,
        mae,
        rmse,
        r2
    ])


# ==========================================
# 8. CREATE RESULTS TABLE
# ==========================================

results_df = pd.DataFrame(
    results,
    columns=[
        "Model",
        "MAE",
        "RMSE",
        "R2"
    ]
)


# ==========================================
# 9. SORT BY R²
# ==========================================

results_df = results_df.sort_values(
    by="R2",
    ascending=False
).reset_index(drop=True)


# ==========================================
# 10. DISPLAY RESULTS
# ==========================================

print("\n==============================")
print("FINAL MODEL COMPARISON")
print("==============================")

print(
    results_df.to_string(
        index=False,
        formatters={
            "MAE": "₹{:,.2f}".format,
            "RMSE": "₹{:,.2f}".format,
            "R2": "{:.4f}".format
        }
    )
)


# ==========================================
# 11. BEST MODEL
# ==========================================

best_model = results_df.iloc[0]

print("\n==============================")
print("BEST MODEL")
print("==============================")

print(f"Model : {best_model['Model']}")
print(f"MAE   : ₹{best_model['MAE']:,.2f}")
print(f"RMSE  : ₹{best_model['RMSE']:,.2f}")
print(f"R²    : {best_model['R2']:.4f}")


# ==========================================
# 12. SAVE COMPARISON
# ==========================================

results_df.to_csv(
    "data/model_comparison.csv",
    index=False
)

print("\nComparison saved to:")
print("data/model_comparison.csv")


# ==========================================
# 13. COMPLETE
# ==========================================

print("\n==============================")
print("MODEL COMPARISON COMPLETE")
print("==============================")