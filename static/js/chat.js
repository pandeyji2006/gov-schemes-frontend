/**
 * Flask Chatbot - Frontend JavaScript
 *
 * This file handles all frontend interactivity for the chat interface:
 * - Loading chat history on page load
 * - Sending messages to backend via AJAX
 * - Displaying messages in the chat area
 * - Auto-scrolling to show latest messages
 * - Event handling (button clicks, Enter key)
 */

// DOM elements
let chatMessages;
let messageInput;
let sendBtn;

/**
 * Initialize the chat interface when page loads
 */
window.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    chatMessages = document.getElementById('chat-messages');
    messageInput = document.getElementById('message-input');
    sendBtn = document.getElementById('send-btn');

    // Focus on input field for immediate typing
    messageInput.focus();

    // Load chat history from server
    loadHistory();

    // Set up event listeners
    setupEventListeners();
});

/**
 * Set up event listeners for user interactions
 */
function setupEventListeners() {
    // Send button click
    sendBtn.addEventListener('click', sendMessage);

    // Enter key in input field
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

/**
 * Load chat history from server and display it
 *
 * Fetches the last 20 messages for the current session from /history endpoint
 * and displays them in chronological order.
 */
function loadHistory() {
    fetch('/history')
        .then(response => response.json())
        .then(data => {
            // Display each message from history
            if (data.messages && data.messages.length > 0) {
                data.messages.forEach(msg => {
                    displayMessage(msg.sender, msg.message);
                });
            }
        })
        .catch(error => {
            console.error('Error loading history:', error);
        });
}

/**
 * Send a message to the chatbot
 *
 * This function:
 * 1. Gets the message from input field
 * 2. Validates it's not empty
 * 3. Displays user message in chat
 * 4. Sends message to backend via POST /chat
 * 5. Displays bot response when received
 */
function sendMessage() {
    // Get message text and trim whitespace
    const message = messageInput.value.trim();

    // Don't send empty messages
    if (!message) {
        return;
    }

    // Display user message immediately
    displayMessage('user', message);

    // Clear input field
    messageInput.value = '';

    // Focus back on input
    messageInput.focus();

    // Send message to backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message
        })
    })
    .then(response => response.json())
    .then(data => {
        // Display bot response
        if (data.response) {
            displayMessage('bot', data.response);
        } else if (data.error) {
            // Display error message as bot message
            displayMessage('bot', 'Sorry, an error occurred: ' + data.error);
        }
    })
    .catch(error => {
        // Display generic error message
        console.error('Error sending message:', error);
        displayMessage('bot', 'Sorry, an error occurred. Please try again.');
    });
}

/**
 * Display a message in the chat area
 *
 * @param {string} sender - Either 'user' or 'bot'
 * @param {string} message - The message text to display
 */
function displayMessage(sender, message) {
    // Create message wrapper div
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + sender;

    // Create message bubble div
    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble';
    bubbleDiv.textContent = message;

    // Append bubble to message wrapper
    messageDiv.appendChild(bubbleDiv);

    // Append message to chat area
    chatMessages.appendChild(messageDiv);

    // Auto-scroll to bottom to show latest message
    scrollToBottom();
}

/**
 * Scroll the chat messages area to the bottom
 *
 * This ensures the latest message is always visible.
 */
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
