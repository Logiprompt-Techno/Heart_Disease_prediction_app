document.getElementById("heartForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    let payload = {
        features: {
            age: Number(age.value),
            sex: Number(sex.value),
            cp: Number(cp.value),
            trestbps: Number(trestbps.value),
            chol: Number(chol.value),
            fbs: Number(fbs.value),
            restecg: Number(restecg.value),
            thalach: Number(thalach.value),
            exang: Number(exang.value),
            oldpeak: Number(oldpeak.value),
            slope: Number(slope.value),
            ca: Number(ca.value),
            thal: Number(thal.value)
        }
    };

    let res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(payload)
    });

    let data = await res.json();

    // ---------- Main result ----------
    document.getElementById("result").innerText =
`Prediction   : ${data.prediction}
Risk Score   : ${data.risk_score}%
Risk Level   : ${data.risk_level}`;

    // ---------- Medical reasons ----------
    const reasonsList = document.getElementById("reasons");
    reasonsList.innerHTML = "";
    data.medical_reasons.forEach(r => {
        const li = document.createElement("li");
        li.textContent = r;
        reasonsList.appendChild(li);
    });

    // ---------- Model drivers ----------
    const driversList = document.getElementById("drivers");
    driversList.innerHTML = "";
    data.model_drivers.forEach(d => {
        const li = document.createElement("li");
        li.textContent = d;
        driversList.appendChild(li);
    });
});
