import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry  

class ProjectManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Система управления проектами")
        self.geometry("600x600")
        self.resizable(False, False)

        self.projects = []
        self.current_project_id = None

        self.project_entry = None
        self.task_entry = None
        self.task_description_entry = None
        self.task_start_date_entry = None
        self.task_end_date_entry = None
        self.tasks_canvas = None
        self.tasks_frame = None

        self.init_ui()

    def init_ui(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        self.projects_tab = ttk.Notebook(main_frame)
        self.projects_tab.pack(fill="both", expand=True)

        self.create_project_tab = ttk.Frame(self.projects_tab)
        self.projects_tab.add(self.create_project_tab, text="Создать проект")

        project_label = tk.Label(self.create_project_tab, text="Название проекта:")
        project_label.pack()

        self.project_entry = tk.Entry(self.create_project_tab, validate="key")
        self.project_entry['validatecommand'] = (self.project_entry.register(self.on_validate), '%P')
        self.project_entry.pack()

        self.max_length_label = tk.Label(self.create_project_tab, text="Максимальное количество символов: 25", fg="red")

        task_label = tk.Label(self.create_project_tab, text="Добавить задачу:")
        task_label.pack()

        self.task_entry = tk.Entry(self.create_project_tab)
        self.task_entry.pack()

        task_description_label = tk.Label(self.create_project_tab, text="Описание задачи:")
        task_description_label.pack()

        self.task_description_entry = tk.Text(self.create_project_tab, height=4)
        self.task_description_entry.pack()

        task_start_date_label = tk.Label(self.create_project_tab, text="Дата начала:")
        task_start_date_label.pack()

        self.task_start_date_entry = DateEntry(self.create_project_tab)
        self.task_start_date_entry.pack()

        task_end_date_label = tk.Label(self.create_project_tab, text="Дата завершения:")
        task_end_date_label.pack()

        self.task_end_date_entry = DateEntry(self.create_project_tab)
        self.task_end_date_entry.pack()

        add_task_button = tk.Button(self.create_project_tab, text="Добавить задачу", command=self.add_task)
        add_task_button.pack()

        create_project_button = tk.Button(self.create_project_tab, text="Создать проект", command=self.create_project)
        create_project_button.pack()

        tasks_scrollbar = tk.Scrollbar(self.create_project_tab, orient=tk.VERTICAL)
        self.tasks_canvas = tk.Canvas(self.create_project_tab, yscrollcommand=tasks_scrollbar.set)
        tasks_scrollbar.config(command=self.tasks_canvas.yview)
        self.tasks_frame = ttk.Frame(self.tasks_canvas)
        self.tasks_canvas.create_window((0, 0), window=self.tasks_frame, anchor="nw")
        self.tasks_canvas.pack(side="left", fill="both", expand=True)
        tasks_scrollbar.pack(side="right", fill="y")
        self.tasks_frame.bind("<Configure>", lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all")))

    def add_task(self):
        task_text = self.task_entry.get()
        task_description = self.task_description_entry.get("1.0", tk.END)
        task_start_date = self.task_start_date_entry.get_date().strftime("%d.%m.%Y")
        task_end_date = self.task_end_date_entry.get_date().strftime("%d.%m.%Y")

        if task_text.strip() == "":
            messagebox.showerror("Ошибка", "Введите название задачи")
            return

        self.task_entry.delete(0, tk.END)
        self.task_description_entry.delete("1.0", tk.END)
        self.task_start_date_entry.delete(0, tk.END)
        self.task_end_date_entry.delete(0, tk.END)

        task_frame = ttk.Frame(self.tasks_frame)
        task_frame.pack(fill="x", pady=5)

        task_name_label = tk.Label(task_frame, text=task_text, font=("Helvetica", 14, "bold"), wraplength=550, anchor="center")
        task_name_label.pack(side="top")

        task_description_label = tk.Label(task_frame, text=task_description, wraplength=550, anchor="center")
        task_description_label.pack(side="top")

        task_start_date_label = tk.Label(task_frame, text="Дата начала: " + task_start_date, anchor="center")
        task_start_date_label.pack(side="top")

        task_end_date_label = tk.Label(task_frame, text="Дата завершения: " + task_end_date, anchor="center")
        task_end_date_label.pack(side="top")

        delete_task_button = tk.Button(task_frame, text="Удалить", command=lambda frame=task_frame: self.delete_task(frame))
        delete_task_button.pack(side="bottom", pady=5)

    def delete_task(self, task_frame):
        task_frame.destroy()

    def create_project(self):
        project_name = self.project_entry.get()
        if project_name:
            project_name = project_name[:25]

            tasks_exist = False
            for child in self.tasks_frame.winfo_children():
                if isinstance(child, ttk.Frame):
                    tasks_exist = True
                    break

            if not tasks_exist:
                messagebox.showerror("Ошибка", "Добавьте хотя бы одну задачу для создания проекта")
                return

            project_tab = ttk.Frame(self.projects_tab)
            self.projects_tab.add(project_tab, text=project_name)

            tasks_scrollbar = tk.Scrollbar(project_tab, orient=tk.VERTICAL)
            tasks_canvas = tk.Canvas(project_tab, yscrollcommand=tasks_scrollbar.set)
            tasks_scrollbar.config(command=tasks_canvas.yview)
            tasks_frame = ttk.Frame(tasks_canvas)
            tasks_canvas.create_window((0, 0), window=tasks_frame, anchor="nw")
            tasks_canvas.pack(side="left", fill="both", expand=True)
            tasks_scrollbar.pack(side="right", fill="y")
            tasks_frame.bind("<Configure>", lambda e: tasks_canvas.configure(scrollregion=tasks_canvas.bbox("all")))

            tasks = []
            for child in self.tasks_frame.winfo_children():
                if isinstance(child, ttk.Frame):
                    task_name_label = child.winfo_children()[0]
                    task_description_label = child.winfo_children()[1]
                    task_start_date_label = child.winfo_children()[2]
                    task_end_date_label = child.winfo_children()[3]
                    tasks.append({
                        "text": task_name_label.cget("text"),
                        "description": task_description_label.cget("text"),
                        "start_date": task_start_date_label.cget("text").split(": ")[1],
                        "end_date": task_end_date_label.cget("text").split(": ")[1]
                    })

            for task in tasks:
                task_frame = ttk.Frame(tasks_frame)
                task_frame.pack(fill="x", pady=5)

                task_name_label = tk.Label(task_frame, text=task["text"], font=("Helvetica", 14, "bold"),
                                           wraplength=550, anchor="center")
                task_name_label.pack(side="top")

                task_description_label = tk.Label(task_frame, text=task["description"], wraplength=550, anchor="center")
                task_description_label.pack(side="top")

                task_start_date_label = tk.Label(task_frame, text="Дата начала: " + task["start_date"], anchor="center")
                task_start_date_label.pack(side="top")

                task_end_date_label = tk.Label(task_frame, text="Дата завершения: " + task["end_date"], anchor="center")
                task_end_date_label.pack(side="top")

                status_options = ["Готово", "Не готово", "В работе"]
                status_var = tk.StringVar(task_frame)
                status_var.set(status_options[0])
                status_menu = tk.OptionMenu(task_frame, status_var, *status_options)
                status_menu.pack(side="right", padx=5)

            delete_project_button = tk.Button(project_tab, text="Удалить проект",
                                              command=lambda: self.delete_project(project_tab))
            delete_project_button.pack(side="bottom", anchor="e", padx=10, pady=10)

            report_button = tk.Button(project_tab, text="Отчет", command=self.generate_project_report)
            report_button.pack(side="bottom", anchor="e", padx=10, pady=10)

    def generate_project_report(self):
        selected_project = self.projects_tab.tab(self.projects_tab.select(), "text")

        tasks_frame = None
        for child in self.projects_tab.winfo_children():
            if isinstance(child, ttk.Frame) and self.projects_tab.tab(child, "text") == selected_project:
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Canvas):
                        tasks_frame = grandchild.winfo_children()[0]
                        break
                break

        if tasks_frame is None:
            messagebox.showerror("Ошибка", "Не удалось найти информацию о проекте")
            return

        tasks_info = []
        for task_frame in tasks_frame.winfo_children():
            if isinstance(task_frame, ttk.Frame):
                task_name = task_frame.winfo_children()[0]["text"]
                task_description = task_frame.winfo_children()[1]["text"]
                start_date = task_frame.winfo_children()[2]["text"].split(": ")[1]
                end_date = task_frame.winfo_children()[3]["text"].split(": ")[1]
                tasks_info.append((task_name, task_description, start_date, end_date))

        report_text = f"Отчет по проекту: {selected_project}\n\n"
        report_text += f"Количество задач: {len(tasks_info)}\n\n"
        for idx, task_info in enumerate(tasks_info, start=1):
            report_text += f"Задача {idx}:\n"
            report_text += f"Название: {task_info[0]}\n"
            report_text += f"Описание: {task_info[1]}\n"
            report_text += f"Дата начала: {task_info[2]}\n"
            report_text += f"Дата завершения: {task_info[3]}\n\n"

        messagebox.showinfo("Отчет о проекте", report_text)

    def delete_project(self, project_tab):
        project_tab.destroy()

    def on_validate(self, value):
        if len(value) > 25:
            if not self.max_length_label.winfo_ismapped():
                self.max_length_label.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            if self.max_length_label.winfo_ismapped():
                self.max_length_label.pack_forget()
        return len(value) <= 25

if __name__ == "__main__":
    app = ProjectManagementApp()
    app.mainloop()
