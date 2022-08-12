import PySimpleGUI as sg

def frame01():
    frame01 = [
        [sg.Multiline('-------------------------------------------Ordens de serviço adicionadas-------------------------------------------', key=('-os_adicionadas-'), size=(75,17), disabled=True)]
    ]
    return frame01

def tab1(frame01):
    tab1 = [ 
        [sg.Text('Ordem de Serviço:'), sg.InputText(key=('-ordem_de_serviço-'), size=(10, 1)), sg.Text('Forma de Pagamento:'), sg.InputCombo(('AMERICAN EXPRESS', 'DEPÓSITO BB - CROQUI', 'DEPÓSITO BNB - CROQUI', 'DINERS - CRÉDITO', 'DINERS - DÉBITO', 'ELO - CRÉDITO', 'ELO - DÉBITO', 'ESPÉCIE', 'HIPERCARD', 'MASTER CRÉDITO - CROQUI', 'MASTER DÉBITO - CROQUI', 'VISA CRÉDITO - CROQUI', 'VISA DÉBITO - CROQUI'), default_value='A DEFINIR', key=('-f_pagamento-'), size=(27,1))],
        [sg.Checkbox('PCP', key=('-pcp-'), default=True), sg.Checkbox('PRODUÇÃO', key=('-producao-') , default=True), sg.Checkbox('FATURAMENTO', key=('-faturamento-'), default=True), sg.Text('', size=(13,1)),  sg.Button('Limpar', key=('-limpar_dados_os-')),sg.Button('Adicionar', key=('-adicionar-'))],
        [sg.Frame('Ordens de Serviço & Logs do Sistema', frame01, font='Any 12')],
        [sg.Button('Iniciar', key=('-iniciar-'), size=(10, 1))]
    ]
    return tab1

def tab2():
    tab2 = [
        [sg.Text('--Area em desenvolvimento--')],
        [sg.Text('Insira a data (dd/mm/aaaa):'), sg.InputText('', key=('-data_relatorio-'), size=(12, 1)), sg.Button('Consultar', key=('-consultar-')), sg.Button('Limpar', key=('-limpar_data-'))],
        [sg.Text('Puxar relatorios de:') ,sg.Checkbox('PLOTAGEM', key=('-plotagem-'), default=True), sg.Checkbox('IMAGEM', key=('-imagem-'))]
    ]
    return tab2

def coluna01():
    coluna01 = [
        [sg.Text('Cliente: ')],
        [sg.Text('Email: ')],
        [sg.Text('OS:')]
    ]
    return coluna01

def coluna02():
    coluna02 = [
        [sg.InputText('', key=('-nome_cliente-'),size=(22, 1))],
        [sg.InputText('', key=('-email_cliente-'), size=(22,1))],
        [sg.InputText('', key=('-n_os-'), size=(22, 1))]
    ]
    return coluna02

def coluna03():
    coluna03 = [
        [sg.Checkbox('CPF', key=('-cpf-')), sg.Checkbox('CPNJ', key=('-cnpj-'))],
        [sg.Text('Forma de Pagto: ')],
        [sg.Text('Data da OS: ')]
    ]
    return coluna03

def coluna04():
    coluna04 = [
        [sg.InputText('', key=('-cpf_cnpj-'), size=(19, 1))],
        [sg.InputText('', key=('-forma_de_pagamento-'), size=(19,1))],
        [sg.InputText('', key=('-data_os-'), size=(19, 1))]
    ]
    return coluna04

def frame02(coluna01, coluna02, coluna03, coluna04):
    frame02 = [
        [sg.Column(coluna01), sg.Column(coluna02), sg.Column(coluna03), sg.Column(coluna04)],
        [sg.Text('', size=(30,1)), sg.Text('Valor da OS:               '), sg.InputText('', key=('-valor_os-'), size=(19,1))],
        [sg.Text('Titulo:    '), sg.InputText('NOTA FISCAL - ', key=('-titulo_email-')),sg.Button('Limpar', key=('-limpar_email-')) ,sg.Button('Confirmar', key=('-confirmar-'))]
    ]
    return frame02

def frame03():
    frame03 = [
        [sg.Multiline('', key=('-corpo_de_email-'),size=(74, 12))]
    ]
    return frame03

def tab3(frame02, frame03):
    tab3 = [
        [sg.Frame('Dados do cliente', frame02)],
        [sg.Frame('Corpo de Email', frame03)]
    ]
    return tab3

def tab4():
    tab4 = [
        [sg.Text('Cliente: '), sg.InputText('',key=('-cliente_recibo-'))],
        [sg.Text('Valor: '), sg.InputText('',key=('-valor_recibo-'))],
        [sg.Text('Valor por extenso'), sg.InputText('',key=('-valor_extenso_recibo-'))],
        [sg.Text('Referente: '), sg.InputText('',key=('-referente_recibo-'))],
        [sg.Text('Data: '), sg.InputText('',key=('-data_recibo-'))],
        [sg.Text('Funcionario: '), sg.InputText('',key=('-funcionario_recibo-'))],
        [sg.Button('Emitir Recibo', key=('-emitir_recibo'))]


    ]
    return tab4

def coluna05():
    coluna05 = [
        [sg.Text('Nome: ')],
        [sg.Text('Telefone: ')],
        [sg.Text('Email: ')],
        [sg.Text('CPF/CNPJ: ')],
    ]
    return coluna05

def coluna06():
    coluna06 = [
        [sg.InputText('', key=('-nome_cliente_cad-'))],
        [sg.InputText('', key=('-telefone-'))],
        [sg.InputText('', key=('-email_cliente_cad-'))],
        [sg.InputText('', key=('-documento_cliente-'))],
    ]
    return coluna06
def frame04(coluna05, coluna06):
    frame04 = [
        [sg.Column(coluna05), sg.Column(coluna06)],
        [sg.Text("                                                    "), sg.Button('Limpar campos', key=('-Limpar_campos_clientes_cad-')), sg.Button('Salvar cliente', key=('-salvar_cliente-'))]
    ]
    return frame04

def tab5(frame04):
    tab5 = [
        [sg.Frame('Cadastros rapido de clientes', frame04)]
    ]
    return tab5

def layout(tab1, tab2, tab3, tab4, tab5):
    layout = [
        [sg.Image("./assets/logo.png")],
        [sg.TabGroup([
            [sg.Tab('Faturamento', tab1)], 
            [sg.Tab('Relatorios', tab2)],
            [sg.Tab('Nota Fiscal', tab3)],
            [sg.Tab('Recibos', tab4)],
            [sg.Tab('Cadastros', tab5)]
            ])],
            [sg.Text('', size=(42,1)), sg.Button('Close'),sg.Button('Sobre', key=('-sobre-')), sg.Button('Headless = ON ', key=('-headless-'))]
        
    ] 
    return layout
