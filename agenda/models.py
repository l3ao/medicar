from datetime import datetime

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions


# Create your models here.
class Horario(models.Model):
    horario = models.TimeField(
        _('Horário'), null=False, blank=False)

    class Meta:
        verbose_name = "Horário"
        verbose_name_plural = "Horários"
        unique_together = ['horario']
        ordering = ['horario']

    def __str__(self) -> str:
        return self.horario.strftime('%H:%M')


class Medico(models.Model):
    nome = models.CharField(
        _('Nome'), max_length=120, null=False, blank=False)

    crm = models.IntegerField(
        _('CRM'), null=False, blank=False)

    email = models.EmailField(
        _('E-mail'), null=False, blank=False)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
        unique_together = ['crm']

    def __str__(self) -> str:
        return f"{self.nome} - {self.crm}"


class Agenda(models.Model):
    medico = models.ForeignKey(
        Medico, verbose_name=_('Médico'), blank=False,
        null=False, on_delete=models.PROTECT)

    dia = models.DateField(_('Data alocação'),
                           blank=False, null=False)

    horarios = models.ManyToManyField(Horario, blank=False)

    class Meta:
        verbose_name = "Agenda"
        verbose_name_plural = "Agendas"
        unique_together = [['medico', 'dia']]

    def __str__(self) -> str:
        from datetime import datetime
        dia = datetime.strftime(self.dia, "%d/%m/%Y")
        return f"{dia} | {self.medico}"

    @classmethod
    def atualizar_horarios(cls):
        agendas_do_dia = Agenda.objects.filter(
            dia=datetime.now().date())
        for agenda in agendas_do_dia:
            horarios_passados = agenda.horarios.filter(
                horario__lte=datetime.now().time())
            for horario in horarios_passados:
                agenda.horarios.remove(horario)

    @classmethod
    def realocar_horario(cls, horario_disponivel, medico, dia):
        horario, created = Horario.objects.get_or_create(horario=horario_disponivel)
        agenda, created = Agenda.objects.get_or_create(medico=medico, dia=dia)
        agenda.horarios.add(horario)
        Agenda.atualizar_horarios()
    
    @classmethod
    def remover_horario(cls, horario, medico, dia):
        horario, created = Horario.objects.get_or_create(horario=horario)
        agenda, created = Agenda.objects.get_or_create(medico=medico, dia=dia)
        agenda.horarios.remove(horario)
        Agenda.atualizar_horarios()
    
    @classmethod
    def atualizar_agendas(cls):
        agendas_passadas = Agenda.objects.filter(dia__lt=datetime.now().date())
        agendas_passadas.delete()
        agendas_sem_horarios = Agenda.objects.filter(dia__gte=datetime.now().date()).distinct()
        for agenda in agendas_sem_horarios:
            if not agenda.horarios.exists():
                agenda.delete()


class Consulta(models.Model):
    medico = models.ForeignKey(
        Medico, verbose_name=_('Médico'), blank=False,
        null=False, on_delete=models.PROTECT)
    dia = models.DateField(_('Data alocação'),
                           blank=False, null=False)
    horario = models.TimeField(verbose_name='Horário', null=False, blank=False)
    data_agendamento = models.DateTimeField(verbose_name='Data do agendamento',
                                            null=False, blank=False, auto_now_add=True)

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
        unique_together = [['medico', 'dia', 'horario']]


@receiver(post_save, sender=Agenda)
def agenda_post_save(sender, **kwargs):
    Agenda.atualizar_horarios()


@receiver(post_save, sender=Consulta)
def consulta_post_save(sender, **kwargs):
    instance = kwargs.get('instance')
    Agenda.remover_horario(instance.horario, instance.medico, instance.dia)


@receiver(post_delete, sender=Consulta)
def consulta_post_delete(sender, **kwargs):
    instance = kwargs.get('instance')
    Agenda.realocar_horario(instance.horario, instance.medico, instance.dia)


@receiver(pre_delete, sender=Consulta)
def consulta_pre_delete(sender, **kwargs):
    instance = kwargs.get('instance')
    agenda, created = Agenda.objects.get_or_create(medico=instance.medico, dia=instance.dia)
    if agenda.dia < datetime.now().date():
        raise exceptions.ParseError(
            "Não é possível desmarcar uma consulta que já aconteceu.")
    elif agenda.dia == datetime.now().date():
        if instance.horario <= datetime.now().time():
            raise exceptions.ParseError(
                "Não é possível desmarcar uma consulta que já aconteceu.")
