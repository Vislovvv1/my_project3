import tkinter as tk
from tkinter import ttk, messagebox
from classes import Task, TaskManager


class TaskManagerApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("600x500")
        self.setup_ui()

    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Настройка веса строк и столбцов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Поля ввода
        ttk.Label(main_frame, text="Название задачи:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = ttk.Entry(main_frame, width=40)
        self.title_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(main_frame, text="Описание:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        self.desc_text = tk.Text(main_frame, height=4, width=30)
        self.desc_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        ttk.Label(main_frame, text="Срок выполнения (ГГГГ-ММ-ДД):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(main_frame, width=20)
        self.date_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Добавить задачу", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить выбранную", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить поля", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)

        # Список задач
        ttk.Label(main_frame, text="Список задач:").grid(row=4, column=0, sticky=tk.NW, pady=5)

        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=4, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.tasks_listbox = tk.Listbox(list_frame, width=50)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tasks_listbox.yview)
        self.tasks_listbox.configure(yscrollcommand=scrollbar.set)

        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Привязка двойного клика для просмотра деталей
        self.tasks_listbox.bind('<Double-Button-1>', self.show_task_details)

        self.update_listbox()

    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get().strip()

        if not title:
            messagebox.showwarning("Ошибка", "Введите название задачи!")
            return

        if not description:
            messagebox.showwarning("Ошибка", "Введите описание задачи!")
            return

        if not due_date:
            messagebox.showwarning("Ошибка", "Введите срок выполнения!")
            return

        # Простая валидация даты
        if len(due_date) != 10 or due_date[4] != '-' or due_date[7] != '-':
            messagebox.showwarning("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД!")
            return

        task = Task(title, description, due_date)
        self.manager.add_task(task)
        self.update_listbox()
        self.clear_inputs()
        messagebox.showinfo("Успех", "Задача успешно добавлена!")

    def delete_task(self):
        selected = self.tasks_listbox.curselection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления!")
            return

        task_title = self.manager.tasks[selected[0]].title
        if messagebox.askyesno("Подтверждение", f"Удалить задачу '{task_title}'?"):
            self.manager.delete_task(selected[0])
            self.update_listbox()
            messagebox.showinfo("Успех", "Задача удалена!")

    def show_task_details(self, event):
        selected = self.tasks_listbox.curselection()
        if selected:
            task = self.manager.tasks[selected[0]]
            details = f"Название: {task.title}\n\nОписание:\n{task.description}\n\nСрок выполнения: {task.due_date}"
            messagebox.showinfo("Детали задачи", details)

    def update_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for i, task in enumerate(self.manager.tasks):
            self.tasks_listbox.insert(tk.END, f"{i + 1}. {task.title} (до {task.due_date})")

    def clear_inputs(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.date_entry.delete(0, tk.END)
        self.title_entry.focus()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()