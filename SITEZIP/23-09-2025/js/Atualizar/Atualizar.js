class CooperadoAPI {
    constructor() {
        this.inputNome = document.getElementById("buscar-nome");
        this.formBuscar = document.getElementById("form-buscar");
        this.tabela = document.getElementById("Tabela-apresentacao");

        // Evento para buscar
        this.formBuscar.addEventListener('submit', (e) => this.buscarCooperado(e));
    }

    async buscarCooperado(e) {
        e.preventDefault();
        const nome = this.inputNome.value.trim();

        if (!nome) {
            alert("Digite um nome para buscar");
            return;
        }

        try {
            const resposta = await fetch(`https://backend-do-erp-001.onrender.com/buscar`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 'nome': nome })
            });

            const dados = await resposta.json();
            console.log(dados)
            this.mostrarNaTabela(dados.cooperados);
            //Parte do codigo que trata os erros de repostas.
        } catch (erro) {
            console.error("Erro na busca:", erro);
        }
    }

    mostrarNaTabela(lista) {
        this.tabela.innerHTML = ""; // Limpa a tabela antes

        lista.forEach(coop => {
            const linha = document.createElement("tr");

            linha.innerHTML = `
                <td>${coop.id}</td>
                <td>${coop.nome}</td>
                <td>${coop.StatusPedencia}</td>
                <td>${coop.observacao}</td>
                <td><button class="btn-atualizar" data-id="${coop.id}">Atualizar</button></td>
            `;
            /*if(coop.pendencias == 'pedente' || coop.pendencias == 'PENDENTE'){
                document.querySelector('.btn-atualiza').style.backgroundColor = 'red';   
            }*/
            this.tabela.appendChild(linha);
            
        });
        // Adiciona eventos nos botões
        //this.Verificação(lista);

        document.querySelectorAll(".btn-atualizar").forEach(botao => {
            botao.addEventListener("click", (e) => this.atualizarCooperado(e.target.dataset.id));

        });
    }

    async atualizarCooperado(id) {
        //const novoNome = prompt("Digite o novo nome do cooperado:");
        const pendencias = prompt("digite os status pra pedencia:")


        try {
            const resposta = await fetch("https://backend-do-erp-001.onrender.com/atualizar", {

                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: id, status: pendencias})
            });

            const dados = await resposta.json();
            alert(dados.mensagem);

            // Atualiza a lista automaticamente
            this.buscarCooperado(new Event("submit"));
        } catch (erro) {
            console.error("Erro ao atualizar:", erro);
        }
    }
}

// Inicia a classe
new CooperadoAPI();
