class DialogflowCXUtils:
    """
    Classe utilitária para interagir com o Dialogflow CX e processar respostas.
    """
    def web_fulfillment_response(self, fulfillments: list) -> str:
        """
        Função que processa o retorno do Dialogflow CX para o WebChat.

        Args:
            fulfillments (list): Lista de respostas do Dialogflow.

        Returns:
            str: Resposta formatada para o WebChat.
        """
        fulfillment_text = str()

        for fulfillment in fulfillments:
            if 'text' in fulfillment:
                fulfillment_text += fulfillment['text']['text'][0] + "\n"

            elif 'payload' in fulfillment:
                for button in fulfillment['payload']['richContent'][0][0]['options']:
                    fulfillment_text += f'<button class="btn btn-warning" onclick="Button_Intent(\'{button["text"]}\')">{button["text"]}</button>'

                fulfillment_text += "\n"

        return fulfillment_text