from django import forms
import re

STATUS_CHOICES = [
    ("review", "En revisión"),
    ("pending", "Pendiente"),
    ("rejected", "Rechazado"),
    ("approved", "Aprobado"),
]


class StudentForm(forms.Form):
    name = forms.CharField()
    identification = forms.CharField()
    student_card = forms.CharField()
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)

    tcu_place = forms.CharField(required=False)
    manager_name = forms.CharField(required=False)

    year = forms.CharField(required=False)
    observations = forms.CharField(widget=forms.Textarea, required=False)

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)

    def clean_identification(self):
        idv = self.cleaned_data["identification"]

        if len(idv) < 6:
            raise forms.ValidationError("La identificación es demasiado corta")

        if not idv.isdigit():
            raise forms.ValidationError("Debe contener solo números")

        return idv

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email:
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, email):
                raise forms.ValidationError("Email inválido")

        return email