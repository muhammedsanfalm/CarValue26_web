import pandas as pd

# -----------------------------------------
# 1. Load the original dataset
# -----------------------------------------

df = pd.read_csv(
    r"C:\Users\sheri\CarValue26_web\cardekho_dataset.csv\cardekho_dataset.csv"
)


print("Original dataset shape:", df.shape)

# -----------------------------------------
# 2. Remove unnecessary index column
# -----------------------------------------

if "Unnamed: 0" in df.columns:
    df.drop("Unnamed: 0", axis=1, inplace=True)

# -----------------------------------------
# 3. Remove duplicate rows
# -----------------------------------------

df.drop_duplicates(inplace=True)

# -----------------------------------------
# 4. Standardize text columns
# -----------------------------------------

text_columns = [
    "car_name",
    "brand",
    "model",
    "seller_type",
    "fuel_type",
    "transmission_type"
]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()

# -----------------------------------------
# 5. Standardize brand names
# -----------------------------------------

df["brand"] = df["brand"].replace({
    "ISUZU": "Isuzu"
})

# -----------------------------------------
# 6. Handle invalid seat values
# -----------------------------------------

# Cars cannot realistically have 0 seats.
df.loc[df["seats"] <= 0, "seats"] = pd.NA

# Remove rows where seats are missing/invalid
df.dropna(subset=["seats"], inplace=True)

# -----------------------------------------
# 7. Check and remove invalid numerical values
# -----------------------------------------

# These values cannot be negative.
numeric_columns = [
    "vehicle_age",
    "km_driven",
    "mileage",
    "engine",
    "max_power",
    "seats",
    "selling_price"
]

for column in numeric_columns:
    df = df[df[column] >= 0]

# -----------------------------------------
# 8. Remove unrealistic mileage values
# -----------------------------------------

# A reasonable range for cars is approximately 5–50 km/l.
df = df[
    (df["mileage"] >= 5) &
    (df["mileage"] <= 50)
]

# -----------------------------------------
# 9. Remove unrealistic engine values
# -----------------------------------------

# Keep realistic passenger-car engine capacities.
df = df[
    (df["engine"] >= 500) &
    (df["engine"] <= 8000)
]

# -----------------------------------------
# 10. Remove unrealistic number of seats
# -----------------------------------------

df = df[
    (df["seats"] >= 2) &
    (df["seats"] <= 10)
]

# -----------------------------------------
# 11. Check missing values
# -----------------------------------------

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# -----------------------------------------
# 12. Final dataset information
# -----------------------------------------

print("\nCleaned dataset shape:", df.shape)

print("\nCleaned dataset:")
print(df.head())

# -----------------------------------------
# 13. Save cleaned dataset
# -----------------------------------------

df.to_csv("cardekho_cleaned.csv", index=False)

print("\nCleaning completed successfully!")
print("Saved as: cardekho_cleaned.csv")