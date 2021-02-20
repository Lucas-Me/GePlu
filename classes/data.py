import pandas as pd
import numpy as np

# Organizacao e Manipulacao dos Dados

def convert_dtype(self, df, colunas):

    '''#Testes de caso e manuseio de erros.
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
                    raise KeyError'''


    '''except ValueError:
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
                                    raise IndexError'''
    return None

def compute(df, intervalos):
	'''Computa os acumulados pluviometricos em diversos intervalos de tempo.'''
	# Recebe um dataframe cujo indices sao objetos datetime64 e a coluna (observado) refere-se a precipitação registrada na estacao.

	interval = np.timedelta64(4, 'D')
	datas = df.index.to_numpy()
	vector = df['observado'].to_numpy()
	
	last = 0
	results = np.zeros(datas.shape)
	for n in range(datas.shape[0]):
		booleans = datas[last:n + 1] > (datas[n] - interval)
		results[n] = np.dot(booleans, vector[last:n + 1])
		last = n - np.sum(booleans) + 1


	return pd.Series(results, df.index)