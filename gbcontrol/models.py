from django.db import models

# Create your models here.

class SensorData(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    umidade = models.IntegerField()  # Pode ser de 0 a 100
    lampada = models.BooleanField(default=False)
    tempo_ciclo = models.TimeField()
    # Armazenaremos o tempo total em segundos, para facilidade.
    tempo_total = models.BigIntegerField()

    def __str__(self):
        return f"{self.data_hora} - Temp: {self.temperatura} Umidade: {self.umidade}%"
