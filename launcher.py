import sys, os

import subprocess

from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
QVBoxLayout)


class Launcher(QDialog):
    def __init__(self):
        super(Launcher, self).__init__()
        self.createForm()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.launch)
        buttonBox.rejected.connect(self.reject)

        main = QVBoxLayout()
        main.addWidget(self.formBox)
        main.addWidget(buttonBox)
        self.setLayout(main)

        self.setWindowTitle("Pylaga Launcher")

    def createForm(self):
        self.formBox = QGroupBox("Configurações")

        res = ["1920 x 1280", "1366 x 768", "1280 x 720", "800 x 600"]
        self.resCombo = QComboBox()
        self.resCombo.addItems(res)

        telas = ["Tela cheia", "Janela"]
        self.telaCombo = QComboBox()
        self.telaCombo.addItems(telas)

        layout = QFormLayout()
        layout.addRow(QLabel("Resolução: "), self.resCombo)
        layout.addRow(QLabel("Tela: "), self.telaCombo)
        self.formBox.setLayout(layout)

    def launch(self):
        ires = str(self.resCombo.currentIndex())
        itela = str(self.telaCombo.currentIndex())
        execstr = "py game.py "+ires+" "+itela

        try:
            import pygame, numpy, cv2
        except ImportError:
            print("INSTALANDO REQUERIMENTOS...")
            exec(open('setup.py').read())

        subprocess.Popen(['python', 'game.py', ires, itela])
        self.accept()

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    sys.exit(launcher.exec_())

