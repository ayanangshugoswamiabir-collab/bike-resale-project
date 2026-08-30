import pandas as pd
import joblib


# ==========================================
# 1. LOAD SAVED MODEL
# ==========================================

model_path = "models/bike_resale_model.pkl"

model = joblib.load(model_path)

print("Saved model loaded successfully!")


# ==========================================
# 2. CREATE TEST BIKE
# ==========================================

bike = pd.DataFrame([
    {
        "brand": "Honda",
        "model": "Shine",
        "engine_cc": 123,
        "age_months": 24,
        "km_driven": 20000,
        "owners": 1,
        "condition": "Good",
        "launch_price": 127140
    }
])


# ==========================================
# 3. DISPLAY BIKE DETAILS
# ==========================================

print("\n==============================")
print("TEST BIKE")
print("==============================")

print(bike.to_string(index=False))


# ==========================================
# 4. PREDICT RESALE PRICE
# ==========================================

prediction = model.predict(bike)

predicted_price = int(round(prediction[0]))


# ==========================================
# 5. DISPLAY PREDICTION
# ==========================================

print("\n==============================")
print("RESALE PRICE PREDICTION")
print("==============================")

print(f"Estimated resale price: ₹{predicted_price:,}")


# ==========================================
# 6. COMPLETE
# ==========================================

print("\n==============================")
print("MODEL TEST COMPLETE")
print("==============================")