from datetime import datetime

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver

from rest_framework import exceptions


# Create your models here.
class Horario(models.Model):
    horario = models.TimeField(verbose_name='Horário', null=False, blank=False)

    class Meta:
        verbose_name = "Horário"
        verbose_name_plural = "Horários"
        unique_together = ['horario']
    
    def __str__(self) -> str:
        return self.horario.strftime('%H:%M')


class Medico(models.Model):
    nome = models.CharField(verbose_name='Nome', max_length=120, null=False, blank=False)
    crm = models.CharField(verbose_name='CRM', max_length=10, null=False, blank=False)
    email = models.EmailField(verbose_name='E-mail', null=False, blank=False)
    
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        unique_together = [['nome', 'crm']]
    
    def __str__(self) -> str:
        return f"{self.nome} - {self.crm}"


class Agenda(models.Model):
    medico = models.ForeignKey(Medico, verbose_name='Médico', blank=False, null=False,
                               on_delete=models.PROTECT)
    dia = models.DateField(verbose_name='Data alocação', blank=False, null=False)
    horarios = models.ManyToManyField(Horario, blank=False)
    
    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agendas"
        unique_together = [['medico', 'dia']]
    
    def __str__(self) -> str:
        from datetime import datetime
        dia = datetime.strftime(self.dia, "%d/%m/%Y")
        return f"{dia} | {self.medico}"

    def horarios_disponiveis(self):
        horarios = self.horarios.all() if self.dia > datetime.now().date() \
            else self.horarios.filter(horario__gte=datetime.now().time())
        return [horario.horario.strftime('%H:%M')
            for horario in horarios]


class Consulta(models.Model):
    agenda = models.ForeignKey(Agenda, null=False, blank=False,
                               on_delete=models.PROTECT)
    horario = models.TimeField(verbose_name='Horário', null=False, blank=False)
    data_agendamento = models.DateTimeField(verbose_name='Data do agendamento',
                                        null=False, blank=False, auto_now_add=True)
    
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        unique_together = [['agenda', 'horario']]


@receiver(post_save, sender=Consulta)
def consulta_post_save(sender, **kwargs):
    instance = kwargs.get('instance')
    horario, created = Horario.objects.get_or_create(horario=instance.horario)
    instance.agenda.horarios.remove(horario)


@receiver(post_delete, sender=Consulta)
def consulta_post_delete(sender, **kwargs):
    instance = kwargs.get('instance')
    horario_aberto, created = Horario.objects.get_or_create(horario=instance.horario)
    instance.agenda.horarios.add(horario_aberto)


@receiver(post_delete, sender=Consulta)
def pre_delete(sender, **kwargs):
    instance = kwargs.get('instance')
    if instance.agenda.dia < datetime.now().date():
        raise exceptions.ParseError("Não é possível desmarcar uma consulta que já aconteceu.")
    elif instance.agenda.dia == datetime.now().date() and instance.horario <= datetime.now().time():
        raise exceptions.ParseError("Não é possível desmarcar uma consulta que já aconteceu.")
