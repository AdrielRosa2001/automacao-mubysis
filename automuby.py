"""from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from playwright.sync_api import sync_playwright
from importlib.resources import path
from logging import handlers
import py_compile"""
from time import sleep
from turtle import update
from playwright.sync_api import sync_playwright
from msilib.schema import Font, Icon
import PySimpleGUI as sg
import interface
import metodos
import os


guias = []


# Metodos playwrigth
headless_set = '--headless-on'


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


window = sg.Window('AutoMuby 5.0', layout, icon='./assets/icon2.0.ico')

# Abrindo configurações:
#database = metodos.coletar_dados("configs.txt", 0)
database = metodos.getDadosLogin()
credenciais_muby = database[0]
credenciais_email = database[1]

# var email
email = ["", ""]

while True:
    print("================================================================================")
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close': # if user closes window or clicks cancel
        break
    
    if event == '-headless-':
        if headless_set == '--headless-on':
            window['-headless-'].update('Headless: OFF')
            headless_set = '--headless-off'
        elif headless_set == '--headless-off':
            window['-headless-'].update('Headless: ON')
            headless_set = '--headless-on'
        pass

    if event == '-adicionar-':
        data_os = "hoje"

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

        
        # (numeroOs, dataOs, formaPagamento, loja, pcp, producao, faturamento, status)
        metodos.insertDadosTabela("dbguias.db", "guias", f" '{str(values['-ordem_de_serviço-'])}', '{data_os}', '{str(values['-f_pagamento-'])}', '{str(credenciais_muby[3])}', {pcp}, {producao}, {faturameno}, 'pendente' ")
        
        procedimentos = [values['-pcp-'], values['-producao-'], values['-faturamento-']]

        guia = [str(values['-ordem_de_serviço-']), data_os, str(values['-f_pagamento-']), credenciais_muby[3], procedimentos]
        print(f"Guia adicionada: {str(guia[0])} - Forma de pagamento: {str(guia[2])}")

        atualizar_campo = f"{values['-os_adicionadas-']}\n{values['-ordem_de_serviço-']} - {values['-f_pagamento-']} || PCP: {procedimentos[0]} - PRODU: {procedimentos[1]} - FATUR: {procedimentos[2]}"
        window['-os_adicionadas-'].update(atualizar_campo)
        
        
    
    if event == '-iniciar-':
        conferencia = metodos.getDadosDb("dbguias.db", "guias")
        if len(conferencia) != 0:
            print("-----------------------------------\nProcesso inciado! - Aguarde um momento...\n-----------------------------------")
            os.system(f'python modulo_muby.py --faturar {headless_set}')
            window['-os_adicionadas-'].update('-------------------------------------------Ordens de serviço adicionadas-------------------------------------------')
            window['-ordem_de_serviço-'].update('')
            window['-f_pagamento-'].update('A DEFINIR')
            conferencia = metodos.getDadosDb("dbguias.db", "guias")
            if len(conferencia) != 0:
                sg.popup('Possa ser que algumas ordens de serviço não tenham sido faturadas corretamente..\nSugiro que clique novamente em "Iniciar" no canto inferior esquerdo do programa')            
        else:
            sg.popup('Não existe nenhuma guia no banco de dados para dar baixa!')

            
            
    if event == '-limpar_dados_os-':
        window['-os_adicionadas-'].update('-------------------------------------------Ordens de serviço adicionadas-------------------------------------------')
        window['-ordem_de_serviço-'].update('')
        window['-f_pagamento-'].update('A DEFINIR')
        window['-pcp-'].update(True)
        window['-producao-'].update(True)
        window['-faturamento-'].update(True)
        guias = []
        metodos.limparDadosBanco("dbguias.db", "guias")
        sg.popup("Dados limpos com sucesso!")

    if event == '-consultar-':
        data = values['-data_relatorio-']

    
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

        email = [titulo_email, corpo_de_email]

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
        email = [titulo, mensagem]
        try:
            metodos.enviar_email(dados_login_email, email, "financeiro@birocroqui.com.br") 
            email = ["", ""]
            sg.popup("Email enviado com sucesso ao financeiro!")

            window['-corpo_de_email-'].update("")
            elementos_email_limpar = ['-corpo_de_email-', '-nome_cliente-', '-email_cliente-', '-n_os-', '-cpf_cnpj-', '-forma_de_pagamento-', '-data_os-', '-valor_os-']
            for i in elementos_email_limpar:
                window[i].update("")
            window['-tipo_doc_cpf-'].update(False)
            window['-tipo_doc_cnpj-'].update(False)
            window['-titulo_email-'].update("NOTA FISCAL - ")
            
            sg.popup("Todos os dados foram limpos!")
        except Exception as erro:
            sg.popup("Houve algum erro ao enviar o email!")
            print(f"Houve algum erro ao enviar o email!\n{erro}")

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

    if event == '-emitir_recibo_Muby-':
        try:
            guia_recibo = values['-os_recibo_muby-']
            os.system(f"python modulo_muby.py --recibo_m {headless_set} {guia_recibo}")
            window['-os_recibo_muby-'].update("")
        except:
            pass

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


