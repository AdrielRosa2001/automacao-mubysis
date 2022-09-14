from ast import Break, arguments
import PySimpleGUI as sg
import metodos
from playwright.sync_api import sync_playwright
import sys
import time

argumentos = sys.argv # --faturar / --testar

#headless_set = 'OFF'

def headless_inicial(argumentos): #--headless-on #--headless-off
    if argumentos[2] == '--headless-on':
        browser = p.chromium.launch()
        return browser
    elif argumentos[2] == '--headless-off':
        browser = p.chromium.launch(headless=False) # exibindo tela
        return browser

def realizar_login(usuario, senha):
    page.goto("https://mubisys.com/index.php?app")
    #page.wait_for_timeout(10000)
    page.fill("input[name='codigo']", '237157')
    page.fill("input[name='usuario']", usuario)
    page.fill("input[name='senha']", senha)
    page.click("ion-icon[name='arrow-forward']")
    page.wait_for_timeout(2000)

def acessar_pagina_pcp():
    page.goto("https://mubisys.com/index.php?modulo=Pcp")

def realizar_pcp(guia):
    #page.goto("https://mubisys.com/index.php?modulo=Pcp")
    page.fill("input[name='search']", guia[0])
    page.locator("[placeholder=\"Buscar\"]").press("Enter")
    page.wait_for_timeout(1000)
    page.click("a[title='Visualizar']")
    page.wait_for_timeout(1000)
    page.locator(".icofont-gear").click()
    page.wait_for_timeout(1000)
    page.locator("text=Finalizar Produção").click()

def realizar_producao(guia):
    page.fill("input[name='search']", guia[0])
    page.locator("[placeholder=\"Buscar\"]").press("Enter")
    page.wait_for_timeout(1000)
    page.click("a[title='Visualizar']")
    page.wait_for_timeout(1000)
    page.locator(".icofont-gear").click()
    page.wait_for_timeout(1000)
    page.locator("text=Baixa Completa").click()

def realizar_faturamento(guia):
    page.goto("https://mubisys.com/index.php?modulo=Faturamento")
    page.wait_for_timeout(4000)
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

def gerar_recibo_muby(guia, path_save):
    #page.wait_for_url("https://mubisys.com/index.php?modulo=Contasareceber")
    page.goto("https://mubisys.com/index.php?modulo=Contasareceber")
    page.wait_for_timeout(500)
    page.locator("#ativarfiltro").click()
    page.wait_for_timeout(500)
    page.locator("input[name=\"b_ordemdeservico\"]").fill(str(guia))
    page.wait_for_timeout(500)
    page.locator("button:has-text(\"Buscar\")").click()
    page.wait_for_timeout(500)
    page.locator(".inline > a > .icofont").first.click()
    page.wait_for_timeout(500)
    with page.expect_download() as download_info:
        with page.expect_popup() as popup_info:
            page.locator("text=Gerar recibo").click()
        page1 = popup_info.value
    download = download_info.value
    download.save_as(f"{path_save}/Recibo - {guia}.pdf")

#------------------------DEFINIÇÃO DE TEMA -----------------
sg.theme('Reddit')
#-----------------------------------------------------------
#--------------------- VARIAVEIS DA GUI ---------------------
procedimento_tipo = None

if argumentos[1] == "--faturar":
    procedimento_tipo = "Baixa e Faturamento"

elif argumentos[1] == "--recibo_m":
    procedimento_tipo = "Gerando Recibo pelo Muby"

elif argumentos[1] == "--testar":
    procedimento_tipo = "Testando Modulo"

layout = [
    [sg.Text('Aguarde um momeno\nRealizando o seguinte procedimentos:', size=(28, 2))],
    [sg.Text(procedimento_tipo, size=(28, 2), font=('Helvetica', 15), justification='center', key=('-tipo_procedimento-'))],
    [sg.Text(font=('Helvetica', 13), justification='center', key=('-text-'))]
]
#------------------------------------------------------------
#--------------------- VARIAVEIS ---------------------

database = metodos.getDadosLogin()
credenciais_muby = database[0]
paths_files = metodos.getPathFilesBanco()


controle_exibicao = ""
realizar_procedimentos = False

window = sg.Window('Modulo de automações - Muby', layout, icon='./assets/icon2.0.ico')

