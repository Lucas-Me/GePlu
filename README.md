# GePlu

Guia de Utilização do programa GePlu  - Nome Provisório

---- introdução -------------

O Programa lê um arquivo no formato .CSV ou .TXT que contenha os dados fornecidos por uma das estações pluviométricas do CEMADEN ou INEA e gera um arquivo de texto em formato .CSV ou .TXT, contendo os dados de chuva acumulada em 1 hora, 4 horas, 24 horas, 48 horas e outros intervalos. Inclui também os dados do Nível do Rio (Opcional) e a última chuva dada.

Para que o programa seja executado corretamente, é necessario que dentro do arquivo estejam presentes pelo menos as colunas associadas ao Ultimo Acumulado de Chuva (Em 15 ou 10 min, dependendo da fonte) e suas respectivas datas e horário de registro.

O Nivel do Rio é opcional e pode ser omitido no arquivo a ser lido.
"Chuva Medida" corresponde ao último valor de precipitação registrada pela estação pluviômétrica.


 --- OBSERVAÇÕES E COMO UTILIZAR O PROGRAMA CORRETAMENTE ----

Caso tenha algum editor de planilha instalado em sua máquina, voce só precisa juntar todos os seus dados em uma única planilha e salvar como arquivo de texto CSV (separado por virgula) ou TXT, e então é só abrir no programa.

OBS: O Cemaden fornece uma planilha por município, e dentro desta planilha se encontra dados misturados de diversas estações presentes no município selecionado. Por favor, crie planilhas separadas para cada estação, voce pode utilizar a função de "FILTRO" do seu editor de planilhas para te ajudar no processo.

Cada coluna no seu arquivo pode estar delimitada por ponto-virgula(;), virgula (,) ou ponto (.), no programa há uma opção para o usuário selecionar o delimitador correto. 
Não há necessidade de se preocupar com a casa decimal dos acumulados, ele pode estar com vírgula ou ponto.

O Campo "Configurar Intervalos" permite ao usuário escolher qual será o intervalo dos acumulados pluviométricos, isto é, se serão em 1 hora, 4 horas e etc. É possível escolher mais de um.
Por padrão, o programa calcula a chuva acumulada em 1 Hora, 4 Horas, 24 Horas, 48 Horas e 96 Horas.

Qualquer erro na leitura do arquivo irá fazer com que ao clicar o botão "Executar", nada aconteça.
EDIÇÃO: Adicionei algumas notificações ao usuario para identificar a raiz do problema e resolve-la, mas pode nao ser suficiente. Se este for o caso me notifique.

- Evite linhas vazias no arquivo a ser lido, o programa pode não executar por isso. # Consertado
- LEMBRE-SE DE ESPECIFICAR DO QUE SE TRATA CADA COLUNA AO ABRIR UM ARQUIVO DENTRO DO PROGRAMA
- Evite Entradas duplicadas ao selecionar o tipo das colunas na tabela.
- ao verificar as colunas, pode deixar as que não serão utilizadas como "Selecionar" ou "Ignorar".

- - - -- > LEMBRE-SE DE VERIFICAR SE A PRIMEIRA LINHA DO SEU ARQUIVO SERÁ CONSIDERADA OU NAO < --------
 
Exemplo de entrada:

--- Formato Padrao INEA ----   -------------- Formato Padrao CEMADEN ------------------------------------------------
DataHora;Chuva;Nivel          	municipio;codEstacao;uf;nomeEstacao;latitude;longitude;datahora;valorMedida
08/04/2018 00:00;0;1.14       	NOVA IGUAÇU;330350004A;RJ;Jardim Guandu;-43,608;-22,828;2018-11-01 00:50:00.0;0,00;
08/04/2018 00:15;0;1.15		NOVA IGUAÇU;330350004A;RJ;Jardim Guandu;-43,608;-22,828;2018-11-01 01:50:00.0;0,00;
08/04/2018 00:30;0;1.15		NOVA IGUAÇU;330350004A;RJ;Jardim Guandu;-43,608;-22,828;2018-11-01 02:50:00.0;0,00;
08/04/2018 00:45;0;1.15		NOVA IGUAÇU;330350004A;RJ;Jardim Guandu;-43,608;-22,828;2018-11-01 03:50:00.0;0,00;
08/04/2018 01:00;0;1.15		NOVA IGUAÇU;330350004A;RJ;Jardim Guandu;-43,608;-22,828;2018-11-01 04:50:00.0;0,00;
.....				.............
.....				............
----------------------------   ----------------------------------------------------------------------------------------	

Dentro do programa é possível especificar do que se trata cada coluna no seu arquivo.
No exemplo do CEMADEN acima, as colunas (municipio, codEstacao, uf, nomeEstacao,latitude,longitude) devem ser ignoradas.
Em ambos os exemplos é necessário ignorar a primeira linha.

--- >> Exemplo de Saida do Programa

Ao final de sua execução, é gerado um arquivo de texto em formato .txt ou .csv.
O Carácter utilizado como separador por padrão é o ponto-vírgula (;)
O Carácter utilizado para casa decimal por padrão é a vírgula (,)

Um exemplo de saída do programa é:
----------------------------------------------
Data Hora;Último Registro;Chuva Acumulada em 1 Hora(s);Chuva Acumulada em 4 Hora(s);Chuva Acumulada em 24 Hora(s);Chuva Acumulada em 48 Hora(s);Chuva Acumulada em 96 Hora(s)
02/02/2020 20:00;45.4;45,4;45,4;46,6;46,6;62,6
02/02/2020 20:15;ND;45,4;45,4;46,6;46,6;62,6
02/02/2020 20:30;ND;45,4;45,4;46,6;46,6;62,6
02/02/2020 20:45;ND;45,4;45,4;46,6;46,6;62,6
02/02/2020 21:00;ND;0;45,4;46,6;46,6;62,6
02/02/2020 21:15;4.0;4,0;49,4;50,6;50,6;66,6
02/02/2020 21:30;0.0;4,0;49,4;50,6;50,6;66,6
02/02/2020 21:45;0.0;4,0;49,4;50,6;50,6;66,6
02/02/2020 22:00;0.0;4,0;49,4;50,6;50,6;66,6
02/02/2020 22:15;0.0;0,0;49,4;50,6;50,6;66,6
02/02/2020 22:30;0.0;0,0;49,4;50,6;50,6;66,6
02/02/2020 22:45;0.0;0,0;49,4;50,6;50,6;66,6
02/02/2020 23:00;0.0;0,0;49,4;50,6;50,6;66,6
02/02/2020 23:15;0.2;0,2;49,6;50,8;50,8;66,8
---------------------------------------------------
O arquivo é salvo no diretório especificado e pode ser aberto por qualquer editor de planilhas, desde que seja selecionado o separador de colunas correto para o seu arquivo.

CASO TENHA IDENTIFICADO ALGUM PROBLEMA OU BUG NO PROGRAMA, POR FAVOR ENTRE EM CONTATO.
Sugestões também são bem-vindas!
Criado por: Lucas da Silva Menezes
E-Mail para Contato: lucasmenezes4502@gmail.com

Observações adicionais:

- O Programa utiliza apenas um núcleo de processamento para realizar as tarefas.
- Arquivos Grandes (cerca de 200.000 linhas) devem levar no mínimo 40s para serem processados, dependendo das especificações do seu computador.
