import { appendBotMessage } from './showMessages.js';

export function sendMessageToServer(message) {
    $.ajax({
        url: '/chat',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ message: message }),
        success: function(response) {
            appendBotMessage(response.message);
        },
        error: function() {
            console.error("Error in API request");
        }
    });
}