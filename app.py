import os
import joblib
import pandas as pd
from flask import Flask, render_template, request

# ============================================================
# Flask App Configuration
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# ============================================================
# Load Model
# ============================================================

MODEL_PATH = os.path.join(BASE_DIR, "models", "loan_model.pkl")
FEATURE_PATH = os.path.join(BASE_DIR, "models", "feature_names.pkl")

loan_prediction_model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURE_PATH)

print("Model Loaded Successfully")
print("Total Features:", len(feature_names))


# ============================================================
# Routes
# ============================================================

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:

        user_data = pd.DataFrame([{
            "Gender": request.form["gender"],
            "Married": request.form["married"],
            "Dependents": request.form["dependents"],
            "Education": request.form["education"],
            "Self_Employed": request.form["self_employed"],
            "ApplicantIncome": float(request.form["applicant_income"]),
            "CoapplicantIncome": float(request.form["coapplicant_income"]),
            "LoanAmount": float(request.form["loan_amount"]),
            "Loan_Amount_Term": float(request.form["loan_term"]),
            "Credit_History": float(request.form["credit_history"]),
            "Property_Area": request.form["property_area"]
        }])

        print("\nOriginal Input")
        print(user_data)

        encoded_user_data = pd.get_dummies(user_data)

        encoded_user_data = encoded_user_data.reindex(
            columns=feature_names,
            fill_value=0
        )

        print("\nEncoded Input")
        print(encoded_user_data)

        prediction = loan_prediction_model.predict(encoded_user_data)

        print("\nPrediction =", prediction)

        if prediction[0] == 1:
            result = "Approved"
        else:
            result = "Rejected"

        return render_template(
            "result.html",
            prediction=result
        )

    except Exception as e:

        print("\nERROR OCCURRED")
        print(e)

        return f"<h2>Error:</h2><pre>{e}</pre>"


if __name__ == "__main__":
    app.run(debug=True)
