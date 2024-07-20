$(document).ready(function() {
    var conversationHistory = {};
    var uploadedImages = []; // 用于保存上传的图片数据
    var uploadedFiles = []; // 用于保存上传的文件数据
    var imageCount = 0; // 用于给粘贴的图片生成唯一文件名

    $('#sendButton').click(function() {
        sendMessage();
    });

    $('#userInput').keypress(function(event) {
        if (event.which === 13 || event.keyCode === 13) {
            event.preventDefault(); // 阻止默认的 Enter 键行为
            sendMessage();
        }
    });

    $('#fileInput').change(function(event) {
        handleFileUpload(event.target.files);
    });

    $('#uploadButton').click(function() {
        $('#fileInput').click();
    });

    $('#userInput').on('paste', function(event) {
        var items = (event.clipboardData || event.originalEvent.clipboardData).items;
        for (var index in items) {
            var item = items[index];
            if (item.kind === 'file') {
                var file = item.getAsFile();
                handleFileUpload([file]);
            }
        }
    });

    $('#userInput').on('drop', function(event) {
        event.preventDefault();
        handleFileUpload(event.originalEvent.dataTransfer.files);
    });

    $('#userInput').on('dragover', function(event) {
        event.preventDefault();
    });

    function handleFileUpload(files) {
        Array.from(files).forEach(file => {
            if (file.type.startsWith('image/')) {
                handleImageFile(file, file.name);
            } else {
                handleNonImageFile(file);
            }
        });
    }

    function handleImageFile(file, name) {
        var reader = new FileReader();
        reader.onload = function(event) {
            var imgData = event.target.result;
            uploadedImages.push({ data: imgData, name: name });
            var imgIndex = uploadedImages.length - 1;
            var img = `<div class="preview-item image-preview-item" data-index="${imgIndex}">
                           <img src="${imgData}" class="uploaded-image">
                           <span class="delete-btn" onclick="removeImage(${imgIndex})">×</span>
                      </div>`;
            $('#preview-container').append(img);
        };
        reader.readAsDataURL(file);
    }

    function handleNonImageFile(file) {
        uploadedFiles.push(file);
        var fileIndex = uploadedFiles.length - 1;
        var fileIcon = `<div class="preview-item file-preview-item" data-index="${fileIndex}">
                            <span class="file-icon">${file.name}</span>
                            <span class="delete-btn" onclick="removeFile(${fileIndex})">×</span>
                        </div>`;
        $('#preview-container').append(fileIcon);
    }

    window.removeImage = function(index) {
        uploadedImages.splice(index, 1);
        $(`.preview-item.image-preview-item[data-index="${index}"]`).remove();
        resetFileInput();
    };

    window.removeFile = function(index) {
        uploadedFiles.splice(index, 1);
        $(`.preview-item.file-preview-item[data-index="${index}"]`).remove();
        resetFileInput();
    };

    function resetFileInput() {
        $('#fileInput').val('');
    }

    $('input[name="apiCheckbox"]').change(function() {
        var selectedCount = $('input[name="apiCheckbox"]:checked').length;
        if (selectedCount > 4) {
            alert('You can only select up to 4 APIs.');
            this.checked = false;
        }
    });

    function sendMessage() {
        var userInput = $('#userInput').val();
        if (!userInput && uploadedImages.length === 0 && uploadedFiles.length === 0) {
            alert('Please enter a message, upload an image, or upload a file');
            return;
        }

        var selectedApis = [];
        $('input[name="apiCheckbox"]:checked').each(function() {
            selectedApis.push($(this).val());
        });

        if (selectedApis.length === 0) {
            alert('Please select at least one API');
            return;
        }

        var formData = new FormData();
        formData.append('message', userInput);
        uploadedImages.forEach((image, index) => {
            var byteString = atob(image.data.split(',')[1]);
            var mimeString = image.data.split(',')[0].split(':')[1].split(';')[0];
            var ab = new ArrayBuffer(byteString.length);
            var ia = new Uint8Array(ab);
            for (var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            var blob = new Blob([ab], { type: mimeString });
            formData.append('images[]', blob, image.name || `pasted_image_${imageCount++}.jpg`);
        });
        uploadedFiles.forEach((file, index) => {
            formData.append('files[]', file);
        });

        selectedApis.forEach(function(api, index) {
            var responseDivId = `response${api}`;

            if (!conversationHistory[api]) {
                conversationHistory[api] = [];
                var responseDiv = `<div class="response-item"><h3>(${api}):</h3><div id="${responseDivId}" class="display-box"></div></div>`;
                $('#response-container').append(responseDiv);
            }

            var messageContent = userInput;
            uploadedImages.forEach(image => {
                messageContent += `<br><img src="${image.data}" class="uploaded-image">`;
            });
            uploadedFiles.forEach(file => {
                messageContent += `<br><span class="file-icon">${file.name}</span>`;
            });
            conversationHistory[api].push({ role: 'user', content: messageContent });
            updateConversationDisplay(api, responseDivId);

            fetch(`/chatbot/${api}`, {
                method: 'POST',
                body: formData
            }).then(response => {
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let accumulatedContent = '';
                conversationHistory[api].push({ role: 'assistant', content: '' });
                return reader.read().then(function processText({ done, value }) {
                    if (done) {
                        return;
                    }
                    const chunk = decoder.decode(value, { stream: true });
                    accumulatedContent += chunk;
                    conversationHistory[api][conversationHistory[api].length - 1].content = accumulatedContent;
                    updateConversationDisplay(api, responseDivId);
                    return reader.read().then(processText);
                });
            }).catch(error => {
                console.log('Error:', error);
            });
        });

        $('#userInput').val('');
        $('#preview-container').html('');
        uploadedImages = [];
        uploadedFiles = [];
        resetFileInput();
    }

    function updateConversationDisplay(api, responseDivId) {
        var conversationHtml = '';
        conversationHistory[api].forEach(function(message) {
            if (message.role === 'user') {
                conversationHtml += `<p><strong>用户：</strong>${message.content}</p>`;
            } else {
                conversationHtml += `<p><strong>助手：</strong>${message.content}</p>`;
            }
        });
        $(`#${responseDivId}`).html(conversationHtml);
    }
});
