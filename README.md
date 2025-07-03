# Mobile ToDo App

A simple mobile ToDo application built with Python using KivyMD framework.

## Features

- Create, read, and delete todo items
- Set due dates for tasks
- Simple and intuitive interface
- Local SQLite database storage
- Cross-platform compatibility (Windows, macOS, Linux)

## Technology Stack

- **Python 3.x**
- **KivyMD 1.2.0** - Material Design UI framework
- **SQLite** - Local database storage
- **Kivy** - Cross-platform application framework

## Setup

1. Clone the repository
2. Install required dependencies:

```bash
pip install kivymd
pip install kivy
```

3. Run the application:

```bash
python main.py
```

## Project Structure

- `main.py` - Main application file with UI and database logic
- `todo.db` - SQLite database file (created automatically, not tracked in git)
- `README.md` - Project documentation

## Key Features

### Task Management
- Add new tasks with optional due dates
- View all tasks in a scrollable list
- Delete tasks by tapping on them
- Date picker for easy due date selection

### User Interface
- Material Design interface using KivyMD
- Clean and modern UI
- Responsive layout
- English interface for maximum compatibility

### Data Persistence
- SQLite database for local storage
- Automatic database creation
- Persistent data across app sessions

## Development Notes

- **Language**: English interface to avoid font rendering issues
- **Compatibility**: Tested on Windows 10 with Python 3.13
- **Database**: SQLite database is created automatically on first run
- **UI Framework**: Uses KivyMD 1.2.0 (note: newer versions available)

## License

This project is open source and available under the [MIT License](LICENSE). 