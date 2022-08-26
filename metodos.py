from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from win32com import client
from pathlib import Path
from num2words import num2words
import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sqlite3

path_folders = None #path (recibos muby, recibos manual, clientes cadastrados)

def getDadosLogin():
    banco = sqlite3.connect('database.db')
    cursor = banco.cursor()

    try:
        cursor.execute("SELECT * FROM loginUsuario")
        dados_login = cursor.fetchall()[0] #(1, usuario, senha, loja)
        cursor.execute("SELECT * FROM loginEmail")
        dados_email = cursor.fetchall()[0] #(email, senha)
        banco.close()
        dados_login_banco = (dados_login, dados_email)
        return dados_login_banco
    except sqlite3.Error as erro:
        print(erro)
        banco.close()
        return False

def getPathFilesBanco():
    banco = sqlite3.connect('database.db')
    cursor = banco.cursor()

    try:
        cursor.execute("SELECT * FROM pathFiles")
        path_files_banco = cursor.fetchall()[0]
        banco.close()
        return path_files_banco
    except sqlite3.Error as erro:
        print(erro)
        banco.close()

def getDadosDb(bancodb, tabela):
    banco = sqlite3.connect(f"{bancodb}")
    cursor = banco.cursor()

    try:
        cursor.execute(f"SELECT * FROM {tabela}")
        guias = cursor.fetchall()
        banco.close()
        return guias
    except sqlite3.Error as erro:
        print(erro)
        banco.close()

def insertDadosTabela(bancodb, tabela, valores):
    banco = sqlite3.connect(f"{bancodb}")
    cursor = banco.cursor()
    try:
        cursor.execute(f"INSERT INTO {tabela} VALUES({valores})")
        banco.commit()
        banco.close()
        print("*** Dados da guia inseridos no banco! ***")
    except:
        print("*** Houve um erro ao tentar inserir os dados no banco! ***")
        banco.close()

def limparDadosBanco(bancodb, tabela):
    banco = sqlite3.connect(f"{bancodb}")
    cursor = banco.cursor()
    try:
        cursor.execute(f"DELETE FROM {tabela}")
        banco.commit()
        banco.close()
        print("*** Dados apagados com sucesso do banco! ***")
    except:
        print("*** Houve um erro ao tentar apagar os dados do banco! ***")
        banco.close()

def deletLinhaBanco(bancodb, tabela, campo, item):
    banco = sqlite3.connect(f"{bancodb}")
    cursor = banco.cursor()
    try:
        #cursor.execute("DELETE FROM loginUsuario WHERE usuario = 'Marques'")
        cursor.execute(f"DELETE FROM {tabela} WHERE {campo} = {item}") # se o item for string inserir o item com aspas duplas depois simples = " 'Adriel' "
        banco.commit()
        banco.close()
        print("*** Dados da coluna apagados com sucesso do banco! ***")
    except:
        print("*** Houve um erro ao tentar apagar os dados da coluna do banco! ***")
        banco.close()

def updateLinhaBanco(bancodb, tabela, campo, item, campo2, item2):
    banco = sqlite3.connect(f"{bancodb}")
    cursor = banco.cursor()
    try:
        #cursor.execute("UPDATE loginUsuario SET usuario= 'Marques' WHERE usuario= 'Adriel'")
        cursor.execute(f"UPDATE {tabela} SET {campo} = '{item}' WHERE {campo2}= '{item2}'") # se o item for string inserir o item com aspas duplas depois simples = " 'Adriel' "
        banco.commit()
        banco.close()
        print("*** Dados da coluna alterados com sucesso do banco! ***")
    except:
        print("*** Houve um erro ao tentar alterar os dados da coluna do banco! ***")
        banco.close()

path_folders = getPathFilesBanco()
print(path_folders)

def getdata(saida):
    data_public = datetime.date.today()
    data_public_str = data_public.strftime("%d/%m/%Y")
    dia, mes, ano = data_public_str.split("/")
    mes_ext = {1: 'JANEIRO', 2 : 'FEVEREIRO', 3: 'MARÇO', 4: 'ABRIL', 5: 'MAIO', 6: 'JUNHO', 7: 'JULHO', 8: 'AGOSTO', 9: 'SETEMBRO', 10: 'OUTUBRO', 11: 'NOVEMBRO', 12: 'DEZEMBRO'}

    data_extenso = {'dia': dia, 'mes': mes_ext[int(mes)], 'ano': ano}
    data_numero = {'dia': dia, 'mes': mes_ext[int(mes)], 'ano': ano}
    datas = {1: data_extenso, 2: data_numero}
    return datas[saida]

