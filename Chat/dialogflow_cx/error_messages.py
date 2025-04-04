"""
Esse arquivo deve conter todos as mensagens fixas de erros no bot.
Dessa forma é possível centralizar todas as mensagens, se precisarmos trocar uma delas, basta alterar aqui.
Essas são mensagens que serão exibidas para o usuário final.
"""
#from .dialogflow_cx_features import DialogflowCXFeatures

class ErrorMessages:
    """
    Classe principal, essas mensagens devem ser destinadas aos usuários,
    serem fáceis de entender e amigáveis, não sendo necessário entrar
    nos detalhes dos erros.
    """
    @staticmethod
    def dialogflow_cx_error() -> list:
        """Função com a mensagem padrão de erro para as integrações com o Dialogflow.

        Returns:
            String: Uma string com a mensagem de erro.
        """
        return "" #DialogflowCXFeatures().fulfillment_message("Desculpe, não vou conseguir te responder agora. Por favor, tente novamente mais tarde.", ['Menu'])