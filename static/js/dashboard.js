/**
 * Dashboard JavaScript
 * Handles data fetching, display, and auto-refresh
 */

// State
let currentTodoFilter = 'all';
let currentEventFilter = 'all';
let dashboardData = null;
let refreshInterval = null;

// DOM Elements
const todosContainer = document.getElementById('todos-container');
const eventsContainer = document.getElementById('events-container');
const lastUpdated = document.getElementById('last-updated');
const refreshBtn = document.getElementById('refresh-btn');
const authBtn = document.getElementById('auth-btn');
const authModal = document.getElementById('auth-modal');
const closeModal = document.querySelector('.close');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard initializing...');

    // Load initial data
    loadDashboardData();

    // Check authentication status
    checkAuthStatus();

    // Set up auto-refresh (every 5 minutes)
    refreshInterval = setInterval(loadDashboardData, 5 * 60 * 1000);

    // Event listeners
    refreshBtn.addEventListener('click', handleManualRefresh);
    authBtn.addEventListener('click', () => authModal.style.display = 'block');
    closeModal.addEventListener('click', () => authModal.style.display = 'none');

    // Close modal when clicking outside
    window.addEventListener('click', (event) => {
        if (event.target === authModal) {
            authModal.style.display = 'none';
        }
    });

    // Filter buttons
    setupFilterButtons();
});

/**
 * Load dashboard data from API
 */
async function loadDashboardData() {
    console.log('Fetching dashboard data...');

    try {
        const response = await fetch('/api/dashboard');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        dashboardData = await response.json();
        console.log('Dashboard data loaded:', dashboardData);

        // Update UI
        updateStats(dashboardData.stats);
        renderTodos(dashboardData.work_todos);
        renderEvents(dashboardData.events);
        updateLastUpdatedTime(dashboardData.last_updated);

        // Show errors if any
        if (dashboardData.errors && dashboardData.errors.length > 0) {
            console.warn('Errors encountered:', dashboardData.errors);
        }
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showError('Failed to load dashboard data. Please try refreshing.');
    }
}

/**
 * Check authentication status for all services
 */
async function checkAuthStatus() {
    try {
        const response = await fetch('/api/auth/status');
        const status = await response.json();

        updateAuthStatus('google', status.google);
        updateAuthStatus('microsoft', status.microsoft);
        updateAuthStatus('slack', status.slack);
        updateAuthStatus('signal', status.signal);
    } catch (error) {
        console.error('Error checking auth status:', error);
    }
}

/**
 * Update authentication status indicator
 */
function updateAuthStatus(service, isAuthenticated) {
    const statusElement = document.getElementById(`auth-status-${service}`);
    if (!statusElement) return;

    const indicator = statusElement.querySelector('.status-indicator');
    const text = statusElement.querySelector('span:last-child');

    if (isAuthenticated) {
        indicator.textContent = '🟢';
        indicator.classList.add('connected');
        text.textContent = 'Connected';
    } else {
        indicator.textContent = '⚪';
        indicator.classList.remove('connected');
        text.textContent = service === 'signal' ? 'Not configured' : 'Not connected';
    }
}

/**
 * Update statistics cards
 */
function updateStats(stats) {
    if (!stats) return;

    document.getElementById('stat-todos').textContent = stats.total_todos || 0;
    document.getElementById('stat-high-priority').textContent = stats.high_priority || 0;
    document.getElementById('stat-events').textContent = stats.total_events || 0;
    document.getElementById('stat-emails').textContent = stats.emails || 0;
}

/**
 * Render work to-dos
 */
function renderTodos(todos) {
    if (!todos || todos.length === 0) {
        todosContainer.innerHTML = '<div class="empty-state">No work items found. Great job! 🎉</div>';
        return;
    }

    // Filter todos based on current filter
    let filteredTodos = todos;
    if (currentTodoFilter !== 'all') {
        filteredTodos = todos.filter(todo => todo.type === currentTodoFilter);
    }

    if (filteredTodos.length === 0) {
        todosContainer.innerHTML = '<div class="empty-state">No items match this filter.</div>';
        return;
    }

    todosContainer.innerHTML = filteredTodos.map(todo => `
        <div class="item-card priority-${todo.priority || 'medium'}">
            <div class="item-header">
                <div class="item-title">${escapeHtml(todo.title)}</div>
            </div>
            <div class="item-meta">
                <span class="badge badge-source">${escapeHtml(todo.source)}</span>
                <span class="badge badge-type">${escapeHtml(todo.type)}</span>
                ${todo.priority === 'high' ? '<span class="badge badge-priority">High Priority</span>' : ''}
            </div>
            <div class="item-description">${escapeHtml(todo.description)}</div>
            ${todo.snippet ? `<div class="item-snippet">${escapeHtml(truncate(todo.snippet, 150))}</div>` : ''}
            <div class="item-actions">
                ${todo.link !== '#' ? `<a href="${escapeHtml(todo.link)}" target="_blank" class="item-link">View →</a>` : ''}
                <span style="color: #999; font-size: 0.85em;">${formatDate(todo.date)}</span>
            </div>
        </div>
    `).join('');
}

