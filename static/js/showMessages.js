export function UserMessage(message) {
    $('#chat-window').append(`
    <div class="flex flex-row px-4 py-8 sm:px-6">
      <img class="mr-2 flex h-8 w-8 rounded-full sm:mr-4" src="https://dummyimage.com/256x256/363536/ffffff&text=U"/>
      <div class="flex max-w-3xl items-center">
        <pre class="whitespace-pre-wrap">${escapeHtml(message)}</pre>
      </div>
    </div>
    `);
    scrollToBottom();
}

export function BotMessage(message) {
    $('#chat-window').append(`
        <div class="flex bg-slate-100 px-4 py-8 dark:bg-slate-900 sm:px-6">
      <img
        class="mr-2 flex h-8 w-8 rounded-full sm:mr-4"
        src="https://dummyimage.com/256x256/354ea1/ffffff&text=G"
      />

      <div class="flex w-full flex-col items-start lg:flex-row lg:justify-between">
        <pre class="whitespace-pre-wrap">${escapeHtml(message)}</pre>
        <div class="mt-4 flex flex-row justify-start gap-x-2 text-slate-500 lg:mt-0">
            ${createLikeButton()}
            ${createDislikeButton()}
            ${createCopyButton(message)}
        </div>
      </div>
    </div>
    `);
    scrollToBottom();
}

function createLikeButton() {
    return `
        <button class="hover:text-blue-600">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path
                d="M7 11v8a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1v-7a1 1 0 0 1 1 -1h3a4 4 0 0 0 4 -4v-1a2 2 0 0 1 4 0v5h3a2 2 0 0 1 2 2l-1 5a2 3 0 0 1 -2 2h-7a3 3 0 0 1 -3 -3"
              ></path>
            </svg>
          </button>
    `;
}

function createDislikeButton() {
    return `
        <button class="hover:text-blue-600" type="button">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path
                d="M7 13v-8a1 1 0 0 0 -1 -1h-2a1 1 0 0 0 -1 1v7a1 1 0 0 0 1 1h3a4 4 0 0 1 4 4v1a2 2 0 0 0 4 0v-5h3a2 2 0 0 0 2 -2l-1 -5a2 3 0 0 0 -2 -2h-7a3 3 0 0 0 -3 3"
              ></path>
            </svg>
          </button>
    `;
}

function createCopyButton(message) {
    return `
        <button class="copy-button hover:text-blue-600" type="button" onclick="copyToClipboard('${escapeHtmlForAttribute(message)}', this)">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path
                d="M8 8m0 2a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2z"
              ></path>
              <path
                d="M16 8v-2a2 2 0 0 0 -2 -2h-8a2 2 0 0 0 -2 2v8a2 2 0 0 0 2 2h2"
              ></path>
            </svg>
          </button>
    `;
}

function escapeHtml(text) {
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

function escapeHtmlForAttribute(text) {
    return text.replace(/'/g, '\\\'').replace(/"/g, '&quot;');
}

function scrollToBottom() {
    const chatWindow = $('#chat-window');
    chatWindow.scrollTop(chatWindow.prop('scrollHeight'));
}

// 用于复制消息到剪贴板的函数
window.copyToClipboard = function(message, button) {
    if (button.classList.contains('copied')) {
        return; // 如果按钮已经显示 "Copied!" 状态，则不再处理
    }

    navigator.clipboard.writeText(message).then(function() {
        // 更改按钮内容为复制成功状态
        button.classList.add('copied');
        const originalIcon = button.innerHTML;
        button.innerHTML = `
        <span class="inline-flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
              fill="none"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
              <path
                d="M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2"
              ></path>
              <path
                d="M9 3m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v0a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z"
              ></path>
              <path d="M9 14l2 2l4 -4"></path>
            </svg>
            <span class="text-sm font-medium">Copied!</span>
            </span>
        `;
        setTimeout(() => {
            button.classList.remove('copied');
            button.innerHTML = originalIcon;
        }, 2000);
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}
