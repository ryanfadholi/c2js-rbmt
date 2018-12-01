import sys
import os
from PyQt5.QtWidgets import (QApplication,  QFileDialog, QHBoxLayout, QLabel, 
    QMainWindow, QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout, QWidget)

import c2js 
import constants

APP_TITLE = 'C-to-Javascript Translator'
INVALID_PATH_MESSAGE = "Invalid path found, operation cancelled."
OPEN_BUTTON_LABEL = "Open"
SAVE_BUTTON_LABEL = "Save"

BASELABEL_LINE_COUNT = "Statement count:"
BASELABEL_DECL = "Deklarasi Variabel/Fungsi\t:"
BASELABEL_INIT = "Inisialisasi/Inisiasi\t:"
BASELABEL_FUNC = "Pemanggilan Fungsi\t:"
BASELABEL_IO = "Masukan/Keluaran\t:"
BASELABEL_COND = "Kondisional\t\t:"
BASELABEL_LOOP = "Pengulangan\t\t:"
BASELABEL_COMMENT = "Komentar\t\t:"
BASELABEL_ETC = "Lain-lain\t\t:"

BASELABEL_ORDER = [BASELABEL_LINE_COUNT, 
                BASELABEL_LINE_COUNT,
                BASELABEL_DECL,
                BASELABEL_INIT,
                BASELABEL_FUNC,
                BASELABEL_IO,
                BASELABEL_COND,
                BASELABEL_LOOP,
                BASELABEL_COMMENT,
                BASELABEL_ETC]

TEXTFIELD_WIDTH = 450
TEXTFIELD_HEIGHT = 600

class C2jsView(QMainWindow):
    
    def __init__(self):
        super().__init__()
    
        #Create the main instance...
        self._c2js = c2js.C2js()

        #Setup the layout, and run!
        main_layout = QWidget(self)
        self._open_button = QPushButton(OPEN_BUTTON_LABEL)
        self._save_button = QPushButton(SAVE_BUTTON_LABEL)
        btnrow = QHBoxLayout()
        txtrow = QHBoxLayout()
        linecountrow = QHBoxLayout()
        detailsrow = QHBoxLayout()

        #set empty widget as the "base" layout
        self.setCentralWidget(main_layout)

        #Set both textedits and its properties
        self.source_text = QPlainTextEdit()
        self.result_text = QPlainTextEdit()
        self.details_text = QPlainTextEdit()
        #Set their size (w * h)
        self.source_text.setMinimumSize(TEXTFIELD_WIDTH, TEXTFIELD_HEIGHT)
        self.result_text.setMinimumSize(TEXTFIELD_WIDTH, TEXTFIELD_HEIGHT)
        self.details_text.setMinimumSize(TEXTFIELD_WIDTH * 2, TEXTFIELD_HEIGHT / 5)
        #Disable edits and line wrapping
        self.source_text.setReadOnly(True)
        self.result_text.setReadOnly(True)
        self.details_text.setReadOnly(True)
        self.source_text.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.result_text.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.details_text.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.source_count = QLabel("")
        self.result_count = QLabel("") 
        self.decl_count = QLabel("")
        self.init_count = QLabel("")
        self.func_count = QLabel("")
        self.io_count = QLabel("")
        self.cond_count = QLabel("")
        self.loop_count = QLabel("")
        self.comment_count = QLabel("")
        self.etc_count = QLabel("")

        self.count_order = [self.source_count,
            self.result_count,
            self.decl_count,
            self.init_count,
            self.func_count,
            self.io_count,
            self.cond_count,
            self.loop_count,
            self.comment_count,
            self.etc_count]

        for label, text in zip(self.count_order, BASELABEL_ORDER):
            label.setText(f"{text} -")

        #Setup the buttons, disable the save_button first
        self._open_button.clicked.connect(self.open)
        self._save_button.clicked.connect(self.save)
        self._save_button.setEnabled(False)

        #Setup the horizontal button row, with "stretch" spaces after buttons
        btnrow.addWidget(self._open_button)
        btnrow.addStretch(1)
        btnrow.addWidget(self._save_button)
        btnrow.addStretch(1)

        #Setup the horizontal text row
        txtrow.addWidget(self.source_text)
        txtrow.addWidget(self.result_text)

        linecountrow.addWidget(self.source_count)
        linecountrow.addStretch(1)
        linecountrow.addWidget(self.result_count)
        linecountrow.addStretch(1)
        linecountrow.setContentsMargins(0,0,0,25)
        detailsrow.addWidget(self.details_text)

        #Stack both rows, texts below buttons
        vbox = QVBoxLayout()
        vbox.addLayout(btnrow)
        vbox.addLayout(txtrow)
        vbox.addLayout(linecountrow)
        vbox.addLayout(detailsrow)
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
            self.statusBar().showMessage(f"{filename} succesfully loaded. Processing...")

            #Process
            hasil = self._c2js.process(filepath, test_mode=True)
            with open(constants.INPUT_TEMPFILE_PATH, 'r') as output:
                data = output.read()
                self.source_text.setPlainText(data)

            for label, text, count in zip(self.count_order, BASELABEL_ORDER, hasil):
                label.setText(f"{text} <b>{count}</b>")
            
            details_text = ""
            details_text += f"Deklarasi Variabel/Fungsi\t: {hasil[2]}\n"
            details_text += f"Inisialisasi/Inisiasi\t: {hasil[3]}\n"
            details_text += f"Pemanggilan Fungsi\t: {hasil[4]}\n"
            details_text += f"Masukan/Keluaran\t: {hasil[5]}\n"
            details_text += f"Kondisional\t\t: {hasil[6]}\n"
            details_text += f"Pengulangan\t\t: {hasil[7]}\n"
            details_text += f"Komentar\t\t: {hasil[8]}\n"
            details_text += f"Lain-lain\t\t: {hasil[9]}\n"

            self.details_text.setPlainText(details_text)
            with open(constants.OUTPUT_TEMPFILE_PATH, 'r') as output:
                data = output.read()
                self.result_text.setPlainText(data)
            self.statusBar().showMessage(f"{filename} succesfully translated. Press Save to create the Javascript file.")
            
            
            #Enable the save button.
            self._save_button.setEnabled(True)
        else:
            self.statusBar().showMessage(INVALID_PATH_MESSAGE)

    def save(self):
        """Opens a save dialog and triggers the c2js saving mechanism."""
        filepath, _filter = QFileDialog.getSaveFileName(self, "Save File", '', "Javascript Files (*.js)")
        _path, filename = os.path.split(filepath)

        if filename:
            self._c2js.save(filepath)
            self.statusBar().showMessage(f"{filename} successfully saved.")
        else:
            self.statusBar().showMessage(INVALID_PATH_MESSAGE)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    instance = C2jsView()
    sys.exit(app.exec_())
