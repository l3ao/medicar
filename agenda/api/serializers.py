from datetime import datetime

from rest_framework import serializers
from ..models import Consulta, Agenda, Horario, Medico


class MedicoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Medico
        fields = ['id', 'nome', 'crm', 'email']


class HorarioListingField(serializers.RelatedField):

    def to_representation(self, value):
        return value.horario.strftime('%H:%M')


class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer()
    horarios = serializers.SerializerMethodField()
    
    def get_horarios(self, obj):
        return obj.horarios_disponiveis()
    
    class Meta:
        model = Agenda
        fields = ['id', 'medico', 'dia', 'horarios']


class ConsultaSerializer(serializers.ModelSerializer):
    agenda_id = serializers.IntegerField()
    horario = serializers.CharField()
    dia = serializers.SerializerMethodField()
    medico = serializers.SerializerMethodField()
    data_agendamento = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Consulta
        fields = ['id', 'agenda_id', 'dia', 'horario',
            'data_agendamento', 'medico']

    def validate_agenda_id(self, value):
        if not value:
            raise serializers.ValidationError("Informe a agenda.")

        agenda = Agenda.objects.get(id=value)
        if not agenda.dia >= datetime.now().date():
            raise serializers.ValidationError(
                "Não é possível marcar uma consulta para um dia passado.")
        
        if not agenda.horarios.filter(horario=self.initial_data['horario']):
            raise serializers.ValidationError(
                "Não é possível marcar uma consulta se o horário já foi preenchido.")
        
        if not agenda.dia >= datetime.now().date() and not datetime.strptime(value, '%H:%M').time() >= datetime.now().time():
            raise serializers.ValidationError(
                "Não é possível marcar uma consulta para um horário passado.")

        return value

    def validate_horario(self, value):
        if not value:
            raise serializers.ValidationError("Informe o horário")
        
        return value

    def get_dia(self, obj):
        return datetime.strftime(obj.agenda.dia, '%Y-%m-%d')
    
    def get_medico(self, obj):
        medico_serializer = MedicoSerializer(instance=obj.agenda.medico)
        return medico_serializer.data
