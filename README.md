# Task tracker

A simple CLI python app.

## Description

This app allows users to manage tasks through a simple command-line interface. You can add, update, delete, and list tasks, as well as change their status.

## Project Structure

```
task_tracker/
├── .gitignore            # python gitignore file
├── .python-version       # fixed python version
├── LICENSE               # license of project
├── README.md             # Documentation
├── pyproject.toml        # Config file of project
├── task_tracker.py       # Entry point of the application
└── uv.lock               # fixed environments
```

## Installation

I am using the `uv` package manager. Therefore, you need to [install `uv`](https://docs.astral.sh/uv/getting-started/installation/) before installing the application.

1. Clone the repository:

```bash
   git clone git@github.com:Dayad1994/task_tracker.git
   cd task_tracker
```

2. Install dependencies:

```bash
    uv sync
```

3. Install project as os app:

```bash
    uv pip install .
```

## Usage

To run the application, activate venv and execute:

```bash
source .venv/bin/activate
task-tracker list
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

## Requirements

- Python 3.13 or higher

## Testing

Run tests with:

```bash
pytest
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
