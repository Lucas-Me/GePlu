from PySide6.QtWidgets import (QMainWindow, QMessageBox, QDialog)
import pandas as pd

# Utilitarios e excecoes


def open_excel(parent, nrows = None):
    header = 0 if parent.ignore.isChecked() else None

    try:
        data_df = pd.read_excel(parent.path.text(), header = header, engine = "openpyxl", nrows = nrows, dtype = 'str')

    except FileNotFoundError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível abrir o arquivo solicitado.", buttons = QMessageBox.Ok, parent = parent)
        x.setInformativeText("Não existe tal arquivo ou diretório.")
        x.setDetailedText(str(Err))
        x.exec()
        raise FileNotFoundError

    return data_df

def open_csv(parent, nrows = None):

    header = 0 if parent.ignore.isChecked() else None
    try:
        data_df = pd.read_csv(parent.path.text(), sep = parent.separador, nrows = nrows, dtype = 'str', header = header)

    except FileNotFoundError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível abrir o arquivo solicitado.", buttons = QMessageBox.Ok, parent = parent)
        x.setInformativeText("Não existe tal arquivo ou diretório.")
        x.setDetailedText(str(Err))
        x.exec()
        raise FileNotFoundError

    return data_df


#def open_odf():

def save_csv(parent, file, delimiter = ';'):

    try:
        with pd.ExcelWriter(parent.folder.text()) as writer:
            file.to_csv(writer, "Dados Brutos", sep = parent.separador)

    except PermissionError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível salvar seu arquivo.", buttons = QMessageBox.Ok, parent = parent)
        x.setInformativeText("O arquivo que voce está tentando sobrescrever já está aberto em outro programa.")
        x.setDetailedText(str(Err))
        x.exec()
        raise PermissionError

# def save_excel():

# def save_opendocument():
