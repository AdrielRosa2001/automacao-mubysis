from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from importlib.resources import path
from logging import handlers
import py_compile
from time import sleep
from turtle import update
from playwright.sync_api import sync_playwright
#from cmath import atan
from msilib.schema import Font, Icon
import PySimpleGUI as sg
import interface
import metodos
import os



# Codigo muby empresa: 237157
#database = dict()
guias = []
headless_set = 'ON'


# Metodos playwrigth

def headless_inicial(headless_set):
    if headless_set == 'ON':
        browser = p.chromium.launch()
        return browser
    elif headless_set == 'OFF':
        browser = p.chromium.launch(headless=False) # exibindo tela
        return browser

def realizar_login(usuario, senha):
    page.goto("https://mubisys.com/index.php?app")
    page.wait_for_timeout(10000)
    page.fill("input[name='codigo']", '237157')
    page.fill("input[name='usuario']", usuario)
    page.fill("input[name='senha']", senha)
    page.click("ion-icon[name='arrow-forward']")
    page.wait_for_timeout(2000)

def realizar_pcp(guia):
    page.goto("https://mubisys.com/index.php?modulo=Pcp")
    page.fill("input[name='search']", guia[0])
    page.locator("[placeholder=\"Buscar\"]").press("Enter")
    page.wait_for_timeout(1000)
    page.click("a[title='Visualizar']")
    page.wait_for_timeout(1000)
    page.locator(".icofont-gear").click()
    page.wait_for_timeout(1000)
    page.locator("text=Finalizar Produção").click()

def realizar_producao(a):
    b = a
    page.goto("https://mubisys.com/index.php?modulo=Producao")
    page.wait_for_timeout(1000)
    saida = True
    sleep(4.0)
    while saida:
        try:
            page.locator(f"text=0 0 {str(b)} 0 >> img").nth(2).click(timeout=250)
            b = b-1
            saida = False
        except:
            b = b+1
            if b >= 30:
                saida = False
            else:
                pass
    page.wait_for_timeout(1000)
    page.locator(selector="#itens > div > table > tbody > tr:nth-child(1) > td:nth-child(10) > a").click()
    page.wait_for_timeout(1000)
    page.locator("#rodapemodal img").nth(2).click()
    page.wait_for_timeout(1000)
    return b

def realizar_faturamento(guia):
    page.goto("https://mubisys.com/index.php?modulo=Faturamento")
    page.locator("[placeholder=\"Buscar\"]").fill(guia[0])
    page.locator("[placeholder=\"Buscar\"]").press("Enter")
    page.locator("#buscargeral").click()
    page.wait_for_timeout(2000)
    page.locator("input[type=\"checkbox\"]").check()
    page.wait_for_timeout(500)
    page.locator("#faturamentos >> text=Faturar...").click()
    page.wait_for_timeout(500)
    page.locator("text=Formas de pagamento A DEFINIR A FATURAR AMERICAN EXPRESS BOLETO BB - CROQUI BOLE >> button[role=\"combobox\"]").click()
    page.wait_for_timeout(500)
    page.locator("text=Formas de pagamento A DEFINIR A FATURAR AMERICAN EXPRESS BOLETO BB - CROQUI BOLE >> [aria-label=\"Search\"]").click()
    page.wait_for_timeout(500)
    page.locator("text=Formas de pagamento A DEFINIR A FATURAR AMERICAN EXPRESS BOLETO BB - CROQUI BOLE >> [aria-label=\"Search\"]").fill(guia[2])
    page.wait_for_timeout(500)
    page.locator("text=Formas de pagamento A DEFINIR A FATURAR AMERICAN EXPRESS BOLETO BB - CROQUI BOLE >> [aria-label=\"Search\"]").press("Enter")
    page.wait_for_timeout(500)
    page.locator("text=Aplicar").click()
    page.wait_for_timeout(500)
    page.locator("button[role=\"combobox\"]:has-text(\"Não\")").nth(2).click()
    page.wait_for_timeout(500)
    if guia[3] == "SJ":
        page.locator("text=CAIXA - LOJA S JOSÉ Não atribuída").click()
    elif guia[3] == "TR":
        page.locator("text=CAIXA - LOJA TRAIRI Não atribuída").click()
    elif guia[3] == "ZS":
        page.locator("text=CAIXA - LOJA Z SUL Não atribuída").click()
    page.locator("#faturarfinal").click()

