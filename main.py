import tkinter as tk
import os
import re
from dotenv import  load_dotenv

from tkinter import ttk
from utils import download_csv, read_filtered_data, create_certificate_jinja, generate_certificates, create_students_info# Импорт новой функции
from tkcalendar import DateEntry
from datetime import datetime
from docxtpl import DocxTemplate

# from create_students_info_doc import create_students_info
from date_utils import try_strptime
# from generate_certificates import generate_certificates

load_dotenv()
CVS_URL = os.getenv('URL')

frame = None
users_doc = []
checkbuttons = []
user_data = []
checkbutton_vars = []


def safe_convert_to_int(value, default=' '):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return default


    
def parse_quantity(value):
    # Проверка, является ли значение числом
    if re.match(r'^\d+$', str(value).strip()):
        return int(value)
    else:
        return 1

def check_nan(value):
    return "                       " if str(value).lower() == "nan" else value



# Функция для безопасного получения элементов из списка
def safe_get(lst, index, default=''):
    try:
        return lst[index]
    except IndexError:
        return default
    
    

def create_main_and_nested_folders():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    main_folder_name = 'AutoStudentDocs'
    main_folder_path = os.path.join(desktop, main_folder_name)
    
    if not os.path.exists(main_folder_path):
        os.makedirs(main_folder_path)
    
    nested_folder_name = datetime.now().strftime("%d.%m.%Y %H-%M-%S")
    nested_folder_path = os.path.join(main_folder_path, nested_folder_name)
    os.makedirs(nested_folder_path)
    
    print(f"Main folder is located at: {main_folder_path}")
    print(f"Nested folder is located at: {nested_folder_path}")
    
    return nested_folder_path


def select_and_save_students(nested_folder_path):
    selected_users = []  # создаем список для выбранных студентов
    selected_students = []  # создаем список для данных выбранных студентов

    for i, record_str in enumerate(user_data):
        if checkbutton_vars[i].get():  # Проверяем, выбран ли студент
            record_list = record_str.split(",")
            date_obj = try_strptime(record_list[0], ['%d.%m.%Y', '%d.%m.%Y %H:%M:%S'])
            record = {
                "d": date_obj.day if date_obj else None,
                "m": date_obj.month if date_obj else None,
                "y": date_obj.year if date_obj else None,
                "full_name": safe_get(record_list, 1, "").title(),
                "group": safe_get(record_list, 2, "   ").upper(),
                "form": check_nan(' '.join(safe_get(record_list, 3).split())),
                "course": safe_convert_to_int(safe_get(record_list, 4)),
                "destination": ' '.join(record_list[5].split()),
                "quantity": parse_quantity(safe_get(record_list, 6))
            }
            print(record, end='\n')
            # Выбираем шаблон справки
            if record['destination'] == 'в пенсионный фонд':
                template_name = 'в пенсионный фонд'
            else:
                template_name = 'по месту требования'

            date = f"{record['d']}.{record['m']}.{record['y']}"

            for j in range(record['quantity']):
                save_path = f"{nested_folder_path}/ {i+1}-{j+1} {template_name} {record['full_name']} {date}.docx"
                # selected_users.append(record_str)  # добавляем студента в список выбранных
                selected_students.append(record)  # добавляем данные в список                
                # Создаем справку
                create_certificate_jinja(template_name, save_path, record)

    # return selected_users, selected_students
    return selected_students


def create_export_folder():
    nested_folder_path = create_main_and_nested_folders()
    # selected_users, selected_students = select_and_save_students(nested_folder_path)
    selected_students = select_and_save_students(nested_folder_path)

    create_students_info('./templates/список студентов.docx', f'{nested_folder_path}/список студентов.docx', selected_students)
    generate_certificates('./templates/весь список.docx', f'{nested_folder_path}/весь список.docx', selected_students)
    return nested_folder_path


def update_data():
    try:
        status_label.config(text="Обновление данных...")
        
        csv_save_path = 'data/downloaded_data.csv'
        download_csv(CVS_URL, csv_save_path)
        status_label.config(text="Данные обновлены.")
    except Exception as e:
        print(f"An error occurred: {e}")


def load_data():
    global checkbuttons, user_data, checkbutton_vars, frame  # Добавьте checkbutton_vars здесь
    for cb in checkbuttons:  # Удаление старых Checkbuttons
        cb.destroy()
    
    checkbuttons.clear()
    checkbutton_vars.clear()  # Очистите список переменных


     # Удаление предыдущего frame, если он существует
    if frame is not None:
        frame.destroy()


    time_period = time_var.get()
    if time_period == "Произвольная дата":
        start_date = date_entry_from.get_date()
        end_date = date_entry_to.get_date()
    else:
        start_date, end_date = None, None
    
    csv_save_path = 'data/downloaded_data.csv'
    user_data = read_filtered_data(csv_save_path, time_period, start_date, end_date)
    # Создание нового frame для checkbuttons и scrollbar
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    # Добавление scrollbar
    scrollbar = tk.Scrollbar(frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Добавление canvas для возможности использования scrollbar
    canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=canvas.yview)

    # Добавление frame внутри canvas для checkbuttons
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    for user in user_data:
        var = tk.BooleanVar(value=True)
        c = tk.Checkbutton(inner_frame, text=user, variable=var)
        c.pack(anchor="w")
        checkbuttons.append(c)
        checkbutton_vars.append(var)
    inner_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def toggle_date_entries(event):
    if time_var.get() == "Произвольная дата":
        date_entry_from.pack()
        date_entry_to.pack()
    else:
        date_entry_from.pack_forget()
        date_entry_to.pack_forget()

root = tk.Tk()
root.title('AutoStudentDocs')

user_data = []

update_button = tk.Button(root, text="Обновить данные", command=update_data)
update_button.pack()

load_button = tk.Button(root, text="Загрузить данные", command=load_data)
load_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

time_label = ttk.Label(root, text="Выберите временной период:")
time_label.pack()

time_options = ["Последние 24 часа", "Последние 48 часов", "Последние 72 часа", "Произвольная дата"]
time_var = tk.StringVar()
time_var.set(time_options[0])

time_combobox = ttk.Combobox(root, textvariable=time_var, values=time_options)
time_combobox.bind('<<ComboboxSelected>>', toggle_date_entries)
time_combobox.pack()

date_entry_from = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
date_entry_to = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)

export_button = tk.Button(root, text="Выгрузить справки", command=create_export_folder)
export_button.pack()

root.mainloop()
