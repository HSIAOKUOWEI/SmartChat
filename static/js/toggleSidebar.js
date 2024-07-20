document.addEventListener('DOMContentLoaded', function() {
    // 动态加载侧边栏
    fetch('/static/html/chatSidebar.html')
        .then(response => response.text())
        .then(data => {
            document.getElementById('sidebar-container').innerHTML = data;
        });

    // 侧边栏切换功能
    document.body.addEventListener('click', function(event) {
        if (event.target.id === 'toggle-sidebar') {
            document.getElementById('sidebar-container').classList.toggle('hidden');
            document.getElementById('chat-window').classList.toggle('flex-1');
        }
    });
});