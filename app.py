from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from gerenciador import GerenciadorCooperados
from config import CONFING
import os

# Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app)

# Instancia a classe responsável pelas operações com o banco
gerenciador = GerenciadorCooperados(CONFING)


# ---------- ROTA: Cadastrar Cooperado ----------
@app.route("/cadastrarPessoa", methods=["POST"])
def cadastrarPessoa():
    dados = request.get_json()
    Matricula = dados.get("Matricula")
    nome = dados.get("nome")

    if not Matricula or not nome:
        return jsonify({"sucesso": False, "mensagem": "Todos os campos obrigatórios devem ser preenchidos."})

    gerenciador.criar_tabela_PSS()
    gerenciador.cadastrar_cooperado(Matricula, nome)

    return jsonify({"sucesso": True, "mensagem": f"Cooperado {nome} cadastrado com sucesso!"})


# ---------- ROTA: Cadastrar Pendência ----------
@app.route("/cadastrarPendencia", methods=["POST"])
def cadastrarPendencia():
    dados = request.get_json()
    Matricula = dados.get("Matricula")
    TipoPendencia = dados.get("TipoPendencia")
    Status = dados.get("Status")
    data = dados.get("data")
    Descricao = dados.get("Descricao")

    if not Matricula or not TipoPendencia or not Status or not data or not Descricao:
        return jsonify({"sucesso": False, "mensagem": "Todos os campos obrigatórios devem ser preenchidos."})

    try:
        data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
    except ValueError:
        return jsonify({"sucesso": False, "mensagem": "Formato de data inválido. Use 'YYYY-MM-DD'."})

    gerenciador.criar_tabela_Pendencia()
    gerenciador.cadastrar_pendencia(Matricula, TipoPendencia, Status, data_formatada, Descricao)

    return jsonify({"sucesso": True, "mensagem": f"Pendência cadastrada com sucesso para a matrícula {Matricula}!"})


# ---------- ROTA: Buscar Cooperados ----------
@app.route("/buscar", methods=["POST"])
def buscar():
    dados = request.get_json()
    nome = dados.get("nome", "")
    resultado = gerenciador.buscar_cooperados(nome)

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


# ---------- ROTA: Atualizar Dados ----------
@app.route("/atualizar", methods=["PUT"])
def atualizar():
    dados = request.get_json()
    id_cooperado = dados.get("id")
    pendencias = dados.get("pendencias")
    data_emissao = dados.get("data_emissao")
    observacao = dados.get("observacao", "")

    if data_emissao:
        try:
            data_emissao = datetime.strptime(data_emissao, '%Y-%m-%d').strftime('%d/%m/%Y')
        except ValueError:
            return jsonify({"sucesso": False, "mensagem": "Formato de data inválido. Use 'YYYY-MM-DD'."})

    if not id_cooperado or not pendencias:
        return jsonify({"sucesso": False, "mensagem": "ID e pendências são obrigatórios."})

    gerenciador.atualizar_cooperado(id_cooperado, pendencias, data_emissao, observacao)

    return jsonify({"sucesso": True, "mensagem": "Status e observação atualizados com sucesso!"})


# ---------- INICIAR APLICAÇÃO ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True) 
