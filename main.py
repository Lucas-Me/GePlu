# Arquivo da Interface GUI do programa.
# Python 3.9.1

from PySide6.QtGui import (QIcon)
from PySide6.QtWidgets import (QMainWindow, QApplication, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout,
QPushButton, QGridLayout, QRadioButton, QGroupBox, QLabel, QTableWidget, QComboBox, QFileDialog,
QTableWidgetItem, QMessageBox, QCheckBox, QDialog)
import classes.utils as utils
import classes.data as dt
import sys, time, ctypes, os
import pandas as pd
import numpy as np

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        # Variaveis
        self.separador = ";" # Separador padrao de colunas em um arquivo txt ou csv
        self.selected = np.array([1, 24, 48, 96]).astype('timedelta64[h]') # selecionados ao iniciar o programa, modificavel.
        self.fileformat =  '' # Reservado para o formato do arquivo a ser aberto. Pode ser .xlsx ou .odf. ou .csv e assim vai.

        # facilita o acesso a variavel.
        self.timedeltastr = ("1 Hora","2 Horas", "3 Horas", "4 Horas","12 Horas",
         "24 Horas", "48 Horas", "72 horas", "96 horas", "30 Dias")
        self.timedeltas = np.array([1, 2, 3, 4, 12, 24, 48, 72, 96, 24*30]).astype('timedelta64[h]')
        self.linktimedelta = dict([(self.timedeltas[x], self.timedeltastr[x]) for x in range(len(self.timedeltastr))])

        self.datastring = ["DD/MM/AAAA",'AAAA/MM/DD', "AAAA-MM-DD", "DD-MM-AAAA"]
        self.dataformat = ["%d/%m/%Y", "%Y/%m/%d", "%Y-%m-%d", "%d-%m-%Y"]
        self.linkdata = dict([(self.datastring[x], self.dataformat[x]) for x in range(len(self.dataformat))])

        self.timestring = ["hh:mm", "hh:mm:ss", "hh:mm:ss.ms"]
        self.timeformat = ["%H:%M", "%H:%M:%S", "%H:%M:%S.%f"]
        self.linktime = dict([(self.timestring[x], self.timeformat[x]) for x in range(len(self.timeformat))])

        #Janela Principal
        widget = QWidget()
        self.setCentralWidget(widget)

        # Inicializa os Widgets
        self.folder = QLineEdit("Salvar Como...")
        self.path = QLineEdit("Abrir arquivo...")
        #
        buttonOpen = QPushButton('Abrir')
        buttonSave = QPushButton("Destino")
        Processar = QPushButton('Executar')
        Ajuda = QPushButton('Informações')
        #
        groupBox2 = QGroupBox("Delimitador")
        self.delimitador1 = QRadioButton("Ponto-Vírgula")
        self.delimitador2 = QRadioButton("Vírgula")
        self.delimitador3 = QRadioButton("Ponto")
        self.delimitador4 = QRadioButton("Tabulação")
        #
        checkGroup = QGroupBox("Mais opções")
        text3 = QPushButton("Configurações")
        text2 = QLabel("Formato da Data")
        text1 = QLabel("Formato da Hora")
        self.FormatoTime = QComboBox()
        self.FormatoTime.addItems(self.timestring)
        self.FormatoData = QComboBox()
        self.FormatoData.addItems(self.datastring)
        #
        text = QLabel("Por favor, selecione na tabela abaixo as colunas a utilizar:")
        self.ignore = QRadioButton("Possui Cabeçalho") # True se estiver selecionado, False caso nao
        #
        self.Tabela = QTableWidget(15,15)
        self.startTable()

        # Layouts
        MainLayout = QVBoxLayout()

        Gridlayout = QGridLayout()
        Gridlayout.addWidget(self.path, 0, 0)
        Gridlayout.addWidget(self.folder, 1, 0)
        Gridlayout.addWidget(buttonOpen, 0, 1)
        Gridlayout.addWidget(buttonSave, 1, 1)
        Gridlayout.addWidget(Processar, 0, 3)
        Gridlayout.addWidget(Ajuda, 1, 3)
        Gridlayout.setColumnStretch(0, 2)
        Gridlayout.setColumnStretch(3, 1)
        Gridlayout.setColumnMinimumWidth(2, 20)

        SecondLayout = QHBoxLayout()
        SecondLayout.addWidget(groupBox2)
        SecondLayout.addSpacing(40)
        SecondLayout.addWidget(checkGroup)
        #
        SepLayout = QVBoxLayout()
        SepLayout.addWidget(self.delimitador1)
        SepLayout.addWidget(self.delimitador2)
        SepLayout.addWidget(self.delimitador3)
        SepLayout.addWidget(self.delimitador4)
        #
        OptionsLayout = QVBoxLayout()
        OptionsLayout.addWidget(text3)
        OptionsLayout.addWidget(text2)
        OptionsLayout.addWidget(self.FormatoData)
        OptionsLayout.addWidget(text1)
        OptionsLayout.addWidget(self.FormatoTime)

        ThirdLayout = QVBoxLayout()
        ThirdLayout.addWidget(self.ignore)
        ThirdLayout.addWidget(text)

        MainLayout.addLayout(Gridlayout)
        MainLayout.addLayout(SecondLayout)
        MainLayout.addLayout(ThirdLayout)
        MainLayout.addWidget(self.Tabela)

        # Coloca o Layout principal na Janela
        widget.setLayout(MainLayout)

        # Comandos dos Widgets e edicoes.
        groupBox2.setLayout(SepLayout)
        self.delimitador1.setChecked(True)
        self.folder.setReadOnly(True)
        self.path.setReadOnly(True)
        checkGroup.setLayout(OptionsLayout)

        buttonOpen.clicked.connect(self.searchFile)
        buttonSave.clicked.connect(self.getNewFile)
        self.delimitador1.clicked.connect(self.updateDelimiter)
        self.delimitador2.clicked.connect(self.updateDelimiter)
        self.delimitador3.clicked.connect(self.updateDelimiter)
        self.delimitador4.clicked.connect(self.updateDelimiter)
        Ajuda.clicked.connect(self.help)
        Processar.clicked.connect(self.taskStart)
        text3.clicked.connect(self.openSubWindow)

        # Propriedades da janela principal
        height = 480
        width = 640
        myappid = 'GePlu.release1_0.0' # arbitrary string
        current_dir = os.path.dirname(os.path.realpath(__file__))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(QIcon(os.path.join(current_dir, "images", "icon6.ico")))
        self.setFixedSize(width, height)
        self.setWindowTitle("GePlu")

    def openSubWindow(self):

        dialog = MyDialog(self)
        dialog.show()
        dialog.exec_()

    def taskStart(self):
        ''' Inicia a execucao do programa, se houver algum erro durante o processo
        notifica o usuario e deixa a funcao imediatamente'''
        if self.folder.isModified() and self.path.isModified(): # o usuario entrou com os enderecos?
            start = time.time()

            # Conhece do que se trata cada coluna na tabela e armazena essa informacao.
            header = {}
            for col in range(15):
                header[self.Tabela.cellWidget(0, col).currentText()] = col

            boolean = 0 if self.ignore.isChecked() else None

            # Le o arquivo e retorna um dataframe de strings
            df_master = utils.read_file(self, header = boolean)
            df_master = dt.data_filter(self, df_master, header)
            df_master = dt.convert_dtype(self, df_master)

            # Computa os acumulados para cada intervalo de tempo (key).
            for key in self.selected:
                array = dt.compute(df_master.index.to_numpy(), df_master['Observado'].to_numpy(), key)
                df_master[self.linktimedelta[key]] = pd.Series(array, df_master.index)

            # salva o arquivo final.
            utils.save_file(self, df_master)

            # Fim do processo
            end = time.time()
            # Notifica o usuario
            QMessageBox.information(self, "Notificação", "Tarefa realizada com sucesso!\nTempo de execução: {} s.".format(round(end-start, 2)))
            # Reseta a tabela e os endereço do arquivo aberto e onde salvar, na janela principal.
            self.resetProgram()

        else:
            QMessageBox.warning(self, "Notificação", "Houve um erro no arquivo ou diretório especificado.\nPor favor, selecione um caminho válido.")


    def help(self):
        x = 'Caso tenha alguma dúvida, abra o documento em PDF presente\nna pasta do programa ou entre em contato.\n\nGeplu\n1.0.0'
        msgBox = QMessageBox.information(self, "Informação", x)

    def resetProgram(self):
        self.Tabela.clearContents()
        self.startTable()
        self.folder.setText("Salvar Como...")
        self.path.setText("Selecionar o arquivo...")
        self.folder.setModified(False)
        self.folder.setModified(False)

    def updateDelimiter(self):
        separadores = {"Ponto-Vírgula": ';', "Vírgula":",", "Ponto":".", "Tabulação":"\t"}
        for x in [self.delimitador1, self.delimitador3, self.delimitador2, self.delimitador4]:
            if x.isChecked():
                self.separador = separadores[x.text()]
                break

        if self.path.isModified():
            self.updateTable()

    def startTable(self):
        for col in range(self.Tabela.columnCount()):
            combo = QComboBox()
            combo.addItems(["Selecionar","Data & Hora","Prec. Observada","Data","Hora","Nível do Rio"])
            self.Tabela.setCellWidget(0, col, combo)

    def updateTable(self):
        # Guarda a primeira linha
        n_col = self.Tabela.columnCount()
        textos = [0]*n_col
        for col in range(n_col): textos[col] = self.Tabela.cellWidget(0, col).currentText()

        self.Tabela.clearContents()
        self.startTable()

        for col in range(n_col): self.Tabela.cellWidget(0, col).setCurrentText(textos[col])

        # Mostra na tabela as primeiras 14 linhas do arquivo que o usuario deseja abrir/utilizar.
        data_df = utils.read_file(self, 14).to_numpy()
        for row in range(data_df.shape[0]):
            for col in range(data_df.shape[1]):
                self.Tabela.setItem(row+1, col, QTableWidgetItem(data_df[row][col]))


    def searchFile(self):
        address, x = QFileDialog.getOpenFileName(self, "Selecione um arquivo",
            filter = "Text files (*.txt *.csv *.xlsx)"
            )
        if len(address) > 0:
            self.path.setText(address)
            self.path.setModified(True)
            self.fileformat = address[address.index('.'):]
            self.updateTable()

    def getNewFile(self):
        address, x = QFileDialog.getSaveFileName(self, "Salvar como",
            filter = "Text files (*.csv);; Text files (*.txt);; Planilha do Microsoft Excel (*.xlsx)"
            )
        if len(address) > 0:
            self.folder.setText(address)
            self.folder.setModified(True)

