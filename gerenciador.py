import mysql.connector
from mysql.connector import Error
       
# Classe que gerencia a conexão e operações com o banco de dados
class GerenciadorCooperados:
       def __init__(self, config):
         self.config = config # Configuração do banco de dados
         
       
       # Conecta ao banco de dados
       def conectar(self):
         try:
            conexao = mysql.connector.connect(**self.config)
            if conexao.is_connected():
                print("Conexão bem-sucedida com o banco de dados.")
                return conexao
         except Error as e:
                print(f"Erro ao conectar no MySQL: {e}")
                return None
       
       # Cria a tabela "cooperados" se ela não existir
       def criar_tabela_PSS(self):
         conexao = self.conectar()
         if conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PSS (
                    Matricula VARCHAR(20) PRIMARY KEY,
                    nome VARCHAR(20) NOT NULL
                )
            """)
            conexao.commit()
            conexao.close()
     
       def criar_tabela_Pendencia(self):
        conexao = self.conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Pendencias (
                    IdPedencias INT AUTO_INCREMENT PRIMARY KEY,
                    Matricula VARCHAR(20),
                    TipoPendencia VARCHAR(100),
                    StatusPendecia VARCHAR(20),
                    Data date,
                    Descricao VARCHAR(100),
                    FOREIGN KEY(Matricula) REFERENCES PSS(Matricula)
                )""")
            conexao.commit()
            conexao.close()
       
       # Cadastra um novo cooperado no banco de dados
       def cadastrar_PSS(self, Matricula, nome):
        conexao = self.conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO PSS (Matricula, nome) VALUES (%s, %s)", (Matricula, nome)
            )
            conexao.commit()
            conexao.close()
           
       def cadastrar_pendencia(self, Matricula, TipoPendencia, StatusPendecia,Data, Descricao):
          conexao = self.conectar()
          if conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO Pendencias (Matricula, TipoPendencia, StatusPendecia,Data, Descricao)VALUES (%s, %s, %s, %s, %s)", 
            (Matricula,TipoPendencia, StatusPendecia,Data, Descricao)
            )
            conexao.commit()
            conexao.close()
                   
       # Busca cooperados pelo nome
       def buscar_cooperados(self, nome):
            conexao = self.conectar()
            cooperados = []
            if conexao:
              cursor = conexao.cursor(dictionary=True)
            cursor.execute("""
             SELECT
                    p.Matricula, p.nome, pe.TipoPendencia, pe.StatusPendecia, pe.Data, pe.Descricao
             FROM PSS p
              LEFT JOIN Pendencias pe ON p.Matricula = pe.Matricula
              WHERE p.nome LIKE %s
                 """, (f"%{nome}%",))
            cooperados = cursor.fetchall()
            conexao.close()
            return cooperados
       
       # Atualiza dados de um cooperado
       def atualizar_pendencia(self, matricula, status, descricao):
         conexao = self.conectar()
         if conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE Pendencias
                SET StatusPendencia = %s, Descricao = %s
                WHERE Matricula = %s
            """, (status, descricao, matricula))
            conexao.commit()
            conexao.close()