guias_old = None
guias = []
try:
    guias_old = metodos.getDadosDb("dbguias.db", "guias")
    print("-Ordens de serviços coletadas e carregadas.")
    for guia in guias_old:
        status = guia[7]
        if status == 'pendente':
            realizar_procedimentos = True
            guias.append(guia)
        else:
            pass
except:
    print("-Houve um erro ai tentar carregar as ordens de serviço do banco.")

#-----------------------------------------------------
if argumentos[1] == "--faturar":
    while True:
        event, values = window.read(timeout=1000)

        if event == sg.WIN_CLOSED or event == 'Close':
            break

        time.sleep(3)
        if realizar_procedimentos == True: 
            with sync_playwright() as p:
                browser = headless_inicial(argumentos)
                page = browser.new_page()
                try:
                    realizar_login(credenciais_muby[1], credenciais_muby[2])
                    print("--Login efetuado.")
                    try:
                        acessar_pagina_pcp()
                        print("----Acessando pagina PCP.")
                    except:
                        print("----Houve um erro ao tentar acessar a pagina PCP")
                    for guia in guias:
                        print("----------------------------------------")
                        controle_de_procedimentos = [guia[4], guia[5], guia[6]]
                        if guia[4] == 1 or guia[5] == 1:
                            acessar_pagina_pcp()
                            if guia[4] == 1:
                                try:
                                    realizar_pcp(guia)
                                    print(f"------{guia[0]} - PCP Realizado!")
                                    metodos.updateLinhaBanco("dbguias.db", "guias", "pcp", 0, "numeroOs", str(guia[0]))
                                    controle_de_procedimentos[0] = 0
                                except:
                                    print(f"------{guia[0]} - PCP FALHOU!")
                            if guia[5] == 1:
                                try:
                                    realizar_producao(guia)
                                    print(f"------{guia[0]} - Produção Realizado!")
                                    metodos.updateLinhaBanco("dbguias.db", "guias", "producao", 0, "numeroOs", str(guia[0]))
                                    controle_de_procedimentos[1] = 0
                                except:
                                    print(f"------{guia[0]} - Produção FALHOU!")
                        if guia[6] == 1:
                            try:
                                realizar_faturamento(guia)
                                print(f"------{guia[0]} - Faturamento Realizado!")
                                print("----------------------------------------")
                                metodos.updateLinhaBanco("dbguias.db", "guias", "faturamento", 0, "numeroOs", str(guia[0]))
                                controle_de_procedimentos[2] = 0
                            except:
                                print(f"------{guia[0]} - Faturamento FALHOU!")
                        
                        if controle_de_procedimentos[0] == 0 and controle_de_procedimentos[1] == 0 and controle_de_procedimentos[2] == 0:
                            metodos.updateLinhaBanco("dbguias.db", "guias", "status", "efetuado", "numeroOS", str(guia[0]))

                        print("----------------------------------------")
                except Exception as erro:
                    print("--Houve um erro ao tentar realizar o login!")
                    print("Erro: ", erro)

            sg.popup("* Procedimentos FINALIZADOS! *")
            metodos.deletLinhaBanco("dbguias.db", "guias", "status", "'efetuado'")
            print('*** Banco limpo com sucesso! ***')
            break
        else:
            print("-Nenhuma ordem de serviço no banco para dar baixa")
        
        if realizar_procedimentos == False: 
            sg.popup("-Nenhuma ordem de serviço no banco para realizar faturamento.-")
            break

elif argumentos[1] == "--recibo_m":
    while True:
        event, values = window.read(timeout=1000)
    
        
        with sync_playwright() as p:
            browser = headless_inicial(argumentos)
            page = browser.new_page()
            try:
                realizar_login(credenciais_muby[1], credenciais_muby[2])
                print("--Login efetuado.")
                try:
                    gerar_recibo_muby(argumentos[3], paths_files[0])
                    print("----Recibo emitido com sucesso!")
                    break
                except Exception as erro:
                    print("----Houve um erro ao tentar emitir o recibo!")
                    print("Erro: ", erro)
                    break
            except Exception as erro:
                print("--Houve um erro ao tentar realizar o login!")
                print("Erro: ", erro)
                break


        if event == sg.WIN_CLOSED or event == 'Close':
            break

elif argumentos[1] == "--testar":
    while True:
        event, values = window.read()
        
        #window['-tipo_procedimento-'].update("Baixa e Faturamento: ")

        if event == sg.WIN_CLOSED or event == 'Close':
            break
        
