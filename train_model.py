import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import joblib


# -----------------------------------------
# 1. Load cleaned dataset
# -----------------------------------------

df = pd.read_csv("cardekho_cleaned.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# -----------------------------------------
# 2. Select features and target
# -----------------------------------------

X = df.drop("selling_price", axis=1)

# car_name is not useful because brand + model already exist
X = X.drop("car_name", axis=1)

y = df["selling_price"]


# -----------------------------------------
# 3. Identify categorical and numerical columns
# -----------------------------------------

categorical_features = [
    "brand",
    "model",
    "seller_type",
    "fuel_type",
    "transmission_type"
]

numerical_features = [
    "vehicle_age",
    "km_driven",
    "mileage",
    "engine",
    "max_power",
    "seats"
]


# -----------------------------------------
# 4. Preprocessing
# -----------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# -----------------------------------------
# 5. Create ML model
# -----------------------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


# -----------------------------------------
# 6. Create pipeline
# -----------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# -----------------------------------------
# 7. Split dataset
# -----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


# -----------------------------------------
# 8. Train model
# -----------------------------------------

print("\nTraining Random Forest model...")

pipeline.fit(X_train, y_train)

print("Model training completed!")


# -----------------------------------------
# 9. Make predictions
# -----------------------------------------

y_pred = pipeline.predict(X_test)


# -----------------------------------------
# 10. Evaluate model
# -----------------------------------------

mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(y_test, y_pred)


print("\n--------------------------------")
print("MODEL EVALUATION")
print("--------------------------------")

print("MAE :", mae)
print("RMSE:", rmse)
print("R²   :", r2)


# -----------------------------------------
# 11. Save trained model
# -----------------------------------------

joblib.dump(
    pipeline,
    "car_price_model.pkl"
)

print("\nModel saved as: car_price_model.pkl")