# ============================================================
# Smart Lender - Loan Eligibility Prediction Web Application
# ============================================================

# =========================
# Import Required Libraries
# =========================

import os
from flask import Flask, render_template, request
import pandas as pd
import joblib

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# ============================================================
# Load Trained Model and Feature Names
# ============================================================

def load_model():
    try:
        model_path = os.path.join(BASE_DIR, "models", "loan_model.pkl")
        trained_model = joblib.load(model_path)
        print("Model loaded successfully.")
        return trained_model
    except FileNotFoundError:
        print("Error: Model file not found.")
        return None


def load_feature_names():
    try:
        feature_path = os.path.join(BASE_DIR, "models", "feature_names.pkl")
        feature_columns = joblib.load(feature_path)
        print("Feature names loaded successfully.")
        return feature_columns
    except FileNotFoundError:
        print("Error: Feature names file not found.")
        return None
loan_prediction_model = load_model()
feature_names = load_feature_names()

# ============================================================
# Home Page
# ============================================================

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/home")
def home():
    return render_template("index.html")

# ============================================================
# Prediction Route
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict loan eligibility based on user input.
    """

    try:

        # Read form data
        form_data = request.form

        # Create dataframe using user input
        user_data = pd.DataFrame({

            "Gender": [form_data["gender"]],
            "Married": [form_data["married"]],
            "Dependents": [form_data["dependents"]],
            "Education": [form_data["education"]],
            "Self_Employed": [form_data["self_employed"]],

            "ApplicantIncome": [
                float(form_data["applicant_income"])
            ],

            "CoapplicantIncome": [
                float(form_data["coapplicant_income"])
            ],

            "LoanAmount": [
                float(form_data["loan_amount"])
            ],

            "Loan_Amount_Term": [
                float(form_data["loan_term"])
            ],

            "Credit_History": [
                float(form_data["credit_history"])
            ],

            "Property_Area": [
                form_data["property_area"]
            ]

        })

        # Convert categorical variables into dummy variables
        encoded_user_data = pd.get_dummies(user_data)

        # Match the exact feature order used during training
        encoded_user_data = encoded_user_data.reindex(
            columns=feature_names,
            fill_value=0
        )

        # Generate prediction
        prediction = loan_prediction_model.predict(encoded_user_data)

        # Display readable result
        if prediction[0] == 1:
           return render_template(
        "result.html",
        prediction="Approved"
    )
        else:
           return render_template(
        "result.html",
        prediction="Rejected"
    )

    except ValueError:

        return render_template(
            "result.html",
            prediction="Rejected"
        )

    except Exception as error:

        return render_template(
            "result.html",
            prediction="Rejected"
        )


# ============================================================
# Run Flask Application
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)
