document.getElementById('logoutBtn').addEventListener('click', () => {
    showModal('Logout Confirmation', 'Are you sure you want to logout?');
});

function showModal(title, message) {
    // 检查模态窗口是否已经存在
    if (document.getElementById('logoutModal') === null) {
        fetch('/static/html/logout_modal.html')
            .then(response => response.text())
            .then(data => {
                document.body.insertAdjacentHTML('beforeend', data);
                bindModalEvents();
                document.getElementById('modal-title').innerText = title;
                document.getElementById('modalMessage').innerText = message;
                document.getElementById('logoutModal').classList.remove('hidden');
            })
            .catch(error => console.error('Error loading modal:', error));
    } else {
        document.getElementById('modal-title').innerText = title;
        document.getElementById('modalMessage').innerText = message;
        document.getElementById('logoutModal').classList.remove('hidden');
    }
}

function bindModalEvents() {
    document.getElementById('confirmLogout').addEventListener('click', async () => {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if (response.ok) {
            // alert('Logout successful');
            document.cookie = 'token=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
            window.location.href = '/auth/login';
        } else {
            alert(`Logout failed: ${result.message}`);
        }
    });

    document.getElementById('closeModal').addEventListener('click', () => {
        document.getElementById('logoutModal').classList.add('hidden');
    });
}
