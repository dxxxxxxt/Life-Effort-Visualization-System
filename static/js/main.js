async function logout() {
    try {
        const response = await fetch('/api/auth/logout', {
            method: 'POST'
        });
        const data = await response.json();
        if (data.success) {
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

function showToast(message, type = 'info') {
    const toastEl = document.getElementById('liveToast');
    const toastBody = document.getElementById('toast-body');
    const toastIcon = document.getElementById('toast-icon');
    const toastTitle = document.getElementById('toast-title');

    toastBody.textContent = message;

    const iconMap = {
        'success': { icon: 'bi-check-circle-fill', title: '成功', color: 'text-success' },
        'danger': { icon: 'bi-x-circle-fill', title: '错误', color: 'text-danger' },
        'warning': { icon: 'bi-exclamation-circle-fill', title: '警告', color: 'text-warning' },
        'info': { icon: 'bi-info-circle-fill', title: '提示', color: 'text-info' }
    };

    const config = iconMap[type] || iconMap['info'];
    toastIcon.className = `bi ${config.icon} ${config.color} me-2`;
    toastTitle.textContent = config.title;

    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatDateTime(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}
