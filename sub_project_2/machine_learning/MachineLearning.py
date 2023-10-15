import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split


class MachineLearning:
    def __init__(self):
        # Завантаження данних з CSV-файлу
        self.data = pd.read_csv('simulation_metrics.csv')

    def train_model(self):
        # Визначте фічі (ознаки) і цільову змінну
        features = self.data[['Optical Drone Observation', 'Distance Between Drones', 'Optical Drone Battery', 'FTP Drone Battery', 'Optical Drone Speed', 'FTP Drone Speed']]
        target = self.data['Emergency Detected']

        # Розділіть дані на тренувальний та тестовий набори
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Ініціалізуйте та навчіть модель RandomForestClassifier
        self.model = RandomForestClassifier(random_state=42)
        self.model.fit(X_train, y_train)

        # Зробіть передбачення на тестовому наборі
        y_pred = self.model.predict(X_test)

        # Оцініть результати
        self.accuracy = accuracy_score(y_test, y_pred)
        self.conf_matrix = confusion_matrix(y_test, y_pred)
        self.report = classification_report(y_test, y_pred)

    def display_results(self):
        print(f'Accuracy: {self.accuracy}')
        print(f'Confusion Matrix:\n{self.conf_matrix}')
        print(f'Classification Report:\n{self.report}')