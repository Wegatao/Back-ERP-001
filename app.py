from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS

from gerenciador import GerenciadorCooperados
from CadastrarPendencia import  CadastrarPendencia
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
    CadastrarPendencia_obj =  CadastrarPendencia(dados)
    Resultado = CadastrarPendencia_obj.CadastrarPendenciaMethod()
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
            "matricula": row["Matricula"],
            "nome": row["nome"],
            "tipo_pendencia": row["TipoPendencia"],
            "status_pendencia": row["StatusPendecia"],
            "data": row["Data"],
            "descricao": row["Descricao"]
        }
        for row in resultado
    ]
    return jsonify({"cooperados": cooperados})


# ---------- ROTA: Atualizar Dados ----------
@app.route("/atualizar", methods=["PUT"])
def atualizar():
    dados = request.get_json()
    matricula = dados.get("matricula")
    status = dados.get("status_pendencia")
    descricao = dados.get("descricao", "")

    if not matricula or not status:
        return jsonify({"sucesso": False, "mensagem": "Campos obrigatórios não informados."})

    gerenciador.atualizar_pendencia(matricula, status, descricao)

    return jsonify({"sucesso": True, "mensagem": "Pendência atualizada com sucesso"})


# ---------- INICIAR APLICAÇÃO ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True) 
