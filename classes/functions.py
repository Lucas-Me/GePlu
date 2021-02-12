from datetime import timedelta, datetime
from PySide2.QtWidgets import (QMainWindow, QMessageBox, QDialog)
import csv


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
            if '.' in time:
                x = str.index(time, '.')
                time = time[:x]
                
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
