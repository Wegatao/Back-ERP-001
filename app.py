from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS

from gerenciador import GerenciadorCooperados
from CadastrarPendencia import CadastrarPendenciaMethod
from CadastrarPessoa import CadastrarPessoa
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
    CadastrarPessoa_obj = CadastrarPessoa(dados)
    Resultado = CadastrarPessoa_obj.CadastraPessoaMethod()
    if Resultado.get("sucesso"):
        return jsonify(Resultado) 
    else:
        return jsonify(Resultado), 400 
     

# ---------- ROTA: Cadastrar Pendência ----------
@app.route("/cadastrarPendencia", methods=["POST"])
def cadastrarPendencia():
    dados = request.get_json()
    CadastrarPendencia_obj = CadastrarPendenciaMethod(dados)
    Resultado = CadastrarPendencia_obj.cadastrar_pendencia()
    if Resultado.get("sucesso"):
        return jsonify(Resultado) 
    else:
        return jsonify(Resultado), 400 


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
