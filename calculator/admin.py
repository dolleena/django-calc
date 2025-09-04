from django.contrib import admin
from .models import Calculation

@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ("id", "number1", "operator", "number2", "number3", "result", "created_at")
    list_filter = ("operator", "created_at")
    search_fields = ("number1", "number2", "number3", "result")
    ordering = ("-created_at",)
