from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData
import json
from datetime import timedelta
import cv2
from django.http import StreamingHttpResponse

def gen_frames():  
    camera = cv2.VideoCapture(0)  # Use 0 para a primeira webcam conectada
    while True:
        success, frame = camera.read()  
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Concatena os quadros do vídeo

def video_stream(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

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
