from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/save-message', methods=['POST'])
def save_message():
    try:
        message = request.json.get('message')
        if not message:
            return jsonify({'error': 'No message provided'}), 400

        # Create messages directory if it doesn't exist
        os.makedirs('messages', exist_ok=True)

        # Format timestamp for filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'messages/{timestamp}.txt'

        # Save message to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(message)

        return jsonify({'success': True, 'filename': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
