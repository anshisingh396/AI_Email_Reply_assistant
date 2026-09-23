// ======================================
// AI Email Reply Assistant
// ======================================

const emailInput = document.getElementById("email");
const replyOutput = document.getElementById("reply");
const charCount = document.getElementById("charCount");

const generateButton = document.querySelector(".generate");

const toneButtons = document.querySelectorAll(".tone");

const actionButtons = document.querySelectorAll(".actions button");

const copyButton = actionButtons[0];
const clearButton = actionButtons[1];
const regenerateButton = actionButtons[2];


// ======================================
// Selected Tone
// ======================================

let selectedTone = "Formal";


// ======================================
// Character Counter
// ======================================

emailInput.addEventListener("input", function () {
    charCount.textContent = emailInput.value.length;
});


// ======================================
// Tone Selection
// ======================================

toneButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        toneButtons.forEach(function (btn) {
            btn.classList.remove("active");
        });

        button.classList.add("active");

        selectedTone = button.textContent.trim();
    });
});


// ======================================
// Generate Reply
// ======================================

async function generateReply() {
    const email = emailInput.value.trim();

    // Check empty email
    if (email === "") {
        replyOutput.value = "Please enter an email first.";
        return;
    }

    // Loading message
    replyOutput.value = "Generating reply...";

    // Disable button while generating
    generateButton.disabled = true;
    generateButton.textContent = "Generating...";

    try {
        const response = await fetch(
            "http://127.0.0.1:5000/generate-reply",   // ✅ FIXED route
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    tone: selectedTone
                })
            }
        );

        const data = await response.json();

        // Check server error
        if (!response.ok) {
            replyOutput.value =
                data.error || "Something went wrong. Please try again.";
            return;
        }

        // Show AI reply
        replyOutput.value = data.reply;
    } catch (error) {
        console.error(error);
        replyOutput.value =
            "Unable to connect to the backend. Please make sure the server is running.";
    } finally {
        // Enable button again
        generateButton.disabled = false;
        generateButton.textContent = "Generate Reply";
    }
}


// ======================================
// Generate Button
// ======================================

generateButton.addEventListener("click", generateReply);


// ======================================
// Copy Button
// ======================================

copyButton.addEventListener("click", function () {
    if (replyOutput.value.trim() === "") {
        alert("There is no reply to copy.");
        return;
    }

    navigator.clipboard.writeText(replyOutput.value);
    alert("Reply copied!");
});


// ======================================
// Clear Button
// ======================================

clearButton.addEventListener("click", function () {
    emailInput.value = "";
    replyOutput.value = "";
    // Reset character counter
    charCount.textContent = "0";
});


// ======================================
// Regenerate Button
// ======================================

regenerateButton.addEventListener("click", function () {
    generateReply();
});
