import { Formulario } from "./IndexClass.js";
import {Alertas} from "./Alert.js"
const Msg = new Alertas(); // ✅ Correção 1: instanciado antes

class IndexAPI {
    constructor() {
        this.FormularioDaPagina = document.getElementById("form-buscar");
        this.carregamento = document.getElementById("Carregamento");
        this.tabela = document.getElementById("tabela-cooperados").querySelector("tbody");
        this.Botão = document.getElementById("Realiza_busca");
        this.FormularioDaPagina.addEventListener("submit", (event) => {
            event.preventDefault(); // Impede o envio do formulário
            this.BuscaCooperados();
        });
        this.Botão.addEventListener("click", (event)=>{
            event.preventDefault();
            this.BuscaCooperados();
        })
    }
 
      BuscaCooperados() {
        const Form = new Formulario();
        
        if (!Msg.VerificaCampos(Form.Nome)) return;
        this.carregamento.style.display = "block";

        fetch("https://backend-do-erp-001.onrender.com/buscar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 'nome': Form.Nome })

        })
       
        .then( async (response) =>
        { 
            if(!response.ok)
            {
                const error = Error(response.status);
                throw new Error(`Erro na resposta:${error} `);                   
            } 
                return response.json();
        })
        
        .then(data =>{
            this.tabela.innerHTML = ""; // Limpa a tabela antes de adicionar novos dados
            console.log('ok')
            console.log(data);
            console.log(data.cooperados.data_emissao);

            this.carregamento.style.display = "none"

            if (data.cooperados && data.cooperados.length === 0) {
                // Alteração: Dinamicamente define o colspan para alinhar com a tabela
                const colunas = this.tabela.parentElement.querySelectorAll("th").length;
                this.tabela.innerHTML = `<tr><td colspan="${colunas}">Nenhum cooperado encontrado.</td></tr>`;

            }
                    
            data.cooperados.forEach(coop => {
                // Verifica se o campo 'pendencias' existe e é um número   
                
                const linha = document.createElement("tr");
                const observacao = this.TruncarTexto(coop.observacao)
                linha.innerHTML = `
                    <td>${coop.nome}</td>
                    <td>${observacao}</td>
                     <td>${coop.data_emissao}</td>
                    <td>${coop.StatusPedencia}</td>
                <td>
                    <button class="Mais-btn"
                    data-id="${coop.id}"
                    data-nome="${coop.nome}"
                    data-observacao="${coop.observacao}"
                    data-data="${coop.data_emissao}"
                    data-StatusPedencia="${coop.StatusPedencia}"
                    data-Tipo="${coop.pendencias}">
                +
                </button>
            </td>
            `;

            this.tabela.appendChild(linha);
        });
                this.AdicionarEventosMais();
        })
        .catch(error => {
                     // Trata erros
                    console.error('Erro:', error);
        })
    }    

    AdicionarEventosMais() {
        const botoes = document.querySelectorAll(".Mais-btn");
        const painel = document.querySelector("#Contéudo-exibição");

        botoes.forEach((btn) => {

            btn.addEventListener("click", () => {

                const pTags_p = painel.querySelectorAll("p");
                const pTags_H = painel.querySelector("h2")
                pTags_H.textContent = btn.getAttribute("data-nome")
                pTags_p[0].textContent = btn.getAttribute("data-data");
                pTags_p[1].textContent = btn.getAttribute("data-observacao");
                pTags_p[2].textContent = btn.getAttribute("data-StatusPedencia");
                pTags_p[3].textContent = btn.getAttribute("data-Tipo");
                painel.style.display = "block";
            });

        painel.addEventListener('click', ()=>{
                painel.style.display = "none";
        })
            
        })};

    
    TruncarTexto(texto, max = 10) {
        if (!texto) 
            return "--";
        else
        return texto.length > max ? texto.substring(0, max) + "..." : texto;
    }

    FormatarData(dataEmissao) {
        if (!dataEmissao) return "Data inválida";

        try {
            const data = new Date(dataEmissao);
            const dia = String(data.getDate()).padStart(2, "0");
            const mes = String(data.getMonth() + 1).padStart(2, "0");
            const ano = data.getFullYear();
            return `${dia}/${mes}/${ano}`;
        } catch (e) {
            return "Data inválida";
        }
    }
}
new IndexAPI();
