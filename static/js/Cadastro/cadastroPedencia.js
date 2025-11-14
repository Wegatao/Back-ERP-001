import { Pedencias } from "./classCadastro.js";

class CooperadoAPI {
  constructor() {
    this.botaoCadastrar = document.getElementById("btn-cadastrar-Pedencia");
    this.carregamento = document.querySelector('#Carregamento');
    // Vincular o método cadastrarCooperado ao evento do botão
    this.botaoCadastrar.addEventListener("click", () => this.cadastrarCooperado());
  }
  
  // Método para mostrar mensagens de status
  mostrarMensagem(mensagem) {

    alert(mensagem);
  }

  // Método para limpar os campos do formulário
  limpaCampos() {
    document.getElementById("Matricula").value = "";
    document.getElementById("Status").value = "";
    document.getElementById("TipoPendencia").value = "";
    document.getElementById("Data").value = "";
    document.getElementById("descricao").value = "";
  }

  // Método para cadastrar cooperado
  async cadastrarCooperado() {
    // Obter os valores dos campos do formulário
   
    const Pedencia = new Pedencias()

    // Verificar se os campos obrigatórios estão preenchidos
    if ( !Pedencia.Matricula || !Pedencia.StatusPendecia || !Pedencia.TipoPendencia || !Pedencia.Data) {
      this.mostrarMensagem("Por favor, preencha todos os campos obrigatórios.", "erro");
      return;
       
    }
    // Exibir o carregamento se algum campo estiver preenchido
    if ( Pedencia.Matricula || Pedencia.StatusPendecia || Pedencia.TipoPendencia || Pedencia.Data || Pedencia.Descricao) {
      this.carregamento.style.display = 'block';      
    }
    console.log("enviado para a API", JSON.stringify(Pedencia, null, 2));
     

    // Enviar os dados para a API
    try {
      const response = await fetch("https://backend-do-erp-001.onrender.com/cadastrarPendencia", {
          method: "POST",  
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(Pedencia),
      });

    
      // Verificar se a resposta foi bem-sucedida
      const data = await response.json();
      this.mostrarMensagem(data.mensagem, data.sucesso ? "sucesso" : "erro");
      console.log(data.Data);

    } catch (error) {
      console.error("Erro ao conectar com a API:", error);
      this.mostrarMensagem("Erro ao conectar com a API.", "erro");
    } finally {
      this.carregamento.style.display = 'none';
      this.limpaCampos();
    }
  }
}

// Instanciar a classe para ativar o comportamento
new CooperadoAPI();