//class Cadastro API
export class Pessoa{
  constructor(){
    this.nome = document.getElementById("nome").value;
    this.Matricula = document.getElementById("Matricula").value;
    this.Mensagem = "Hellow World";
  }
}

// class PedenciasAPI 
export class Pedencias{
  constructor(){
    this.Matricula = document.getElementById("Matricula").value;
    this.StatusPendecia = document.getElementById("Status").value;
    this.TipoPendencia = document.getElementById("TipoPendencia").value;
    this.Data = this.TransformaData(document.getElementById("Data").value);
    this.Descricao = document.getElementById("descricao").value;
  }
  TransformaData(i){
    const DT = new Date(i)
    const Trans_Data = DT.toLocaleDateString('pt-BR', { timeZone: "UTC"})
    return Trans_Data;
  }

}
