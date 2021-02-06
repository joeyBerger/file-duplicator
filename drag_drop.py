from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QPushButton, QLabel, QCheckBox
from PyQt5 import QtCore 
import sys
import os
import shutil


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Duplicator")
        self.setFixedSize(500, 300)       
        self.setAcceptDrops(True)

        widget_buffer = (30,50)
        text_field_size = (350,30)
        label_buffer = 30

        self.file_display_text = QTextEdit(self)
        self.file_display_text.setReadOnly(True)
        self.file_display_text.move(int(self.rect().width()/2-text_field_size[0]/2),int(widget_buffer[1]-text_field_size[1]/2))
        self.file_display_text.resize(text_field_size[0],text_field_size[1])
        container_dimensions = (self.rect().width(),self.rect().height())

        self.file_display_label = QLabel('Left', self)
        self.file_display_label.resize(200,30)
        self.file_display_label.move(int(container_dimensions[0]/2-self.file_display_label.rect().width()/2),int(widget_buffer[1]-text_field_size[1]/2-label_buffer))
        self.file_display_label.setText("File To Duplicate (Drag File):")

        text_field_size = (150,30)

        self.new_flie_name_text = QTextEdit(self)
        self.new_flie_name_text.move(widget_buffer[0],int(container_dimensions[1]/2-text_field_size[1]/2))
        self.new_flie_name_text.resize(text_field_size[0],text_field_size[1])
        self.new_flie_name_text_label = QLabel('Center', self)
        self.new_flie_name_text_label.resize(120,30)
        self.new_flie_name_text_label.move(self.new_flie_name_text.pos().x(),int(container_dimensions[1]/2-text_field_size[1]/2-label_buffer))
        self.new_flie_name_text_label.setText("New File Name:")

        text_field_size = (60,30)

        self.starting_number_text = QTextEdit(self)
        self.starting_number_text.move(int(container_dimensions[0]/2-20),int(container_dimensions[1]/2-text_field_size[1]/2))
        self.starting_number_text.resize(text_field_size[0],text_field_size[1])
        self.starting_number_text.setPlainText("1")
        self.starting_number_text.textChanged.connect(lambda: self.onAmountChange(self.starting_number_text))

        self.starting_number_label = QLabel('Center', self)
        self.starting_number_label.resize(120,30)
        self.starting_number_label.move(self.starting_number_text.pos().x(),int(container_dimensions[1]/2-text_field_size[1]/2-label_buffer))
        self.starting_number_label.setText("Starting Number:")

        self.copy_amount_text = QTextEdit(self)  
        self.copy_amount_text.move(int(container_dimensions[0]-(widget_buffer[0]*2+text_field_size[0])),int(container_dimensions[1]/2-text_field_size[1]/2))        
        self.copy_amount_text.resize(text_field_size[0],text_field_size[1])

        self.copy_amount_label = QLabel('Center', self)
        self.copy_amount_label.resize(120,30)
        self.copy_amount_label.move(self.copy_amount_text.pos().x(),int(container_dimensions[1]/2-text_field_size[1]/2-label_buffer))
        self.copy_amount_label.setText("Duplications:")
        self.copy_amount_text.setPlainText("1")
        self.copy_amount_text.textChanged.connect(lambda: self.onAmountChange(self.copy_amount_text))

        self.replace_ending_file_name_number_button = QCheckBox("Replace Last Number?",self)
        self.replace_ending_file_name_number_button.move(self.starting_number_text.pos().x(),int(self.starting_number_text.pos().y()+label_buffer*1.5))
        self.replace_ending_file_name_number_button.resize(320,40)
        
        self.duplicate_button = QPushButton('Duplicate', self)
        self.duplicate_button.move(int(container_dimensions[0]/2-self.duplicate_button.rect().width()/2),int(container_dimensions[1]-widget_buffer[1]-self.duplicate_button.rect().height()/2+label_buffer/2))
        self.duplicate_button.clicked.connect(self.onClick)
        
    def onClick(self):
        if self.file_display_text.toPlainText() == "":
            return
        
        path = os.path.dirname(self.dropped_file_paths[0])
        base = os.path.basename(self.dropped_file_paths[0])
        ext = os.path.splitext(base)[1]
        replacement_text =self.new_flie_name_text.toPlainText()
        file_name = replacement_text if replacement_text != "" else os.path.splitext(base)[0]
        starting_numb = int(self.starting_number_text.toPlainText())
        duplication_amount = int(self.copy_amount_text.toPlainText())
        if self.replace_ending_file_name_number_button.isChecked() and replacement_text == "":
            file_name = file_name[:-1]

        for i in range(duplication_amount):
            new_file = f"{path}/{file_name}{i+starting_numb}{ext}"
            shutil.copy(self.dropped_file_paths[0],new_file)       

    def onAmountChange(self,text_object):
        if text_object.toPlainText().isdigit() == False:
            text_object.setPlainText("1")        

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        self.dropped_file_paths = [u.toLocalFile() for u in event.mimeData().urls()]
        self.file_display_text.setPlainText(os.path.basename(self.dropped_file_paths[0]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWidget()
    ui.show()
    sys.exit(app.exec_())