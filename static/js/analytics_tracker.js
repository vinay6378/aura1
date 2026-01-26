// Analytics Tracker for Real-time Dashboard
class AnalyticsTracker {
    constructor() {
        this.sessionId = this.getSessionId();
        this.trackPageView();
        this.trackEvents();
    }

    getSessionId() {
        let sessionId = sessionStorage.getItem('analytics_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            sessionStorage.setItem('analytics_session_id', sessionId);
        }
        return sessionId;
    }

    trackPageView() {
        const data = {
            page_url: window.location.pathname,
            page_title: document.title,
            referrer: document.referrer,
            user_agent: navigator.userAgent,
            session_id: this.sessionId
        };

        this.sendData('/api/track/pageview', data);
    }

    trackEvents() {
        // Track button clicks
        document.addEventListener('click', (e) => {
            if (e.target.tagName === 'BUTTON' || e.target.tagName === 'A') {
                this.trackEvent('click', {
                    element: e.target.tagName,
                    text: e.target.textContent?.trim(),
                    href: e.target.href
                });
            }
        });

        // Track form submissions
        document.addEventListener('submit', (e) => {
            this.trackEvent('form_submit', {
                form_id: e.target.id,
                form_action: e.target.action
            });
        });

        // Track page exit
        window.addEventListener('beforeunload', () => {
            this.trackEvent('page_exit', {
                time_on_page: Date.now() - performance.now()
            });
        });
    }

    trackEvent(eventType, data) {
        const eventData = {
            event_type: eventType,
            data: data,
            page_url: window.location.pathname,
            session_id: this.sessionId
        };

        this.sendData('/api/track/event', eventData);
    }

    sendData(endpoint, data) {
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        }).catch(error => {
            console.log('Analytics tracking failed:', error);
        });
    }
}

// Initialize tracker when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AnalyticsTracker();
});