def realizar_relatorio_muby(data, loja, relatorios): # relatorios(plotagem, imagem)
    page.goto("https://mubisys.com/index.php?modulo=Contasareceber")
    page.wait_for_timeout(3000)
    page.locator("#ativarfiltro").click()
    #page.locator("input[name=\"datainicial\"]").click()
    page.wait_for_timeout(1000)
    data = data.replace("/", "-")
    print(data)
    page.locator("input[name=\"datainicial\"]").fill(data)
    page.wait_for_timeout(2000)
    page.locator("input[name=\"datafinal\"]").fill(data)
    page.wait_for_timeout(2000)
    #page.wait_for_timeout(1000)
    #page.locator(".active.day").click()
    #page.locator("input[name=\"datainicial\"]").click()
    #page.locator("input[name=\"datainicial\"]").press("Enter")
    #page.wait_for_timeout(1500)
    #page.locator("input[name=\"datainicial\"]").press('Enter')
    #page.locator("input[name=\"datainicial\"]").click()
    #page.locator("input[name=\"datafinal\"]").fill(data)
    #page.locator("input[name=\"datainicial\"]").click()
    #page.wait_for_timeout(1500)
    #page.locator("input[name=\"datafinal\"]").press('Enter')
    
    page.wait_for_timeout(500)
    page.locator(selector="#maisopcoes > div:nth-child(1) > div:nth-child(4) > div > button").click()
    page.locator(selector="#bs-select-4-2").click()
    page.locator(selector="#maisopcoes > div:nth-child(1) > div:nth-child(4) > div > button").click()
    if relatorios[0] == 1: # plotagem
        page.locator(selector="#maisopcoes > div:nth-child(1) > div:nth-child(5) > div > button").click()
        if loja == "SJ": 
            page.locator(selector="#bs-select-5-4").click()
        elif loja == "TR":
            page.locator(selector="#bs-select-5-5").click()
        elif loja == "ZS":
            page.locator(selector="#bs-select-5-6").click()
    else: 
        pass
    if relatorios[1] == 1: # imagem
        page.locator(selector="#maisopcoes > div:nth-child(1) > div:nth-child(5) > div > button").click()
        if loja == "SJ": 
            page.locator(selector="#bs-select-5-1").click()
        elif loja == "TR":
            page.locator(selector="#bs-select-5-2").click()
        elif loja == "ZS":
            page.locator(selector="#bs-select-5-3").click()
    else:
        pass
    page.locator(selector="#maisopcoes > div:nth-child(3) > div:nth-child(3) > div:nth-child(2) > div > button").click()
    page.locator(selector="#bs-select-10-3").click() # AMERICAN EXPRESS
    page.locator(selector="#bs-select-10-6").click() # DEPOSITO BB
    page.locator(selector="#bs-select-10-7").click() # DEPOSITO BNB
    page.locator(selector="#bs-select-10-8").click() # DINER CREDITO
    page.locator(selector="#bs-select-10-9").click() # DINER DEBITO
    page.locator(selector="#bs-select-10-10").click() # ELO CREDITO
    page.locator(selector="#bs-select-10-11").click() # ELO DEBITO
    page.locator(selector="#bs-select-10-12").click() # ESPECIE
    page.locator(selector="#bs-select-10-13").click() # HIPERCARD
    page.locator(selector="#bs-select-10-14").click() # MASTER CREDITO
    page.locator(selector="#bs-select-10-15").click() # MASTER DEBITO
    page.locator(selector="#bs-select-10-18").click() # VISA CREDITO
    page.locator(selector="#bs-select-10-19").click() # VISA DEBITO
    page.locator(selector="#maisopcoes > div:nth-child(3) > div:nth-child(3) > div:nth-child(2) > div > button").click() 
    page.locator(selector="#buscar").click()
    page.wait_for_timeout(6000)
    with page.expect_download() as donwload_info:
        page.click(selector="#gerarpdfresultado")
    donwload = donwload_info.value
    donwload.save_as("./caminho")
    path = donwload.path()

    print(path)
    print(type(path))
    """os.system(f"explorer.exe \"{path}\"")

    lista_arquivos = os.listdir(path)

    page.wait_for_timeout(5000)

    for arquivo in lista_arquivos:
        print(arquivo)
        if ".pdf" in arquivo:
            os.rename(f"{path}\\{arquivo}", f"C:\\Users\\PRODUCAOPC2\\Desktop\\Relatorios_e_Recibos\\{arquivo}")
            print(f"movendo \"{arquivo}\", para novo diretorio!")

    os.system("explorer.exe \"C:\\Users\\PRODUCAOPC2\\Desktop\\Relatorios_e_Recibos")"""


#Tema do programa deifindo
sg.theme('Reddit')

