from django.shortcuts import render
from django.http import HttpResponse
from Chat.dialogflow_cx.dialogflow_cx_integration import DialogflowCXIntegration
from Chat.dialogflow_cx.dialogflow_cx_utils import DialogflowCXUtils

def web_inbound(request):
    """
    Renderiza a página de entrada do chatbot.
    """
    #session_id = request.POST.get("session")
    #message = request.POST.get("data")

    dialogflow = DialogflowCXIntegration("1234567").detect_intent("Olá")

    # if len(message) > 256:
    #     dialogflow['fulfillment'] = DialogflowFeatures().fulfillment_message("Mensagem muito longa. Por favor, tente novamente com uma mensagem mais curta.")

    fulfillment = DialogflowCXUtils().web_fulfillment_response(dialogflow['result']['fulfillment_messages'])

    return HttpResponse(fulfillment)