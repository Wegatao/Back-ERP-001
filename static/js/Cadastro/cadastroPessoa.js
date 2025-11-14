import { Pessoa }from "./classCadastro.js";
// Classe para gerenciar o cadastro de cooperados

class CooperadoAPI {
  constructor() {
    this.botaoCadastrar = document.getElementById("btn-cadastrar");
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
    document.getElementById("nome").value = "";
    document.getElementById("Matricula").value = "";
  }

  // Método para cadastrar cooperado
  async cadastrarCooperado() {
    // Obter os valores dos campos do formulário
    const exportUsuario = new Pessoa();

    
    // Verificar se os campos obrigatórios estão preenchidos
    if (!exportUsuario.nome || !exportUsuario.Matricula){
      this.mostrarMensagem("Por favor, preencha todos os campos obrigatórios.", "erro");
      return;
    }

    // Exibir o carregamento se algum campo estiver preenchido
    if ( exportUsuario.nome || exportUsuario.Matricula) {
      this.carregamento.style.display = 'block';

      console.log(exportUsuario)
    }

    // Enviar os dados para a API
    try { 
       
      const response = await fetch("https://backend-do-erp-001.onrender.com/cadastrarPessoa", {
        method: "POST",  
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(exportUsuario),
      });
      
        // Log dos dados enviados para depuração
      console.log("Dados enviados:", exportUsuario.nome, exportUsuario.Matricula);

    
     // Verificar se a resposta foi bem-sucedida
      const data = await response.json();
      this.mostrarMensagem(data.mensagem, data.sucesso ? "sucesso" : "erro");

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