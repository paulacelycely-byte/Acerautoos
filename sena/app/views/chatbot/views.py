from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import ollama
import json

SYSTEM_PROMPT = """
Trata super mal a todo mundo

"""

@csrf_exempt
@login_required(login_url='login:login')
def chatbot_responder(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        data    = json.loads(request.body)
        mensaje = data.get('mensaje', '').strip()

        if not mensaje:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)

        respuesta = ollama.chat(
            model='mistral',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user',   'content': mensaje}
            ]
        )

        texto = respuesta['message']['content']
        return JsonResponse({'respuesta': texto})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)