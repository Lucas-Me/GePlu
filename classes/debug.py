from PySide2.QtWidgets import (QMainWindow, QApplication, QProgressDialog)
from datetime import timedelta, datetime

class Acumulados():
    ''' Tentativa de criar uma classe que representa todos os acumulados de uma estacao.'''

    def __init__(self, ChuvaAcumulada = [], dicChuva = {}, dicNivel = {}):
        self.Chuva = dicChuva #Dicionario contendo o horario e seus respectivos acumulados
        self.valuesIn = ChuvaAcumulada # cada inteiro representa minuto.
        self.Nivel = dicNivel #Dicionario contendo o horario e seus respectivos niveis do rio, se houver.
        self.isNivel = True if len(dicNivel) != 0 else False

    def getValues(self):
        return self.valuesIn

    def setData(self, Data):
        self.Chuva = Data

    def setDataHeight(self, Data, Ativar  = True):
        self.isNivel = Ativar
        self.Nivel = Data

    def setValues(self, Values):
        self.valuesIn = sorted(Values)

    def calcularAcumulado(self, parent):    
        ''' Calcula todos os acumulados do documento
        intervalos consiste em uma lista contendo o tempo dos acumulados solicitados, sao eles em: (1,4,24,48,96) horas'''
        intervalos = self.valuesIn # [60, 240, 1440, 2880, 5760] Minutos
        intervalosTime = [timedelta(minutes = x) for x in self.valuesIn]
        tamanho = len(intervalos) 
        dicionario = self.Chuva
        ArrayDatas = tuple(sorted(dicionario.keys()))

        # Constroi o Dialogo de Progresso
        progress = QProgressDialog("Gerando os valores de chuva acumulada...","Cancelar", 0, len(dicionario), parent = parent)
        progress.setMinimumDuration(0)
        progress.setWindowTitle("Progresso")
        progress.setModal(True)
        j = 0

        for pos in range(len(ArrayDatas)): #posicoes = [15/04/2018 10:00, 15/04/2018 10:15, ..]
            QApplication.processEvents()
            progress.setValue(j)
            if progress.wasCanceled():
                # Cancelado pelo usuario
                break
            j += 1

            currentKey = ArrayDatas[pos]
            count = 0
            posAcumulado = 0
            somatorio = 0.0
            limites = [currentKey - time for time in intervalosTime]
            while True:
                indice = pos + count
                if indice == -1:
                    dicionario[currentKey][posAcumulado + 2] = somatorio
                    posAcumulado += 1
                    if posAcumulado == tamanho:
                        break
                    else:
                        continue
                        
                lastKey = ArrayDatas[indice]
                if lastKey > limites[posAcumulado]:
                    # Do something
                    valores = dicionario[lastKey][:2]
                    if valores[0]:
                        somatorio += valores[1]
                    count -= 1
                else:
                    # Do something2
                    dicionario[currentKey][posAcumulado + 2] = somatorio
                    posAcumulado += 1
                    if posAcumulado == tamanho:
                        break
                
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

