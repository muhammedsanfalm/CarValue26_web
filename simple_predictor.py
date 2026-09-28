import csv
import math
import os


DATASET_FILE = "cardekho_cleaned.csv"


def load_dataset():
    """Load the cleaned car dataset using Python's built-in csv module."""

    if not os.path.exists(DATASET_FILE):
        raise FileNotFoundError(
            f"{DATASET_FILE} was not found in the project folder."
        )

    with open(DATASET_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def normalize(value, minimum, maximum):
    """Convert a numerical value to a 0-1 range."""

    if maximum == minimum:
        return 0

    return (value - minimum) / (maximum - minimum)


def predict_price(car_data):
    """
    Estimate the car price using similar cars from the cleaned dataset.

    This version does not use NumPy, SciPy or scikit-learn.
    """

    data = load_dataset()

    # Convert numerical columns
    for row in data:
        row["vehicle_age"] = float(row["vehicle_age"])
        row["km_driven"] = float(row["km_driven"])
        row["mileage"] = float(row["mileage"])
        row["engine"] = float(row["engine"])
        row["max_power"] = float(row["max_power"])
        row["seats"] = float(row["seats"])
        row["selling_price"] = float(row["selling_price"])

    # Find ranges for numerical features
    numeric_columns = [
        "vehicle_age",
        "km_driven",
        "mileage",
        "engine",
        "max_power",
        "seats"
    ]

    ranges = {}

    for column in numeric_columns:
        values = [row[column] for row in data]

        ranges[column] = (
            min(values),
            max(values)
        )

    # Calculate similarity score for every car
    scored_cars = []

    for row in data:

        distance = 0

        # Numerical features
        for column in numeric_columns:

            user_value = float(car_data[column])

            minimum, maximum = ranges[column]

            user_normalized = normalize(
                user_value,
                minimum,
                maximum
            )

            row_normalized = normalize(
                row[column],
                minimum,
                maximum
            )

            difference = user_normalized - row_normalized

            distance += difference ** 2

        # Categorical features
        categorical_columns = [
            "brand",
            "model",
            "seller_type",
            "fuel_type",
            "transmission_type"
        ]

        for column in categorical_columns:

            if (
                str(car_data[column]).strip().lower()
                != str(row[column]).strip().lower()
            ):
                distance += 0.15

        distance = math.sqrt(distance)

        scored_cars.append(
            (distance, row["selling_price"])
        )

    # Sort cars by similarity
    scored_cars.sort(key=lambda item: item[0])

    # Use the 10 most similar cars
    nearest_cars = scored_cars[:10]

    if not nearest_cars:
        return 0

    # Weighted average
    total_price = 0
    total_weight = 0

    for distance, price in nearest_cars:

        # Prevent division by zero
        weight = 1 / (distance + 0.001)

        total_price += price * weight
        total_weight += weight

    predicted_price = total_price / total_weight

    return round(predicted_price)