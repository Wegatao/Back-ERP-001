import mysql.connector
from mysql.connector import Error

# Classe que gerencia a conexão e operações com o banco de dados
class GerenciadorCooperados:
       def _init_(self, config):
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
                    Matricula VACHAR(20) PRYMARY KEY,
                    nome VARCHAR(20) NOT NULL,
                )
            """)
            conexao.commit()
            conexao.close()
            
    def criar_tabela_Pedencia(self):
        conexao = self.conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PSS (
                    IdPedencias INT AUTO_INCREMENT PRIMARY KEY,
                    Matricula VARCHAR(20),
                    TipoPendencia VARCHAR(100),
                    SatatusPendecia VARCHAR(20),
                    DataTyme DATE,
                    Descricao VARCHAR(100),
                    FOREIGN KEY(Matricula) REFERENCES PSS(Matricula)
                )
            """)
            conexao.commit()
            conexao.close()

    # Cadastra um novo cooperado no banco de dados
    def cadastrar_cooperado(self, Matricula, nome):
        conexao = self.conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO cooperados (Matricula, nome) VALUES (%s, %s)",
                (Matricula, nome)
            )
            conexao.commit()
            conexao.close()

    # Busca cooperados pelo nome
    def buscar_cooperados(self, nome):
        conexao = self.conectar()
        cooperados = []
        if conexao:
            cursor = conexao.cursor(dictionary=True)
            cursor.execute("SELECT * FROM cooperados WHERE nome LIKE %s", (f"%{nome}%",))
            cooperados = cursor.fetchall()
            conexao.close()
        return cooperados

    # Atualiza dados de um cooperado
    def atualizar_cooperado(self, id_cooperado, pendencias, data_emissao, observacao):
        conexao = self.conectar()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute(
                "UPDATE cooperados SET pendencias = %s, data_emissao = %s, observacao = %s WHERE id = %s",
                (pendencias, data_emissao, observacao, id_cooperado)
            )
            conexao.commit()
            conexao.close()
