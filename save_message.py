import os
import sys
from datetime import datetime

def save_message(message):
    # Create messages directory if it doesn't exist
    os.makedirs('messages', exist_ok=True)
    
    # Format timestamp for filename
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = os.path.join('messages', f'{timestamp}.txt')
    
    # Save message to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(message)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        message = sys.argv[1]
        save_message(message)
    else:
        print("No message provided")
