from django.contrib import admin
from agenda import models
from agenda.forms import AgendaForm


# Register your models here.
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'crm', 'email')


class AgendaAdmin(admin.ModelAdmin):
    form = AgendaForm
    list_display = ('dia', 'medico')


class HorarioAdmin(admin.ModelAdmin):
    
    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(models.Medico, MedicoAdmin)
admin.site.register(models.Agenda, AgendaAdmin)
admin.site.register(models.Horario, HorarioAdmin)
