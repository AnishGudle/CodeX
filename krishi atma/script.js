const chatMessages = document.getElementById("chat-messages");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const micButton = document.getElementById("mic-button");

function addMessage(sender, message) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(sender === "user" ? "user-message" : "bot-message");
    messageDiv.innerText = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom of the chat container
}

function startListening() {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

        recognition.onresult = function (event) {
            const userMessage = event.results[0][0].transcript;

            addMessage("user", userMessage);

            setTimeout(() => {
                addMessage("bot", "This is a sample bot response.");
            }, 500);
        };

        recognition.start();
    } else {
        alert("Speech recognition is not supported in your browser.");
    }
}

sendButton.addEventListener("click", () => {
    const userMessage = userInput.value;
    if (userMessage.trim() === "") return;

    addMessage("user", userMessage);

    setTimeout(() => {
        addMessage("bot", "This is a sample bot response.");
    }, 500);

    userInput.value = "";
});
document.addEventListener('DOMContentLoaded', function () {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            const dataList = document.getElementById('data-list');
            data.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = 'Name: ${item.name}, Value: ${item.value}';
                dataList.appendChild(listItem);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});