# Tasker – Simple CLI Task Tracker

A fast and minimal command-line tool to manage your tasks.

## Description

A simple command-line tool to manage personal tasks.
You can add, update, delete, list tasks, and mark them as in progress or done.

## Project Structure

```
tasker/
├── .gitignore            # Standard Python gitignore
├── LICENSE               # Project license
├── README.md             # Project documentation
├── pyproject.toml        # Build system and ruff/formatting config
├── tasker.py             # Application entry point
└── test_tasker.py        # Unit tests
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
    pipx install git+https://github.com/Dayad1994/tasker.git
```

3. Create a directory for the project and navigate into it:

The application creates a JSON-based database file upon launch. To avoid cluttering your working directory, it's recommended to run it from a separate folder.

```bash
    mkdir tasker
    cd tasker
```

## Usage

If installed via `pipx`, you can run the app from anywhere using:

```bash
tasker <command> [args]
```

Example:

```bash
# Adding a new task
tasker add "Buy groceries"
# Updating and deleting tasks
tasker update 1 "Buy groceries and cook dinner"
tasker delete 1
# Marking a task as in progress or done
tasker mark-in-progress 1
tasker mark-done 1
# Listing all tasks
tasker list
# Listing tasks by status
tasker list done
tasker list todo
tasker list in-progress
```

## Development

In the project directory, create a virtual environment and install the project in editable mode. I recommend using the uv package manager.

```bash
    uv venv
```

**uv** is a fast Python package manager compatible with pip and venv.

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

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Authors

- [Dayan Iskhakov](https://github.com/Dayad1994)
