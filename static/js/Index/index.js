document.getElementById("form-buscar").addEventListener("submit", async function(event) {
    event.preventDefault();

    const nome = document.getElementById("section-container-painel-busca-input").value;

    // Verifica se o nome foi preenchido
    if (nome.trim() === "") {
        alert("Por favor, insira o nome do cooperado.");
        return;
    }


    // Fazendo a requisição POST para buscar os cooperados
    if(nome){
        document.querySelector('#Carregamento').style.display = 'block';
    }

    await fetch(`https://backend-do-erp-001.onrender.com/buscar`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "nome": nome })
    })
    .then( async response =>
    { 
        if(!response.ok)
        {
            const error = Error(response.status);
            throw new Error(`Erro na resposta:${error} `);                   
        } 
                return response.json();
    })
    
    .then(data => {
     console.log('ok')
     
     const tabelaCooperados = document.getElementById("tabela-cooperados").querySelector('tbody');
     tabelaCooperados.innerHTML = "";

        if (data.cooperados && data.cooperados.length === 0) {

            // Alteração: Dinamicamente define o colspan para alinhar com a tabela
            tabelaCooperados.innerHTML = `<tr><td colspan="${tabelaCooperados.parentElement.querySelectorAll('th').length}">Nenhum cooperado encontrado.</td></tr>`;
          } else {

            data.cooperados.forEach(cooperado => {
                const row = document.createElement("tr");
                const dataFormatada = formatarData(cooperado.data_emissao);
                const tamNomeObservação= TamNomPendcia(cooperado.observacao);

                console.log(data)
                        row.innerHTML = `
                            <td>${cooperado.nome}</td>
                            <td>${tamNomeObservação}</td>
                            <td>${dataFormatada}</td>
                            <td>${cooperado.pendencias}</td>
                            <button class="Mais-btn" data-id="${cooperado.id}" 
                                                     data-Obes="${cooperado.observacao}
                                                     data-nome="${cooperado.nome}"
                                                     data-data="${dataFormatada}"
                                                     data-pedencia="${cooperado.pendencias}"
                            >+</button>
                        `;


                        tabelaCooperados.appendChild(row);

                         if(data)
                        {
                            document.querySelector('#Carregamento').style.display = 'none';
                        }
                    })

                    
                    adicionarEventosAtualizar();
                    
                    }})
                              
        .catch(error => {
        console.error("Erro ao buscar cooperados:", error);
    });
});


function adicionarEventosAtualizar() 
{
        const BotoesEvento = document.querySelectorAll(".Mais-btn");
        

        BotoesEvento.forEach(botao =>{
            botao.addEventListener("click",()=>{

                //Pegando Elementos.
                const Tela = document.querySelector("#Contéudo-exibição");
                const Data = Tela.getElementsByTagName("p")[0];
                const Obs = Tela.getElementsByTagName("p")[1];
                const status = Tela.getElementsByTagName("p")[2]; 
                const ID = botao.getAttribute('data-id');
                const Nome = botao.getAttribute('data-nome');
                const observacao = botao.getAttribute('data-Obes');
                const pendencias = botao.getAttribute('data-pedencia');
                
                //Exibindo tela.
                Tela.style.display = "block";


                console.log(ID);
                console.log(Nome);
                console.log(observacao);
                console.log(pendencias);

            })
        })

        //document.getElementById("Contéudo-exibição").style.display = "block"
     
        
}

function TamNomPendcia(i){

    let textoInicial  = i;
    let textoNova = textoInicial.substring(0, 15);
    return `${textoNova} ...`
}

function formatarData(dataEmissao) {
    // Verifica se a data está no formato esperado (YYYY-MM-DD)
    if (!dataEmissao) return "Data inválida";

    if (dataEmissao.includes("/")) {

         // Divide a string em partes: [YYYY, MM, DD]
         const partes =  dataEmissao.split("/");
         if (partes.length !== 3) return "Data inválida";
         const dia = partes[0];
         const mes = partes[1];
         const ano = partes[2];
         // Retorna a data no formato DD/MM/YYYY
         return `${dia}/${mes}/${ano}`;


    } else if (dataEmissao.includes("-")) {

         const partes =  dataEmissao.split("-");
         if (partes.length !== 3) return "Data inválida";
         const ano = partes[0];
         const mes = partes[1];
         const dia = partes[2];
         // Retorna a data no formato DD/MM/YYYY
         return `${dia}/${mes}/${ano}`;

    } 
    else 
    {
        return "O formato da data é inválido";
    }
}



// Exemplo de uso
const dataOriginal = "2024-12-23"; // Exemplo do formato bruto
const dataFormatada = formatarData(dataOriginal);
console.log(dataFormatada); // "23/12/2024"

