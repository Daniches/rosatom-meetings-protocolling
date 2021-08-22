import os
import time
import protocol_processing
import settings
import subprocess
import sys

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import (QFileDialog,QMessageBox)

firstcheck = True
Form, _ = uic.loadUiType("main.ui")
path = ""
pathall = ""
check = False
opener = "open" if sys.platform == "darwin" else "xdg-open"

class Ui(QtWidgets.QDialog, Form):
    """
    Класс инициализирующий форму и определяющий взаимодействия с ней
    """

    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        # self.pushButton.clicked.connect(lambda: self.printButtonPressed(self.lineEdit_2.text()))
        self.choosefile.clicked.connect(lambda: self.showdialog())
        self.convert.clicked.connect(lambda: self.hiden())
        self.pushButton1_2.clicked.connect(lambda: self.nolike())
        self.pushButton1_3.clicked.connect(lambda: self.yeslike())
        self.editkey.clicked.connect(lambda: self.keywords())
        self.hidemenu1.clicked.connect(lambda: self.hidemenu())
        self.editkeywords.clicked.connect(lambda: subprocess.call([opener, settings.keywords_file]))
        self.addtriggerword.clicked.connect(lambda: self.add(self.lineEdit_2.text()))
        self.hintme.clicked.connect(lambda: self.hintmeplease())
        self.firsthide()
        self.setGeometry(500, 250, 465, 520)
        if os.path.isfile(settings.keywords_file):
            text_file = open(settings.keywords_file, "a")
        else:
            text_file = open(settings.keywords_file, "w")
            text_file.write(
                "Обсуждение решения" + '\n' + "Ответственный за исполнение" + '\n' + "Срок исполнения"
                + '\n' + "Принятое решение" + '\n')

    def hintmeplease(self):
        QMessageBox.about(self, "Добро пожаловать!",
                          "Чтобы добавить файл - выберете кнопку открыть файл и выберете файл формата "
                          "'mp4', 'mp3' или 'wav'."
                          + '\n' + "Чтобы отредактировать ключевые слова по которым будет собираться протокол "
                                   "откройте соответствующее меню."
                          + '\n' + "Чтобы конвертировать файл - нажмите кнопку Конвертировать."
                          + '\n' + "После конвертации откроется текстовый документ с результатом."
                          + '\n' + "Чтобы принять результат - нажмите кнопку Да, в этом случае Вам откроется "
                                   "папка содержащая исходный файл и файл-протокол."
                          + '\n' + "Чтобы не принять результат - нажмите кнопку Нет, в этом случае протокол "
                                   "сохранён не будет."
                          )
    
    def add(self, text):

        if text != " " and text != "":
            fin = open(settings.keywords_file, "a")
            fin.write(text + '\n')
            fin.close()
        QMessageBox.about(self, "Сообщение", "Успешно добавлено!")
        self.lineEdit_2.setText("")

    def hidemenu(self):
        global check
        check = True
        self.firsthide()

    def keywords(self):
        self.setGeometry(500, 250, 764, 521)
        self.editkeywords.setHidden(False)
        self.convert.setEnabled(False)
        self.choosefile.setEnabled(False)
        self.hidemenu1.setHidden(False)
        self.editkey.setHidden(False)
        self.lineEdit_2.setEnabled(True)
        self.lineEdit_2.setHidden(False)
        self.label_4.setHidden(False)
        self.addtriggerword.setHidden(False)

    def showdialog(self):
        global path, pathall

        fname = QFileDialog.getOpenFileName(self, 'Open file', '')[0]

        file, extension = os.path.splitext(fname)
        path = file
        pathall = fname
        self.lineEdit.setText(fname)
        if fname != "":
            self.convert.setEnabled(True)
            self.editkey.setEnabled(True)
        if extension not in ['.mp4', '.mp3', '.wav']:
            self.lineEdit.setText('Можно выбрать только .mp4, .mp3 или .wav файл')
            self.convert.setEnabled(False)
            self.editkey.setEnabled(False)

    def hiden(self):
        self.setGeometry(500, 250, 922, 520)
        self.label_2.setHidden(False)
        self.label_3.setHidden(False)
        self.progressBar.setHidden(False)
        self.pushButton1_2.setHidden(False)
        self.pushButton1_3.setHidden(False)
        self.choosefile.setEnabled(False)
        self.convert.setEnabled(False)
        self.editkey.setEnabled(False)
        self.doaction()

    def nolike(self):
        global path
        path += ".docx"
        os.remove(path)
        path = path[:-5]
        self.firsthide()

    def yeslike(self):
        global path
        os.startfile(os.path.dirname(path))
        self.firsthide()

    def doaction(self):
        global path
        self.progressBar.setValue(0)
        protocol_processing.process(pathall, path+'.docx');
        for i in range(101):
            time.sleep(0.015)
            self.progressBar.setValue(i)

        self.pushButton1_3.setEnabled(True)
        self.pushButton1_2.setEnabled(True)

        path += ".docx"
        subprocess.call([opener, path])
        path = path[:-5]

    def firsthide(self):
        global check
        self.convert.setEnabled(True)
        self.label.setHidden(False)
        self.label_2.setHidden(True)
        self.label_3.setHidden(True)
        self.lineEdit.setHidden(False)
        self.progressBar.setHidden(True)
        self.choosefile.setHidden(False)
        self.convert.setHidden(False)
        self.pushButton1_2.setHidden(True)
        self.pushButton1_3.setHidden(True)
        self.choosefile.setEnabled(True)
        self.convert.setEnabled(False)
        self.pushButton1_2.setHidden(True)
        self.convert.setEnabled(True)
        self.pushButton1_3.setHidden(True)
        self.hidemenu1.setHidden(True)
        self.editkeywords.setHidden(True)
        self.lineEdit_2.setHidden(True)
        self.label_4.setHidden(True)
        self.addtriggerword.setHidden(True)
        self.editkey.setEnabled(False)
        self.convert.setEnabled(False)
        self.setGeometry(500, 250, 465, 520)
        self.lineEdit.setText("")
        if check is True:
            global pathall
            self.lineEdit.setText(pathall)
            self.convert.setEnabled(True)
            self.editkey.setEnabled(True)
            check = False

    def backs(self):
        self.setGeometry(500, 250, 465, 520)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())
