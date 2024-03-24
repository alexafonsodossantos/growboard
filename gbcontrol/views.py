from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData
import json
from datetime import timedelta
from django.views.generic import TemplateView


@csrf_exempt
def sensor_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Converter tempo total em segundos
            total_time = timedelta(weeks=int(data['tempo_total']['semanas']), 
                                   days=int(data['tempo_total']['dias']), 
                                   hours=int(data['tempo_total']['horas']), 
                                   minutes=int(data['tempo_total']['minutos']), 
                                   seconds=int(data['tempo_total']['segundos'])).total_seconds()
            SensorData.objects.create(
                temperatura=data['temperatura'],
                umidade=data['umidade'],
                lampada=data['lampada'],
                tempo_ciclo=data['tempo_ciclo'],
                tempo_total=total_time
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    elif request.method == 'GET':
        medicoes = list(SensorData.objects.all().order_by('-data_hora')[:100].values())
        return JsonResponse(medicoes, safe=False)


class IndexView(TemplateView):
    template_name = 'index.html'  # Caminho para o template HTML
