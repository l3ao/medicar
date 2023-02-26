from datetime import datetime

from django import forms

from agenda.models import Agenda


class AgendaForm(forms.ModelForm):
    
    def clean_dia(self):
        dia = self.cleaned_data["dia"]
        if dia < datetime.now().date():
            raise forms.ValidationError(
                'Não é possível criar uma agenda para um médico em um dia passado.')
        return self.cleaned_data["dia"]
    
    class Meta:
        model = Agenda
        fields = ['medico', 'dia', 'horarios']
