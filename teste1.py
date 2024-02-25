import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import pickle
import os

TASKS_FILE = "tasks.pickle"

class Task:
    PRIORITIES = {"Baixa": 1, "Média": 2, "Alta": 3}

    def __init__(self, disciplina, descricao, start_date, end_date, tipo_atividade, priority="Média"):
        self.disciplina = disciplina
        self.descricao = descricao
        self.start_date = datetime.strptime(start_date, "%d/%m/%Y")
        self.end_date = datetime.strptime(end_date, "%d/%m/%Y")
        self.tipo_atividade = tipo_atividade
        self.priority = priority
    
    def get_priority(self):
        return self.PRIORITIES.get(self.priority, 2)

    #criar algumas tasks inciais
with open(TASKS_FILE, "wb") as f:
    pickle.dump(Task("Matemática", "Calcular o", "10/02/2024", "25/02/2024", "E-Folio", "Média") f)

    
class Folio(Task):
    def __init__(self, disciplina, descricao, start_date, end_date, priority="Média"):
        super().__init__(
            disciplina, descricao, start_date, end_date, "E-Folio", priority
        )


class SessaoSincrona(Task):
    def __init__(self, disciplina, descricao, start_date, end_date, priority="Média"):
        super().__init__(
            disciplina, descricao, start_date, end_date, "Sessao Sincrona", priority
        )


class AtividadeFormativa(Task):
    def __init__(self, disciplina, descricao, start_date, end_date, priority="Média"):
        super().__init__(
            disciplina, descricao, start_date, end_date, "Atividade Formativa", priority
        )


class ExameGlobal(Task):
    def __init__(self, disciplina, descricao, start_date, end_date, priority="Média"):
        super().__init__(
            disciplina, descricao, start_date, end_date, "Exame Global", priority
        )


class TaskList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        self.sort_tasks()

    def remove_task(self, index):
        del self.tasks[index]
        self.sort_tasks()

    def sort_tasks(self):
        self.tasks.sort(key=lambda x: x.get_priority())

    def edit_task(self, index, updated_task):
        self.tasks[index] = updated_task
        self.sort_tasks()


