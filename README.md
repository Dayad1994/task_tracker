# Task tracker

A simple CLI python app.

## Description

This app allows users to manage tasks through a simple command-line interface. You can add, update, delete, and list tasks, as well as change their status.

## Project Structure

```
task_tracker/
├── .gitignore            # python gitignore file
├── LICENSE               # license of project
├── README.md             # Documentation
├── pyproject.toml        # Config file of project
└── task_tracker.py       # Entry point of the application
```

## Installation

Requires Python 3.11 or newer to be installed.

1. Install **pipx**:
   _pipx_ is a tool to install and run Python CLI apps in isolated environments. It lets you globally install Python-based command-line tools without affecting system or project environments.

```bash
   python3 -m pip install pipx
```

2. Install project:

```bash
    pipx install git+https://github.com/Dayad1994/task_tracker.git
```

3. Create a directory for the project and navigate into it:

The application creates a JSON-based database file upon launch. To avoid cluttering your working directory, it's recommended to run it from a separate folder.

```bash
    mkdir task-tracker
    cd task-tracker
```

## Usage

To run the app, execute:

```bash
task-tracker add "go to school"
```

Example:

```bash
# Adding a new task
task-tracker add "Buy groceries"
# Updating and deleting tasks
task-tracker update 1 "Buy groceries and cook dinner"
task-tracker delete 1
# Marking a task as in progress or done
task-tracker mark-in-progress 1
task-tracker mark-done 1
# Listing all tasks
task-tracker list
# Listing tasks by status
task-tracker list done
task-tracker list todo
task-tracker list in-progress
```

## Development

In the project directory, create a virtual environment and install the project in editable mode. I recommend using the uv package manager.

```bash
    uv venv
```

## Requirements

- Python 3.11 or higher

## Testing

Run tests with:

```bash
python -m unittest
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m "Description of changes"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://chatgpt.com/c/LICENSE) file for details.

## Authors

- [Dayan Iskhakov](https://github.com/Dayad1994)
