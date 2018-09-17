import sys
import os
from PyQt5.QtWidgets import (QApplication,  QFileDialog, QHBoxLayout, QMainWindow, 
    QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget)

import c2js 

APP_TITLE = 'C-to-Javascript Translator'
INVALID_PATH_MESSAGE = "Invalid path found, operation cancelled."
OPEN_BUTTON_LABEL = "Open"
SAVE_BUTTON_LABEL = "Save"

TEXTFIELD_WIDTH = 450
TEXTFIELD_HEIGHT = 600

class C2jsView(QMainWindow):
    
    def __init__(self):
        super().__init__()
    
        #Create the main instance...
        self.c2js = c2js.C2js()

        #Setup the layout, and run!
        main_layout = QWidget(self)
        self.open_button = QPushButton(OPEN_BUTTON_LABEL)
        self.save_button = QPushButton(SAVE_BUTTON_LABEL)
        btnrow = QHBoxLayout()
        txtrow = QHBoxLayout()

        #set empty widget as the "base" layout
        self.setCentralWidget(main_layout)

        #Set both textedits and its properties
        self.source_text = QPlainTextEdit()
        self.result_text = QPlainTextEdit()
        #Set their size (w * h)
        self.source_text.setMinimumSize(TEXTFIELD_WIDTH, TEXTFIELD_HEIGHT)
        self.result_text.setMinimumSize(TEXTFIELD_WIDTH, TEXTFIELD_HEIGHT)
        #Disable edits and line wrapping
        self.source_text.setReadOnly(True)
        self.result_text.setReadOnly(True)
        self.source_text.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.source_text.setLineWrapMode(QPlainTextEdit.NoWrap)

        #Setup the buttons, disable the save_button first
        self.open_button.clicked.connect(self.open)
        self.save_button.clicked.connect(self.save)
        self.save_button.setEnabled(False)

        #Setup the horizontal button row, with "stretch" spaces after buttons
        btnrow.addWidget(self.open_button)
        btnrow.addStretch(1)
        btnrow.addWidget(self.save_button)
        btnrow.addStretch(1)

        #Setup the horizontal text row
        txtrow.addWidget(self.source_text)
        txtrow.addWidget(self.result_text)

        #Stack both rows, texts below buttons
        vbox = QVBoxLayout()
        vbox.addLayout(btnrow)
        vbox.addLayout(txtrow)

        #Set the stacked rows as the layout
        main_layout.setLayout(vbox)

        #Set the main layout knick-knacks
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setWindowTitle(APP_TITLE)
        self.statusBar().showMessage('Ready.')

        self.show()

    def open(self):
        """Opens a file picker, and executes the c2js on the file chosen (if valid)"""
        filepath, _filter = QFileDialog.getOpenFileName(self, "Open File", '', 'C Files (*.c)')
        _path, filename = os.path.split(filepath)

        if filename:
            #Loads file
            self.c2js.load(filename)
            with open(c2js.SOURCE_TEMPFILE_PATH, 'r') as output:
                data = output.read()
                self.source_text.setPlainText(data)
            self.statusBar().showMessage(f"{filename} succesfully loaded. Processing...")

            #Process
            self.c2js.process()
            with open(c2js.OUTPUT_TEMPFILE_PATH, 'r') as output:
                data = output.read()
                self.result_text.setPlainText(data)
            self.statusBar().showMessage(f"{filename} succesfully translated. Press Save to create the Javascript file.")
            
            #Enable the save button.
            self.save_button.setEnabled(True)
        else:
            self.statusBar().showMessage(INVALID_PATH_MESSAGE)

    def save(self):
        """Opens a save dialog and triggers the c2js saving mechanism."""
        filepath, _filter = QFileDialog.getSaveFileName(self, "Save File", '', "Javascript Files (*.js)")
        _path, filename = os.path.split(filepath)

        if filename:
            self.c2js.save(filepath)
            self.statusBar().showMessage(f"{filename} successfully saved.")
        else:
            self.statusBar().showMessage(INVALID_PATH_MESSAGE)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = C2jsView()
    sys.exit(app.exec_())
