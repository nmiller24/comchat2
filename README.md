# BookChat

A simple, modern chat application with both browser-based and server-side message storage capabilities.

## Features

- Dual storage system:
  - Browser-based message storage using localStorage
  - Server-side message storage for persistence
- Modern, responsive UI
- Works with or without server
- Supports offline mode
- Real-time messaging capabilities

## Dependencies

### Backend
- Python 3.x with Flask 3.0.0
- Node.js with Express 4.18.2

## Project Structure

- `index.html`: Main application page
- `app.py`: Flask application server
- `server.js`: Express.js server
- `server.py`: Alternative Python server implementation
- `save_message.py`: Message persistence handler
- `static/`: Frontend assets
  - `css/`: Stylesheets
  - `js/`: JavaScript files
- `templates/`: HTML templates
- `messages/`: Server-side message storage
- `backups/`: Backup storage directory

## Usage

You can run the application in two ways:

### Using Node.js
```bash
npm start
```

### Using Python/Flask
```bash
python app.py
```

Then open your web browser and navigate to the provided local address.

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
