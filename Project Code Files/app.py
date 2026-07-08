from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load model, scaler, encoders
with open("loan_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)


def encode_input(data):
    encoded = []

    column_order = [
        "Gender",
        "Married",
        "Dependents",
        "Education",
        "Self_Employed",
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Loan_Amount_Term",
        "Credit_History",
        "Property_Area",
    ]

    for col in column_order:
        value = data[col]

        if col in label_encoders:
            le = label_encoders[col]

            if value not in le.classes_:
                value = le.classes_[0]

            value = le.transform([value])[0]
            encoded.append(value)
        else:
            encoded.append(float(value))

    return np.array(encoded).reshape(1, -1)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/predict-page")
def predict_page():
    return render_template("predict.html")


@app.route("/predict", methods=["POST"])
def predict():
    form_data = {
        "Gender": request.form["Gender"],
        "Married": request.form["Married"],
        "Dependents": request.form["Dependents"],
        "Education": request.form["Education"],
        "Self_Employed": request.form["Self_Employed"],
        "ApplicantIncome": request.form["ApplicantIncome"],
        "CoapplicantIncome": request.form["CoapplicantIncome"],
        "LoanAmount": request.form["LoanAmount"],
        "Loan_Amount_Term": request.form["Loan_Amount_Term"],
        "Credit_History": request.form["Credit_History"],
        "Property_Area": request.form["Property_Area"],
    }

    input_data = encode_input(form_data)
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]

    result = "Loan Approved" if prediction == 1 else "Loan Rejected"

    return render_template("submit.html", prediction=result)


if __name__ == "__main__":
    app.run(debug=True)
