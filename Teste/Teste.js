
class AtualizadorCooperado {
    constructor(formId) {
        this.formulario = document.getElementById(formId);
        this.init();
    }

    init() {
        this.adicionarEventos();
    }

    adicionarEventos() {
        const botoes = document.querySelectorAll(".Mais-btn");

        botoes.forEach(botao => {
            botao.addEventListener("click", () => this.abrirJanelaAtualizacao(botao));
        });
    }

    async abrirJanelaAtualizacao(botao) {
        const id = botao.dataset.id;
        const nome = botao.dataset.nome;
        const data = botao.dataset.data;
        const pendencia = botao.dataset.pendencia;
        const observacao = botao.dataset.obes;

        const novoStatus = prompt("Digite o novo status (F/V) para o cooperado:", pendencia);
        const novaObs = prompt("Digite a nova observação:, observacao");

        if (!novoStatus || (novoStatus !== "F" && novoStatus !== "V")) {
            alert("Status inválido! Use apenas 'F' ou 'V'.");
            return;
        }

        const dataAtual = this.getDataAtualFormatada();

        try {
            const resposta = await fetch("https://backend-do-erp-001.onrender.com/atualizar", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    id,
                    pendencias: novoStatus,
                    observacao: novaObs,
                    data_emissao: dataAtual
                })
            });

            const resultado = await resposta.json();

            alert(resultado.mensagem);

            // Atualiza a tabela se tudo deu certo
            if (resultado.sucesso && this.formulario) {
                this.formulario.dispatchEvent(new Event("submit"));
            }
        } catch (erro) {
            console.error("Erro ao atualizar:", erro);
            alert("Houve um erro na atualização.");
        }
    }

    getDataAtualFormatada() {
        const hoje = new Date();
        const ano = hoje.getFullYear();
        const mes = String(hoje.getMonth() + 1).padStart(2, '0');
        const dia = String(hoje.getDate()).padStart(2, '0');
        return `${ano}-${mes}-${dia}`;
    }
}

new AtualizadorCooperado();