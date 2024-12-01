import json
from datetime import datetime
from typing import List, Optional

class Task:
    def __init__(self, task_id: int, title: str, description: str, category: str, due_date: str, priority: str, status: str = "Не выполнена"):
        self.id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict):
        return Task(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"]
        )

class TaskManager:
    def __init__(self, storage_file: str):
        self.storage_file = storage_file
        self.tasks: List[Task] = []
        self.last_id = 0
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.storage_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task) for task in data]
                if self.tasks:
                    self.last_id = max(task.id for task in self.tasks)
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("Ошибка при загрузке данных. Файл поврежден.")

    def save_tasks(self):
        with open(self.storage_file, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title: str, description: str, category: str, due_date: str, priority: str):
        if not title:
            raise ValueError("Название задачи не может быть пустым.")
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неправильный формат даты. Используйте YYYY-MM-DD.")
        
        self.last_id += 1
        new_task = Task(self.last_id, title, description, category, due_date, priority)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Задача '{title}' добавлена успешно!")

    def view_tasks(self, category: Optional[str] = None):
        if not self.tasks:
            print("Нет задач для отображения.")
            return
        for task in self.tasks:
            if category is None or task.category == category:
                print(task.to_dict())

    def edit_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                category: Optional[str] = None, due_date: Optional[str] = None, priority: Optional[str] = None,
                status: Optional[str] = None):
        task = self.get_task_by_id(task_id)
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if category:
                task.category = category
            if due_date:
                task.due_date = due_date
            if priority:
                task.priority = priority
            if status:
                task.status = status
            self.save_tasks()
            print(f"Задача с ID {task_id} успешно обновлена!")
        else:
            print("Задача с таким ID не найдена.")

    def delete_task(self, task_id: Optional[int] = None, category: Optional[str] = None):
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
            print(f"Задача с ID {task_id} удалена.")
        elif category:
            self.tasks = [task for task in self.tasks if task.category != category]
            print(f"Все задачи в категории '{category}' удалены.")
        else:
            print("Необходимо указать ID задачи или категорию для удаления.")
        self.save_tasks()

    def search_tasks(self, keyword: Optional[str] = None, category: Optional[str] = None, status: Optional[str] = None):
        results = self.tasks
        if keyword:
            results = [task for task in results if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]
        if category:
            results = [task for task in results if task.category == category]
        if status:
            results = [task for task in results if task.status == status]
        if results:
            for task in results:
                print(task.to_dict())
        else:
            print("Задачи не найдены.")

    def mark_task_as_done(self, task_id: int):
        self.edit_task(task_id, status="Выполнена")

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

if __name__ == "__main__":
    manager = TaskManager("tasks.json")
    while True:
        print("\nМенеджер задач: ")
        print("1. Просмотреть задачи")
        print("2. Добавить задачу")
        print("3. Изменить задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")
        print("6. Отметить задачу как выполненную")
        print("0. Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            category = input("Введите категорию (или оставьте пустым для просмотра всех задач): ")
            manager.view_tasks(category if category else None)
        elif choice == "2":
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            category = input("Введите категорию задачи: ")
            due_date = input("Введите срок выполнения (YYYY-MM-DD): ")
            priority = input("Введите приоритет (низкий, средний, высокий): ")
            try:
                manager.add_task(title, description, category, due_date, priority)
            except ValueError as e:
                print(e)
        elif choice == "3":
            task_id = int(input("Введите ID задачи для изменения: "))
            title = input("Новое название (или оставьте пустым): ")
            description = input("Новое описание (или оставьте пустым): ")
            category = input("Новая категория (или оставьте пустым): ")
            due_date = input("Новый срок выполнения (или оставьте пустым): ")
            priority = input("Новый приоритет (или оставьте пустым): ")
            status = input("Новый статус (или оставьте пустым): ")
            manager.edit_task(task_id, title, description, category, due_date, priority, status)
        elif choice == "4":
            task_id = input("Введите ID задачи для удаления (или оставьте пустым для удаления по категории): ")
            if task_id:
                manager.delete_task(task_id=int(task_id))
            else:
                category = input("Введите категорию для удаления задач: ")
                manager.delete_task(category=category)
        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска (или оставьте пустым): ")
            category = input("Введите категорию для поиска (или оставьте пустым): ")
            status = input("Введите статус для поиска (или оставьте пустым): ")
            manager.search_tasks(keyword if keyword else None, category if category else None, status if status else None)
        elif choice == "6":
            task_id = int(input("Введите ID задачи для отметки как выполненной: "))
            manager.mark_task_as_done(task_id)
        elif choice == "0":
            break
        else:
            print("Неверный выбор, попробуйте снова.")