# Importando Layout do programa
frame01 = interface.frame01()
tab1 =  interface.tab1(frame01)
tab2 = interface.tab2()
coluna01 = interface.coluna01()
coluna02 = interface.coluna02()
coluna03 = interface.coluna03()
coluna04 = interface.coluna04()
frame02 = interface.frame02(coluna01, coluna02, coluna03, coluna04)
frame03 = interface.frame03()
tab3 = interface.tab3(frame02, frame03)
coluna07 = interface.coluna07()
coluna08 = interface.coluna08()
frame05 = interface.frame05(coluna07, coluna08)
frame06 = interface.frame06()
tab4 = interface.tab4(frame05, frame06)
coluna05 = interface.coluna05()
coluna06 = interface.coluna06()
frame04 = interface.frame04(coluna05, coluna06)
tab5 = interface.tab5(frame04)
layout = interface.layout(tab1, tab2, tab3, tab4, tab5)


window = sg.Window('AutoMuby 3.0', layout, icon='./assets/icon2.0.ico')

# Abrindo configurações:
#database = metodos.coletar_dados("configs.txt", 0)
database = metodos.getDadosLogin()
credenciais_muby = database[0]
credenciais_email = database[1]

# var email
email = ("", "")

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
        break
    
    if event == '-headless-':
        if headless_set == 'ON':
            window['-headless-'].update('Headless: OFF')
            headless_set = 'OFF'
        elif headless_set == 'OFF':
            window['-headless-'].update('Headless: ON')
            headless_set = 'ON'
        pass

    if event == '-adicionar-':
        data_os = "hoje"
        procedimentos = [values['-pcp-'], values['-producao-'], values['-faturamento-']]

        pcp = 0
        producao = 0
        faturameno = 0

        if values['-pcp-'] == True:
            pcp = 1
        else:
            pcp = 0

        if values['-producao-'] == True:
            producao = 1
        else:
            producao = 0

        if values['-faturamento-'] == True:
            faturameno = 1
        else:
            faturameno = 0

        guia = [str(values['-ordem_de_serviço-']), data_os, str(values['-f_pagamento-']), credenciais_muby[3], procedimentos]
        # (numeroOs, dataOs, formaPagamento, loja, pcp, producao, faturamento)
        metodos.insertDadosTabela("dbguias.db", "guias", f" '{str(values['-ordem_de_serviço-'])}', '{data_os}', '{str(values['-f_pagamento-'])}', '{str(credenciais_muby[3])}', {pcp}, {producao}, {faturameno}")
        guias.append(guia)
        atualizar_campo = f"{values['-os_adicionadas-']}\n{values['-ordem_de_serviço-']} - {values['-f_pagamento-']} || PCP: {procedimentos[0]} - PRODU: {procedimentos[1]} - FATUR: {procedimentos[2]}"
        window['-os_adicionadas-'].update(atualizar_campo)
        print(f"Guia adicionada: {str(guia[0])} - Forma de pagamento: {str(guia[2])}")
    
    if event == '-iniciar-':
        print("-----------------------------------\nProcesso inciado! - Aguarde um momento...\n-----------------------------------")
        resultado = None
        if resultado != False:
            while resultado != False:
                os_falas = []
                guias_erro_exibir = ""
                with sync_playwright() as p:
                    browser = headless_inicial(headless_set)
                    page = browser.new_page()
                    try:
                        realizar_login(credenciais_muby[1], credenciais_muby[2]) 
                        print("---Login realizado com sucesso!---")
                        a = 0
                        concluido = 0
                        for guia in guias:
                                falhou = 0
                                processos = guia[4]
                                print('----------------------------------')
                                if processos[0] == True:
                                    try:
                                        realizar_pcp(guia)
                                        print("PCP OK - Os: "+str(guia[0]))
                                    except:
                                        guias_erro_exibir = f"{guias_erro_exibir}{guia[0]} - PCP Falhou!\n"
                                        p = [True, False, True]
                                        guia[4] = p
                                        falhou = 1
                                        """tem_processos = processos
                                        tem_processos[0] = True
                                        guia[4] = tem_processos"""
                                        #guias_erro_repetir.append(guia)
                                        print("PCP Falhou! - Os: "+str(guia[0]))
                                if processos[1] == True:
                                    try:
                                        b = realizar_producao(a)
                                        a = b
                                        print("Produção OK - Os: "+str(guia[0]))
                                    except:
                                        #guias_erro_exibir = f"{guias_erro_exibir}{guia[0]} - Produção Falhou!\n"
                                        print("Produção Falhou!!! - Os: "+str(guia[0]))
                                if processos[2] == True:
                                    try:
                                        realizar_faturamento(guia)
                                        print("Faturamento OK - Os: "+str(guia[0]))
                                    except:
                                        guias_erro_exibir = f"{guias_erro_exibir}{guia[0]} - Faturamento Falhou!\n"
                                        p = [True, False, True]
                                        guia[4] = p
                                        falhou = 1
                                        """tem_processos = processos
                                        tem_processos[0] = True
                                        guia[4] = tem_processos"""
                                        #guias_erro_repetir.append(guia)
                                        print("Faturamento Falhou!!! - Os: "+str(guia[0]))
                                if falhou == 1:
                                    os_falas.append(guia)
                                    falhou = 0
                                    concluido = 1
                                elif falhou == 0:
                                    concluido = 0
                                print('----------------------------------')
                        if concluido == 0:
                            window['-os_adicionadas-'].update('-------------------------------------------Ordens de serviço adicionadas-------------------------------------------')
                            window['-ordem_de_serviço-'].update('')
                            window['-f_pagamento-'].update('A DEFINIR')
                            guias = []
                            resultado = False
                            page.wait_for_timeout(5000)
                            browser.close()
                            sg.popup("Tarefas Efetuadas com sucesso!")
                            print("Tarefas Efetuadas com sucesso!")
                        if concluido == 1:
                            # Filtrar erro posteriormente de uma entrada errada
                            e = sg.popup_get_text(f"As seguintes ordens de serviço são foram finalizadas corretamente: \n{guias_erro_exibir}\n\n Deseja tentar novamente?\nS - PARA SIM | N - PARA NÃO")
                            escolha = str(e).upper()
                            if escolha == "S":
                                resultado = os_falas
                            elif escolha == "N":
                                print("------------------Processos finalizados------------------")
                                window['-os_adicionadas-'].update('-------------------------------------------Ordens de serviço adicionadas-------------------------------------------')
                                window['-ordem_de_serviço-'].update('')
                                window['-f_pagamento-'].update('A DEFINIR')
                                guias = []
                                resultado = False
                    except Exception as err:
                        sg.popup("----Login Falhou!---- ;(\n Verifique sua conexão com a internet ou contate o suporte/desenvolvedor do programa, ou seja, Adriel! :)")
                        print("Login falhou!! Programa Encerrado!!")
                        print(err)
                        page.wait_for_timeout(5000)
                        browser.close()
        
            
    if event == '-limpar_dados_os-':
        window['-os_adicionadas-'].update('-------------------------------------------Ordens de serviço adicionadas-------------------------------------------')
        window['-ordem_de_serviço-'].update('')
        window['-f_pagamento-'].update('A DEFINIR')
        guias = []
        metodos.limparDadosBanco("dbguias.db", "guias")
        print("Dados do servidor limpos com sucesso!")
        sg.popup("Dados limpos com sucesso!")

    if event == '-consultar-':

        data = values['-data_relatorio-']

        os.system('python modulo_muby.py')
        """data = values['-data_relatorio-']

        plotagem = 0
        imagem = 0
        if values['-plotagem-'] == True:
            plotagem = 1
        if values['-imagem-'] == True:
            imagem = 1
        else:
            pass
        relatorios = (plotagem, imagem)
        # realizar_relatorio_muby(str(data), "SJ", relatorios)
        with sync_playwright() as p:
            browser = headless_inicial(headless_set)
            page = browser.new_page()
            try:
                realizar_login(credenciais_muby[1], credenciais_muby[2])
                print("---Login realizado com sucesso!---")
                try:
                    realizar_relatorio_muby(str(data), credenciais_muby[3], relatorios)
                except Exception as err:
                    print(err)
            except:
                pass
            page.wait_for_timeout(5000)
            browser.close()
            browser.close()"""

    
    if event == '-confirmar-':
        cliente = values['-nome_cliente-']
        email_cliente = values['-email_cliente-']
        num_os = values['-n_os-']
        documento = values['-cpf_cnpj-']
        f_pagamento = values['-forma_de_pagamento-']
        data_os = values['-data_os-']
        valor_os = float(str(values['-valor_os-']).replace(",", "."))
        metragem = str("%.4f" %(valor_os/14.60))
        valor_os = str("%.2f" %(valor_os)).replace(".", ",")

        tipo_doc_clienter = ""
        if values['-tipo_doc_cpf-'] == True:
            tipo_doc_clienter = "CPF"
        elif values['-tipo_doc_cnpj-'] == True:
            tipo_doc_clienter = "CNPJ"
        else:
            tipo_doc_clienter = "DOCUMENTO: "
            sg.popup("Tipo de documento do cliente não selecionado!\nSelecione e aplique novamente.")

        titulo_email = f"NOTA FISCAL - {cliente}"
        
        corpo_de_email = f"Boa Tarde, Luciana\n\n\nSegue abaixo dados para emissão de Nota Fiscal.\n\n{cliente}\n{tipo_doc_clienter}: {documento}\nEMAIL : {email_cliente}\nFORMA DE PAGAMENTO : {f_pagamento}\nSEGUE ABAIXO DESCRIÇÃO DOS SERVIÇOS\n\nOS : {num_os} DATA: {data_os}\nPlotagem em Papel Sulfite 75g Modelo: Color Linhas\nVALOR METRO: R$ 14,60\nMETRAGEM: {metragem}\nVALOR : R$ {valor_os}\n\nVALOR TOTAL: R$ {valor_os}\n\nGrato,\n\n{credenciais_muby[1]},\nEquipe São José\n"

        email = (titulo_email, corpo_de_email)

        window['-corpo_de_email-'].update(corpo_de_email)
        window['-titulo_email-'].update(titulo_email)
        sg.popup("Corpo de Email gerado!\nVerifique se o corpo de email está correto antes do envio!")
    

    if event == '-limpar_email-':
        elementos_email_limpar = ['-corpo_de_email-', '-nome_cliente-', '-email_cliente-', '-n_os-', '-cpf_cnpj-', '-forma_de_pagamento-', '-data_os-', '-valor_os-']
        for i in elementos_email_limpar:
            window[i].update("")
        window['-tipo_doc_cpf-'].update(False)
        window['-tipo_doc_cnpj-'].update(False)
        window['-titulo_email-'].update("NOTA FISCAL - ")
        
        sg.popup("Todos os dados foram limpos!")

    if event == '-enviar_email-':
        dados_login_email = (credenciais_email[0], credenciais_email[1])
        titulo = email[0]
        mensagem = values['-corpo_de_email-']
        email = (titulo, mensagem)
        try:
            metodos.enviar_email(dados_login_email, email, "financeiro@birocroqui.com.br")
            email = ("", "")
            sg.popup("Email enviado com sucesso ao financeiro!")

            window['-corpo_de_email-'].update("")
            elementos_email_limpar = ['-corpo_de_email-', '-nome_cliente-', '-email_cliente-', '-n_os-', '-cpf_cnpj-', '-forma_de_pagamento-', '-data_os-', '-valor_os-']
            for i in elementos_email_limpar:
                window[i].update("")
            window['-tipo_doc_cpf-'].update(False)
            window['-tipo_doc_cnpj-'].update(False)
            window['-titulo_email-'].update("NOTA FISCAL - ")
            
            sg.popup("Todos os dados foram limpos!")
        except:
            sg.popup("Houve algum erro ao enviar o email!")

    if event == '-emitir_recibo_manual-':
        try:
            dados_recibo = {'cliente': values['-cliente_recibo-'], 'valor': values['-valor_recibo-'], 'referente': values['-referente_recibo-'], 'funcionario': values['-funcionario_recibo-']}
            metodos.gerar_recibo(dados_recibo)
            sg.popup("Recibo gerado com sucesso!")
            window['-cliente_recibo-'].update("")
            window['-valor_recibo-'].update("")
            window['-referente_recibo-'].update("")
            window['-funcionario_recibo-'].update("")

        except Exception as err:
            sg.popup("Houve um erro ao gerar o recibo")
            print(err)


    if event == '-salvar_cliente-':
        try:
            new_cliente = [values['-nome_cliente_cad-'], values['-telefone-'], values['-email_cliente_cad-'], values['-documento_cliente-']]
            #metodos.salvar_dados(f"clientes_cadastrados/{new_cliente[0].upper()}.txt", new_cliente)
            metodos.salvar_cliente(new_cliente)
            window['-nome_cliente_cad-'].update("")
            window['-telefone-'].update("")
            window['-email_cliente_cad-'].update("")
            window['-documento_cliente-'].update("")
            sg.popup("Dados do cliente salvos com sucesso!")      
        except Exception as errodado:
            sg.popup("Houve algo de errado no salvamento!")
            print(errodado)
    if event == '-Limpar_campos_clientes_cad-':
        window['-nome_cliente_cad-'].update("")
        window['-telefone-'].update("")
        window['-email_cliente_cad-'].update("")
        window['-documento_cliente-'].update("")
        sg.popup("Dados limpos com sucesso!")
        
    if event == '-configs-':
        os.system("python configs.py")
    if event == '-sobre-':
        sg.popup("Aplicação desenvolvida por @adri3lr00 ;p\n\nBibliotecas Utilizadas:\n- PySimpleGui(4.56.0)\n- Playwright(1.21)\n- openpyxl()")

window.close()


