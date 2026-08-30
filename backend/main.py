from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
from pathlib import Path


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Bike Resale Price Prediction API",
    description="API for predicting used bike resale prices",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# FILE PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "bike_resale_model.pkl"
BIKE_MASTER_PATH = BASE_DIR / "data" / "bike_master.csv"


# =========================================================
# LOAD MACHINE LEARNING MODEL
# =========================================================

try:

    model = joblib.load(MODEL_PATH)

    print("Machine learning model loaded successfully!")

except Exception as error:

    print("ERROR: Could not load machine learning model.")
    print(error)

    model = None


# =========================================================
# LOAD BIKE MASTER DATABASE
# =========================================================

try:

    bike_master = pd.read_csv(BIKE_MASTER_PATH)

    # Clean column names
    bike_master.columns = (
        bike_master.columns
        .str.strip()
    )

    # Clean brand
    bike_master["brand"] = (
        bike_master["brand"]
        .astype(str)
        .str.strip()
    )

    # Clean model
    bike_master["model"] = (
        bike_master["model"]
        .astype(str)
        .str.strip()
    )

    # Convert engine CC to numeric
    bike_master["engine_cc"] = pd.to_numeric(
        bike_master["engine_cc"],
        errors="coerce"
    )

    # Remove invalid rows
    bike_master = bike_master.dropna(
        subset=[
            "brand",
            "model",
            "engine_cc"
        ]
    )

    # Convert engine CC to integer
    bike_master["engine_cc"] = (
        bike_master["engine_cc"]
        .astype(int)
    )

    print(
        f"Loaded {len(bike_master)} valid bike variants successfully!"
    )

except Exception as error:

    print("ERROR: Could not load bike master database.")
    print(error)

    bike_master = pd.DataFrame(
        columns=[
            "brand",
            "model",
            "engine_cc"
        ]
    )


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Bike Resale Price Prediction API is running!"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {

        "status": "healthy",

        "model_loaded":
            model is not None,

        "bike_master_loaded":
            not bike_master.empty,

        "bike_variants":
            len(bike_master)

    }


# =========================================================
# GET ALL BIKE DATA
# =========================================================

@app.get("/bikes")
def get_bikes():

    bikes = bike_master.to_dict(
        orient="records"
    )

    return {

        "count":
            len(bikes),

        "bikes":
            bikes

    }


# =========================================================
# GET MODELS FOR A BRAND
# =========================================================

