# BookChat

A modern real-time chat application with GitHub integration for message persistence.

## Features

- Real-time message updates with 5-second polling
- GitHub-based message persistence
- Modern, responsive UI
- SQLite database for local storage
- Comprehensive test coverage

## Prerequisites

- Python 3.11+
- Git
- GitHub account with personal access token

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd bookchat
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with the following configuration:
```
GITHUB_TOKEN=your_github_token
FLASK_ENV=development
PORT=5002
```

5. Initialize the database:
```bash
python app.py init-db
```

## Running the Application

Start the server:
```bash
python app.py
```

The application will be available at `http://localhost:5002`

## Testing

Run the test suite:
```bash
python run_tests.py
```

## Project Structure

- `app.py`: Main application entry point
- `config.py`: Configuration management
- `utils/`: Utility modules for database, GitHub integration, etc.
- `static/`: Frontend assets (CSS, JavaScript)
- `templates/`: HTML templates
- `tests/`: Test suite

## API Endpoints

- `GET /messages`: Retrieve message history
- `POST /messages`: Create new message
- `GET /status`: System status and statistics

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
