import PySimpleGUI as sg
import sqlite3

sg.theme('Reddit')

dados_login = None #(Usuario, senha, loja)
dados_email = None #(email, senha)
psswrd_char_m = "*"
psswrd_char_e = "*"

# =======================CONEXÃO E CARREGAMENTO DO BANCO DE DADOS======================
banco = sqlite3.connect('database.db')
cursor = banco.cursor()

try:
    cursor.execute("SELECT * FROM loginUsuario")
    dados_login = cursor.fetchall()[0]
    cursor.execute("SELECT * FROM loginEmail")
    dados_email = cursor.fetchall()[0]
    banco.close()
except sqlite3.Error as erro:
    sg.popup("Algo deu errado ao tentar carregar os dados do BANCO DE DADOS!\nTente preencher os campos de configuração e clicar em -Salvar Alterações-.")
    print(erro)
    banco.close()

def carregar_dados():
    banco = sqlite3.connect('database.db')
    cursor = banco.cursor()

    try:
        cursor.execute("SELECT * FROM loginUsuario")
        dados_login = cursor.fetchall()[0]
        cursor.execute("SELECT * FROM loginEmail")
        dados_email = cursor.fetchall()[0]
        banco.close()
    except sqlite3.Error as erro:
        sg.popup("Algo deu errado ao tentar carregar os dados do BANCO DE DADOS!\nTente preencher os campos de configuração e clicar em -Salvar Alterações-.")
        print(erro)
        banco.close()
# =====================================================================================
def atualizar_campos():
    #atualizar os valores dos campos na interface grafica
    try:
        window['-usuario_muby-'].update(dados_login[0])
        window['-senha_muby-'].update(dados_login[1])
        window['-loja_usuario-'].update(dados_login[2])
        window['-usuario_email-'].update(dados_email[0])
        window['-senha_email-'].update(dados_email[1])
    except:
        pass
def salvar_dados():
    banco = sqlite3.connect('database.db')
    cursor = banco.cursor()
    try:
        cursor.execute(f"UPDATE loginUsuario set usuario = '{values['-usuario_muby-']}' WHERE usuario = '{dados_login[0]}' ")
        cursor.execute(f"UPDATE loginUsuario set senha = '{values['-senha_muby-']}' WHERE senha = '{dados_login[1]}' ")
        cursor.execute(f"UPDATE loginUsuario set loja = '{values['-loja_usuario-']}' WHERE loja = '{dados_login[2]}' ")
        cursor.execute(f"UPDATE loginEmail set email = '{values['-usuario_email-']}' WHERE email = '{dados_email[0]}' ")
        cursor.execute(f"UPDATE loginEmail set senha = '{values['-senha_email-']}' WHERE senha = '{dados_email[1]}' ")
        banco.close()
        sg.popup("Dados salvos com sucesso!")
        carregar_dados()
        atualizar_campos()
    except sqlite3.Error as erro:
        sg.popup("Algo deu errado ao tentar salvar os dados no BANCO DE DADOS!")
        print(erro)
        banco.close()
#================================= FRAME LOGIN MUBY ====================================
coluna_fcl_1 = [
    [sg.Text('Usuario:')],
    [sg.Text('Senha:')],
    [sg.Text('Loja:')]
]
coluna_fcl_2 = [
    [sg.InputText('', key=('-usuario_muby-'), size=(25,1))],
    [sg.InputText('', key=('-senha_muby-'), size=(25,1), password_char=(psswrd_char_m))],
    [sg.Combo(("SJ", "TR", "ZS"), default_value=("SJ"), key=('-loja_usuario-'), size=(23, 1))]
]
coluna_fcl_3 = [
    [sg.Text('')],
    [sg.Button('Ver', key=('-ver_pw_muby-'))],
    [sg.Text('')]
]

frame_config_login =[
    [sg.Column(coluna_fcl_1), sg.Column(coluna_fcl_2), sg.Column(coluna_fcl_3)]
]

#========================================================================================
#================================= FRAME LOGIN EMAIL =====================================
coluna_fce_1 = [
    [sg.Text('Email:  ')],
    [sg.Text('Senha:')]
]
coluna_fce_2 = [
    [sg.InputText('', key=('-usuario_email-'), size=(25,1))],
    [sg.InputText('', key=('-senha_email-'), size=(25,1), password_char=(psswrd_char_e))]
]
coluna_fce_3 = [
    [sg.Text('')],
    [sg.Button('Ver', key=('-ver_pw_email-'))]
]

frame_config_email =[
    [sg.Column(coluna_fce_1), sg.Column(coluna_fce_2), sg.Column(coluna_fce_3)]
]

#========================================================================================
#=============================== FRAME CAMINHOS DE ARQUIVOS =============================
coluna_fca_1 = [
    [sg.Text('Banco de Dados:')],
    [sg.Text('Recibos Manual')],
    [sg.Text('Cadastros Rapidos:')]
]
coluna_fca_2 = [
    [sg.InputText('', key=('-path_banco_dados-'), size=(25,1))],
    [sg.InputText('', key=('-recibos_manual-'), size=(25,1))],
    [sg.InputText('', key=('-cadastros_clientes_rapidos-'), size=(25,1))]
]
coluna_fca_3 = [
    [sg.Text("")]
]

frame_caminho_arquivos =[
    [sg.Column(coluna_fca_1), sg.Column(coluna_fca_2), sg.Column(coluna_fca_3)]
]

#========================================================================================
layout = [
    [sg.Frame('Configurações de Login - Muby', frame_config_login)],
    [sg.Frame('Configurações de Login - Email', frame_config_email)],
    [sg.Frame('Configurações de Caminhos', frame_caminho_arquivos)],
    [sg.Text('Aviso: Clique em "Atualizar Informações" para baixar \nas informações do banco de dados')],
    [sg.Button("Atualizar Informações", key=('-atualizar_informacoes-'), size=(22, 1)), sg.Button("Savar Alterações", key=('-salvar_alteracoes-'), size=(22, 1))]
]

window = sg.Window('Configurações - AutoMuby', layout, icon='./assets/icon2.0.ico')



while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Close':
        break

    if event == '-salvar_alteracoes-':
        salvar_dados()

    if event == '-atualizar_informacoes-':
        atualizar_campos()

    if event == '-ver_pw_muby-':
        if psswrd_char_m == "*":
            psswrd_char_m = None
            window['-senha_email-'].update(password_char=(None))
        else:
            psswrd_char_m = "*"
            window['-senha_email-'].update(password_char=("*"))


    if event == '-ver_pw_email-':
        if psswrd_char_e == "*":
            psswrd_char_e = None
        else:
            psswrd_char_e = "*"
    