/**
 * Render events
 */
function renderEvents(events) {
    if (!events || events.length === 0) {
        eventsContainer.innerHTML = '<div class="empty-state">No upcoming events found.</div>';
        return;
    }

    // Filter events based on current filter
    let filteredEvents = events;
    if (currentEventFilter !== 'all') {
        filteredEvents = events.filter(event => event.type === currentEventFilter);
    }

    if (filteredEvents.length === 0) {
        eventsContainer.innerHTML = '<div class="empty-state">No events match this filter.</div>';
        return;
    }

    eventsContainer.innerHTML = filteredEvents.map(event => `
        <div class="event-card">
            <div class="item-header">
                <div class="item-title">${escapeHtml(event.title)}</div>
            </div>
            <div class="item-meta">
                <span class="badge badge-source">${escapeHtml(event.source)}</span>
            </div>
            ${event.start ? `<div class="event-time">📅 ${formatEventTime(event.start, event.end)}</div>` : ''}
            ${event.description ? `<div class="item-description">${escapeHtml(truncate(event.description, 200))}</div>` : ''}
            ${event.location ? `<div class="event-location">📍 ${escapeHtml(event.location)}</div>` : ''}
            <div class="item-actions">
                ${event.link ? `<a href="${escapeHtml(event.link)}" target="_blank" class="item-link">View Details →</a>` : ''}
            </div>
        </div>
    `).join('');
}

/**
 * Set up filter button handlers
 */
function setupFilterButtons() {
    // Todo filters
    const todoFilterBtns = document.querySelectorAll('.panel:nth-of-type(1) .tab-btn');
    todoFilterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            todoFilterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentTodoFilter = btn.dataset.filter;
            if (dashboardData) {
                renderTodos(dashboardData.work_todos);
            }
        });
    });

    // Event filters
    const eventFilterBtns = document.querySelectorAll('.panel:nth-of-type(2) .tab-btn');
    eventFilterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            eventFilterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentEventFilter = btn.dataset.filter;
            if (dashboardData) {
                renderEvents(dashboardData.events);
            }
        });
    });
}

/**
 * Handle manual refresh
 */
async function handleManualRefresh() {
    refreshBtn.disabled = true;
    refreshBtn.textContent = '↻ Refreshing...';

    try {
        await fetch('/api/refresh');
        await loadDashboardData();
    } catch (error) {
        console.error('Error refreshing:', error);
        showError('Failed to refresh data.');
    } finally {
        refreshBtn.disabled = false;
        refreshBtn.textContent = '↻ Refresh';
    }
}

/**
 * Update last updated time display
 */
function updateLastUpdatedTime(timestamp) {
    if (!timestamp) return;

    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);

    if (diffMins < 1) {
        lastUpdated.textContent = 'Updated just now';
    } else if (diffMins < 60) {
        lastUpdated.textContent = `Updated ${diffMins} min${diffMins > 1 ? 's' : ''} ago`;
    } else {
        const diffHours = Math.floor(diffMins / 60);
        lastUpdated.textContent = `Updated ${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    }
}

/**
 * Format date for display
 */
function formatDate(dateStr) {
    if (!dateStr) return '';

    try {
        const date = new Date(dateStr);
        const now = new Date();
        const diffMs = now - date;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

        if (diffDays === 0) {
            return 'Today';
        } else if (diffDays === 1) {
            return 'Yesterday';
        } else if (diffDays < 7) {
            return `${diffDays} days ago`;
        } else {
            return date.toLocaleDateString();
        }
    } catch (e) {
        return dateStr;
    }
}

/**
 * Format event time
 */
function formatEventTime(start, end) {
    try {
        const startDate = new Date(start);
        const endDate = end ? new Date(end) : null;

        const options = {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };

        let timeStr = startDate.toLocaleString('en-US', options);

        if (endDate) {
            const endOptions = { hour: '2-digit', minute: '2-digit' };
            timeStr += ` - ${endDate.toLocaleString('en-US', endOptions)}`;
        }

        return timeStr;
    } catch (e) {
        return start;
    }
}

/**
 * Truncate text
 */
function truncate(text, maxLength) {
    if (!text || text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show error message
 */
function showError(message) {
    // Simple error display - could be enhanced with a toast/notification system
    console.error(message);
    alert(message);
}

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});
