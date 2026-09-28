import os
import joblib

from flask import Flask, render_template, redirect, url_for, session, request, flash

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import os
from dotenv import load_dotenv
from pymongo import MongoClient

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# Load trained car price prediction model
car_price_model = joblib.load("car_price_model.pkl")

# Load .env file
load_dotenv()

app = Flask(__name__)

load_dotenv()

mongo_client = MongoClient(os.getenv("MONGO_URI"))

db = mongo_client["CarValue26"]

users_collection = db["users"]

# Load trained car price prediction model
car_price_model = joblib.load("car_price_model.pkl")
# Secret key for Flask sessions
app.secret_key = os.getenv("SECRET_KEY")

# Google OAuth setup
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile"
    }
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Find user in MongoDB
        user = users_collection.find_one({"email": email})

        if not user:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

        # Check password
        if not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

        # Store user information in session
        session["user"] = {
            "name": user["name"],
            "email": user["email"]
        }

        flash("Login successful!", "success")
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Check required fields
        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        # Check password length
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
            return redirect(url_for("register"))

        # Check password confirmation
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("register"))

        # Check if email already exists
        existing_user = users_collection.find_one({"email": email})

        if existing_user:
            flash("An account with this email already exists.", "error")
            return redirect(url_for("register"))

        # Hash password before storing
        password_hash = generate_password_hash(password)

        # Save user in MongoDB
        users_collection.insert_one({
            "name": name,
            "email": email,
            "password_hash": password_hash
        })

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


# Start Google Login
@app.route("/google/login")
def google_login():
    redirect_uri = url_for("google_callback", _external=True)
    return google.authorize_redirect(redirect_uri)


# Google Login Callback
@app.route("/google/callback")
def google_callback():
    token = google.authorize_access_token()

    user_info = token.get("userinfo")

    if user_info:
        session["user"] = {
            "name": user_info.get("name"),
            "email": user_info.get("email"),
            "picture": user_info.get("picture")
        }

    return redirect(url_for("home"))

@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        brand = request.form.get("brand", "").strip()
        model = request.form.get("model", "").strip()

        year = int(request.form.get("year"))
        kilometers = int(request.form.get("kilometers"))

        seller_type = request.form.get("seller_type")
        fuel_type = request.form.get("fuel_type")
        transmission_type = request.form.get("transmission_type")

        mileage = float(request.form.get("mileage"))
        engine = int(request.form.get("engine"))
        max_power = float(request.form.get("max_power"))
        seats = int(request.form.get("seats"))

        # Convert manufacturing year to vehicle age
        vehicle_age = 2026 - year

        # Create input data
        input_data = {
            "brand": [brand],
            "model": [model],
            "vehicle_age": [vehicle_age],
            "km_driven": [kilometers],
            "seller_type": [seller_type],
            "fuel_type": [fuel_type],
            "transmission_type": [transmission_type],
            "mileage": [mileage],
            "engine": [engine],
            "max_power": [max_power],
            "seats": [seats]
        }

        # Make prediction
        predicted_price = car_price_model.predict(input_data)[0]

        predicted_price = round(predicted_price)

        return render_template(
            "predict.html",
            prediction=predicted_price
        )

    return render_template("predict.html")


    if request.method == "POST":
        brand = request.form.get("brand", "").strip()
        model = request.form.get("model", "").strip()
        year = request.form.get("year", "")
        kilometers = request.form.get("kilometers", "")
        mileage = request.form.get("mileage", "")
        fuel_type = request.form.get("fuel_type", "")
        transmission = request.form.get("transmission", "")
        owners = request.form.get("owners", "")
        service_history = request.form.get("service_history", "")

        # Temporary test
        return f"""
        Brand: {brand}<br>
        Model: {model}<br>
        Year: {year}<br>
        Kilometers: {kilometers}<br>
        Mileage: {mileage}<br>
        Fuel Type: {fuel_type}<br>
        Transmission: {transmission}<br>
        Owners: {owners}<br>
        Service History: {service_history}
        """

    return render_template("predict.html")

# Logout
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/db-test")
def db_test():
    try:
        mongo_client.admin.command("ping")
        return "MongoDB connected successfully!"
    except Exception as e:
        return f"MongoDB connection failed: {e}"


if __name__ == "__main__":
    app.run(debug=True)