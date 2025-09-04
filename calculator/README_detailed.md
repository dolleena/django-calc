# Django Calculator App

This is a step-by-step project built on **Windows 11** using
**Django**.\
It lets you input 3 numbers, select an operator (+, -, ×, ÷), compute
the result, save it in the database, view recent results, **delete any
entry**, and also use the Django Admin panel to manage calculations.

------------------------------------------------------------------------

## Requirements

-   Windows 11
-   Python 3.13+ (installed from python.org with "Add to PATH" checked)
-   pip (comes with Python)
-   (Optional but recommended) Visual Studio Code

------------------------------------------------------------------------

## Setup Instructions

### 1. Verify Python and pip

``` powershell
python --version
pip --version
```

Expected output:

    Python 3.13.x
    pip 25.x from ... (python 3.13)

------------------------------------------------------------------------

### 2. Create project folder & virtual environment

``` powershell
mkdir $HOME\projects\django-calc
cd $HOME\projects\django-calc

python -m venv .venv
```

**Allow PowerShell scripts (one-time for your user):**

``` powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Activate the venv:**

``` powershell
.\.venv\Scripts\Activate.ps1
```

Upgrade pip and install Django:

``` powershell
python -m pip install --upgrade pip setuptools wheel
pip install Django
python -m django --version
```

------------------------------------------------------------------------

### 3. Create the Django project

``` powershell
django-admin startproject calcsite .
```

Folder tree:

    django-calc/
    │   manage.py
    │
    └── calcsite/
        ├── __init__.py
        ├── settings.py
        ├── urls.py
        ├── asgi.py
        └── wsgi.py

------------------------------------------------------------------------

### 4. Create the app & register it

``` powershell
python manage.py startapp calculator
```

Edit `calcsite/settings.py` → add `'calculator'` to `INSTALLED_APPS`.

Folder tree now:

    django-calc/
    │   manage.py
    │
    ├── calcsite/
    │   └── ...
    │
    └── calculator/
        ├── admin.py
        ├── apps.py
        ├── migrations/
        │   └── __init__.py
        ├── models.py
        └── views.py

------------------------------------------------------------------------

### 5. Create the model

`calculator/models.py`

``` python
from django.db import models

class Calculation(models.Model):
    number1 = models.FloatField()
    number2 = models.FloatField()
    number3 = models.FloatField()
    operator = models.CharField(max_length=10)
    result = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.number1} {self.operator} {self.number2} {self.operator} {self.number3} = {self.result}"
```

Apply migrations:

``` powershell
python manage.py makemigrations
python manage.py migrate
```

------------------------------------------------------------------------

### 6. Create the form

`calculator/forms.py`

``` python
from django import forms

class CalculationForm(forms.Form):
    number1 = forms.FloatField(label="Number 1")
    number2 = forms.FloatField(label="Number 2")
    number3 = forms.FloatField(label="Number 3")
    OP_CHOICES = [('+','Add (+)'),('-','Subtract (-)'),('*','Multiply (×)'),('/','Divide (÷)')]
    operator = forms.ChoiceField(choices=OP_CHOICES, label="Operator")

    def clean(self):
        cleaned = super().clean()
        op = cleaned.get('operator')
        n2 = cleaned.get('number2')
        n3 = cleaned.get('number3')
        if op == '/' and ((n2 == 0) or (n3 == 0)):
            raise forms.ValidationError("Division by zero is not allowed.")
        return cleaned
```

------------------------------------------------------------------------

### 7. Views & URLs

`calculator/views.py`

``` python
from django.shortcuts import render, redirect
from .forms import CalculationForm
from .models import Calculation
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest

def _apply(op, a, b):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a / b
    raise ValueError("Unknown operator")

def index(request):
    initial = None
    selected = None
    rec_id = request.GET.get("id")
    if rec_id:
        try:
            selected = Calculation.objects.get(pk=rec_id)
            initial = {
                "number1": selected.number1,
                "number2": selected.number2,
                "number3": selected.number3,
                "operator": selected.operator,
            }
        except Calculation.DoesNotExist:
            pass

    if request.method == "POST":
        form = CalculationForm(request.POST)
        if form.is_valid():
            n1 = form.cleaned_data["number1"]
            n2 = form.cleaned_data["number2"]
            n3 = form.cleaned_data["number3"]
            op = form.cleaned_data["operator"]
            try:
                partial = _apply(op, n1, n2)
                result = _apply(op, partial, n3)
            except ZeroDivisionError:
                form.add_error(None, "Division by zero is not allowed.")
            else:
                calc = Calculation.objects.create(
                    number1=n1, number2=n2, number3=n3, operator=op, result=result
                )
                return redirect(f"/?id={calc.id}")
    else:
        form = CalculationForm(initial=initial)

    recent = Calculation.objects.order_by("-created_at")[:10]
    return render(request, "calculator/index.html", {"form": form, "recent": recent, "selected": selected})