class MyDialog(QDialog):

    def __init__(self, master):
        QDialog.__init__(self)
        self.setWindowTitle("Configuração")
        self.setFixedSize(200, 200)
        self.setWindowIcon(QIcon(r'images\icon6.ico'))
        self.setModal(True)

        button1 = QPushButton("Cancelar")
        button1.clicked.connect(self.closeDialog)
        button2 = QPushButton("Confirmar")
        button2.clicked.connect(lambda: self.saveAndClose(master))

        num_elementos = len(master.timedeltas)
        self.checkboxes = [0]*num_elementos
        for i in range(num_elementos):
            self.checkboxes[i] = QCheckBox(master.timedeltastr[i])

        # Organizando o layout
        grupo = QGroupBox("Precipitação Acumulada em")
        grid = QGridLayout()
        for x in range(num_elementos):
            if x < num_elementos/2:
                grid.addWidget(self.checkboxes[x], x , 0)
            else:
                grid.addWidget(self.checkboxes[x], x - num_elementos/2, 1)
        #
        grupo.setLayout(grid)
        self.startCheckboxes(master)
        #
        sublayout = QHBoxLayout()
        sublayout.addWidget(button1)
        sublayout.addWidget(button2)
        #
        layout = QVBoxLayout()
        layout.addWidget(grupo)
        layout.addLayout(sublayout)
        self.setLayout(layout)

    def startCheckboxes(self, master):
        ''' Marcas as checkboxes cujos valores ja foram selecionados previamente'''
        for x in range(len(self.checkboxes)):
            self.checkboxes[x].setChecked(master.timedeltas[x] in master.selected)

    def saveAndClose(self, master):
        ''' Salva as modificacoes, colocando as checkboxes selecionadas dentro do array self.selected, e fecha a janela'''
        connections = []
        for x in range(len(self.checkboxes)):
            if self.checkboxes[x].isChecked():
                connections.append(master.timedeltas[x])


        master.selected = np.array(connections).astype('timedelta64[h]')
        self.close()

    def closeDialog(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Cria e Inicia a janela principal
    window = MainWindow()
    window.show()
    # Loop principal
    sys.exit(app.exec_())
