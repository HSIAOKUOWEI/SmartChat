document.addEventListener('DOMContentLoaded', () => {
    
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const attachButton = document.getElementById('attachButton');
    const fileInput = document.getElementById('fileInput');
    const attachments = document.getElementById('attachments');
    const toggleApiKey = document.getElementById('toggleApiKey');
    const apiKeyInput = document.getElementById('apiKey');
    const modelSelect = document.getElementById('modelSelect');


    let isApiKeyVisible = false;
    let uploadedFiles = [];
    let isWaitingForResponse = false; // New variable to track if we're waiting for a response


    if (typeof hljs === 'undefined') {
        console.error('highlight.js is not loaded');
    } else {
        hljs.configure({ ignoreUnescapedHTML: true });
    }
    
    
    // Function to adjust textarea height
    function adjustTextareaHeight() {
        userInput.style.height = 'auto';
        userInput.style.height = (userInput.scrollHeight > 200 ? 200 : userInput.scrollHeight) + 'px';
    }

    // Function to send message
    async function sendMessage(message = null, botMessageDiv = null, retryButton = null, isRetry = false) {
        if (isWaitingForResponse) return; // If waiting for a response, don't send a new message
        isWaitingForResponse = true; // Set waiting flag

        sendButton.disabled = true;

        if (retryButton) {
            retryButton.style.backgroundColor = 'lightgray'; // Disable Retry button visually
        }

        if (!message) {
            message = userInput.value.trim();
        }

        if (message === '' && uploadedFiles.length === 0) {
            sendButton.disabled = false;
            isWaitingForResponse = false; // Reset waiting flag if no message to send
            if (retryButton) {
                retryButton.style.backgroundColor = ''; // Enable Retry button visually
            }
            return;
        }


        // Display user message only if not retrying
        if (!botMessageDiv && !isRetry) {
            displayUserMessage(message, uploadedFiles);
        } else if (isRetry) {
            // Clear all messages after the retried message
            while (botMessageDiv.nextSibling) {
                chatMessages.removeChild(botMessageDiv.nextSibling);
            }
        }

        // Clear input and attachments only if not retrying
        if (!botMessageDiv && !isRetry) {
            userInput.value = '';
            fileInput.value = '';
            attachments.innerHTML = '';
            adjustTextareaHeight();
        }

        // Prepare form data
        const formData = new FormData();
        formData.append('message', message);

        // Process files
        for (const file of uploadedFiles) {
            if (file.type.startsWith('image/')) {
                const imageUrl = URL.createObjectURL(file);
                formData.append('images', imageUrl);
            } else {
                formData.append('files', file);
            }
        }

        // Create or clear bot message div
        if (!botMessageDiv) {
            botMessageDiv = document.createElement('div');
            botMessageDiv.classList.add('mb-4', 'p-2', 'rounded', 'text-left', 'bg-gray-100', 'max-w-full', 'break-words', 'flex');
            chatMessages.appendChild(botMessageDiv);
        } else {
            botMessageDiv.innerHTML = '';
        }

        // Add loading spinner
        const spinnerDiv = document.createElement('div');
        spinnerDiv.classList.add('loading-spinner', 'mr-2');
        spinnerDiv.innerHTML = `
            <svg class="animate-spin h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
        `;
        botMessageDiv.appendChild(spinnerDiv);

        try {
            const response = await fetch('/agent_chat', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            let botMessage = '';
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                const chunk = decoder.decode(value, { stream: true });
                botMessage += chunk;
                displayBotMessage(botMessage, botMessageDiv, false);
            }

            // Remove loading spinner
            spinnerDiv.remove();

            // After full message is received, display with buttons
            displayBotMessage(botMessage, botMessageDiv, true);

        } catch (error) {
            console.error('Error:', error);
            displayBotMessage('An error occurred while processing your request.');
        } finally {
            uploadedFiles = [];
            sendButton.disabled = false;
            isWaitingForResponse = false; // Reset waiting flag
            if (retryButton) {
                retryButton.classList.remove('disabled');
                retryButton.style.backgroundColor = ''; // Enable Retry button visually
                retryButton.style.cursor = 'pointer';
            }
        }
    }

    // Function to display user message
    function displayUserMessage(message, files = []) {
        const messageWrapper = document.createElement('div');
        messageWrapper.classList.add('mb-4', 'flex', 'justify-end', 'clear-both');

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('p-2', 'rounded', 'bg-blue-100', 'inline-block', 'text-right', 'max-w-full', 'break-words');

        // Separate images and other files
        const images = files.filter(file => file.type.startsWith('image/'));
        const otherFiles = files.filter(file => !file.type.startsWith('image/'));

        // Display images
        if (images.length > 0) {
            let imageRow = document.createElement('div');
            imageRow.classList.add('flex', 'flex-wrap', 'justify-end');

            images.forEach((file, index) => {
                if (index > 0 && index % 3 === 0) {
                    messageDiv.appendChild(imageRow);
                    imageRow = document.createElement('div');
                    imageRow.classList.add('flex', 'flex-wrap', 'justify-end');
                }

                const imgDiv = document.createElement('div');
                imgDiv.classList.add('mb-2', 'mr-2', 'last:mr-0', 'text-right');

                const img = document.createElement('img');
                img.src = URL.createObjectURL(file);
                img.classList.add('max-w-xs', 'rounded', 'cursor-pointer');
                // max-h-20 and max-w-20 if more than 3 images, otherwise max-h-40 and max-w-xs
                if (images.length >= 3) {
                    img.style.maxHeight = '5rem';
                    img.style.maxWidth = '5rem';
                } else {
                    img.style.maxHeight = '10rem';
                    img.style.maxWidth = 'auto';
                }

                img.onclick = () => openImageInModal(img.src);
                imgDiv.appendChild(img);

                imageRow.appendChild(imgDiv);
            });

            messageDiv.appendChild(imageRow);
        }

        // Display other files
        otherFiles.forEach(file => {
            const fileDiv = document.createElement('div');
            fileDiv.classList.add('mb-2', 'text-right','w-full');

            const fileIcon = document.createElement('div');
            fileIcon.classList.add('flex', 'items-center', 'justify-end', 'mb-2', 'float-right',"w-full");
            fileIcon.innerHTML = `
                <svg class="inline w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                </svg>
                <span>${file.name}</span>`;
            fileDiv.appendChild(fileIcon);

            messageDiv.appendChild(fileDiv);
        });

        // Display message text
        if (message) {
            const textDiv = document.createElement('div');
            textDiv.classList.add('inline-block', 'p-2', 'rounded', 'bg-blue-500', 'text-white', 'text-right', 'max-w-full', 'whitespace-pre-wrap', 'break-words');

            // Preserve whitespace and newlines
            const formattedMessage = message.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, language, code) => {
                return `<pre><code class="language-${language || ''}">${escapeHtml(code.trim())}</code></pre>`;
            });

            textDiv.innerHTML = formattedMessage;
            messageDiv.appendChild(textDiv);
        }

        messageWrapper.appendChild(messageDiv);
        chatMessages.appendChild(messageWrapper);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to display bot message
    function displayBotMessage(message, botMessageDiv, showButtons = false) {
        // Clear existing content
        botMessageDiv.innerHTML = '';

        // Add bot avatar
        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('mr-2', 'flex-shrink-0');
        avatarDiv.innerHTML = `
            <svg class="w-8 h-8 text-gray-600" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M11 2a1 1 0 011 1v1h-2V3a1 1 0 011-1zm0 3h2V4h-2zm4.6 2.2l1.4-1.4a1 1 0 10-1.4-1.4l-1.4 1.4a5.07 5.07 0 00-1.2-.2V5a3 3 0 00-6 0v1a5.07 5.07 0 00-1.2.2L5.4 4.8a1 1 0 00-1.4 1.4l1.4 1.4A5.07 5.07 0 004 8v2a5 5 0 005 5v1H6a1 1 0 000 2h12a1 1 0 000-2h-3v-1a5 5 0 005-5V8a5.07 5.07 0 00-1.2-.2l1.4-1.4a1 1 0 00-1.4-1.4l-1.4 1.4a5.07 5.07 0 00-1.2-.2V5a3 3 0 00-6 0v1a5.07 5.07 0 00-1.2.2zM12 12a4 4 0 014-4v3h-2v1h2v2h-4zm-4-4a4 4 0 014 4h4a4 4 0 01-4-4H8a4 4 0 014-4zm1 5h2v2h-2zm6 3v1h2v-1z"/>
            </svg>
        `;
        botMessageDiv.appendChild(avatarDiv);

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('flex-grow', 'flex', 'flex-col');

        // Display message text
        const textDiv = document.createElement('div');
        textDiv.classList.add('inline-block', 'p-2', 'rounded', 'bg-gray-300', 'text-black', 'max-w-full', 'whitespace-pre-wrap', 'break-words');

        // Check for code blocks and apply syntax highlighting
        const formattedMessage = message.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, language, code) => {
            const highlightedCode = hljs.highlightAuto(code.trim(), language ? [language] : undefined).value;
            return `
                <div class="code-block bg-gray-800 rounded-lg p-4 my-2">
                    <div class="flex justify-between items-center mb-2">
                        <span class="text-xs text-gray-400">${language || 'Code'}</span>
                        <button class="copy-code-btn text-xs text-gray-400 hover:text-white">Copy Code</button>
                    </div>
                    <pre><code class="hljs ${language || ''}">${highlightedCode}</code></pre>
                </div>
            `;
        });

        textDiv.innerHTML = formattedMessage;
        contentDiv.appendChild(textDiv);

       // Add copy and retry buttons after the message is fully displayed
        if (showButtons) {
        const buttonsDiv = document.createElement('div');
        buttonsDiv.classList.add('mt-2', 'flex', 'space-x-2');

        const copyButton = document.createElement('button');
        copyButton.innerHTML = `
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
            </svg>
        `;
        copyButton.classList.add('p-1', 'bg-gray-200', 'rounded', 'hover:bg-gray-300', 'transition', 'duration-200');
        copyButton.title = 'Copy';
        copyButton.onclick = () => copyToClipboard(message, copyButton);

        const retryButton = document.createElement('button');
        retryButton.innerHTML = `
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
        `;
        retryButton.classList.add('p-1', 'bg-gray-200', 'rounded', 'hover:bg-gray-300', 'transition', 'duration-200');
        retryButton.title = 'Retry';
        retryButton.onclick = () => retryMessage(message, botMessageDiv, retryButton);
        // Add event listeners for hover effect
        retryButton.addEventListener('mouseenter', () => {
            if (isWaitingForResponse) {
                retryButton.style.cursor = 'not-allowed';
            }
        });
        retryButton.addEventListener('mouseleave', () => {
            retryButton.style.cursor = 'pointer';
        });


        buttonsDiv.appendChild(copyButton);
        buttonsDiv.appendChild(retryButton);
        contentDiv.appendChild(buttonsDiv);
        }

        botMessageDiv.appendChild(contentDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Apply syntax highlighting to code blocks
        setTimeout(() => {
            botMessageDiv.querySelectorAll('pre code').forEach((block) => {
                hljs.highlightElement(block);
            });
        }, 0);

        // Add event listeners for "Copy Code" buttons
        botMessageDiv.querySelectorAll('.copy-code-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const codeBlock = this.closest('.code-block').querySelector('code');
                copyToClipboard(codeBlock.textContent, this);
            });
        });
    }

    // Function to open image in modal
    function openImageInModal(src) {
        const modal = document.createElement('div');
        modal.classList.add('fixed', 'inset-0', 'flex', 'items-center', 'justify-center', 'bg-black', 'bg-opacity-75', 'z-50');

        const img = document.createElement('img');
        img.src = src;
        img.classList.add('max-w-full', 'max-h-full', 'rounded');

        const closeButton = document.createElement('button');
        closeButton.textContent = '×';
        closeButton.classList.add('absolute', 'top-0', 'right-0', 'm-4', 'text-white', 'text-2xl');
        closeButton.onclick = () => modal.remove();

        modal.appendChild(img);
        modal.appendChild(closeButton);
        document.body.appendChild(modal);
    }

    // Function to escape HTML special characters
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Function to copy message to clipboard
    function copyToClipboard(text, button) {
        navigator.clipboard.writeText(text).then(() => {
            const originalContent = button.innerHTML;
            button.textContent = 'Copied';
            setTimeout(() => {
                button.innerHTML = originalContent;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy: ', err);
        });
    }

    // Function to retry a message
    function retryMessage(message, botMessageDiv, retryButton) {
        if (isWaitingForResponse) return; // If waiting for a response, don't execute retry
        botMessageDiv.innerHTML = ''; // Clear the current message box
        retryButton.classList.add('disabled'); // Add disabled class
        retryButton.style.backgroundColor = 'lightgray'; // Change background color
        retryButton.style.cursor = 'not-allowed'; // Change cursor style

        // Find the user's message corresponding to the bot's response
        const userMessageDiv = botMessageDiv.previousSibling;
        if (userMessageDiv && userMessageDiv.classList.contains('justify-end')) {
            const userMessageText = userMessageDiv.querySelector('div').textContent;
            // Call sendMessage function to resend the user message and update the same message box
            sendMessage(userMessageText, botMessageDiv, retryButton, true);
        } else {
            retryButton.classList.remove('disabled');
            retryButton.style.backgroundColor = '';
            retryButton.style.cursor = 'pointer';
        }
    }

    // Function to create a file preview
    function createFilePreview(file) {
        const previewDiv = document.createElement('div');
        previewDiv.classList.add('relative', 'inline-block', 'mr-2', 'mb-2');

        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.classList.add('w-16', 'h-16', 'object-cover', 'rounded');
            img.onclick = () => openImageInModal(img.src);
            previewDiv.appendChild(img);
        } else {
            const fileIcon = document.createElement('div');
            fileIcon.innerHTML = `
                <svg class="w-8 h-8 mx-auto mb-1" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                </svg>
            `;
            fileIcon.classList.add('w-16', 'h-16', 'flex', 'flex-col', 'items-center', 'justify-center', 'bg-gray-200', 'rounded', 'text-xs', 'font-bold');
            
            const fileName = document.createElement('span');
            fileName.textContent = file.name.length > 10 ? file.name.substring(0, 7) + '...' : file.name;
            fileName.classList.add('text-center', 'overflow-hidden', 'text-ellipsis', 'w-full', 'px-1');
            
            fileIcon.appendChild(fileName);
            previewDiv.appendChild(fileIcon);
        }

        const deleteButton = document.createElement('button');
        deleteButton.innerHTML = '&times;';
        deleteButton.classList.add('absolute', 'top-0', 'right-0', 'bg-red-500', 'text-white', 'rounded-full', 'w-5', 'h-5', 'flex', 'items-center', 'justify-center', 'opacity-0', 'transition-opacity', 'duration-200');
        deleteButton.onclick = () => {
            uploadedFiles = uploadedFiles.filter(f => f !== file);
            previewDiv.remove();
        };

        previewDiv.appendChild(deleteButton);

        previewDiv.addEventListener('mouseenter', () => deleteButton.classList.remove('opacity-0'));
        previewDiv.addEventListener('mouseleave', () => deleteButton.classList.add('opacity-0'));

        return previewDiv;
    }

    // Handle paste event for image upload
    document.addEventListener('paste', (e) => {
        if (e.clipboardData && e.clipboardData.files.length) {
            for (let i = 0; i < e.clipboardData.files.length; i++) {
                const file = e.clipboardData.files[i];
                uploadedFiles.push(file);
                const previewDiv = createFilePreview(file);
                attachments.appendChild(previewDiv);
            }
        }
    });

    // Event listeners
    userInput.addEventListener('input', adjustTextareaHeight);
    sendButton.addEventListener('click', () => {
        if (!isWaitingForResponse) {
            sendMessage();
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    attachButton.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', () => {
        Array.from(fileInput.files).forEach(file => {
            uploadedFiles.push(file);
            const previewDiv = createFilePreview(file);
            attachments.appendChild(previewDiv);
        });
    });

    toggleApiKey.addEventListener('click', () => {
        isApiKeyVisible = !isApiKeyVisible;
        apiKeyInput.type = isApiKeyVisible ? 'text' : 'password';
        toggleApiKey.innerHTML = isApiKeyVisible
            ? '<svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>'
            : '<svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>';
    });

    modelSelect.addEventListener('change', () => {
        // Handle model change (you can add your logic here)
        console.log('Selected model:', modelSelect.value);
    });

    // Initial call to adjust textarea height
    adjustTextareaHeight();
});
