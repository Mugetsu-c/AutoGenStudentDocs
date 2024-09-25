# from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox
# from PyQt5.QtCore import Qt

# class ComboBoxDelegate(QStyledItemDelegate):
#     def __init__(self, options, parent=None):
#         super().__init__(parent)
#         self.options = options

#     def createEditor(self, parent, option, index):
#         combo = QComboBox(parent)
#         combo.addItems(self.options)
#         combo.setEditable(True)  # Разрешаем ввод от руки
#         return combo

#     def setEditorData(self, editor, index):
#         value = index.data(Qt.EditRole)
#         if value is not None:
#             idx = editor.findText(str(value))
#             if idx >= 0:
#                 editor.setCurrentIndex(idx)
#             else:
#                 editor.setEditText(str(value))

#     def setModelData(self, editor, model, index):
#         value = editor.currentText()
#         model.setData(index, value, Qt.EditRole)



from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox

class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.items = items

    def createEditor(self, parent, option, index):
        comboBox = QComboBox(parent)
        comboBox.addItems(self.items)
        comboBox.setEditable(True)
        return comboBox

    def setEditorData(self, editor, index):
        text = index.data(Qt.DisplayRole)
        idx = editor.findText(text)
        if idx >= 0:
            editor.setCurrentIndex(idx)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.EditRole)