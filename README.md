# Tasker – Simple CLI Task Tracker

**Tasker** — быстрый и минималистичный инструмент командной строки для управления задачами.

## Description

Этот проект реализован в рамках одного из [идей проектов с roadmap.sh](https://roadmap.sh/projects/task-tracker).  
С помощью Tasker вы можете добавлять, обновлять, удалять, просматривать задачи, а также отмечать их как "в процессе" или "завершённые".

## Project Structure

```
tasker/
├── .gitignore            # Стандартный gitignore для Python
├── LICENSE               # Лицензия проекта
├── README.md             # Документация проекта
├── pyproject.toml        # Конфигурация сборки и форматирования (ruff)
├── tasker.py             # Точка входа в приложение
└── test_tasker.py        # Юнит-тесты
```

## Installation

Требуется Python версии 3.11 или новее.

1. Установите **pipx** — утилиту для установки и запуска Python CLI-приложений в изолированных окружениях. Это позволит глобально установить инструменты командной строки без влияния на системные или проектные зависимости.

```bash
python3 -m pip install pipx
```

2. Установите проект:

```bash
pipx install git+https://github.com/dayanik/tasker.git
```

3. Создайте отдельную директорию для работы с проектом и перейдите в неё:

Приложение создаёт файл базы данных в формате JSON при первом запуске. Чтобы избежать засорения текущей рабочей папки, рекомендуется запускать программу из отдельного каталога.

```bash
mkdir tasker
cd tasker
```

## Usage

Если установлено через `pipx`, запускать приложение можно из любой папки:

```bash
tasker <command> [args]
```

Примеры:

```bash
# Добавить новую задачу
tasker add "Buy groceries"

# Обновить или удалить задачу
tasker update 1 "Buy groceries and cook dinner"
tasker delete 1

# Пометить задачу как в процессе или выполненную
tasker mark-in-progress 1
tasker mark-done 1

# Показать все задачи
tasker list

# Показать задачи по статусу
tasker list done
tasker list todo
tasker list in-progress
```

## Development

Для разработки создайте виртуальное окружение и установите проект в режиме редактирования. Рекомендую использовать пакетный менеджер **uv**:

```bash
uv venv
```

**uv** — это быстрый менеджер пакетов, совместимый с pip и venv.

## Requirements

- Python 3.11 и выше

## Testing

Запуск тестов:

```bash
python -m unittest
```

## Contributing

Буду рад вашим изменениям! Пожалуйста, следуйте этим шагам:

1. Форкните репозиторий.
2. Создайте новую ветку: `git checkout -b feature-name`.
3. Внесите изменения и сделайте коммит: `git commit -m "Description of changes"`.
4. Отправьте ветку на сервер: `git push origin feature-name`.
5. Создайте pull request.

## License

Проект лицензирован под MIT License. Подробнее в файле [LICENSE](./LICENSE).

## Authors

- [Dayan Iskhakov](https://github.com/dayanik)