@require_POST
def delete_calculation(request, pk):
    try:
        Calculation.objects.get(pk=pk).delete()
    except Calculation.DoesNotExist:
        return HttpResponseBadRequest("Record not found.")
    return redirect("/")
```

`calculator/urls.py`

``` python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("delete/<int:pk>/", views.delete_calculation, name="delete_calc"),
]
```

`calcsite/urls.py`

``` python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("calculator.urls")),
]
```

------------------------------------------------------------------------

### 8. Template

Path: `calculator/templates/calculator/index.html`

``` html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Django Calculator</title>
  <style>
    body { font-family: Segoe UI, Arial, sans-serif; margin: 2rem; }
    form, table { max-width: 640px; }
    label { display: block; margin-top: .75rem; font-weight: 600; }
    input, select, button { padding: .5rem; font-size: 1rem; }
    .errors { background: #ffecec; border: 1px solid #f5c2c2; color: #b30000; padding: .75rem; margin-bottom: 1rem; }
    table { width: 100%; border-collapse: collapse; margin-top: 1.5rem; }
    th, td { border: 1px solid #ddd; padding: .5rem .6rem; text-align: left; }
    tr.highlight { background: #fff8d6; }
    .muted { color: #666; font-size: .9rem; }
  </style>
</head>
<body>
  <h1>Calculator</h1>

  {% if form.non_field_errors %}
  <div class="errors">
    {% for err in form.non_field_errors %}<div>{{ err }}</div>{% endfor %}
  </div>
  {% endif %}

  <form method="post" action="">
    {% csrf_token %}
    <label>Number 1</label>{{ form.number1 }}
    <label>Number 2</label>{{ form.number2 }}
    <label>Number 3</label>{{ form.number3 }}
    <label>Operator</label>{{ form.operator }}
    <div style="margin-top: 1rem;">
      <button type="submit">Compute & Save</button>
    </div>
  </form>

  <h2>Recent calculations</h2>
  <p class="muted">Click a row to refill the form with those values.</p>

  <table>
    <thead>
      <tr><th>When</th><th>Expression</th><th>Result</th><th>Actions</th></tr>
    </thead>
    <tbody>
      {% for c in recent %}
        <tr class="{% if selected and selected.id == c.id %}highlight{% endif %}">
          <td><a href="?id={{ c.id }}">{{ c.created_at|date:"Y-m-d H:i:s" }}</a></td>
          <td>{{ c.number1 }} {{ c.operator }} {{ c.number2 }} {{ c.operator }} {{ c.number3 }}</td>
          <td>{{ c.result }}</td>
          <td>
            <form method="post" action="{% url 'delete_calc' c.id %}" onsubmit="return confirm('Delete this entry?');">
              {% csrf_token %}
              <button type="submit">Delete</button>
            </form>
          </td>
        </tr>
      {% empty %}
        <tr><td colspan="4">No calculations yet.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</body>
</html>
```

------------------------------------------------------------------------

### 9. Run the server

``` powershell
python manage.py runserver
```

Visit <http://127.0.0.1:8000/>.\
- Enter 3 numbers + operator → Compute & Save\
- Recent table updates\
- Delete any row with its button

------------------------------------------------------------------------

### 10. Django Admin

`calculator/admin.py`

``` python
from django.contrib import admin
from .models import Calculation

@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ("id", "number1", "operator", "number2", "number3", "result", "created_at")
    list_filter = ("operator", "created_at")
    search_fields = ("number1", "number2", "number3", "result")
    ordering = ("-created_at",)
```

Create superuser:

``` powershell
python manage.py createsuperuser
```

Visit: <http://127.0.0.1:8000/admin/> → login → manage Calculations.

------------------------------------------------------------------------

## Common Pitfalls

-   **Activation error**: run

    ``` powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```

-   **Template not found**: path must be
    `calculator/templates/calculator/index.html`

-   **Entries not saving**: check `views.py` is calling
    `Calculation.objects.create(...)`

-   **Admin missing model**: confirm `@admin.register(Calculation)` is
    in `admin.py`.

------------------------------------------------------------------------

## Features

-   Input 3 numbers + operator
-   Compute result left-to-right
-   Save to DB (SQLite by default)
-   List 10 most recent entries
-   Delete entries from page
-   Django Admin for full CRUD

------------------------------------------------------------------------

Enjoy building 🚀
