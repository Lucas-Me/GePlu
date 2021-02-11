# Arquivo da Interface GUI do programa.
# Python 3.7.7

from PySide2.QtGui import (QIcon)
from PySide2.QtCore import (QUrl, QObject)
from PySide2.QtWidgets import (QMainWindow, QApplication, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout,
QBoxLayout, QPushButton, QGridLayout, QRadioButton, QGroupBox, QLabel, QTableWidget, QComboBox, QFileDialog,
QTableWidgetItem, QProgressDialog, QMessageBox, QCheckBox, QDialog, QInputDialog)
import classes.Generator as Ac
import classes.functions as Fc
import sys, csv, time, os, ctypes

class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        # Variaveis
        self.Gerador = Ac.Acumulados([60, 60*4, 60*24, 60*48, 60*96])
        self.separador = ";"

        #Janela Principal
        widget = QWidget()
        self.setCentralWidget(widget)

        # Inicializa os Widgets
        self.folder = QLineEdit("Salvar Como...")
        self.path = QLineEdit("Abrir arquivo...")

        buttonOpen = QPushButton('Abrir')
        buttonSave = QPushButton("Destino")
        Processar = QPushButton('Executar')
        Ajuda = QPushButton('Informações')

        groupBox2 = QGroupBox("Delimitador")
        self.delimitador1 = QRadioButton("Ponto-Vírgula")
        self.delimitador2 = QRadioButton("Vírgula")
        self.delimitador3 = QRadioButton("Ponto")

        text3 = QPushButton("Configurar Intervalos")
        text2 = QLabel("Formato da Data")
        self.FormatoData = QComboBox()
        self.FormatoData.addItems(["DD/MM/AAAA",'AAAA/MM/DD'])
        checkGroup = QGroupBox("Mais opções")

        text = QLabel("Por favor, selecione na tabela abaixo as colunas a utilizar:")
        self.ignore = QRadioButton("Ignorar Primeira Linha do Arquivo")

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
        SecondLayout.addSpacing(70)
        SecondLayout.addWidget(checkGroup)
        #
        SepLayout = QVBoxLayout()
        SepLayout.addWidget(self.delimitador1)
        SepLayout.addWidget(self.delimitador2)
        SepLayout.addWidget(self.delimitador3)
        #
        OptionsLayout = QVBoxLayout()
        OptionsLayout.addWidget(text3)
        OptionsLayout.addWidget(text2)
        OptionsLayout.addWidget(self.FormatoData)

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
        self.ignore.clicked.connect(self.updateIgnoreButton)
        Ajuda.clicked.connect(self.help)
        Processar.clicked.connect(self.taskStart)
        text3.clicked.connect(self.openSubWindow)

        # Propriedades da janela principal
        myappid = 'GePlu.release1_03' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(QIcon('icon6.ico'))
        self.setFixedSize(640,480)
        self.setWindowTitle("GePlu")

    def openSubWindow(self):

        dialog = MyDialog(self.Gerador)
        dialog.show()
        dialog.exec_()

    def taskStart(self):
        ''' Inicia a execucao do programa, se houver algum erro durante o processo
        notifica o usuario e deixa a funcao imediatamente, devido a isso eu escrevi dois linhas
        para garantir que os dados no objeto Gerador estejam resetados e o objeto esteja pronto para
        a proxima interacao'''
        if self.folder.isModified() and self.path.isModified(): # o usuario entrou com os caminhos (paths)?
            # Garante que os dados são novos, ou seja, reseta se ja houve uma interacao antes.
            self.Gerador.setData({})
            self.Gerador.setDataHeight({},False)
            # Verifica os nomes das colunas na tabela do programa e armazena em uma variavel
            colunas = {}
            for col in range(self.Tabela.columnCount()):
                colunas[self.Tabela.cellWidget(0,col).currentText()] = col
            # Comeca a cronometrar
            start = time.time()
            # Abre o arquivo e armazena em uma variavel
            rawText = Fc.openFile(self)
            # Pega o arquivo e converte os dados de data/hora em datetime, e valores de registro (ultima chuva) em floats, se possivel.
            # Depois coloca o resultado dentro do objeto Gerador
            Fc.toDict(self, rawText, colunas)
            rawText = None
            # Calcula todos os acumulados em x,y,z horas (especificado pelo usuario) de todos os horarios
            self.Gerador.calcularAcumulado(self)
            # Poe o resultado em uma matriz e retorna ela
            Result = self.Gerador.getChart()
            # Abre um novo arquivo csv e escreve os dados da matriz nesse arquivo, por fim salva.
            Fc.saveFile(self, Result)
            # Fim do processo
            end = time.time()
            # Notifica o usuario
            QMessageBox.information(self, "Notificação", "Tarefa realizada com sucesso!\nTempo de execução: {} s.".format(round(end-start, 2)))
            # Reseta a tabela e os endereço do arquivo aberto e onde salvar, na janela principal.
            self.resetProgram()
        else:
            QMessageBox.warning(self, "Notificação", "Houve um erro no arquivo ou diretório especificado.\nPor favor, selecione um caminho válido.")


    def help(self):
        x = "Caso tenha alguma dúvida, abra o arquivo de texto 'Leia-me' presente\nna pasta do programa ou entre em contato\n\nVersão 1.03\nCriado por Lucas da Silva Menezes\nContato: lucasmenezes4502@gmail.com"
        msgBox = QMessageBox.information(self, "Informação", x)

    def resetProgram(self):
        self.Tabela.clearContents()
        self.startTable()
        self.folder.setText("Salvar Como...")
        self.path.setText("Selecionar o arquivo...")
        self.folder.setModified(False)
        self.folder.setModified(False)

    def updateIgnoreButton(self):
        if self.path.isModified():
            self.updateTable()

    def updateDelimiter(self):
        separadores = {"Ponto-Vírgula": ';', "Vírgula":",","Ponto":"."}
        for x in [self.delimitador1, self.delimitador3, self.delimitador2]:
            if x.isChecked():
                self.separador = separadores[x.text()]
                break
        if self.path.isModified():
            self.updateTable()

    def startTable(self):
        for col in range(self.Tabela.columnCount()):
            combo = QComboBox()
            combo.addItems(["Selecionar","Data & Hora","Chuva Medida","Data","Hora","Nível do Rio","Ignorar"])
            self.Tabela.setCellWidget(0, col, combo)

    def updateTable(self):
        textos = [0]*15
        for col in range(15):
            textos[col] = self.Tabela.cellWidget(0, col).currentText()

        self.Tabela.clearContents()
        self.startTable()

        for col in range(15):
            self.Tabela.cellWidget(0, col).setCurrentText(textos[col])

        resultado = self.ignore.isChecked()
        try:
            with open(self.path.text(), newline = '') as csvfile:
                file = csv.reader(csvfile, delimiter = self.separador)
                n = 0
                for row in file:
                    if n == 0 and resultado:
                        resultado = False
                        continue
                    for col in range(len(row)):
                        if col < self.Tabela.columnCount():
                            self.Tabela.setItem(n + 1, col, QTableWidgetItem(row[col]))
                    n += 1
                    if n == 14:
                        break
        except FileNotFoundError as Err:
            x = QMessageBox(QMessageBox.Critical, "Erro de Acesso",  "Não foi possível abrir o arquivo selecionado.", parent = self)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText("Não existe tal arquivo ou diretório.")
            x.setDetailedText(str(Err))
            x.exec()
            raise PermissionError


    def searchFile(self):
        address, x = QFileDialog.getOpenFileName(self, "Selecione um arquivo", filter = "Text files (*.txt *.csv)")
        if len(address) > 0:
            self.path.setText(address)
            self.path.setModified(True)
            self.updateTable()

    def getNewFile(self):
        address, x = QFileDialog.getSaveFileName(self, "Salvar como", filter = "Text files (*.csv);; Text files (*.txt)")
        if len(address) > 0:
            self.folder.setText(address)
            self.folder.setModified(True)

