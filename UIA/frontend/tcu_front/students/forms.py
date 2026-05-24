from django import forms
import re

STATUS_CHOICES = [
    ("review", "En revisión"),
    ("pending", "Pendiente"),
    ("rejected", "Rechazado"),
    ("approved", "Aprobado"),
]


class StudentForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre completo'
        })
    )
    identification = forms.CharField(
        widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Identificación'
        })
    )
    student_card = forms.CharField(
            widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Carnet'
        })
    )
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        })
    )
    phone = forms.CharField(
            widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono'
        })
    )
    tcu_place = forms.CharField(
            required=False,
            widget=forms.TextInput(
            attrs={
            'class': 'form-control',
            'placeholder': 'Lugar TCU'
            })
    )
    manager_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Encargado'
        })
    )
    observations = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Observaciones'
        })
    )
    year = forms.ChoiceField(
            choices=[
            ('2026', '2026'),
            ('2027', '2027'),
            ('2028', '2028'),
            ],
            widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
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