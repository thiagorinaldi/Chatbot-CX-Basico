import secrets
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Chat.dialogflow_cx.dialogflow_cx_integration import DialogflowCXIntegration
from Chat.dialogflow_cx.dialogflow_cx_utils import DialogflowCXUtils

def chat(request: HttpResponse) -> HttpResponse:
    """
    Função que renderiza a página principal do chatbot.

    Args:
        request (HttpRequest): Requisição HTTP recebida.

    Returns:
        HttpResponse: Resposta HTTP com o conteúdo da página renderizada.
    """
    return render(request, 'chat/chat.html', {'token': secrets.token_urlsafe(15)})

@csrf_exempt
def web_inbound(request: HttpResponse) -> HttpResponse:
    """
    Função que renderiza a página de entrada do chatbot.

    Args:
        request (HttpRequest): Requisição HTTP recebida.

    Returns:
        HttpResponse: Resposta HTTP com o conteúdo da página renderizada.
    """
    session_id = request.POST.get("session")
    message = request.POST.get("data")

    dialogflow = DialogflowCXIntegration(session_id).detect_intent(message)

    # if len(message) > 256:
    #     dialogflow['fulfillment'] = DialogflowFeatures().fulfillment_message("Mensagem muito longa. Por favor, tente novamente com uma mensagem mais curta.")

    fulfillment = DialogflowCXUtils().web_fulfillment_response(dialogflow['result']['fulfillment_messages'])

    return HttpResponse(fulfillment)