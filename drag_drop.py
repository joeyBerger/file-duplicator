from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit, QPushButton, QLabel
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

        widget_buffer = 50
        text_field_size = (350,30)

        self.file_display_text = QTextEdit(self)
        self.file_display_text.setReadOnly(True)
        self.file_display_text.move(int(self.rect().width()/2-text_field_size[0]/2),int(widget_buffer-text_field_size[1]/2))
        self.file_display_text.resize(text_field_size[0],text_field_size[1])

        self.file_display_label = QLabel('Left', self)
        self.file_display_label.resize(200,30)
        self.file_display_label.move(int(self.rect().width()/2-self.file_display_label.rect().width()/2),int(widget_buffer-text_field_size[1]/2-25))
        self.file_display_label.setText("File To Duplicate (Drag File):")

        text_field_size = (60,30)
        self.copy_amount_text = QTextEdit(self)
        self.copy_amount_text.move(int(self.rect().width()/2-text_field_size[0]/2),int(self.rect().height()/2-text_field_size[1]/2))        
        self.copy_amount_text.resize(text_field_size[0],text_field_size[1])
        # self.copy_amount_text.setAlignment(QtCore.Qt.AlignRight)
        # self.copy_amount_text.setHtml("<p align=\"right\">This paragraph is right aligned")
        self.copy_amount_label = QLabel('Center', self)
        self.copy_amount_label.move(int(self.rect().width()/2-self.copy_amount_text.rect().width()/2),int(self.rect().height()/2-text_field_size[1]/2-25))
        self.copy_amount_label.setText("Duplication Amount:")
        self.copy_amount_text.setPlainText("1")
        self.copy_amount_text.textChanged.connect(self.onAmountChange) 



        self.duplicate_button = QPushButton('Duplicate', self)
        self.duplicate_button.move(int(self.rect().width()/2-self.duplicate_button.rect().width()/2),int(self.rect().height()-widget_buffer-self.duplicate_button.rect().height()/2))
        self.duplicate_button.clicked.connect(self.onClick)
        
    def onClick(self):
        if self.file_display_text.toPlainText() == "":
            return
        
        path = os.path.dirname(self.dropped_file_paths[0])
        base = os.path.basename(self.dropped_file_paths[0])
        file_name = os.path.splitext(base)[0]
        ext = os.path.splitext(base)[1]

        duplication_amount = int(self.copy_amount_text.toPlainText())

        for i in range(duplication_amount):
            new_file = f"{path}/{file_name}{i+1}{ext}"
            shutil.copy(self.dropped_file_paths[0],new_file)       

    def onAmountChange(self):
        if self.copy_amount_text.toPlainText().isdigit() == False:
            self.copy_amount_text.setPlainText("1")
        

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