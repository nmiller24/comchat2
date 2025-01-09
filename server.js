const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static('.'));

app.post('/save-message', async (req, res) => {
    try {
        const { message } = req.body;
        if (!message) {
            return res.status(400).json({ error: 'No message provided' });
        }

        // Create messages directory if it doesn't exist
        await fs.mkdir('messages', { recursive: true });

        // Format timestamp for filename
        const timestamp = new Date().toISOString().replace(/:/g, '-').replace('T', '_');
        const filename = path.join('messages', `${timestamp}.txt`);

        // Save message to file
        await fs.writeFile(filename, message);

        res.json({ success: true, filename });
    } catch (error) {
        console.error('Error saving message:', error);
        res.status(500).json({ error: error.message });
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
