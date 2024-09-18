from docx import Document
from docxtpl import DocxTemplate
from date_utils import try_strptime

def create_students_info(template_path, save_path, user_data):
    doc = DocxTemplate(template_path)
    
    context = []
    
    for record_str in user_data:
        record_list = record_str.split(",")
        

        date_obj = try_strptime(record_list[0], ['%d.%m.%Y', '%d.%m.%Y %H:%M:%S'])
        date = date_obj.strftime('%d.%m.%Y')  # конвертируем объект datetime в строку
        
        # Заполняем информацию о студенте
        context.append({
            'ФИО': record_list[1],
            'Группа': record_list[2],
            'Дата': date,
            'Куда': record_list[4]
        })
        
    doc.render({'students': context})
    doc.save(save_path)
