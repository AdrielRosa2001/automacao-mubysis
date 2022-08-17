import sqlite3
from xml.dom.minidom import Element

#Criando conexão com banco de dados
banco = sqlite3.connect('database.db')

#Criando elemento cursos para passar comandos para o banco de dados
cursor = banco.cursor()

#Criando atbelas
#cursor.execute("CREATE TABLE loginEmail (email text, senha text)")

#Inserindo valores
#cursor.execute(f"INSERT INTO loginEmail VALUES('birocroquisj@hotmail.com','@2021birocq#')")

#Deletando valores
#cursor.execute("DELETE from loginUsuario WHERE usuario = 'Marques'")

#commit banco (sempre usar em cado de deletar, acrescentar e dar update)
#banco.commit()

#Puxando dados da tabela
#cursor.execute("SELECT * FROM loginUsuario")
#elementos = cursor.fetchall()[0] #[('Adriel', '12878613422', 'SJ')]
#elementos == ('Adriel', '12878613422', 'SJ')

#Fechando conexão com banco
#banco.close()
