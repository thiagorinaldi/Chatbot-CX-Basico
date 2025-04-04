from google.cloud import dialogflowcx_v3
from google.api_core.exceptions import InvalidArgument
from .config import initialize_dialogflow_cx
from .error_messages import ErrorMessages

class DialogflowCXIntegration:
    def __init__(self, session_id: str) -> None:
        """
        Inicializa a integração com o Dialogflow CX.

        Args:
            session_id (str): ID da sessão.
        """
        self.session_id = session_id
        self.dialogflow_cx_model = initialize_dialogflow_cx(session_id)
        self.client = dialogflowcx_v3.SessionsClient()

    def detect_intent(self, text: str) -> dict:
        """
        Detecta a intenção de uma mensagem de texto usando Dialogflow CX.

        Args:
            text (str): Mensagem de texto a ser analisada.

        Returns:
            dict: Mensagens de resposta do Dialogflow CX.
        """
        try:
            session_path = f"projects/{self.dialogflow_cx_model.project_id}/locations/{self.dialogflow_cx_model.location}/agents/{self.dialogflow_cx_model.agent_id}/sessions/{self.session_id}"

            text_input = dialogflowcx_v3.TextInput(text = text)

            query_input = dialogflowcx_v3.QueryInput(text = text_input, language_code = self.dialogflow_cx_model.language_code)

            detect_intent_request = dialogflowcx_v3.DetectIntentRequest(
                session = session_path,
                query_input = query_input
            )

            response = self.client.detect_intent(request = detect_intent_request)

            # Convertendo a resposta para dicionário
            # Isso é necessário porque a resposta original é um objeto protobuf
            response = dialogflowcx_v3.DetectIntentResponse.to_dict(response)

            intent_name = response['query_result']['intent']['display_name']
            intent_confidence = response['query_result']['intent_detection_confidence']
            fulfillment_messages = response['query_result']['response_messages']
            #fulfillment = ["".join(msg.text.text) for msg in response.query_result.response_messages]

            return dict(code = 200, message = "Detect intent successfully", result = dict(intent_name = intent_name, intent_confidence = intent_confidence, fulfillment_messages = fulfillment_messages))

        except InvalidArgument as e:
            print(f"Error: {e}")

            return dict(code = 400, message = "Invalid argument", result = None)

        except Exception as e:
            print(f"Unexpected error: {e}")

            return dict(code = 500, message = ErrorMessages().dialogflow_cx_error(), result = None)