from PySide6.QtWidgets import (QMainWindow, QMessageBox, QDialog)
import pandas as pd

# Utilitarios e excecoes
# Organizar isso mais tarde


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

def save_excel(parent, file, engine = 'openpyxl'):
     try:
        with pd.ExcelWriter(parent.folder.text()) as writer:
            file.to_csv(writer, "Dados Brutos", engine = engine)

     except PermissionError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível salvar seu arquivo.", buttons = QMessageBox.Ok, parent = parent)
        x.setInformativeText("O arquivo que voce está tentando sobrescrever já está aberto em outro programa.")
        x.setDetailedText(str(Err))
        x.exec()
        raise PermissionError


def read_file(parent, nrows = None, header = None):
    extension = parent.fileformat
    pathname = parent.path.text()

    try:
        if extension == ".xlsx":
            data_df = pd.read_excel(pathname, header = header, engine = "openpyxl", nrows = nrows, dtype = 'str')

        #elif self.filefomart == ".ods":
            #data_df = utils.open_odf(self, 14).to_numpy()
        else:
            data_df = pd.read_csv(pathname, sep = parent.separador, nrows = nrows, dtype = 'str', header = header, keep_default_na = False)

    except PermissionError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível salvar seu arquivo.", buttons = QMessageBox.Ok, parent = parent)
        x.setInformativeText("O arquivo que voce está tentando sobrescrever já está aberto em outro programa.")
        x.setDetailedText(str(Err))
        x.exec()
        raise PermissionError

    except pd.errors.ParserError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível ler o arquivo com o delimitador especificado.", buttons = QMessageBox.Ok, parent = parent)
        x.setInformativeText("Por favor, tente utilizar um outro tipo de delimitador para os seus dados.")
        x.setDetailedText(str(Err))
        x.exec()
        raise pd.errors.ParserError

    return data_df