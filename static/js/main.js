// BookChat main JavaScript file
document.addEventListener('DOMContentLoaded', () => {
    const messageContainer = document.getElementById('message-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    let sessionLog = [];

    // Create download log button
    const downloadLogButton = document.createElement('button');
    downloadLogButton.textContent = 'Download Session Log';
    downloadLogButton.className = 'download-log-btn';
    document.querySelector('.container').appendChild(downloadLogButton);

    // Initialize messages from localStorage
    function getMessages() {
        const messages = localStorage.getItem('bookchat_messages');
        return messages ? JSON.parse(messages) : [];
    }

    function saveMessages(messages) {
        localStorage.setItem('bookchat_messages', JSON.stringify(messages));
    }

    function updateMessages(messages) {
        if (!messages.length) return;
        
        messageContainer.innerHTML = messages.map(message => `
            <div class="message">
                <div class="message-content">${escapeHtml(message.content)}</div>
                <div class="message-timestamp">${formatTimestamp(message.created_at)}</div>
            </div>
        `).join('');
        
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

    function downloadSessionLog() {
        if (sessionLog.length === 0) {
            showError('No messages in current session');
            return;
        }

        const logContent = sessionLog.map(entry => 
            `[${entry.timestamp}] ${entry.message}`
        ).join('\n');

        const timestamp = new Date().toISOString().replace(/:/g, '-').replace('T', '_');
        const filename = `session_log_${timestamp}.txt`;
        
        const blob = new Blob([logContent], { type: 'text/plain' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = filename;
        
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(a.href);
    }

    async function addMessage(content) {
        const messages = getMessages();
        const timestamp = new Date().toISOString();
        const newMessage = {
            content,
            created_at: timestamp
        };
        
        try {
            // Add to session log
            sessionLog.push({
                timestamp: timestamp,
                message: content
            });
            
            // Continue with normal message display
            messages.push(newMessage);
            saveMessages(messages);
            updateMessages(messages);
            messageInput.value = '';
        } catch (error) {
            showError('Error saving message: ' + error.message);
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
    messageForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const content = messageInput.value.trim();
        if (content) {
            await addMessage(content);
        }
    });

    downloadLogButton.addEventListener('click', downloadSessionLog);

    // Initial load of messages
    updateMessages(getMessages());
});
