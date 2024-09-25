import sys
import os
sys.path.append(os.getcwd())

import csv
import requests
from pprint import pprint
from datetime import datetime, timedelta
from App.Model.Students import Student
from App.Model.BusinessLogic import determine_year_of_admission, determine_study_duration, check_study_base


class CSVDataHandler():
    def __init__(self, filepath: str ='./data/downloaded_data.csv'):
        '''
        Инициализация обработчика данных CVS.
        :param filepath: Путь к файлу CSV.
        '''
        self.filepath = filepath
        
    
    def read_csv(self):
        '''
        Читает данные из CSV файла и возвращает их в виде списка словарей.
        Каждая строка файла преобразуется в словарь, где ключи - это заголовки столбцов.
        :return: Список словарей с данными.
        '''
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            print(f'Ошибка при чтении файла {self.filepath}: {e}')
            return None
        
    def download_csv(self, url: str = 'https://docs.google.com/spreadsheets/d/1KXlQoXBkdeDiPIImMCwGR6-f1-8MQmRnQDjKmKZiut0/export?format=csv'):
        '''
        Скачивает файл CSV по указанному URL и сохраняет его по пути self.filepath.
        :param url: URL адрес файла CSV.
        '''
        try:
            response = requests.get(url) # Отправляем запрос по ссылке
            response.raise_for_status() # Проверяем, не произошла ли ошибка при запросе
            with open(self.filepath, 'wb') as f:
                f.write(response.content)
            print(f'Файл успешно скачан и сохранен в {self.filepath}')
        except requests.exceptions.RequestException as e:
            print(f'Ошибка при скачивании файла: {e}')
        
        
    def load_data(self, time_frame: int = 24):
        '''
        Загружает данные за указанное количество часов из файла.
        :param time_frame: количество часов для загрузки данных.
        '''
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=time_frame)
        data = self.read_csv()
        if data is None:
            print('No data loaded.')
            return []

        filtered_data = [
            entry for entry in data if datetime.strptime(entry['Отметка времени'], '%d.%m.%Y %H:%M:%S') >= start_time
        ]
        return filtered_data
        
    def parse_data_to_students(self, raw_data: list):
        students = []
        for data in raw_data:
            try:
                # Преобразуем данные в нужные типы
                course = int(data.get('На каком курсе вы обучаетесь?', None))
                quantity = int(data.get('В каком количестве нужна справка ?', None))
                timestamp = datetime.strptime(data['Отметка времени'], '%d.%m.%Y %H:%M:%S')
                date_of_receipt = int(determine_year_of_admission(group_name=data['Группа'], current_course=course))
                study_base = check_study_base(study_base=data['Основа обучения (бюджет/контракт)?'])
                study_duration = int(determine_study_duration(group_name=data['Группа']))
                

                # Создаем объект Student
                student = Student(
                    full_name=data.get('ФИО (в дательном падеже)', None),
                    group=(data.get('Группа', None)).upper(),
                    course=course,
                    study_form=data.get('По какой форме вы обучаетесь?', None),
                    destination=data.get('Куда нужна справка?', None),
                    quantity=quantity,
                    timestamp=timestamp,
                    date_of_receipt=date_of_receipt,
                    study_base=study_base,
                    study_duration = study_duration,
                    order_number=data.get('Приказ зачисления', None)
                )
                students.append(student)
                
            except KeyError as e:
                print(f'Missing data for required field: {e}')
            except ValueError as e:
                print(f'Error processing data for Student: {e}')

        return students

def main():
    csv_handler = CSVDataHandler()
    raw_data = csv_handler.load_data(400)
    data_students = csv_handler.parse_data_to_students(raw_data)
    

if __name__ == '__main__':
    main()