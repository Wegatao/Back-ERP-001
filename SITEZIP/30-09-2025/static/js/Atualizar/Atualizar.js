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
            console.log(dados);
            this.mostrarNaTabela(dados.cooperados);
            //Parte do codigo que trata os erros de repostas.
        } catch (erro) {
            console.error("Erro na busca:", erro);
        }
    }
    // essa função apenas  "mostrarNaTabela(lista){ }" preenche as linhas da tabela. 
    mostrarNaTabela(lista) {
        this.tabela.innerHTML = ""; // Limpa a tabela antes

        lista.forEach(coop => {
            const linha = document.createElement("tr");

            linha.innerHTML = `
                <td>${coop.id}</td>
                <td>${coop.nome}</td>
                <td>${coop.StatusPedencia}</td>
                <td>${coop.observacao}</td>
                <td><button class="btn-atualizar" data-id="${coop.IdPedencias}">Atualizar</button></td>
            `;

           if(coop.StatusPedencia?.toUpperCase() === 'OK' && coop.pendencias?.toUpperCase() === 'OK'){
                linha.querySelector('.btn-atualizar').style.backgroundColor = 'blue';

                //Nessa linha de codigo, eu modifiquei pra poder pegar a linha do codigo que tem esse elemenot, pra não dar erro.
            } else {
                 linha.querySelector('.btn-atualizar').style.backgroundColor = 'red';  
            }
            //
            this.tabela.appendChild(linha);
            

        });

        this.atualizarCooperado()
        // Adiciona eventos nos botões
        //this.Verificação(lista);
       
   
    }

    async atualizarCooperado() {
        //const novoNome = prompt("Digite o novo nome do cooperado:");

        const botao = document.querySelectorAll(".btn-atualizar")

         botao.forEach((btn)=>{
            
                btn.addEventListener("click", async () => {  
                const PessoaAutorizada = prompt("Digite o status do Autorizado:");
                const AssinaturaCooperado = prompt("Digite o status do Cooperado:");                    
                const IdPedencias = btn.getAttribute("data-id")

            try {
                    const resposta =  await fetch("https://backend-do-erp-001.onrender.com/atualizar", {
                        method: "PUT",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ IdPedencias: IdPedencias, PessoaAutorizada: PessoaAutorizada, AssinaturaCooperado: AssinaturaCooperado })
                    });

                    console.log(IdPedencias,PessoaAutorizada, AssinaturaCooperado)
                    const dados =  await resposta.json();

                    alert(dados.mensagem);
                     this.buscarCooperado(new Event("submit"));
                    } catch (erro) {
                        console.error("Erro ao atualizar:", erro);
                    }
                });
        })
        // Atualiza a lista automaticamente  
    }
}

// Inicia a classe
new CooperadoAPI();
