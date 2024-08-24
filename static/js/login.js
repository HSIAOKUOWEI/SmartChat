$(document).ready(function() {

    const $passwordField = $('#password');
    const $eyeOffIcon = $('#togglePassword .eye-off');
    const $eyeIcon = $('#togglePassword .eye');
    const $usernameField = $('#username');
    const $loginForm = $('#loginForm');
    const $message = $('#message');

    // 是否顯示密碼
    $('#togglePassword').on('click', function() {
        if ($passwordField.attr('type') === 'password') {
            $passwordField.attr('type', 'text');
            $eyeOffIcon.addClass('hidden');
            $eyeIcon.removeClass('hidden');
        } else {
            $passwordField.attr('type', 'password');
            $eyeIcon.addClass('hidden');
            $eyeOffIcon.removeClass('hidden');
        }
    });

    // 登入
    $loginForm.submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/auth/login',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                username: $usernameField.val(),
                password: $passwordField.val()
            }),
            success: function(response) {
                if (response.status) {
                    // 存储token到cookie
                    document.cookie = "token=" + response.token + "; path=/";
                    window.location.href = '/chat/agent_chat';
                } else {
                    showMessage(response.message);
                }
                // Clear username and password fields
                clearFields();
            },
            error: function(xhr) {
                showMessage(xhr.responseJSON.message);
            }
        });
    });

    function showMessage(message) {
        $message.text(message).show();
        setTimeout(function() {
            $message.fadeOut();
        }, 3000); // 显示3秒后隐藏
    }

    function clearFields() {
        $usernameField.val('');
        $passwordField.val('');
    }
});
