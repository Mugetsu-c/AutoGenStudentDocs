import sys
import os
sys.path.append(os.getcwd())

from docx import Document
from pprint import pprint

from docxtpl import DocxTemplate
from datetime import datetime

class DocumentGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    # def generate_documents(self, students, template_dir):
    #     #для справок
    #     template_path = os.path.join(template_dir, 'Справки.docx')  # Правильно формируем путь
        
    #     doc = DocxTemplate(template_path)
    #     context = {'students': students}
    #     doc.render(context)
        
    #     output_filename = f'Справки.docx'
        
    #     temp_output_path = self.get_path_folder()
        
    #     output_path = os.path.join(temp_output_path, output_filename)
    #     doc.save(output_path)
    def generate_spravki(self, students, template_dir):
        template_path = os.path.join(template_dir, 'Справки.docx')
        
        doc = DocxTemplate(template_path)
        context = {'students': students}
        doc.render(context)
        
        output_filename = 'Справки.docx'
        output_path = self.get_path_folder()
        
        output_path = os.path.join(output_path, output_filename)
        doc.save(output_path)
        print(f'Справки сохранены в: {output_path}')

    def generate_student_list(self, students, template_dir):
        template_path = os.path.join(template_dir, 'Список.docx')
        
        doc = DocxTemplate(template_path)
        context = {'students': students}
        doc.render(context)
        
        output_filename = 'Список.docx'
        output_path = self.get_path_folder()
        
        output_path = os.path.join(output_path, output_filename)
        doc.save(output_path)
        
        print(f'Список студентов сохранен в: {output_path}')

    def generate_documents(self, students, template_dir):
        self.generate_spravki(students, template_dir)
        self.generate_student_list(students, template_dir)
        
    def get_path_folder(self):
        output_folder = f'Сгенерированные справки за {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}'
        output_path = os.path.join(self.output_dir, output_folder)  # Используем os.path.join для формирования пути к выходному файлу
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            
        return output_path

def main():
    pass
    
if __name__ == '__main__':
    main()