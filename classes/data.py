from PySide6.QtWidgets import QMessageBox
import pandas as pd
import numpy as np

# Organizacao e Manipulacao dos Dados

def data_filter(master, df, headerdict):
    '''Recebe um dataframe de strings e filtra as colunas.'''


    # Filtra no primeiro dataframe as colunas correspondentes a: datas, precipitacao observada/registrada.
    # se estas colunas nao existirem, provoca um erro e avisa ao usuario.

    # filtra coluna correspondente a precipitação observada.
    try:
        observados = df[df.columns[headerdict["Prec. Observada"]]].str.replace(',','.')

    except:
        x = QMessageBox(QMessageBox.Warning, "Erro de Seleçao",  'A coluna "Prec. Observada" não foi selecionada.', parent = master)
        x.addButton(QMessageBox.Ok)
        x.setInformativeText("Por favor, verifique a tabela e selecione a coluna correta.")
        x.exec()
        raise KeyError

    # filtra a(s) coluna(s) correspondente(s) a data/hora.
    if "Data" in headerdict.keys():
        try:
            datetime = df[df.columns[headerdict["Data"]]] + ' ' + df[df.columns[headerdict["Hora"]]]

        except:
            x = QMessageBox(QMessageBox.Warning, "Erro de Seleçao",  'A coluna correspondente a "Hora" não foi selecionada', parent = master)
            x.addButton(QMessageBox.Ok)
            x.setInformativeText("Por favor, verifique a tabela e selecione a coluna correta.")
            x.exec()
            raise KeyError


    elif "Data & Hora" in headerdict.keys():
        datetime = df[df.columns[headerdict["Data & Hora"]]]

    else:
        x = QMessageBox(QMessageBox.Warning, "Erro de Seleçao",  'A coluna correspondente a "Data" ou "Hora" não foi selecionada', parent = master)
        x.addButton(QMessageBox.Ok)
        x.setInformativeText("Por favor, verifique a tabela e selecione a coluna correta.")
        x.exec()
        raise KeyError

    new_df = pd.DataFrame(observados.to_numpy(), datetime.to_numpy(), columns = ["Observado"])

    return new_df

def convert_dtype(master, df):
    ''' Recebe o dataframe e converte os tipos de suas colunas.'''
    dataformat = master.linkdata[master.FormatoData.currentText()]
    timeformat = master.linktime[master.FormatoTime.currentText()]
    datetimeformat = dataformat + ' ' + timeformat

    try:
        df.index = pd.to_datetime(df.index, format = datetimeformat)

    except ValueError:
        x = QMessageBox(QMessageBox.Critical, "Erro de Formatação",  "O formato especificado para Data ou Hora é inválido.", parent = master)
        x.addButton(QMessageBox.Ok)
        x.setInformativeText("Por favor, verifique o formato da data ou o conteúdo da coluna.")
        x.exec()
        raise ValueError

    try:
        df['Observado'] = pd.to_numeric(df['Observado'], errors = "coerce")

    except ValueError:
        x = QMessageBox(QMessageBox.Critical, "Erro de Formatação",  "Não foi possível identificar o valor registrado", parent = master)
        x.addButton(QMessageBox.Ok)
        x.setInformativeText('Por favor, verifique o conteúdo da coluna associada a precipitação registrada.')
        x.exec()
        raise ValueError
    
    return df

def compute(datearr, floatarr, timedelta):
	'''Computa o acumulado pluviometrico de um conjunto de dados, em um dado intervalo de tempo.'''
    # Para um conjunto de 75'000 observacoes e timedelta de 96 horas (4 dias), tempo de execucao = 2s.
    # Realizar essa operacao da forma tradicional levaria 2 minutos aprox.
	
	last = 0
	results = np.zeros(datearr.shape)
	for n in range(datearr.shape[0]):
		boolarr = datearr[last:n + 1] > (datearr[n] - timedelta)
		results[n] = np.nansum(boolarr * floatarr[last:n + 1])
		last = n - np.count_nonzero(boolarr) + 1

	return results
