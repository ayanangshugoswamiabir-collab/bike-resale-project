import pandas as pd

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("data/used_bikes_clean.csv")

print("Original rows:", len(df))


# ==========================================
# 2. REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates()

print("Rows after removing duplicates:", len(df))


# ==========================================
# 3. RESET INDEX
# ==========================================

df = df.reset_index(drop=True)


# ==========================================
# 4. SAVE CLEAN DATASET
# ==========================================

df.to_csv("data/bikes_model_ready.csv", index=False)


# ==========================================
# 5. FINAL SUMMARY
# ==========================================

print("\n==============================")
print("DATA CLEANING COMPLETE")
print("==============================")

print("Final rows:", len(df))
print("Final columns:", len(df.columns))

print("\nSaved cleaned dataset to:")
print("data/bikes_model_ready.csv")