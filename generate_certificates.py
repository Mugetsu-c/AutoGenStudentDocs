def generate_certificates(template_path, save_path, students):
    # Создаем экземпляр документа
    docx = DocxTemplate(template_path)

    # Определяем данные студентов
    context = {'students': students}

    # Рендерим шаблон с данными студентов
    docx.render(context)

    # Сохраняем общий документ
    docx.save(save_path)
    print(students)
    print(f'Все справки сохранены в файле: {save_path}')








































# from docx import Document
# from docxtpl import DocxTemplate

# def generate_certificates(students):
#     # Создаем экземпляр документа
#     doc = DocxTemplate('./templates/весь список.docx')

#     # Определяем данные студентов
#     context = {'students': students}

#     # Рендерим шаблон с данными студентов
#     doc.render(context)

#     # Сохраняем общий документ
#     output_path = 'certificates.docx'
#     doc.save(output_path)

#     print(f'Все справки сохранены в файле: {output_path}')

# if __name__ == '__main__':
#     # Пример списка студентов (добавьте своих студентов)
#     students = [
#         {
#             'destination': 'в пенсионный фонд',
#             'full_name': 'Иванов Иван Иванович',
#             'well': 3,
#             'group': 'A123',
#         },
#         {
#             'destination': 'по месту требования',
#             'full_name': 'Петров Петр Петрович',
#             'well': 2,
#             'group': 'B456',
#         },
#         # Добавьте данные других студентов
#     ]

#     # Генерируем справки для всех студентов
#     generate_certificates(students)











from docx import Document
from docxtpl import DocxTemplate

def generate_certificates(template_path, save_path, students):
    # Создаем экземпляр документа
    doc = DocxTemplate(template_path)

    # Определяем данные студентов
    context = {'students': students}

    # Рендерим шаблон с данными студентов
    doc.render(context)

    # Сохраняем общий документ
    doc.save(save_path)
    print(students)
    print(f'Все справки сохранены в файле: {save_path}')


# if __name__ == '__main__':
#     # Вызываем функцию select_and_save_students для выбора студентов и получения списка
#     nested_folder_path = create_main_and_nested_folders()
#     selected_users = select_and_save_students(nested_folder_path)

#     # Передаем список выбранных студентов в функцию generate_certificates
#     generate_certificates(selected_users)
