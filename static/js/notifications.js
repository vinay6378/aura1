// Real-time notification system
class NotificationSystem {
    constructor() {
        this.notifications = [];
        this.container = null;
        this.init();
    }

    init() {
        // Create notification container
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(this.container);

        // Check for new notifications periodically
        this.startPolling();
    }

    show(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            background: white;
            border-left: 4px solid ${this.getColor(type)};
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateX(100%);
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 12px;
        `;

        const icon = document.createElement('i');
        icon.className = this.getIcon(type);
        icon.style.cssText = `
            font-size: 20px;
            color: ${this.getColor(type)};
        `;

        const content = document.createElement('div');
        content.style.cssText = 'flex: 1;';
        content.innerHTML = `<div style="font-weight: 600; margin-bottom: 4px;">${this.getTitle(type)}</div>
                             <div style="font-size: 14px; color: #666;">${message}</div>`;

        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.style.cssText = `
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: #999;
            padding: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        `;
        closeBtn.onclick = () => this.remove(notification);

        notification.appendChild(icon);
        notification.appendChild(content);
        notification.appendChild(closeBtn);

        this.container.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Auto remove
        if (duration > 0) {
            setTimeout(() => this.remove(notification), duration);
        }

        return notification;
    }

    remove(notification) {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }

    getColor(type) {
        const colors = {
            'success': '#28a745',
            'error': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8'
        };
        return colors[type] || colors.info;
    }

    getIcon(type) {
        const icons = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-exclamation-circle',
            'warning': 'fas fa-exclamation-triangle',
            'info': 'fas fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    getTitle(type) {
        const titles = {
            'success': 'Success',
            'error': 'Error',
            'warning': 'Warning',
            'info': 'Information'
        };
        return titles[type] || titles.info;
    }

    startPolling() {
        // Poll for new notifications every 30 seconds
        setInterval(() => {
            this.checkNewNotifications();
        }, 30000);
    }

    async checkNewNotifications() {
        try {
            const response = await fetch('/api/notifications');
            if (response.ok) {
                const notifications = await response.json();
                notifications.forEach(notification => {
                    this.show(notification.message, notification.type);
                });
            }
        } catch (error) {
            console.log('Error checking notifications:', error);
        }
    }
}

// Initialize notification system
const notificationSystem = new NotificationSystem();

// Export for global use
window.notificationSystem = notificationSystem;
