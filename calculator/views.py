from django.shortcuts import render, redirect
from .forms import CalculationForm
from .models import Calculation

def _apply(op, a, b):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        return a / b
    raise ValueError("Unknown operator")

def index(request):
    """
    Shows a form for 3 numbers + operator.
    On POST: computes ((n1 op n2) op n3), stores the record, and redirects to show it.
    Also lists recent calculations and lets you click one to refill the form.
    """
    # If user clicked a previous row, prefill the form from DB using ?id=
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

            # Compute left-to-right: ((n1 op n2) op n3)
            try:
                partial = _apply(op, n1, n2)
                result = _apply(op, partial, n3)
            except ZeroDivisionError:
                form.add_error(None, "Division by zero is not allowed.")
            else:
                calc = Calculation.objects.create(
                    number1=n1, number2=n2, number3=n3, operator=op, result=result
                )
                # Redirect so refresh doesn't resubmit; also highlights the new row
                return redirect(f"/?id={calc.id}")
    else:
        form = CalculationForm(initial=initial)

    recent = Calculation.objects.order_by("-created_at")[:10]
    return render(
        request,
        "calculator/index.html",
        {"form": form, "recent": recent, "selected": selected},
    )
