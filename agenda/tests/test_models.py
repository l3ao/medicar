from datetime import datetime
from django.test import TestCase
from agenda.models import Medico, Agenda, Consulta, Horario


class MedicoTestCase(TestCase):
    
    def setUp(self):
        Medico.objects.create(
            nome='João Silva',
            crm=1234,
            email='joao.silva@email.com'
        )
    
    def test_retorno_crm_novo_medico(self):
        medico_joao = Medico.objects.get(crm=1234)
        self.assertEqual(medico_joao.crm, 1234)


class HorarioTestCase(TestCase):
    
    def setUp(self):
        horarios = ['10:00', '12:00', '13:00']
        for horario in horarios:
            Horario.objects.create(
                horario=datetime.strptime(horario, '%H:%M').time()
            )
    
    def test_retorno_novos_horarios(self):
        horario_atual = datetime.strptime('12:00', '%H:%M').time()
        horario = Horario.objects.get(horario=horario_atual)
        self.assertEqual(horario.horario, horario_atual)


class AgendaTestCase(TestCase):
    
    def setUp(self):
        medico = Medico.objects.create(
            nome='João Silva',
            crm=1234,
            email='joao.silva@email.com'
        )
        Agenda.objects.create(
            medico=medico,
            dia=datetime.now().date()
        )

    def test_retornar_nova_agenda_horarios(self):
        agenda = Agenda.objects.get(dia=datetime.now().date())
        self.assertEqual(agenda.dia, datetime.now().date())
        

class ConsultaTestCase(TestCase):
    
    def setUp(self):
        medico = Medico.objects.create(
            nome='João Silva',
            crm=1234,
            email='joao.silva@email.com'
        )
        Agenda.objects.create(
            medico=medico,
            dia=datetime.now().date()
        )
        agenda = Agenda.objects.get(dia=datetime.now().date())
        Consulta.objects.create(
            medico=agenda.medico,
            dia=agenda.dia,
            horario='12:00'
        )
    
    def test_retorno_nova_consulta(self):
        medico = Medico.objects.get(crm=1234)
        agenda = Agenda.objects.get(dia=datetime.now().date())
        consulta = Consulta.objects.get(
            medico=agenda.medico,
            dia=agenda.dia,
            horario='12:00'
        )
        self.assertEqual(consulta.dia, datetime.now().date())
        self.assertEqual(consulta.medico.nome, medico.nome)
