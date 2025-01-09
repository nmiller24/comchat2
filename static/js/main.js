// BookChat main JavaScript file
document.addEventListener('DOMContentLoaded', () => {
    const messageContainer = document.getElementById('message-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    let lastMessageTimestamp = null;

    // Poll for new messages every 5 seconds
    const pollInterval = 5000;

    async function fetchMessages() {
        try {
            const response = await fetch('/messages');
            if (!response.ok) throw new Error('Failed to fetch messages');
            const messages = await response.json();
            updateMessages(messages);
        } catch (error) {
            showError('Error fetching messages: ' + error.message);
        }
    }

    function updateMessages(messages) {
        if (!messages.length) return;
        
        const latestTimestamp = messages[messages.length - 1].created_at;
        if (latestTimestamp === lastMessageTimestamp) return;
        
        messageContainer.innerHTML = messages.map(message => `
            <div class="message ${message.synced ? 'synced' : 'pending'}">
                <div class="message-content">${escapeHtml(message.content)}</div>
                <div class="message-timestamp">${formatTimestamp(message.created_at)}</div>
                ${message.synced ? '<div class="sync-status">✓</div>' : ''}
            </div>
        `).join('');
        
        lastMessageTimestamp = latestTimestamp;
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    async function sendMessage(content) {
        try {
            const response = await fetch('/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content })
            });
            
            if (!response.ok) throw new Error('Failed to send message');
            
            messageInput.value = '';
            await fetchMessages();
        } catch (error) {
            showError('Error sending message: ' + error.message);
        }
    }

    function showError(message) {
        const errorDiv = document.getElementById('error-notification');
        errorDiv.textContent = message;
        errorDiv.classList.add('show');
        setTimeout(() => errorDiv.classList.remove('show'), 5000);
    }

    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function formatTimestamp(timestamp) {
        return new Date(timestamp).toLocaleTimeString();
    }

    // Event Listeners
    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const content = messageInput.value.trim();
        if (content) {
            sendMessage(content);
        }
    });

    // Initial fetch and polling setup
    fetchMessages();
    setInterval(fetchMessages, pollInterval);
});
