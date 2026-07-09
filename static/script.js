const form = document.getElementById("predictionForm");

form.addEventListener("submit", function(e){

    e.preventDefault();

    document.getElementById("loadingIndicator").classList.remove("hidden");
    document.getElementById("resultSection").classList.add("hidden");
    document.getElementById("errorSection").classList.add("hidden");

    setTimeout(function(){

        document.getElementById("loadingIndicator").classList.add("hidden");

        const income =
        parseFloat(document.getElementById("income_annual").value);

        const loan =
        parseFloat(document.getElementById("loan_amount").value);

        const cibil =
        parseInt(document.getElementById("cibil_score").value);

        const result =
        document.getElementById("resultSection");

        const content =
        document.getElementById("resultContent");

        if(cibil >= 700 && income >= loan){

            result.className = "result-section approved";

            content.innerHTML = `
            <h2>✅ Loan Approved</h2>
            <p>The applicant is likely eligible for the loan.</p>
            `;

        }

        else{

            result.className = "result-section rejected";

            content.innerHTML = `
            <h2>❌ Loan Rejected</h2>
            <p>The applicant is unlikely to qualify for the loan.</p>
            `;

        }

        result.classList.remove("hidden");

    },2000);

});