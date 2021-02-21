from PySide6.QtWidgets import QMessageBox
import pandas as pd

# Utilitarios
# Organizar isso mais tarde


def save_file(master, file, delimiter = ';'):
    pathname = master.folder.text()
    extension = pathname[pathname.index('.'):]

    try:
        if extension == ".xlsx":
            with pd.ExcelWriter(pathname) as writer:
                file.to_excel(
                    writer, 
                    "Dados Brutos", 
                    engine = 'openpyxl',
                    na_rep = "NaN",
                    float_format = "%.2f"
                    )


        else:
            decimal = ',' if master.separador == '.' else '.'
            with open(pathname, 'wb') as writer:
                file.to_csv(
                    writer,
                    sep = master.separador,
                    na_rep = "NaN",
                    float_format = "%.2f",
                    decimal = decimal
                    )

    except PermissionError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível salvar seu arquivo.", buttons = QMessageBox.Ok, parent = master)
        x.setInformativeText("O arquivo que voce está tentando sobrescrever já está aberto em outro programa.")
        x.setDetailedText(str(Err))
        x.exec()
        raise PermissionError


def read_file(master, nrows = None, header = None):
    extension = master.fileformat
    pathname = master.path.text()

    try:
        if extension == ".xlsx":
            data_df = pd.read_excel(pathname,
                header = header, 
                engine = "openpyxl",
                nrows = nrows,
                dtype = 'str'
                )

        #elif self.filefomart == ".ods":
            #data_df = utils.open_odf(self, 14).to_numpy()
        else:
            data_df = pd.read_csv(pathname, 
                sep = master.separador,
                nrows = nrows,
                dtype = 'str',
                header = header, 
                keep_default_na = False
                )

    except PermissionError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível salvar seu arquivo.", buttons = QMessageBox.Ok, parent = master)
        x.setInformativeText("O arquivo que voce está tentando sobrescrever já está aberto em outro programa.")
        x.setDetailedText(str(Err))
        x.exec()
        raise PermissionError

    except pd.errors.ParserError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível ler o arquivo com o delimitador especificado.", buttons = QMessageBox.Ok, parent = master)
        x.setInformativeText("Por favor, tente utilizar um outro tipo de delimitador para os seus dados.")
        x.setDetailedText(str(Err))
        x.exec()
        raise pd.errors.ParserError

    return data_df