@app.get("/models")
def get_models(
    brand: str
):

    brand = brand.strip()

    brand_bikes = bike_master[
        bike_master["brand"].str.lower()
        == brand.lower()
    ]

    if brand_bikes.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                f"No bikes found for brand "
                f"'{brand}'."
            )
        )

    models = (
        brand_bikes["model"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return {

        "brand":
            brand,

        "models":
            models

    }


# =========================================================
# GET ENGINE CC FOR A MODEL
# =========================================================

@app.get("/engine")
def get_engine(
    brand: str,
    model_name: str
):

    brand = brand.strip()
    model_name = model_name.strip()

    matching_bikes = bike_master[
        (
            bike_master["brand"].str.lower()
            == brand.lower()
        )
        &
        (
            bike_master["model"].str.lower()
            == model_name.lower()
        )
    ]

    if matching_bikes.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Bike '{brand} {model_name}' "
                "was not found in the bike database."
            )
        )

    engines = (
        matching_bikes["engine_cc"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return {

        "brand":
            brand,

        "model":
            model_name,

        "engine_cc":
            engines

    }


# =========================================================
# VALIDATE BIKE
# =========================================================

def validate_bike(
    brand,
    model_name,
    engine_cc
):

    try:

        engine_cc = int(engine_cc)

    except:

        return False

    matching_bike = bike_master[
        (
            bike_master["brand"].str.lower()
            == brand.strip().lower()
        )
        &
        (
            bike_master["model"].str.lower()
            == model_name.strip().lower()
        )
        &
        (
            bike_master["engine_cc"]
            == engine_cc
        )
    ]

    return not matching_bike.empty


# =========================================================
# CALCULATE REALISTIC DEPRECIATION
# =========================================================

def calculate_depreciation_rate(
    age_months,
    km_driven,
    owners,
    condition
):

    # -----------------------------------------------------
    # AGE DEPRECIATION
    # -----------------------------------------------------
    #
    # Approximately 8% depreciation per year.
    #
    # Example:
    #
    # 17 months = 1.42 years
    #
    # Age depreciation ≈ 11.3%
    #

    age_years = age_months / 12

    age_depreciation = (
        age_years * 8.0
    )


    # -----------------------------------------------------
    # KILOMETRE DEPRECIATION
    # -----------------------------------------------------
    #
    # 0.5% for every 10,000 km.
    #

    km_depreciation = (
        km_driven / 10000
    ) * 0.5


    # -----------------------------------------------------
    # OWNER DEPRECIATION
    # -----------------------------------------------------
    #
    # First owner = 0%
    # Second owner = 4%
    # Third owner = 8%
    # etc.
    #

    owner_depreciation = (
        max(0, owners - 1) * 4.0
    )


    # -----------------------------------------------------
    # CONDITION DEPRECIATION
    # -----------------------------------------------------

    condition = (
        str(condition)
        .strip()
        .lower()
    )

    condition_depreciation = {

        "excellent": 0.0,

        "good": 1.5,

        "fair": 3.0,

        "poor": 6.0

    }.get(
        condition,
        3.0
    )


    # -----------------------------------------------------
    # TOTAL DEPRECIATION
    # -----------------------------------------------------

    total_rate = (
        age_depreciation
        +
        km_depreciation
        +
        owner_depreciation
        +
        condition_depreciation
    )


    # -----------------------------------------------------
    # SAFETY LIMITS
    # -----------------------------------------------------
    #
    # Never allow:
    #
    # less than 5% depreciation
    #
    # or more than 70% depreciation.
    #

    total_rate = max(
        5.0,
        total_rate
    )

    total_rate = min(
        70.0,
        total_rate
    )


    return total_rate


# =========================================================
# PREDICTION
# =========================================================

@app.get("/predict")
def predict(

    brand: str,

    model_name: str,

    engine_cc: int,

    age_months: int,

    km_driven: int,

    owners: int,

    condition: str,

    launch_price: int

):

    # =====================================================
    # BASIC VALIDATION
    # =====================================================

    if model is None:

        raise HTTPException(
            status_code=500,
            detail=(
                "Machine learning model "
                "is not loaded."
            )
        )


    if engine_cc <= 0:

        raise HTTPException(
            status_code=400,
            detail=(
                "Engine capacity must "
                "be greater than 0."
            )
        )


    if age_months < 1:

        raise HTTPException(
            status_code=400,
            detail=(
                "Bike age must be "
                "at least 1 month."
            )
        )


    if age_months > 180:

        raise HTTPException(
            status_code=400,
            detail=(
                "Bike age cannot "
                "exceed 180 months."
            )
        )


    if km_driven < 0:

        raise HTTPException(
            status_code=400,
            detail=(
                "Kilometers driven "
                "cannot be negative."
            )
        )


    if km_driven > 500000:

        raise HTTPException(
            status_code=400,
            detail=(
                "Kilometers driven "
                "cannot exceed 500,000."
            )
        )


    if owners < 1:

        raise HTTPException(
            status_code=400,
            detail=(
                "Number of owners must "
                "be at least 1."
            )
        )


    if launch_price <= 0:

        raise HTTPException(
            status_code=400,
            detail=(
                "Launch price must "
                "be greater than 0."
            )
        )


    # =====================================================
    # NORMALIZE INPUT
    # =====================================================

    brand = brand.strip()

    model_name = model_name.strip()

    condition = (
        condition
        .strip()
        .lower()
    )


    # =====================================================
    # VALIDATE BRAND + MODEL + ENGINE
    # =====================================================

    if not validate_bike(
        brand,
        model_name,
        engine_cc
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid bike combination: "
                f"{brand} {model_name} "
                f"with {engine_cc} CC."
            )
        )


    # =====================================================
    # CREATE MODEL INPUT
    # =====================================================

    input_data = pd.DataFrame(
        [[

            brand,

            model_name,

            engine_cc,

            age_months,

            km_driven,

            owners,

            condition,

            launch_price

        ]],

        columns=[

            "brand",

            "model",

            "engine_cc",

            "age_months",

            "km_driven",

            "owners",

            "condition",

            "launch_price"

        ]
    )


    # =====================================================
    # MACHINE LEARNING PREDICTION
    # =====================================================

    try:

        prediction = model.predict(
            input_data
        )

        ml_predicted_price = int(
            round(prediction[0])
        )

    except Exception as error:

        print(
            "Prediction error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Machine learning model "
                "could not make a prediction."
            )
        )


    # =====================================================
    # CALCULATE REALISTIC DEPRECIATION
    # =====================================================

    depreciation_rate = (
        calculate_depreciation_rate(

            age_months,

            km_driven,

            owners,

            condition

        )
    )


    # =====================================================
    # CALCULATE MAXIMUM REALISTIC RESALE PRICE
    # =====================================================
    #
    # Example:
    #
    # Launch price = ₹50,000
    #
    # Depreciation = 18.9%
    #
    # Maximum realistic resale:
    #
    # ₹50,000 × (1 - 0.189)
    #
    # = approximately ₹40,550
    #

    maximum_realistic_price = (
        launch_price
        *
        (1 - depreciation_rate / 100)
    )


    # =====================================================
    # FINAL RESALE PRICE
    # =====================================================
    #
    # The ML prediction is still used.
    #
    # But if the ML model predicts an unrealistic
    # value higher than the realistic ceiling,
    # we use the realistic ceiling.
    #

    predicted_price = min(

        ml_predicted_price,

        int(
            round(
                maximum_realistic_price
            )
        )

    )


    # =====================================================
    # EXTRA SAFETY
    # =====================================================
    #
    # Never allow resale price to equal or exceed
    # launch price for a used bike.
    #

    if age_months >= 1:

        predicted_price = min(

            predicted_price,

            launch_price - 1

        )


    # Make sure price never becomes negative

    predicted_price = max(
        1,
        predicted_price
    )


    # =====================================================
    # FINAL ACTUAL DEPRECIATION
    # =====================================================

    depreciation_amount = (
        launch_price
        -
        predicted_price
    )


    depreciation_percentage = (

        depreciation_amount
        /
        launch_price

    ) * 100


    value_retained_percentage = (

        predicted_price
        /
        launch_price

    ) * 100


    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "estimated_resale_price":
            predicted_price,

        "brand":
            brand,

        "model":
            model_name,

        "engine_cc":
            engine_cc,

        "age_months":
            age_months,

        "km_driven":
            km_driven,

        "owners":
            owners,

        "condition":
            condition,

        "launch_price":
            launch_price,

        "ml_predicted_price":
            ml_predicted_price,

        "depreciation_amount":
            round(
                depreciation_amount,
                2
            ),

        "depreciation_percentage":
            round(
                depreciation_percentage,
                2
            ),

        "value_retained_percentage":
            round(
                value_retained_percentage,
                2
            )

    }