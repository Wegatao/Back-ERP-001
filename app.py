from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from gerenciador import GerenciadorCooperados
from CadastrarPendencia import CadastrarPendencia
from CadastrarPessoa import CadastrarPessoa
from config import CONFING
import os

app = Flask(__name__)
CORS(app)

gerenciador = GerenciadorCooperados(CONFING)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensagem": "Backend do ERP está online!"})
    
@app.route("/cadastrarPessoa", methods=["POST"])
def cadastrarPessoa():
    dados = request.get_json()
    resultado = CadastrarPessoa(dados).CadastraPessoaMethod()
    return jsonify(resultado), 200 if resultado.get("sucesso") else 400

@app.route("/cadastrarPendencia", methods=["POST"])
def cadastrarPendencia():
    dados = request.get_json()
    resultado = CadastrarPendencia(dados).CadastrarPendenciaMethod()
    return jsonify(resultado), 200 if resultado.get("sucesso") else 400


@app.route("/buscar", methods=["POST"])
def buscar():
    dados = request.get_json()
    print(dados)
    nome = dados.get("nome", "")  # ✅ Pega apenas o campo "nome" do dicionário
    print(f"Nome recebido para busca: {nome}")  # ✅ Log do nome recebido
    resultado = gerenciador.buscar_cooperados(nome)  # ✅ Agora sim: passa apenas a string "nome"

    cooperados = [
     {
        "IdPedencias": row["IdPedencias"],
        "id": row["Matricula"],
        "nome": row["nome"],
        "TipoPendencia": row["TipoPendencia"],     # renomeado
        "StatusPendecia": row["StatusPendecia"],
        "observacao": row["Descricao"],         # renomeado
        "data_emissao": row["Data"]             # renomeado
     }
        for row in resultado
    ]
    return jsonify({"cooperados": cooperados})



@app.route("/atualizar", methods=["PUT"])
def atualizar():
    dados = request.get_json();
    IdPendencia = dados.get("IdPedencias");# Matricula usada como ID
    PessoaAutorizada = dados.get("PessoaAutorizada");
    AssinaturaCooperado = dados.get("AssinaturaCooperado");

    if not PessoaAutorizada or not AssinaturaCooperado :
        return jsonify({"sucesso": False, "mensagem": "Campos obrigatórios não informados."})

    gerenciador.atualizar_pendencia(IdPendencia, PessoaAutorizada, AssinaturaCooperado);
    
    return jsonify({"sucesso": True, "mensagem": "Pendência atualizada com sucesso"})


#Essa função ainda não estpa criada.
@app.route("/deletar", methods=["DELETE"]) 
def deletar():
    dados = request.get_json()
    matricula = dados.get("id")
    if not matricula:
        return jsonify({"sucesso": False, "mensagem": "Matricula não informada."})
    gerenciador.deletar_pendencia(matricula) 
    return jsonify({"sucesso": True, "mensagem": "Pendência deletada com sucesso"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


