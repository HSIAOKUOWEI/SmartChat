// dialogue_management.js

document.addEventListener('DOMContentLoaded', () => {
    const sidebarContent = document.querySelector('.sidebar-content');
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    let currentDialogueId = null;

    // Function to fetch and display dialogues
    async function fetchAndDisplayDialogues() {
        try {
            const response = await fetch('/get_dialogues');
            const dialogues = await response.json();
            displayDialogues(dialogues);
        } catch (error) {
            console.error('Error fetching dialogues:', error);
        }
    }

    // Function to display dialogues in the sidebar
    function displayDialogues(dialogues) {
        sidebarContent.innerHTML = `
            <button id="newDialogueBtn" class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 mb-4">
                New Dialogue
            </button>
            <div id="dialogueList"></div>
        `;

        const dialogueList = document.getElementById('dialogueList');
        dialogues.forEach(dialogue => {
            const dialogueEl = document.createElement('div');
            dialogueEl.className = 'dialogue-item p-2 hover:bg-gray-200 cursor-pointer relative';
            dialogueEl.innerHTML = `
                <span>${dialogue.title}</span>
                <span class="dialogue-actions hidden absolute right-2 top-2">⋮</span>
            `;
            dialogueEl.dataset.id = dialogue.id;
            dialogueList.appendChild(dialogueEl);

            dialogueEl.addEventListener('click', () => selectDialogue(dialogue.id));
            dialogueEl.addEventListener('mouseenter', showDialogueActions);
            dialogueEl.addEventListener('mouseleave', hideDialogueActions);
        });

        document.getElementById('newDialogueBtn').addEventListener('click', createNewDialogue);
    }

    // Function to show dialogue actions
    function showDialogueActions(event) {
        const actionsEl = event.currentTarget.querySelector('.dialogue-actions');
        actionsEl.classList.remove('hidden');
        actionsEl.addEventListener('click', showDialogueMenu);
    }

    // Function to hide dialogue actions
    function hideDialogueActions(event) {
        const actionsEl = event.currentTarget.querySelector('.dialogue-actions');
        actionsEl.classList.add('hidden');
    }

    // Function to show dialogue menu
    function showDialogueMenu(event) {
        event.stopPropagation();
        const dialogueId = event.target.closest('.dialogue-item').dataset.id;
        const menu = document.createElement('div');
        menu.className = 'absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10';
        menu.innerHTML = `
            <button class="block w-full text-left px-4 py-2 hover:bg-gray-100" data-action="rename">Rename</button>
            <button class="block w-full text-left px-4 py-2 hover:bg-gray-100" data-action="delete">Delete</button>
        `;
        event.target.appendChild(menu);

        menu.addEventListener('click', (e) => handleDialogueAction(e, dialogueId));

        // Close menu when clicking outside
        document.addEventListener('click', closeMenu);
        function closeMenu() {
            menu.remove();
            document.removeEventListener('click', closeMenu);
        }
    }

    // Function to handle dialogue actions
    function handleDialogueAction(event, dialogueId) {
        const action = event.target.dataset.action;
        if (action === 'rename') {
            renameDialogue(dialogueId);
        } else if (action === 'delete') {
            deleteDialogue(dialogueId);
        }
    }

    // Function to rename dialogue
    function renameDialogue(dialogueId) {
        const dialogueEl = document.querySelector(`.dialogue-item[data-id="${dialogueId}"]`);
        const titleSpan = dialogueEl.querySelector('span');
        const currentTitle = titleSpan.textContent;
        
        const input = document.createElement('input');
        input.type = 'text';
        input.value = currentTitle;
        input.className = 'w-full p-1 border rounded';
        
        titleSpan.replaceWith(input);
        input.focus();

        input.addEventListener('blur', updateDialogueTitle);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                updateDialogueTitle();
            }
        });

        function updateDialogueTitle() {
            const newTitle = input.value.trim();
            if (newTitle && newTitle !== currentTitle) {
                fetch(`/update_title/${dialogueId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ new_title: newTitle }),
                })
                .then(response => response.json())
                .then(() => {
                    titleSpan.textContent = newTitle;
                    input.replaceWith(titleSpan);
                })
                .catch(error => {
                    console.error('Error updating dialogue title:', error);
                    input.replaceWith(titleSpan);
                });
            } else {
                input.replaceWith(titleSpan);
            }
        }
    }

    // Function to delete dialogue
    function deleteDialogue(dialogueId) {
        if (confirm('Are you sure you want to delete this dialogue?')) {
            fetch(`/delete_dialogue/${dialogueId}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(() => {
                fetchAndDisplayDialogues();
                if (currentDialogueId === dialogueId) {
                    currentDialogueId = null;
                    chatMessages.innerHTML = '';
                }
            })
            .catch(error => console.error('Error deleting dialogue:', error));
        }
    }

    // Function to select a dialogue
    function selectDialogue(dialogueId) {
        currentDialogueId = dialogueId;
        document.querySelectorAll('.dialogue-item').forEach(el => {
            el.classList.remove('bg-blue-100');
        });
        document.querySelector(`.dialogue-item[data-id="${dialogueId}"]`).classList.add('bg-blue-100');
        fetchDialogueMessages(dialogueId);
    }

    // Function to fetch dialogue messages
    async function fetchDialogueMessages(dialogueId) {
        try {
            const response = await fetch(`/get_messages/${dialogueId}`);
            const messages = await response.json();
            displayMessages(messages);
        } catch (error) {
            console.error('Error fetching dialogue messages:', error);
        }
    }

    // Function to display messages
    function displayMessages(messages) {
        chatMessages.innerHTML = '';
        messages.forEach(message => {
            if (message.role === 'user') {
                displayUserMessage(message.content);
            } else {
                displayBotMessage(message.content);
            }
        });
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to create a new dialogue
    function createNewDialogue() {
        currentDialogueId = null;
        chatMessages.innerHTML = '';
        document.querySelectorAll('.dialogue-item').forEach(el => {
            el.classList.remove('bg-blue-100');
        });
    }

    // Modify sendMessage function to include dialogueId
    const originalSendMessage = window.sendMessage;
    window.sendMessage = function(message = null, botMessageDiv = null, retryButton = null, isRetry = false) {
        const dialogueId = currentDialogueId;
        // Call the original sendMessage function with the additional dialogueId parameter
        originalSendMessage(message, botMessageDiv, retryButton, isRetry, dialogueId);
    };

    // Initialize dialogue management
    fetchAndDisplayDialogues();

    // Event listener for send button
    sendButton.addEventListener('click', () => {
        if (!window.isWaitingForResponse) {
            window.sendMessage();
        }
    });

    // Event listener for user input
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            window.sendMessage();
        }
    });
});