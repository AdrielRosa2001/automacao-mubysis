from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from win32com import client
from pathlib import Path

def coletar_dados(caminho_arquivo_txt, tipo):
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
        return temp_dict

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

def gerar_email(cnpj, valor, data):
    pass

def gerar_recibo(dados):
    nome = dados[0]
    valor = dados[1]
    extenso = dados[2]
    referente = dados[3]
    data = dados[4]
    data = data.split("/")
    dia = data[0]
    mes = data[1]
    ano = data[2]
    funcionario = dados[5]

    #criando planilha (Book)
    arquivo = load_workbook('./recibos/source/recibo.xlsx')

    recibo = arquivo['page01']
    recibo = arquivo.active

    recibo['H3'] = valor
    recibo['C6'] = nome
    recibo['C8'] = extenso
    recibo['C10'] = referente
    recibo['B13'] = dia
    recibo['D13'] = mes
    recibo['G13'] = ano
    recibo['I13'] = funcionario

    arquivo.save(f'./recibos/reciboTemp.xlsx')
    path_fille = Path('./recibos/reciboTemp.xlsx').absolute()
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
