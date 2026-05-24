from django.shortcuts import render, redirect
from .forms import StudentForm
import requests

ODOO_API = "http://localhost:8069"


# -------------------------
# LISTAR
# -------------------------
def student_list(request):

    identification = request.GET.get(
        'identification',
        ''
    )

    students = []

    try:

        response = requests.get(
            f"{ODOO_API}/api/tcu/students",
            params={
                'identification': identification
            }
        )

        data = response.json()

        students = data.get('data', [])

    except Exception as e:

        print("Error Odoo:", e)

    return render(
        request,
        'students/list.html',
        {
            'students': students,
            'identification': identification
        }
    )


# -------------------------
# CREAR
# -------------------------
def create_student(request):

    message = None
    periods = []
    # =========================
    # CARGAR PERIODOS
    # =========================
    try:

        period_response = requests.get(
            f"{ODOO_API}/api/tcu/periods"
        )
        period_data = period_response.json()

        periods = period_data.get('data', [])
    except Exception as e:
        print("Error cargando periodos:", e)
    # =========================
    # CREAR ESTUDIANTE
    # =========================
    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():

            json_data = {
                "name": form.cleaned_data["name"],
                "identification": form.cleaned_data["identification"],
                "student_card": form.cleaned_data["student_card"],
                "email": form.cleaned_data["email"],
                "phone": form.cleaned_data["phone"],
                "tcu_place": form.cleaned_data["tcu_place"],
                "manager_name": form.cleaned_data["manager_name"],
                "observations": form.cleaned_data["observations"],
                "year": form.cleaned_data["year"],
                "period_id": request.POST.get("period_id"),
                "status": "review"
            }

            try:

                response = requests.post(
                    f"{ODOO_API}/api/tcu/student",
                    json=json_data
                )

                data = response.json()

                

                if data.get('success'):
                    return redirect('student_list')

                message = data.get(
                    'message',
                    'Error creando estudiante'
                )
            except Exception as e:
                message = str(e)

    else:
        form = StudentForm()

    return render(
        request,
        'students/create.html',
        {
            'form': form,
            'message': message,
            'periods': periods
        }
    )


# -------------------------
# EDITAR ESTADO
# -------------------------
def edit_status(request, student_id):

    STATUS_CHOICES = [
        ("review", "En revisión"),
        ("pending", "Pendiente"),
        ("rejected", "Rechazado"),
        ("approved", "Aprobado"),
    ]

    message = None

    if request.method == "POST":

        status = request.POST.get("status")
        observations = request.POST.get("observations")

        payload = {
            "jsonrpc": "2.0",
            "params": {
                "id": student_id,
                "status": status,
                "observations": observations
            }
        }

        try:

            response = requests.post(
                f"{ODOO_API}/api/tcu/student/status",
                json=payload,
                headers={
                    "Content-Type": "application/json"
                }
            )

            print(response.text)

            data = response.json()

            result = data.get("result", {})

            if result.get("success"):
                return redirect("student_list")

            message = result.get("message")

        except Exception as e:
            message = str(e)

    return render(request, "students/edit_status.html", {
        "student_id": student_id,
        "statuses": STATUS_CHOICES,
        "message": message
    })