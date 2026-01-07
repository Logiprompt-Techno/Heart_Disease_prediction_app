document.getElementById("heartForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const features = {
        age: +age.value,
        sex: +sex.value,
        cp: +cp.value,
        trestbps: +trestbps.value,
        chol: +chol.value,
        fbs: +fbs.value,
        restecg: +restecg.value,
        thalach: +thalach.value,
        exang: +exang.value,
        oldpeak: +oldpeak.value,
        slope: +slope.value,
        ca: +ca.value,
        thal: +thal.value
    };

    const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features })
    });

    const data = await res.json();

    document.getElementById("output").classList.remove("hidden");

    const card = document.getElementById("resultCard");
    card.className = "";

    if (data.risk_level === "Low Risk") card.classList.add("low");
    else if (data.risk_level === "Moderate Risk") card.classList.add("moderate");
    else card.classList.add("high");

    document.getElementById("prediction").innerText =
        "Prediction: " + data.prediction;

    document.getElementById("probability").innerText =
        "Risk Score: " + data.risk_score + " %";

    document.getElementById("risk").innerText =
        "Risk Level: " + data.risk_level;
});