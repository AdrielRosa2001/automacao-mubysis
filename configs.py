import PySimpleGUI as sg
import sqlite3
from pathlib import Path

sg.theme('Reddit')

dados_login, dados_email, path_recibos_mu, path_recibos_ma, path_cadastros_clientes = None, None, None, None, None #(id, usuario, senha, loja), (email, senha)


# =======================CONEXÃO E CARREGAMENTO DO BANCO DE DADOS======================
def getCredenciaisBanco():
    banco = sqlite3.connect('database.db')
    cursor = banco.cursor()

    try:
        cursor.execute("SELECT * FROM loginUsuario")
        dados_login = cursor.fetchall()[0]
        cursor.execute("SELECT * FROM loginEmail")
        dados_email = cursor.fetchall()[0]
        banco.close()
        saida = (dados_login, dados_email)
        return saida
    except sqlite3.Error as erro:
        sg.popup("Algo deu errado ao tentar carregar os dados do BANCO DE DADOS!\nTente preencher os campos de configuração e clicar em -Salvar Alterações-.")
        print(erro)
        banco.close()
        return False

dados_recuperados_credenciais = getCredenciaisBanco()
try:
    dados_login = dados_recuperados_credenciais[0]
    dados_email = dados_recuperados_credenciais[1]
except:
    pass

def getPathFilesBanco():
    banco = sqlite3.connect('database.db')
    cursor = banco.cursor()

    try:
        cursor.execute("SELECT * FROM pathFiles")
        path_files_banco = cursor.fetchall()[0]
        banco.close()
        return path_files_banco
    except sqlite3.Error as erro:
        sg.popup("Algo deu errado ao tentar carregar os caminhos dos diretorios no BANCO DE DADOS!\nTente preencher os campos de configuração e clicar em -Salvar Alterações-.")
        print(erro)
        banco.close()
# =====================================================================================
dados_recuperados_path = getPathFilesBanco()
try:
    path_recibos_mu, path_recibos_ma, path_cadastros_clientes = dados_recuperados_path[0], dados_recuperados_path[1], dados_recuperados_path[2]
except:
    path_files = Path(f'configs.py').absolute()
    path_files = (str(path_files).replace("\configs.py", "")).replace("\\", "/")
    path_recibos_mu, path_recibos_ma, path_cadastros_clientes = path_files+"/recibos/", path_files+"/recibos/", path_files+"/clientes_cadastrados/"

print(path_recibos_mu)
print(path_recibos_ma)
print(path_cadastros_clientes)

def salvar_dados():
    usuario_m = values['-usuario_muby-']
    senha_m = values['-senha_muby-']
    loja_m = values['-loja_usuario-']
    usuario_e = values['-usuario_email-']
    senha_e = values['-senha_email-']
    path_r_muby = values['-path_r_muby-']
    path_r_manual = values['-path_r_manual-']
    path_clientes_m = values['-path_clientes_m-'] 

    sg.popup("-- NOVOS DADOS --\n", usuario_m, senha_m, loja_m, usuario_e, senha_e, path_r_muby, path_r_manual, path_clientes_m)
    banco = sqlite3.connect('database.db')
    cursor = banco.cursor()
    try:
        cursor.execute(f"UPDATE loginUsuario set usuario = '{usuario_m}' WHERE id = 1 ")
        cursor.execute(f"UPDATE loginUsuario set senha = '{senha_m}' WHERE id = 1 ")
        cursor.execute(f"UPDATE loginUsuario set loja = '{loja_m}' WHERE id = 1 ")
        cursor.execute(f"UPDATE loginEmail set email = '{usuario_e}' WHERE email = '{dados_email[0]}' ")
        cursor.execute(f"UPDATE loginEmail set senha = '{senha_e}' WHERE senha = '{dados_email[1]}' ")
        cursor.execute(f"UPDATE pathFiles set pathRmuby = '{path_r_muby}' WHERE pathRmuby = '{path_recibos_mu}' ")
        cursor.execute(f"UPDATE pathFiles set pathRmanual = '{path_r_manual}' WHERE pathRmanual = '{path_recibos_ma}' ")
        cursor.execute(f"UPDATE pathFiles set pathClientesM = '{path_clientes_m}' WHERE pathClientesM = '{path_cadastros_clientes}' ")
        
        banco.commit()
        banco.close()
        sg.popup("Dados salvos com sucesso!")
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
try:
    coluna_fcl_2 = [
        [sg.InputText(f'{dados_login[1]}', key=('-usuario_muby-'), size=(25,1))],
        [sg.InputText(f'{dados_login[2]}', key=('-senha_muby-'), size=(25,1), password_char=("*"))],
        [sg.Combo(("SJ", "TR", "ZS"), default_value=(f"{dados_login[3]}"), key=('-loja_usuario-'), size=(23, 1))]
    ]
except:
    coluna_fcl_2 = [
        [sg.InputText('', key=('-usuario_muby-'), size=(25,1))],
        [sg.InputText('', key=('-senha_muby-'), size=(25,1), password_char=("*"))],
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
try:
    coluna_fce_2 = [
        [sg.InputText(f'{dados_email[0]}', key=('-usuario_email-'), size=(25,1))],
        [sg.InputText(f'{dados_email[1]}', key=('-senha_email-'), size=(25,1), password_char=("*"))]
    ]
    
except:
    coluna_fce_2 = [
        [sg.InputText('', key=('-usuario_email-'), size=(25,1))],
        [sg.InputText('', key=('-senha_email-'), size=(25,1), password_char=("*"))]
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
    [sg.Text('Recibos Muby:')],
    [sg.Text('Recibos Manual:')],
    [sg.Text('Cadastros Rapidos:')]
]
coluna_fca_2 = [
    [sg.In(size=(25,1), default_text=(f"{path_recibos_mu}"), enable_events=True ,key='-path_r_muby-'), sg.FolderBrowse()],
    [sg.In(size=(25,1), default_text=(f"{path_recibos_ma}"), enable_events=True ,key='-path_r_manual-'), sg.FolderBrowse()],
    [sg.In(size=(25,1), default_text=(f"{path_cadastros_clientes}"), enable_events=True ,key='-path_clientes_m-'), sg.FolderBrowse()]
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
    [sg.Button("Savar Alterações", key=('-salvar_alteracoes-'), size=(44, 1))]
]

window = sg.Window('Configurações - AutoMuby', layout, icon='./assets/icon2.0.ico')



while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Close':
        break

    if event == '-salvar_alteracoes-':
        salvar_dados()

    if event == '-ver_pw_muby-':
        sg.popup("SENHA:", values['-senha_muby-'])

    if event == '-ver_pw_email-':
        sg.popup("SENHA:", values['-senha_email-'])
    