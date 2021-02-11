from datetime import timedelta, datetime
from PySide2.QtWidgets import (QMainWindow, QApplication, QProgressDialog, QMessageBox, QDialog)
import csv

class Acumulados():
    ''' Tentativa de criar uma classe que representa todos os acumulados de uma estacao.'''

    def __init__(self, minutes = None, ChuvaAcumulada = [], dicChuva = {}, dicNivel = {}):
        self.Chuva = dicChuva #Dicionario contendo o horario e seus respectivos acumulados
        self.valuesIn = ChuvaAcumulada # cada inteiro representa minuto.
        self.minutes = minutes
        self.Nivel = dicNivel #Dicionario contendo o horario e seus respectivos niveis do rio, se houver.
        self.isNivel = True if len(dicNivel) != 0 else False

    def getValues(self):
        return self.valuesIn

    def getTime(self):
        return self.minutes

    def setData(self, Data):
        self.Chuva = Data

    def setDataHeight(self, Data, Ativar  = True):
        self.isNivel = Ativar
        self.Nivel = Data

    def setValues(self, Values):
        for x in range(len(Values)):
            if Values[x] <= self.minutes:
                del Values[x]
        self.valuesIn = sorted(Values)

    def setTime(self, time):
        for x in range(len(self.valuesIn)):
            if self.valuesIn[x] <= time:
                del self.valuesIn[x]
        self.minutes = time

    def calcularAcumulado(self, parent):
        ''' Calcula todos os acumulados do documento
        intervalos consiste em uma lista contendo o tempo dos acumulados solicitados, sao eles em: (1,4,24,48,96) horas'''
        intervalos = self.valuesIn # [60, 240, 1440, 2880, 5760]
        tamanho = len(self.valuesIn) 
        constante = self.minutes
        const2 = timedelta(minutes = constante)
        dicionario = self.Chuva

        # Constroi o Dialogo de Progresso
        progress = QProgressDialog("Gerando os valores de chuva acumulada...","Cancelar", 0, len(dicionario), parent = parent)
        progress.setMinimumDuration(0)
        progress.setWindowTitle("Progresso")
        progress.setModal(True)
        j = 0
        #Calcula para cada chave do dicionario, exemplo:
        lastKey = datetime.now()
        for currentKey in sorted(dicionario.keys()): #Currentkey = 15/04/2018 10:15, lastKey = 15/04/2018 10:00
            QApplication.processEvents()
            progress.setValue(j)
            if progress.wasCanceled():
                # Cancelado pelo usuario
                break
            j += 1
            # Se eu ja tiver calculado para a data/hora anterior a este, vou usar os dados do anterior para acelerar o processo.
            if currentKey == lastKey + const2: # True
                values = dicionario[lastKey][2:] # [0,0;17,8;17,8;17,8;17,8]
                teste1, currentValue = dicionario[currentKey][:2] # [True, 0,0]
                for i in range(tamanho): # [0,1,2,3,4]    
                    teste2, lastValue = dicionario.get(currentKey - const2*(intervalos[i]//constante), (False, None))[:2]  
                    if teste1:
                        values[i] += currentValue
                    if teste2:
                        values[i] -= lastValue
                dicionario[currentKey][2:] = [round(x,1) for x in values]

            # Caso contrario, eu gero para esta data/hora, o processo mais lento.
            else:
                acumulado, count = 0.0, 0

                #Comeca a somar os acumulados de x horas
                for i in range(intervalos[-1]//constante):
                    # Adquire e soma o valor, se o resultado do teste for True
                    teste, valor = dicionario.get(currentKey - const2*i, (False, None))[:2]
                    if teste:
                        acumulado += valor

                    #Verifica se o horario correspondednte ao acumulado eh o limite.
                    if i + 1 == intervalos[count]//constante:
                        dicionario[currentKey][count + 2] = acumulado
                        count += 1
            lastKey = currentKey

        progress.close()
        self.Chuva = dicionario

    def getChart(self):
        ''' retorna um lista, cada item da lista representa uma linha.
        Por sua vez, cada linha contem uma lista separada em: [data hora, acumulados, ..., nivel do rio]'''
        Universal = []
        linhaInicial = ["Data Hora", "Último Registro"]
        ini = "Chuva Acumulada em "
        for time in self.valuesIn:
            if time > 60*96:
                linhaInicial.append(ini + str(time//(60*24)) + " Dias")
            elif time >= 60:
                linhaInicial.append(ini + str(time//60) + " Hora(s)")
            else:
                linhaInicial.append(ini + str(time) + " Min")

        if self.isNivel:
            linhaInicial.append("Nivel do Rio")
            
        Universal.append(linhaInicial)

        #Formatando o texto data/hora de yyyy-mm-dd 00:00:00 para dd/mm/yyyy 00:00.
        for datetime1 in self.Chuva.keys():
            linha = []

            texto = datetime1.isoformat(" ")
            data, hora = texto.split(" ")
            data = data.split("-")
            data.reverse()
            data  = "/".join(data)
            hora = hora[:5]
            texto = data + " " + hora
            linha.append(texto)

            #Agora adicionando os valores dos acumulados a linha.
            first = True
            for acumulado in self.Chuva[datetime1][1:]:
                ac = 0
                if first:
                    ac = str(acumulado).replace('.',',')
                    first = False
                else:
                    ac = str(round(acumulado, 1)).replace('.',',')
                linha.append(ac)

            #Adicionando o respectivo nivel do rio, se houver.
            if self.isNivel:
                linha.append(self.Nivel[datetime1])

            #Adicionando a linha na lista Universal.
            Universal.append(linha)

        return Universal

''' Funcoes definidas '''
def toDict(self, archive, colunas):
    objeto = self.Gerador
    formatoData = self.FormatoData.currentText()
    dicChuva = {}
    dicNivel = {}
    chaves = colunas.keys()
    itens = len(objeto.getValues())
    AreTogether = "Data & Hora" in chaves
    isNivel = "Nível do Rio" in chaves

    #Testes de caso e manuseio de erros.
    if not AreTogether:
        if not "Data" in chaves or not "Hora" in chaves:
            x = QMessageBox(QMessageBox.Warning, "Erro de Seleçao",  'A coluna correspondente a "Data" ou "Hora" não foi selecionada', parent = self)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText("Por favor, verifique a tabela e selecione a coluna correta.")
            x.exec()
            raise KeyError

    if not "Chuva Medida" in chaves:
        x = QMessageBox(QMessageBox.Warning, "Erro de Seleçao",  'A coluna "Chuva Medida" não foi selecionada', parent = self)
        x.addButton(QMessageBox.Ok)
        x.setInformativeText("Por favor, verifique a tabela e selecione a coluna correta.")
        x.exec()
        raise KeyError

    for row in archive:
        try:
            # Formata o texto de DataHora e convertem em um tipo datetime.
            time, date = '', ''
            if not AreTogether:
                time = row[colunas["Hora"]]
                date = row[colunas["Data"]]
            else:
                date, time = row[colunas["Data & Hora"]].split(" ")

            if formatoData == "DD/MM/AAAA":
                date = date.split("/") if "/" in date else date.split('-')
                date.reverse()
                for num in range(len(date)):
                    if len(date[num]) == 1:
                        date[num] = '0'+date[num]
                date = "-".join(date)
            else:
                date = date.replace("/","-") 
            timedate = datetime.fromisoformat(date + ' ' + time)

        except ValueError:
            x = QMessageBox(QMessageBox.Critical, "Erro de Formatação",  "O formato especificado para Data ou Hora é inválido.", parent = self)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText("Por favor, verifique o formato da data ou o conteúdo da coluna.")
            x.exec()
            raise ValueError
        # Valor do Acumulado
        try:
            item = row[colunas["Chuva Medida"]].replace(",", ".")
            teste = False
            if '.' in item or item.isnumeric():
                item = float(item)
                teste = True
                
            dicChuva[timedate] = [teste, item] + [0]*itens

            #Valor do Nivel do Rio, se houver.
            if isNivel:
                dicNivel[timedate] = row[colunas["Nível do Rio"]]
        except ValueError:
            x = QMessageBox(QMessageBox.Critical, "Erro de Formatação",  "Não foi possível identificar o valor registrado", parent = self)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText('Por favor, verifique o conteúdo da coluna "Chuva Medida".')
            x.exec()
            raise ValueError

        except IndexError:
            x = QMessageBox(QMessageBox.Critical, "Erro de Seleção",  "Não foi possível identificar o valor registrado", parent = self)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText('A Coluna Selecionada para "Chuva Medida" está vazia ou não existe.')
            x.exec()
            raise IndexError

    objeto.setData(dicChuva)
    if len(dicNivel) > 0:
        objeto.setDataHeight(dicNivel)
    return None


def openFile(parent):
    ''' Abre o arquivo e adiciona os seus dados a dois dicionarios.
    o arquivo .csv deve conter as colunas representando a data/hora, o ult.acumulado e o nivel do rio (opcional)
    cada dicionario contem os dados de Chuva e Nivel do rio, respectivamente.'''
    Archive = []
    Ignore = parent.ignore.isChecked()
    try:
        with open(parent.path.text(), newline = '') as csvfile:
            newfile = csv.reader(csvfile, delimiter = parent.separador)
            for row in newfile:
                # Primeira linha.
                if Ignore:
                    Ignore = False
                    continue
                if len(row[0]) > 0:
                    Archive.append(row)

    except FileNotFoundError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível abrir o arquivo solicitado.", buttons = QMessageBox.Ok, parent = parent)
        x.setInformativeText("Não existe tal arquivo ou diretório.")
        x.setDetailedText(str(Err))
        x.exec()
        raise FileNotFoundError

    return Archive

def saveFile(parent, File, Delimiter = ';'):

    try:
        with open(parent.folder.text(), mode = 'w', newline = '') as csvfile:
            arquivo = csv.writer(csvfile, delimiter = Delimiter, quoting = csv.QUOTE_MINIMAL)
            for row in File:
                arquivo.writerow(row)
    except PermissionError as Err:
        x = QMessageBox(QMessageBox.Critical, "Erro de Acesso", "Não foi possível salvar seu arquivo.", buttons = QMessageBox.Ok, parent = parent)
        x.setInformativeText("O arquivo que voce está tentando sobrescrever já está aberto em outro programa.")
        x.setDetailedText(str(Err))
        x.exec()
        raise PermissionError