class MyDialog(QDialog):

    def __init__(self, gerador):
        QDialog.__init__(self)
        self.setWindowTitle("Configuração")
        self.setFixedSize(200,200)
        self.setWindowIcon(QIcon('icon6.ico'))
        self.setModal(True)
        self.intervalos = [60, 60*2, 60*3, 60*4, 60*12, 60*24, 60*48, 60*72, 60*96, 60*24*30]

        button1 = QPushButton("Cancelar")
        button1.clicked.connect(self.closeDialog)
        button2 = QPushButton("Confirmar")
        button2.clicked.connect(lambda: self.saveAndClose(gerador))

        horarios = ["1 Hora","2 Horas", "3 Horas", "4 Horas","12 Horas",
         "24 Horas", "48 Horas", "72 horas", "96 horas", "30 Dias"]
        self.checkboxes = [0]*10
        for i in range(10):
            self.checkboxes[i] = QCheckBox(horarios[i])

        grupo = QGroupBox("Incluir Precipitação Acumulada Em")
        grid = QGridLayout()
        for x in range(10):
            if x < 5:
                grid.addWidget(self.checkboxes[x], x , 0)
            else:
                grid.addWidget(self.checkboxes[x], x - 5, 1)
        grupo.setLayout(grid)
        self.startCheckboxes(gerador)

        sublayout = QHBoxLayout()
        sublayout.addWidget(button1)
        sublayout.addWidget(button2)

        layout = QVBoxLayout()
        layout.addWidget(grupo)
        layout.addLayout(sublayout)
        self.setLayout(layout)

    def startCheckboxes(self, gerador):
        for x in range(10):
            self.checkboxes[x].setChecked(self.intervalos[x] in gerador.getValues())

    def saveAndClose(self, gerador):
        connections = []
        for x in range(10):
            if self.checkboxes[x].isChecked():
                connections.append(self.intervalos[x])

        gerador.setValues(connections)
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
