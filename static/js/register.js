$(document).ready(function() {
    // 加载注册弹窗
    $.get('/static/html/register_user.html', function(data) {
        $('body').append(data);
        bindRegisterEvents();
    });

    function bindRegisterEvents() {
        $('#createAccount').on('click', function(e) {
            e.preventDefault();
            $('#registerModal').removeClass('hidden');
        });

        $('#closeRegisterModal').on('click', function() {
            $('#registerModal').addClass('hidden');
            clearRegisterForm();
        });

        // 密码可见性切换
        $('.togglePassword').on('click', function() {
            const passwordField = $(this).siblings('input');
            const type = passwordField.attr('type') === 'password' ? 'text' : 'password';
            passwordField.attr('type', type);
            $(this).find('.eye-open, .eye-closed').toggleClass('hidden');
        });

        // 实时验证密码匹配
        $('#confirmPassword').on('input', function() {
            const password = $('#newPassword').val();
            const confirmPassword = $(this).val();
            if (password !== confirmPassword) {
                $('#passwordMismatch').removeClass('hidden');
            } else {
                $('#passwordMismatch').addClass('hidden');
            }
        });

        $('#confirmRegister').on('click', function() {
            var username = $('#newUsername').val();
            var password = $('#newPassword').val();
            var confirmPassword = $('#confirmPassword').val();

            // 检查密码是否匹配
            if (password !== confirmPassword) {
                $('#registerMessage').text('Passwords do not match.').removeClass('hidden');
                return;
            }

            // 检查特殊字符
            var specialChars = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/;
            if(specialChars.test(username) || specialChars.test(password)) {
                showTemporaryMessage('Username and password cannot contain special characters.').removeClass('hidden');
                return;
            }

            $.ajax({
                url: '/users/register',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    username: username,
                    password: password
                }),
                success: function(response) {
                    if (response.success) {
                        $('#registerModal').addClass('hidden');
                        showSuccessModal('Registration successful! You can now log in and use your account.');
                        clearRegisterForm();
                    } else {
                        $('#registerMessage').text(response.message).removeClass('hidden');
                    }
                },
                error: function(xhr) {
                    if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.error === "Account already exists") {
                        showTemporaryMessage('This username already exists. Please choose another username.').removeClass('hidden');
                    } else {
                        showTemporaryMessage('Registration failed, please try again later.').removeClass('hidden');
                    }
                }
            });
        });
        // 确保这个事件处理程序被正确绑定
        $(document).on('click', '#closeSuccessModal', function() {
            $('#successModal').addClass('hidden');
        });
    }

    function clearRegisterForm() {
        $('#newUsername').val('');
        $('#newPassword').val('');
        $('#confirmPassword').val('');
        $('#passwordMismatch').addClass('hidden');
        $('#registerMessage').addClass('hidden');
        // 重置密码可见性
        $('input[type="password"]').attr('type', 'password');
        $('.eye-open').removeClass('hidden');
        $('.eye-closed').addClass('hidden');
    }

    function showSuccessModal(message) {
        $('#success-modal-message').text(message);
        $('#successModal').removeClass('hidden');
    }

    function showTemporaryMessage(message, type) {
        var messageElement = $('#registerMessage');
        messageElement.text(message).removeClass('hidden');

        if (type === 'error') {
            messageElement.addClass('error-message');
        } else {
            messageElement.removeClass('error-message');
        }

        // 2秒后隐藏消息
        setTimeout(function() {
            messageElement.addClass('hidden');
        }, 2000);
    }
});