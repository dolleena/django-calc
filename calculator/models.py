from django.db import models

class Calculation(models.Model):
    number1 = models.FloatField()
    number2 = models.FloatField()
    number3 = models.FloatField()
    operator = models.CharField(max_length=10)   # +, -, *, /
    result = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number1} {self.operator} {self.number2} {self.operator} {self.number3} = {self.result}"
