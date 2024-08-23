(function() {
    function loadForgotPasswordModal() {
        if ($('#forgotPasswordModal').length === 0) {
            $.get('/static/html/forgotPassword.html', function(data) {
                $('body').append(data);
                bindForgotPasswordEvents();
                $('#forgotPasswordModal').removeClass('hidden');
            });
        } else {
            $('#forgotPasswordModal').removeClass('hidden');
        }
    }

    function bindForgotPasswordEvents() {
        $('#closeForgotPasswordModal').on('click', function() {
            $('#forgotPasswordModal').addClass('hidden');
            clearForgotPasswordForm();
        });

        // Password visibility toggle
        $('.toggleForgotPassword').on('click', function() {
            const passwordField = $(this).siblings('input');
            const type = passwordField.attr('type') === 'password' ? 'text' : 'password';
            passwordField.attr('type', type);
            $(this).find('.eye-open, .eye-closed').toggleClass('hidden');
        });

        // Real-time password match and special character validation
        $('#forgotNewPassword, #forgotConfirmNewPassword, #forgotResetUsername').on('input', function() {
            validatePasswords();
        });

        $('#confirmForgotPassword').on('click', function() {
            var username = $('#forgotResetUsername').val().trim();
            var newPassword = $('#forgotNewPassword').val();

            if (!validatePasswords()) {
                return;
            }

            $.ajax({
                url: 'users/password',
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify({
                    username: username,
                    new_password: newPassword
                }),
                success: function(response) {
                    if (response.success) {
                        $('#forgotPasswordModal').addClass('hidden');
                        showResetSuccessModal('Password reset successful! You can now log in with your new password.');
                        clearForgotPasswordForm();
                    } else {
                        showTemporaryMessage(response.message, 'error');
                    }
                },
                error: function(xhr) {
                    if (xhr.status === 404 && xhr.responseJSON && xhr.responseJSON.error === "Account does not exist") {
                        showTemporaryMessage('This account does not exist. Please check your username.', 'error');
                    } else {
                        showTemporaryMessage('Password reset failed. Please try again later.', 'error');
                    }
                }
            });
        });

        $('#closeForgotResetSuccessModal').on('click', function() {
            $('#forgotResetSuccessModal').addClass('hidden');
        });
    }

    function validatePasswords() {
        const username = $('#forgotResetUsername').val().trim();
        const password = $('#forgotNewPassword').val();
        const confirmPassword = $('#forgotConfirmNewPassword').val();
        const $passwordMismatch = $('#forgotPasswordMismatch');
        const $confirmResetButton = $('#confirmForgotPassword');
        const forbiddenChars = /[{}[\]\\|<>\/]+/;
    
        let isValid = true;
        let errorMessage = '';
    
        // Check for forbidden characters in username
        if (forbiddenChars.test(username)) {
            errorMessage = 'Username cannot contain special characters like {}[]\\|<>/';
            isValid = false;
        }
    
        // Check for forbidden characters in password
        if (forbiddenChars.test(password)) {
            errorMessage = 'Password cannot contain special characters like {}[]\\|<>/';
            isValid = false;
        }
    
        // Check if passwords match
        if (password !== confirmPassword) {
            errorMessage = 'Passwords do not match.';
            isValid = false;
        }
    
        // Display or hide error message
        if (!isValid) {
            $passwordMismatch.removeClass('hidden').text(errorMessage);
        } else {
            $passwordMismatch.addClass('hidden').text('');
        }
    
        // Enable or disable the reset button based on validation
        if (isValid && username && password && confirmPassword) {
            $confirmResetButton.prop('disabled', false).removeClass('opacity-50 cursor-not-allowed');
        } else {
            $confirmResetButton.prop('disabled', true).addClass('opacity-50 cursor-not-allowed');
        }
    
        return isValid;
    }

    function clearForgotPasswordForm() {
        $('#forgotResetUsername').val('');
        $('#forgotNewPassword').val('');
        $('#forgotConfirmNewPassword').val('');
        $('#forgotPasswordMismatch').addClass('hidden').text('');
        $('#forgotResetMessage').addClass('hidden').text('');
        // Reset password visibility
        $('input[type="password"]').attr('type', 'password');
        $('.eye-open').removeClass('hidden');
        $('.eye-closed').addClass('hidden');
        // Disable reset button
        $('#confirmForgotPassword').prop('disabled', true).addClass('opacity-50 cursor-not-allowed');
    }

    function showTemporaryMessage(message, type) {
        var messageElement = $('#forgotResetMessage');
        messageElement.text(message).removeClass('hidden');

        if (type === 'error') {
            messageElement.addClass('text-red-600');
        } else {
            messageElement.removeClass('text-red-600');
        }

        // Hide message after 3 seconds
        setTimeout(function() {
            messageElement.addClass('hidden');
        }, 3000);
    }

    function showResetSuccessModal(message) {
        $('#forgot-reset-success-modal-message').text(message);
        $('#forgotResetSuccessModal').removeClass('hidden');
    }

    $(document).on('click', '#forgotPassword', function(e) {
        e.preventDefault();
        loadForgotPasswordModal();
    });

    if (document.readyState === 'complete' || document.readyState === 'interactive') {
        bindForgotPasswordEvents();
    } else {
        $(document).ready(bindForgotPasswordEvents);
    }
})();