def gerar_numero_por_extenso(valor_entrada):
    valor = float(valor_entrada)

    valor_str = str(valor)
    valor_str = valor_str.split(".")
    real = valor_str[0]
    decimal = (valor*100)%100
    if decimal != 0:
        num_ptbr1 = str(num2words(int(real), lang='pt-br'))
        num_ptbr2 = str(num2words(int(decimal), lang='pt-br'))
        valor_total_extenso = f"{str(num_ptbr1).upper()} REAIS E {num_ptbr2.upper()} CENTAVOS"

        return valor_total_extenso
    else:
        num_ptbr1 = str(num2words(int(real), lang='pt-br'))
        valor_total_extenso = f"{str(num_ptbr1).upper()} REAIS"

        return valor_total_extenso

""" def coletar_dados(caminho_arquivo_txt, tipo):
    # 0 para lista
    # 1 para dict
    #retorna uma lista ou um dict
    arquivo = open(caminho_arquivo_txt, "r")
    lista = arquivo.readlines()
    arquivo.close()
    if tipo == 0:
        temp_list = []
        for i in lista:
            i = i.replace("\n", "")
            i = i.replace(" ", "")
            temp_list.append(i)
        return temp_list
    elif tipo == 1:
        cont = 0
        temp_dict = {}
        for i in lista:
            i = i.replace("\n", "")
            i = i.replace(" ", "")
            temp_dict[cont] = i
            cont = cont+1
        return temp_dict """

def salvar_dados(caminho_arquivo, lista):
    # 0 para lista
    # 1 para dict
    # não retorna nada = void
    temp_list = []
    temp_dict = {}
    if type(lista) == type(temp_list):
        temp_list = []
        for i in lista:
            i = str(i)+" \n"
            temp_list.append(i)
        arquivo = open(caminho_arquivo, "w")
        arquivo.writelines(temp_list)
        arquivo.close()
        print("Dados salvos!!")
    elif type(lista) == type(temp_dict):
        temp_list = []
        for i in lista:
            x = lista[i]
            temp_list.append(str(x) + " \n")
        arquivo = open(caminho_arquivo, "w")
        arquivo.writelines(temp_list)
        arquivo.close()
        print("Dados salvos!!")

def salvar_cliente(cliente):
    temp_list = []
    for i in cliente:
        temp_list.append(i+str("\n"))
    arquivo = open(str(path_folders[0])+f"/{str(cliente[0]).upper()}.txt", "w")
    arquivo.writelines(temp_list)
    arquivo.close()
    print("Dados salvos!!")

def enviar_email(dados, mensagem, destino):
    # Configuração
    host = "smtp.office365.com"
    port = 587
    user = dados[0]
    password = dados[1]

    # Criando objeto
    server = smtplib.SMTP(host, port)

    # Login com servidor
    server.ehlo()
    server.starttls()
    server.login(user, password)


    # Criando mensagem
    message = mensagem[1]
    email_msg = MIMEMultipart()
    email_msg['From'] = user
    email_msg['To'] = destino
    email_msg['Subject'] = mensagem[0]

    #Adicionando texto.
    email_msg.attach(MIMEText(message, 'plain'))

    # Enviando mensagem
    print('Enviando mensagem...')
    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    print('Mensagem enviada!')
    server.quit()

def gerar_recibo(dados):

    nome = dados['cliente']
    valor = float(str(dados['valor']).replace(",", "."))
    
    extenso = gerar_numero_por_extenso(valor)
    referente = dados['referente']
    
    data = getdata(1)
    dia = data['dia']
    mes = data['mes']
    ano = data['ano']

    funcionario = dados['funcionario']

    #criando planilha (Book)
    arquivo = load_workbook('./recibos/source/recibo.xlsx')

    recibo = arquivo['page01']
    recibo = arquivo.active

    recibo['H3'] = ("R$ "+(str("%.2f" %(valor)).replace(".", ",")))
    recibo['C6'] = nome
    recibo['C8'] = extenso
    recibo['C10'] = referente
    recibo['B13'] = dia
    recibo['D13'] = mes
    recibo['G13'] = ano
    recibo['I13'] = funcionario


    nome_save = str(nome).replace(" ", "-")

    arquivo.save(f'./recibos/recibo-{nome_save}.xlsx')
    path_fille = Path(f'./recibos/recibo-{nome_save}.xlsx').absolute()
    path_fille = str(path_fille)
    path_fille = path_fille.replace("\\", "\\\\")

    #Abrindo Aplicativo Excel
    app_excel = client.DispatchEx("Excel.Application")
    app_excel.Interactive = False
    app_excel.Visible = False

    #Abrindo arquivo excel
    workbook = app_excel.Workbooks.Open(path_fille)
    #Convertendo em PDF
    workbook.ActiveSheet.ExportAsFixedFormat(0, path_fille)
    workbook.Close()
    os.remove(path_fille)
