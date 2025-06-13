from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from gerenciador import GerenciadorCooperados
from CadastrarPendencia import CadastrarPendencia
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
    try:
        dados = request.get_json()
        nome = dados.get("nome")
        Matricula = dados.get("Matricula")
        
        if not Matricula or not nome:
            return jsonify({"sucesso": False, "mensagem": "Todos os campos obrigatórios devem ser preenchidos."})
        
        gerenciador.criar_tabela_PSS()
        gerenciador.cadastrar_PSS(Matricula, nome)

        return jsonify({"sucesso": True, "mensagem": f"Cooperado {nome} cadastrado com sucesso!"})
    
    except Exception as e:
        print("Erro ao cadastrar pessoa:", e)
        return jsonify({"sucesso": False, "mensagem": f"Erro interno: {str(e)}"}),500


# ---------- ROTA: Cadastrar Pendência ----------
@app.route("/cadastrarPendencia", methods=["POST"])
def cadastrarPendencia():
    
    dados = request.get_json()
    CadastrarPendencia_obj = CadastrarPendencia(dados)
    Resultado = CadastrarPendencia_obj.cadastrar_pendencia()
    return jsonify(Resultado)

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
