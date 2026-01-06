from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import joblib
import pandas as pd
import shap


app = Flask(__name__)
CORS(app)


# -------- Load Model + SHAP --------
model = joblib.load("heart_model.pkl")
explainer = joblib.load("shap_explainer.pkl")


# -------- Frontend Route --------
@app.route("/")
def home():
    return render_template("landingpg.html")

@app.route("/predict")
def predict_page():
    return render_template("index.html")



# -------- Prediction API --------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json["features"]
    df = pd.DataFrame([data])

    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1] * 100

    if prob < 40:
        risk_level = "Low Risk"
    elif prob < 70:
        risk_level = "Moderate Risk"
    else:
        risk_level = "High Risk"

    prediction_text = "Heart Disease Risk" if pred == 1 else "No Risk"

    # ---- SHAP Explainability ----
    shap_values = explainer(df)

    values = shap_values.values
    flat_values = values.reshape(-1)

    feature_impact = {
        col: float(val)
        for col, val in zip(df.columns, flat_values)
    }

    return jsonify({
        "prediction": prediction_text,
        "risk_score": round(prob, 2),
        "risk_level": risk_level,
        #"explanation": feature_impact
    })
if __name__ == "__main__":
    app.run(debug=True)