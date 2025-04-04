# from pydialogflow_fulfillment import DialogflowRequest
# from Chat.servicenow.servicenow_integration import ServiceNowEasyConnect
# from Chat.servicenow.servicenow_model import OpenIncidentEasyConnectModel
# from Chat.models import TbTicketLog, TbSurveyLog, TbErrorLog

class DialogflowCXFeatures():
    def get_incident(self, request, session_id: str) -> list:
        """
        Função que busca informações de um chamado no ServiceNow.

        Args:
            request (http request): Requisição HTTP recebida do Dialogflow.
            session_id (str): ID da sessão do usuário.

        Returns:
            list: Lista de resposta formatada.
        """
        try:
            dialog_request = DialogflowRequest(request)

            query_values = dialog_request.get_single_ouputcontext("awaiting_name")

            ticket = query_values["parameters"]["Ticket"].upper()
            username = query_values["parameters"]["UserLogin"].upper()

            response = ServiceNowEasyConnect().get_incident(ticket, username)

            if response['code'] == 200 and response['result'] != None:
                TbTicketLog(number = response['result']['number'], username = username, type = "GET_TICKET", short_description = response['result']['short_description'], session_id = session_id).save()

                return self.fulfillment_message(f"Encontrei estas informações para este chamado:\n\nTicket: {response['result']['number']}\nDescrição: {response['result']['short_description']}\nStatus: {response['result']['state']}\n\nPosso te ajudar em algo mais?", ['Sim', 'Não'])

            return dialog_request.request_data['queryResult']['fulfillmentMessages']

        except Exception as e:
            TbErrorLog(message = str(e), method = f"{__name__}.get_incident", session_id = session_id).save()
            return self.fulfillment_message("Desculpe, ocorreu um erro ao buscar as informações do chamado. Tente novamente mais tarde.", ['Menu'])

    def create_incident(self, request, session_id: str) -> list:
        """
        Função que cria um chamado no ServiceNow.

        Args:
            request (http request): Requisição HTTP recebida do Dialogflow.
            session_id (str): ID da sessão do usuário.

        Returns:
            list: Lista de resposta formatada.
        """
        try:
            dialog_request = DialogflowRequest(request)

            query_values = dialog_request.get_single_ouputcontext("awaiting_name")

            impacted_application = "Laptop / Notebook"
            configuration_item = query_values["parameters"]["Hostname"]
            summary = "Bot - Abertura de incidente Teste"
            locality = query_values["parameters"]["Localidade"]
            telephone = query_values["parameters"]["Telefone"]
            description = query_values["parameters"]["Descricao"]
            assignment_group = "L_BRA_XXX_CLIENT_O365"
            username = query_values["parameters"]["UserLogin"].upper()
            priority = "3"

            #response = {'code': 201, 'result': {'display_value': 'INC0000001'}}
            response = ServiceNowEasyConnect().open_incident(OpenIncidentEasyConnectModel(impacted_application, configuration_item, summary, f"Localidade: {locality}\nTelefone: {telephone}\nDescrição: {description}", assignment_group, username, priority))

            if response.get('result', {}).get('display_value'):
                TbTicketLog(number = response['result']['display_value'], username = username, type = "OPEN_TICKET", impacted_application = impacted_application, configuration_item = configuration_item, short_description = summary, description = description, assignment_group = assignment_group, session_id = session_id).save()

                return self.fulfillment_message(f"Chamado criado com sucesso!\n\nO número do chamado é {response['result']['display_value']}.\n\nPosso te ajudar em algo mais?", ['Sim', 'Não'])

            return dialog_request.request_data['queryResult']['fulfillmentMessages']

        except Exception as e:
            TbErrorLog(message = str(e), method = f"{__name__}.create_incident", session_id = session_id).save()

            return self.fulfillment_message("Desculpe, ocorreu um erro ao criar o chamado. Tente novamente mais tarde.", ['Menu'])

    def save_survey(self, request, session_id: str) -> list:
        """
        Função que salva a pesquisa de satisfação no banco de dados.

        Args:
            request (http request): Requisição HTTP recebida do Dialogflow.
            session_id (str): ID da sessão do usuário.

        Returns:
            list: Lista de resposta formatada.
        """
        try:
            dialog_request = DialogflowRequest(request)

            query_values = dialog_request.get_single_ouputcontext("awaiting_name")

            username = query_values["parameters"]["UserLogin"].upper()
            survey = int(query_values["parameters"]["Survey.original"])
            satisfaction_survey = query_values["parameters"]["Survey"]
            comment = query_values["parameters"]["Description"]
            intent = dialog_request.get_intent_displayName()

            TbSurveyLog(username = username, survey = survey, satisfaction_survey = satisfaction_survey, comment = comment, intent = intent, session_id = session_id).save()

            return dialog_request.request_data['queryResult']['fulfillmentMessages']

        except Exception as e:
            TbErrorLog(message = str(e), method = f"{__name__}.save_survey", session_id = session_id).save()

            return self.fulfillment_message("Desculpe, ocorreu um erro ao salvar a pesquisa de satisfação. Tente novamente mais tarde", ['Menu'])

    def fulfillment_message(self, message: str, buttons: list = None) -> list:
        """
        Função que formata a mensagem de retorno.

        Args:
            message (str): Mensagem de retorno.
            buttons (list, optional): Lista de botões. Defaults to None.

        Returns:
            list: Lista de respostas formatadas.
        """
        if buttons:
            return [dict(text = dict(text = [message])),dict(payload = dict(richContent = [[dict(options = [dict(text = button) for button in buttons])]]))]

        return [dict(text = dict(text = [message]))]