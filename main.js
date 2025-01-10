
async function askMagicBall() {
    const question = document.getElementById("user-question").value;
    console.log(question);
    if (!question) {
        document.getElementById("response").textContent = "Please enter a question!";
        return;
    }


    document.getElementById("response").textContent = "Shaking the Magic Ball...";

    //Send to flask.
    try {
        const response = await fetch("http://127.0.0.1:5000/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        });

        const data = await response.json();
        document.getElementById("response").textContent = data.answer;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("response").textContent = "Something went wrong. Please try again later.";
    }
}
