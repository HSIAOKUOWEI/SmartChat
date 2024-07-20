import { UserMessage, BotMessage } from './showMessages.js';

let isSubmitting = false;

export function bindEvents() {
    $('#chat-form').on('submit', handleFormSubmit);
    $('#chat-input').on('input', adjustTextareaHeight);
    $('#chat-input').on('keypress', handleKeyPress);
}

export function handleFormSubmit(event) {
    event.preventDefault();

    if (isSubmitting) return;

    let userMessage = $('#chat-input').val();
    if (userMessage.trim() === "") return;

    // Append user message to chat window
    UserMessage(userMessage);

    // Clear the input field
    $('#chat-input').val('');
    adjustTextareaHeight();


    // Disable submit button to prevent multiple submissions
    isSubmitting = true;
    $('#chat-form button[type="submit"]').attr('disabled', true);

    // Send user message to server
    sendMessageToServer(userMessage);
}

export function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        $('#chat-form').submit();
    }
}

export function adjustTextareaHeight() {
    let textarea = $('#chat-input');
    textarea.css('height', 'auto');
    let newHeight = Math.min(textarea.prop('scrollHeight'), 200);
    textarea.css('height', newHeight + 'px');
}

function sendMessageToServer(message) {
    $.ajax({
        url: '/chat',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ message: message }),
        success: function(response) {
            BotMessage(response.message);
            // Enable submit button after response
            isSubmitting = false;
            $('#chat-form button[type="submit"]').attr('disabled', false);
        
        },
        error: function() {
            console.error("Error in API request");
            // Enable submit button after response
            isSubmitting = false;
            $('#chat-form button[type="submit"]').attr('disabled', false);
        }
    });
}
