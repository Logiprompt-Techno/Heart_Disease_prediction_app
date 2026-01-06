document.getElementById("heartForm").addEventListener("submit", async (e)=> {
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

    document.getElementById("result").innerText =
`
Prediction   : ${data.prediction}
Risk Score   : ${data.risk_score}
Risk Level   : ${data.risk_level}
`;

    let shapText = "";
    for (let k in data.explanation){
        shapText += `${k} : ${data.explanation[k].toFixed(4)}\n`;
    }

    document.getElementById("shap").innerText = shapText;
});