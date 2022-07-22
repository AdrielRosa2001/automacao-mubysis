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

