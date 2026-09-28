import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------------------
# 1. Load cleaned dataset
# -----------------------------------------

df = pd.read_csv("cardekho_cleaned.csv")

print("Dataset Shape:")
print(df.shape)


# -----------------------------------------
# 2. Display first 5 rows
# -----------------------------------------

print("\nFirst 5 rows:")
print(df.head())


# -----------------------------------------
# 3. Dataset information
# -----------------------------------------

print("\nDataset Information:")
print(df.info())


# -----------------------------------------
# 4. Statistical summary
# -----------------------------------------

print("\nStatistical Summary:")
print(df.describe())


# -----------------------------------------
# 5. Unique values in categorical columns
# -----------------------------------------

print("\nNumber of Brands:")
print(df["brand"].nunique())

print("\nBrands:")
print(df["brand"].unique())

print("\nFuel Types:")
print(df["fuel_type"].value_counts())

print("\nTransmission Types:")
print(df["transmission_type"].value_counts())

print("\nSeller Types:")
print(df["seller_type"].value_counts())


# -----------------------------------------
# 6. Missing values
# -----------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())


# -----------------------------------------
# 7. Duplicate values
# -----------------------------------------

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# -----------------------------------------
# 8. Selling price statistics
# -----------------------------------------

print("\nSelling Price:")
print("Minimum:", df["selling_price"].min())
print("Maximum:", df["selling_price"].max())
print("Average:", df["selling_price"].mean())
print("Median:", df["selling_price"].median())


# -----------------------------------------
# 9. Vehicle age statistics
# -----------------------------------------

print("\nVehicle Age:")
print("Minimum:", df["vehicle_age"].min())
print("Maximum:", df["vehicle_age"].max())
print("Average:", df["vehicle_age"].mean())


# -----------------------------------------
# 10. Kilometers driven statistics
# -----------------------------------------

print("\nKilometers Driven:")
print("Minimum:", df["km_driven"].min())
print("Maximum:", df["km_driven"].max())
print("Average:", df["km_driven"].mean())


# -----------------------------------------
# 11. Most common car brands
# -----------------------------------------

print("\nTop 10 Car Brands:")
print(df["brand"].value_counts().head(10))


# -----------------------------------------
# 12. Average price by fuel type
# -----------------------------------------

print("\nAverage Price by Fuel Type:")
print(
    df.groupby("fuel_type")["selling_price"]
    .mean()
    .sort_values(ascending=False)
)


# -----------------------------------------
# 13. Average price by transmission
# -----------------------------------------

print("\nAverage Price by Transmission:")
print(
    df.groupby("transmission_type")["selling_price"]
    .mean()
    .sort_values(ascending=False)
)


# -----------------------------------------
# 14. Plot 1 - Selling Price Distribution
# -----------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(df["selling_price"], bins=50)

plt.title("Selling Price Distribution")
plt.xlabel("Selling Price")
plt.ylabel("Number of Cars")

plt.tight_layout()
plt.show()


# -----------------------------------------
# 15. Plot 2 - Vehicle Age Distribution
# -----------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(df["vehicle_age"], bins=20)

plt.title("Vehicle Age Distribution")
plt.xlabel("Vehicle Age (Years)")
plt.ylabel("Number of Cars")

plt.tight_layout()
plt.show()


# -----------------------------------------
# 16. Plot 3 - Fuel Type Distribution
# -----------------------------------------

plt.figure(figsize=(8, 5))

df["fuel_type"].value_counts().plot(kind="bar")

plt.title("Fuel Type Distribution")
plt.xlabel("Fuel Type")
plt.ylabel("Number of Cars")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


# -----------------------------------------
# 17. Plot 4 - Transmission Distribution
# -----------------------------------------

plt.figure(figsize=(8, 5))

df["transmission_type"].value_counts().plot(kind="bar")

plt.title("Transmission Distribution")
plt.xlabel("Transmission Type")
plt.ylabel("Number of Cars")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()


# -----------------------------------------
# 18. Plot 5 - Price vs Kilometers
# -----------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    df["km_driven"],
    df["selling_price"],
    alpha=0.5
)

plt.title("Selling Price vs Kilometers Driven")
plt.xlabel("Kilometers Driven")
plt.ylabel("Selling Price")

plt.tight_layout()
plt.show()


# -----------------------------------------
# 19. Plot 6 - Price vs Vehicle Age
# -----------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    df["vehicle_age"],
    df["selling_price"],
    alpha=0.5
)

plt.title("Selling Price vs Vehicle Age")
plt.xlabel("Vehicle Age (Years)")
plt.ylabel("Selling Price")

plt.tight_layout()
plt.show()


print("\nEDA completed successfully!")