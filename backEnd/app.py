from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from gerenciador import GerenciadorCooperados
from config import CONFING  # Importa a configuração do banco de dados
import os

# Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app)  # Permite requisições de outros domínios (útil para frontend separado)


# Instancia a classe (objeto responsável pelas operações com o banco)
gerenciador = GerenciadorCooperados(CONFING)
# Rota para cadastrar um cooperado


@app.route("/cadastrarPessoa", methods=["POST"])
def cadastrarPessoa():
    dados = request.get_json()
    Matricula = request.get("Matricula")
    nome = dados.get("nome")
    
    
    # Valida e formata a data
    ''''if data_emissao:
        try:
            data_emissao = datetime.strptime(data_emissao, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            return jsonify({"sucesso": False, "mensagem": "Formato de data inválido. Use 'YYYY-MM-DD'."})'''

    # Verifica se os campos obrigatórios foram preenchidos
    if  not nome or not Matricula:
        return jsonify({"sucesso": False, "mensagem": "Todos os campos obrigatórios devem ser preenchidos."})

    # Chama a função da classe para cadastrar
    gerenciador.criar_tabela_PSS()  # Garante que a tabela existe antes de cadastrar
    gerenciador.cadastrar_cooperado(Matricula,nome)

    return jsonify({"sucesso": True, "mensagem": f"Cooperado {nome} cadastrado com sucesso!"})


@app.route("/cadastrarPedencia", methods=["POST"])
def cadastrarPendecia():
    dados = request.get_json()
    Matricula = request.get("Matricula")
    TipoPedencia = request.get("TipoPedencia")
    Status = request.get("Status")
    data = request.get("data")
    Descricao = request.get("Descricao")
        
    
    # Valida e formata a data
    if data_emissao:
        try:
            data_emissao = datetime.strptime(data_emissao, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            return jsonify({"sucesso": False, "mensagem": "Formato de data inválido. Use 'YYYY-MM-DD'."})

    # Verifica se os campos obrigatórios foram preenchidos
    if not Matricula or not TipoPedencia or not Status or not data or not Descricao:
        return jsonify({"sucesso": False, "mensagem": "Todos os campos obrigatórios devem ser preenchidos."})

    # Chama a função da classe para cadastrar
    gerenciador.criar_tabela_Pedencia()  # Garante que a tabela existe antes de cadastrar
    gerenciador.cadastrar_cooperado(Matricula,TipoPedencia, Status, data, Descricao)

    return jsonify({"sucesso": True, "mensagem": f"Pessoa da {Matricula} foi cadastrado com sucesso!"})


# Rota para buscar cooperados pelo nome
@app.route("/buscar", methods=["POST"])
def buscar():
    dados = request.get_json()
    nome = dados.get("nome", "")
    resultado = gerenciador.buscar_cooperados(nome)

    # Monta a resposta com os dados retornados
    cooperados = [
        {
            "id": row["id"],
            "nome": row["nome"],
            "pendencias": row["pendencias"],
            "data_emissao": row["data_emissao"],
            "observacao": row["observacao"]
        }
        for row in resultado
    ]
    return jsonify({"cooperados": cooperados})


# Rota para atualizar dados de um cooperado
@app.route("/atualizar", methods=["PUT"])
def atualizar():
    dados = request.get_json()
    id_cooperado = dados.get("id")
    pendencias = dados.get("pendencias")
    data_emissao = dados.get("data_emissao")
    observacao = dados.get("observacao", "")

    # Validação e formatação da data
    if data_emissao:
        try:
            data_emissao = datetime.strptime(data_emissao, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            return jsonify({"sucesso": False, "mensagem": "Formato de data inválido. Use 'YYYY-MM-DD'."})

    # Verificação de campos obrigatórios
    if not id_cooperado or not pendencias:
        return jsonify({"sucesso": False, "mensagem": "ID e pendências são obrigatórios."})

    # Chama a função da classe para atualizar
    gerenciador.atualizar_cooperado(id_cooperado, pendencias, data_emissao, observacao)

    return jsonify({"sucesso": True, "mensagem": "Status e observação atualizados com sucesso!"})


# Inicia a aplicação Flask
if __name__ == "_main_":
    port = int(os.environ.get("PORT", 5000))  # Suporte para plataformas como Render
    app.run(host="0.0.0.0", port=port)