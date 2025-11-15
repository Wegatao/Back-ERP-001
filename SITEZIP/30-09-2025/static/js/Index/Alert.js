
export class Alertas
{
    MostrarMensagem(mensagem) 
    {
        alert(mensagem);
    }

    VerificaCampos(valor) {
        if (!valor || valor.trim() === "") {
            this.MostrarMensagem("Por favor, preencha o campo de buscar");
            return false;
        }
        return true;
    }
}

  