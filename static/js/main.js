// BookChat main JavaScript file
document.addEventListener('DOMContentLoaded', () => {
    const messageContainer = document.getElementById('message-container');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');
    const emojiButton = document.getElementById('emoji-button');
    const emojiPicker = document.getElementById('emoji-picker');
    let sessionLog = [];

    // Common emojis array
    const commonEmojis = [
        '😊', '😂', '🤣', '❤️', '😍', '😒', '👍', '😭',
        '😘', '🥰', '😅', '😉', '🙂', '😎', '🤔', '😢',
        '😆', '🥺', '😋', '😇', '😡', '🤗', '😴', '🤓',
        '👋', '🎉', '✨', '🌟', '💡', '📚', '✅', '❌'
    ];

    // Initialize emoji picker
    function initializeEmojiPicker() {
        commonEmojis.forEach(emoji => {
            const emojiElement = document.createElement('div');
            emojiElement.className = 'emoji-item';
            emojiElement.textContent = emoji;
            emojiElement.addEventListener('click', () => {
                insertEmoji(emoji);
                emojiPicker.classList.remove('active');
            });
            emojiPicker.appendChild(emojiElement);
        });
    }

    // Insert emoji at cursor position
    function insertEmoji(emoji) {
        const start = messageInput.selectionStart;
        const end = messageInput.selectionEnd;
        const text = messageInput.value;
        const before = text.substring(0, start);
        const after = text.substring(end);
        messageInput.value = before + emoji + after;
        messageInput.focus();
        messageInput.selectionStart = messageInput.selectionEnd = start + emoji.length;
    }

    // Auto-resize textarea
    function autoResizeTextarea() {
        messageInput.style.height = 'auto';
        messageInput.style.height = (messageInput.scrollHeight) + 'px';
    }

    messageInput.addEventListener('input', autoResizeTextarea);
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            messageForm.dispatchEvent(new Event('submit'));
        }
    });

    // Toggle emoji picker
    emojiButton.addEventListener('click', (e) => {
        e.stopPropagation();
        emojiPicker.classList.toggle('active');
    });

    // Close emoji picker when clicking outside
    document.addEventListener('click', (e) => {
        if (!emojiPicker.contains(e.target) && !emojiButton.contains(e.target)) {
            emojiPicker.classList.remove('active');
        }
    });

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

    function addMessage(content) {
        const messages = getMessages();
        const newMessage = {
            id: Date.now(),
            content,
            created_at: new Date().toISOString()
        };
        
        messages.push(newMessage);
        saveMessages(messages);
        updateMessages(messages);
        
        // Add to session log
        sessionLog.push({
            timestamp: newMessage.created_at,
            message: content
        });
        
        return newMessage;
    }

    function showError(message) {
        const errorNotification = document.getElementById('error-notification');
        errorNotification.textContent = message;
        errorNotification.classList.add('show');
        setTimeout(() => errorNotification.classList.remove('show'), 3000);
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
        const date = new Date(timestamp);
        const now = new Date();
        const isToday = date.toDateString() === now.toDateString();
        
        const timeStr = date.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit'
        });
        
        if (isToday) {
            return `🕒 ${timeStr}`;
        } else {
            const dateStr = date.toLocaleDateString([], { 
                month: 'short', 
                day: 'numeric' 
            });
            return `📅 ${dateStr}, ${timeStr}`;
        }
    }

    // Event Listeners
    messageForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const content = messageInput.value.trim();
        
        if (content) {
            addMessage(content);
            messageInput.value = '';
            messageInput.style.height = 'auto';
        }
    });

    // Initial load of messages
    updateMessages(getMessages());
    initializeEmojiPicker();
});
