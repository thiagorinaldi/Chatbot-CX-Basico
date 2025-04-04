import os
from .dialogflow_cx_model import DialogflowCXModel

def initialize_dialogflow_cx(session_id: str) -> DialogflowCXModel:
    """
    Função para instanciar os parâmetros do Dialogflow CX.

    Args:
        session_id (str): ID da sessão.

    Returns:
        DialogflowCXModel: configuração do modelo do Dialogflow CX.
    """
    try:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("DFCX_CREDENTIALS_PATH")

        dialogflow_model = DialogflowCXModel(
            os.getenv("DFCX_PROJECT_ID"),
            os.getenv("DFCX_LOCATION"),
            os.getenv("DFCX_LANGUAGE_CODE"),
            os.getenv("DFCX_AGENT_ID"),
            session_id
        )

        return dialogflow_model

    except Exception as e:
        #TbErrorLog(message = str(e), method = f"{__name__}.initialize_dialogflow", session_id = channel_name).save()

        return DialogflowCXModel()