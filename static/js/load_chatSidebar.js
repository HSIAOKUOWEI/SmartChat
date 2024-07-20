// static/js/loadSidebar.js
$(document).ready(function() {
    // 动态加载侧边栏
    $('#sidebar-container').load('/static/html/chatSidebar.html', function() {
        console.log("Sidebar loaded.");
    });
});