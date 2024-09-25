import sys
import os
sys.path.append(os.getcwd())

from datetime import datetime
from dataclasses import dataclass

@dataclass
class Student:
    full_name: str  # 'ФИО (в дательном падеже)'
    group: str  # 'Группа'
    course: int  # 'На каком курсе вы обучаетесь?'
    study_form: str  # 'По какой форме вы обучаетесь?'
    destination: str  # 'Куда нужна справка?'
    quantity: int  # 'В каком количестве нужна справка ?'
    timestamp: datetime  # 'Отметка времени'
    date_of_receipt: int = None # 'Дата поступления'
    study_base: str = None  # 'Нужно указать что обучается на контрактной/бюджетной основе?(+Стипендию не получает/стипендию получает)'
    study_duration: int = None  # Срок обучения
    order_number: str = None  # 'Приказ зачисления' если добавляется
    '''
    Инициализация нового объекта Student с полной информацией о студенте.
    :param full_name: ФИО студента.
    :param group: Группа.
    :param course: Курс, на котором учится студент.
    :param study_form: Форма обучения (очно, очно-заочно, заочно).
    :param destination: Место назначения справки.
    :param quantity: Количество требуемых справок.
    :param timestamp: Время оставления заявки.
    :param date_of_receipt: Дата поступления.
    :param study_base: Основа обучения (контракт, бюджет).
    :param study_duration: Срок обучения.
    :param order_number: Приказ зачисления.
    '''

def main():
    pass
    
if __name__ == '__main__':
    main()