class TaskApp:
    def __init__(self, master):
        self.master = master
        master.title("TaskApp")

        self.task_list = TaskList()

        self.selected_task_index = None

        #  carregar tasks 
    def load_tasks_from_file(self):
        if os.path.exists("tasks.pickle") and os.path.getsize("tasks.pickle") > 0:
            with open("tasks.pickle", "rb") as f:
                try:
                    self.task_list.tasks = pickle.load(f)
                    self.update_task_listbox()
                except pickle.UnpicklingError:
                    print("Error loading pickle. File may be corrupted.")

    def save_tasks_to_file(self):
        with open("tasks.pickle", "wb") as f:
            pickle.dump(self.task_list.tasks, f)

    def add_task_button_click(self, master):  # Add master as an argument

        self.selected_index = None

        self.disciplina_label = ttk.Label(master, text="Disciplina")
        self.disciplina_entry = ttk.Entry(master)

        self.descricao_label = ttk.Label(master, text="Descrição")
        self.descricao_entry = ttk.Entry(master, width=40)

        self.start_date_label = ttk.Label(master, text="Data de início")
        self.start_date_entry = ttk.Entry(master, width=20)

        self.end_date_label = ttk.Label(master, text="Data de término")
        self.end_date_entry = ttk.Entry(master, width=20)

        self.tipo_atividade_label = ttk.Label(master, text="Tipo de Atividade")
        self.tipo_atividade_entry = ttk.Combobox(
            master,
            values=[
                "Folio",
                "Sessao Sincrona",
                "Atividade Formativa",
                "Exame Global",
                ],
            )

        self.priority_label = ttk.Label(master, text="Prioridade")
        self.priority_combobox = ttk.Combobox(master, values=["Baixa", "Média", "Alta"])
        self.priority_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.priority_combobox.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_task_button = ttk.Button(
            master, text="Adicionar tarefa", command=self.add_task_button_click
        )

        self.remove_task_button = ttk.Button(
            master, text="Remover tarefa", command=self.remove_task_button_click
        )

        self.edit_task_button = ttk.Button(
            master, text="Editar tarefa", command=self.edit_task_button_click
        )

        self.disciplina_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.disciplina_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        self.descricao_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.descricao_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        self.start_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        self.end_date_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.end_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

        self.tipo_atividade_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.tipo_atividade_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

        self.add_task_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.remove_task_button.grid(row=8, column=0, columnspan=2, pady=10)

        self.edit_task_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.task_listbox = tk.Listbox(
            master, selectmode=tk.SINGLE, width=50, height=10
        )
        self.task_listbox.grid(row=7, column=0, columnspan=2, pady=10, padx=5)

        y_scrollbar = tk.Scrollbar(
            master, orient=tk.VERTICAL, command=self.task_listbox.yview
        )
        y_scrollbar.grid(row=7, column=2, sticky=tk.NS)
        self.task_listbox.config(yscrollcommand=y_scrollbar.set)

        self.task_listbox.bind("<<ListboxSelect>>", self.show_selected_task)

    def get_specific_class(self, tipo_atividade):
        type_mapping = self.get_type_mapping()
        return type_mapping.get(tipo_atividade, Task)

    def add_task_button_click(self, master):  # Add master as an argument
        disciplina = self.disciplina_entry.get()
        descricao = self.descricao_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        tipo_atividade = self.tipo_atividade_entry.get()
        priority = self.priority_combobox.get()

        if not all(
            [disciplina, descricao, start_date, end_date, tipo_atividade, priority]
        ):
            messagebox.showwarning(
                "Aviso", "Preencha todos os campos antes de adicionar uma tarefa."
            )
        else:
            try:
                if tipo_atividade not in self.get_type_mapping():
                    messagebox.showerror("Erro", "Tipo de atividade inválido.")
                    return

                specific_class = self.get_specific_class(tipo_atividade)

                if specific_class == Task:
                    task = specific_class(
                        disciplina,
                        descricao,
                        start_date,
                        end_date,
                        tipo_atividade,
                        priority,
                    )
                else:
                    task = specific_class(
                        disciplina,
                        descricao,
                        start_date,
                        end_date,
                        priority=priority,
                    )

                self.task_list.add_task(task)
                self.task_list.sort_tasks()

                task_info = f"{disciplina} - {descricao} - {tipo_atividade} - {start_date} a {end_date} - Prioridade: {priority}"
                self.task_listbox.insert(tk.END, task_info)

                with open("tasks.pickle", "wb") as f:
                    pickle.dump(self.task_list.tasks, f)

            except ValueError:
                messagebox.showerror(
                    "Erro", "Formato de data inválido. Use o formato dd/mm/yyyy."
                )



    def remove_task_button_click(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            try:
                self.task_list.remove_task(selected_index[0])
                self.task_listbox.delete(selected_index[0])

                with open("tasks.json", "w") as f:
                    json.dump(self.task_list.tasks, f)
            except IndexError:
                messagebox.showwarning("Aviso", "Selecione uma tarefa para remover.")

    def show_selected_task(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_task = self.task_list.tasks[selected_index[0]]
            descricao = selected_task.descricao
            self.descricao_entry.delete(0, tk.END)
            self.descricao_entry.insert(0, descricao)

    def edit_task_button_click(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_task = self.task_list.tasks[selected_index[0]]

            selected_task.disciplina = self.disciplina_entry.get()
            selected_task.descricao = self.descricao_entry.get()
            selected_task.start_date = self.start_date_entry.get()
            selected_task.end_date = self.end_date_entry.get()
            selected_task.tipo_atividade = self.tipo_atividade_entry.get()

            self.task_list.sort_tasks()

            task_info = f"{selected_task.disciplina} - {selected_task.tipo_atividade} - {selected_task.start_date} a {selected_task.end_date} - Prioridade: {selected_task.priority}"
            self.task_listbox.delete(selected_index[0])
            self.task_listbox.insert(selected_index[0], task_info)

            with open("tasks.json", "w") as f:
                json.dump(self.task_list.tasks, f, cls=DateTimeEncoder)

            self.disciplina_entry.delete(0, tk.END)
            self.descricao_entry.delete(0, tk.END)
            self.start_date_entry.delete(0, tk.END)
            self.end_date_entry.delete(0, tk.END)
            self.tipo_atividade_entry.set("")

    def get_type_mapping(self):
        return {
            "E-Folio": Folio,
            "Sessao Sincrona": SessaoSincrona,
            "Atividade Formativa": AtividadeFormativa,
            "Exame Global": ExameGlobal,
        }


root = tk.Tk()
app = TaskApp(root)
root.mainloop()
