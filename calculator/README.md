# Django Calculator App

This is a step-by-step project built on **Windows 11** using
**Django**.\
It lets you input 3 numbers, select an operator (+, -, ×, ÷), compute
the result, save it in the database, view recent results, and delete any
entry.\
It also includes a Django Admin panel to manage calculations.

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

Expected:

    Python 3.13.x
    pip 25.x from ... (python 3.13)

------------------------------------------------------------------------

### 2. Create project folder & virtual environment

``` powershell
mkdir $HOME\projects\django-calc
cd $HOME\projects\django-calc

python -m venv .venv
```

**Allow PowerShell scripts (one-time):**

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

`calculator/views.py` → index view (compute, save, list recent).\
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

Path: `calculator/templates/calculator/index.html`\
Contains HTML form and recent calculations table with Delete buttons.

------------------------------------------------------------------------

### 9. Run the server

``` powershell
python manage.py runserver
```

Open browser: <http://127.0.0.1:8000/>

------------------------------------------------------------------------

### 10. Django Admin

Register model in `calculator/admin.py`:

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

Create a superuser:

``` powershell
python manage.py createsuperuser
```

Access admin: <http://127.0.0.1:8000/admin/>

------------------------------------------------------------------------

## Common Pitfalls

-   **Activation error**: run

    ``` powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```

-   **Template not found**: ensure path is exactly
    `calculator/templates/calculator/index.html`

-   **No recent entries**: check `views.py` saves calculations
    correctly.

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
