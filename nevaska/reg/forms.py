from django import forms
from .models import Arquivos_empresa, User


class ArquivosForm(forms.ModelForm):
    class Meta:
        model = Arquivos_empresa
        fields = ['name', 'arquivo']

        name = forms.CharField(
            widget=forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Tipo de Aquivo: Contrato, NF e etc'})
        )

        arquivo = forms.FileField(
            widget=forms.ClearableFileInput(
                attrs={'class': 'form-control-file'})
        )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'rca', 'cargos']
