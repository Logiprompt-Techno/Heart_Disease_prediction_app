from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import shap

app = Flask(__name__)
CORS(app)

# Load Trained Model and SHAP
model = joblib.load("heart_model.pkl")
explainer = joblib.load("shap_explainer.pkl")

# Frontend Routes
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict-page")
def predict_page():
    return render_template("index.html")

# Prediction API
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json["features"]
    df = pd.DataFrame([data])

    # ---------- Prediction ----------
    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1] * 100

    # ---------- Risk Level ----------
    if prob < 40:
        risk_level = "Low Risk"
    elif prob < 70:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    prediction_text = "Heart Disease Risk" if pred == 1 else "No Risk"

    # SHAP Explainability
    shap_values = explainer(df)
    values = shap_values.values.reshape(-1)

    feature_impact = {
        col: float(val)
        for col, val in zip(df.columns, values)
    }

    # Medical Explanation Engine
    reasons = []

    if data["age"] >= 45:
      reasons.append("Age above 45 increases heart disease risk")

    # Chest pain risk
    if data["cp"] in [1, 2, 3]:
        reasons.append("Abnormal chest pain pattern detected")

    # Exercise angina
    if data["exang"] == 1:
        reasons.append("Exercise-induced chest pain detected")

    # ECG abnormality
    if data["restecg"] != 0:
        reasons.append("Abnormal ECG activity detected")

    # ST depression
    if data["oldpeak"] >= 1:
        reasons.append("ST depression indicates myocardial ischemia")

    # Blocked arteries
    if data["ca"] >= 1:
        reasons.append("Blocked coronary blood vessels detected")

    # Thalassemia
    if data["thal"] in [2, 3]:
        reasons.append("Abnormal thalassemia test detected")

    # Heart rate
    if data["thalach"] <= 140:
        reasons.append("Low maximum heart rate response")

    # Blood pressure
    if data["trestbps"] >= 140:
        reasons.append("High resting blood pressure detected")

    # Cholesterol
    if data["chol"] >= 240:
        reasons.append("High cholesterol detected")

    if prob < 40:
        reasons = ["Overall clinical profile indicates low cardiac risk despite minor symptoms"]

    # Top SHAP Model Drivers
    top_features = sorted(
        feature_impact.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:5]

    shap_drivers = [
        f"{feature} strongly influenced the prediction"
        for feature, value in top_features
    ]

    # Final JSON Response
    return jsonify({
        "prediction": prediction_text,
        "risk_score": round(prob, 2),
        "risk_level": risk_level,
        "medical_reasons": reasons,
        "model_drivers": shap_drivers
    })

# Run Server
if __name__ == "__main__":
    app.run(debug=True)
