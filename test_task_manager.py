import pytest
from task_manager import TaskManager, Task
import os
import tempfile

# Создание временного файла для тестирования
@pytest.fixture
def temp_task_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    os.remove(path)

@pytest.fixture
def task_manager(temp_task_file):
    return TaskManager(temp_task_file)

# Тест: Добавление задачи
def test_add_task(task_manager):
    task_manager.add_task("Test Task", "Test Description", "Test Category", "2024-12-31", "высокий")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Test Task"

# Тест: Отметка задачи как выполненной
def test_mark_task_as_done(task_manager):
    task_manager.add_task("Test Task", "Test Description", "Test Category", "2024-12-31", "высокий")
    task_manager.mark_task_as_done(1)
    assert task_manager.tasks[0].status == "Выполнена"

# Тест: Поиск задачи по ключевому слову
def test_search_task_by_keyword(task_manager):
    task_manager.add_task("Test Task", "Test Description", "Test Category", "2024-12-31", "высокий")
    task_manager.add_task("Another Task", "Another Description", "Another Category", "2024-12-31", "средний")
    results = [task for task in task_manager.tasks if "Another" in task.title or "Another" in task.description]
    assert len(results) == 1
    assert results[0].title == "Another Task"

# Тест: Удаление задачи по идентификатору
def test_delete_task_by_id(task_manager):
    task_manager.add_task("Test Task", "Test Description", "Test Category", "2024-12-31", "высокий")
    task_manager.delete_task(task_id=1)
    assert len(task_manager.tasks) == 0

# Тест: Обработка невалидной даты
def test_invalid_due_date(task_manager):
    with pytest.raises(ValueError, match="Неправильный формат даты. Используйте YYYY-MM-DD."):
        task_manager.add_task("Invalid Date Task", "Description", "Category", "invalid-date", "высокий")

# Тест: Обработка пустого названия задачи
def test_empty_task_title(task_manager):
    with pytest.raises(ValueError, match="Название задачи не может быть пустым."):
        task_manager.add_task("", "Description", "Category", "2024-12-31", "высокий")

# Тест: Уникальные идентификаторы задач
def test_unique_task_ids(task_manager):
    task_manager.add_task("Task 1", "Description 1", "Category 1", "2024-12-31", "высокий")
    task_manager.add_task("Task 2", "Description 2", "Category 2", "2024-12-31", "средний")
    assert task_manager.tasks[0].id != task_manager.tasks[1].id

# Тест: Редактирование задачи
def test_edit_task(task_manager):
    task_manager.add_task("Task to Edit", "Description", "Category", "2024-12-31", "средний")
    task_manager.edit_task(1, title="Edited Task", priority="высокий")
    task = task_manager.get_task_by_id(1)
    assert task.title == "Edited Task"
    assert task.priority == "высокий"

# Тест: Поиск задачи по категории
def test_search_task_by_category(task_manager):
    task_manager.add_task("Task 1", "Description 1", "Work", "2024-12-31", "высокий")
    task_manager.add_task("Task 2", "Description 2", "Personal", "2024-12-31", "средний")
    results = [task for task in task_manager.tasks if task.category == "Work"]
    assert len(results) == 1
    assert results[0].category == "Work"

# Тест: Удаление задач по категории
def test_delete_task_by_category(task_manager):
    task_manager.add_task("Task 1", "Description 1", "Work", "2024-12-31", "высокий")
    task_manager.add_task("Task 2", "Description 2", "Work", "2024-12-31", "средний")
    task_manager.delete_task(category="Work")
    assert len(task_manager.tasks) == 0

