import sys
import os
sys.path.append(os.getcwd())

from datetime import datetime
import re

def determine_year_of_admission(
    group_name: str, 
    current_course: int
    ) -> int:
    current_year = datetime.now().year
    group_name = group_name.strip().upper().replace(' ', '')
    # Заменяем различные варианты дефисов на стандартный дефис
    group_name = re.sub(r'[–—_]', '-', group_name)
    # Регулярное выражение для поиска года в названии группы
    match = re.search(r'(\d{2})(?:[–—-]\d+)?[М]?$', group_name)
    if match:
        year_suffix = match.group(1) or match.group(2)
        possible_year = int('20' + year_suffix)
        if 2000 <= possible_year <= current_year:
            return possible_year
        elif possible_year > current_year:
            # Если год больше текущего, возможно, это текущий год
            return current_year - current_course + 1
    # Если не удалось извлечь год из группы, используем текущий курс
    return current_year - current_course + 1

def determine_study_duration(
    group_name: str
    ) -> str:
    # Нормализация названия группы
    group_name = group_name.strip().upper().replace(' ', '')
    group_name = re.sub(r'[–—_]', '-', group_name)

    
    # Извлекаем код направления (до первого дефиса)
    group_code_match = re.match(r'^([А-Я]+)', group_name)
    if group_code_match:
        group_code = group_code_match.group(1)
    else:
        group_code = ''
    
    # Список исключений для магистратуры
    master_exceptions = {'ГМС', 'ГМУ', 'УМБ', 'ВГМС', 'ВГМУ', 'ВУМБ'}

    # Проверяем, является ли магистратурой
    is_master = False
    if re.search(r'М$', group_name):
        if group_code not in master_exceptions:
            is_master = True

    # Проверяем, является ли направлением ТД или ЭБ
    if group_code in {'ТД', 'ЭБ'}:
        return 5

    # Определяем срок обучения
    if is_master:
        return 2
    else:
        return 4

def check_study_base(
    study_base: str
) -> str:
    if study_base == 'На контрактной основе':
        return 'На контрактной основе, стипендию не получает'
    return study_base

def get_path_save() -> str:
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    main_folder_name = 'Справки'
    main_folder_path = os.path.join(desktop, main_folder_name)
    
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)
    # os.makedirs(temp_output_path, exist_ok=True)
        
    print(f'Путь функции {main_folder_path}')
    return main_folder_path
    
def main():
    get_path_save()
    
if __name__ == '__main__':
    main()