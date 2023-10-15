import tkinter as tk
from tkinter import Text

from sub_project_2.machine_learning.MachineLearning import MachineLearning


# Клас для інтерфейсу Tkinter
class GUI:
    def __init__(self):
        # Створюємо головне вікно Tkinter
        self.root = tk.Tk()
        self.root.title("Результати машинного навчання")

        # Створюємо текстове поле для результатів та кнопку для оновлення
        self.results_text_widget = Text(self.root, wrap=tk.WORD, height=20, width=60)
        self.results_text_widget.pack()

        self.update_button = tk.Button(self.root, text="Оновити результати", command=self.update_results)
        self.update_button.pack()

    def update_results(self):
        # Замініть цей блок коду на ваш код, який генерує результати машинного навчання
        # Отримайте результати з класу MachineLearning
        ml = MachineLearning()
        ml.train_model()
        results_text = f'Accuracy: {ml.accuracy}\n\nConfusion Matrix:\n{ml.conf_matrix}\n\nClassification Report:\n{ml.report}'

        # Видаляємо попередні дані у текстовому полі
        self.results_text_widget.delete(1.0, tk.END)

        # Додаємо нові дані у текстове поле
        self.results_text_widget.insert(tk.END, results_text)

    def run(self):
        self.root.mainloop()
