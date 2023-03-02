from datetime import datetime

from rest_framework import serializers
from .models import Consulta, Agenda, Medico


class MedicoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Medico
        fields = ['id', 'nome', 'crm', 'email']


class HorarioListingField(serializers.RelatedField):

    def to_representation(self, value):
        return value.horario.strftime('%H:%M')


class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer()
    horarios = HorarioListingField(
        many=True,
        read_only=True
    )
    
    class Meta:
        model = Agenda
        fields = ['id', 'medico', 'dia', 'horarios']


class ConsultaSerializer(serializers.ModelSerializer):
    agenda_id = serializers.IntegerField(
        required=False)
    horario = serializers.CharField()
    dia = serializers.DateField(
        read_only=True)
    medico = MedicoSerializer(
        read_only=True)
    data_agendamento = serializers.DateTimeField(
        read_only=True)
    
    class Meta:
        model = Consulta
        fields = ['id', 'agenda_id', 'dia', 'horario',
            'data_agendamento', 'medico']
    
    def create(self, validated_data):
        agenda = Agenda.objects.get(id=validated_data.pop('agenda_id'))
        validated_data['horario'] = datetime.strptime(
            validated_data.get('horario'), '%H:%M').time()
        validated_data['dia'] = agenda.dia
        validated_data['medico'] = agenda.medico
        return Consulta.objects.create(**validated_data)

    def validate_agenda_id(self, value):
        qs_agenda = Agenda.objects.filter(id=value)
        if not qs_agenda.exists():
            raise serializers.ValidationError("Informe uma agenda válida.")

        if not value:
            raise serializers.ValidationError("Informe a agenda.")
        
        agenda = qs_agenda.first()
        if not agenda.dia >= datetime.now().date():
            raise serializers.ValidationError(
                "Não é possível marcar uma consulta para um dia passado.")

        return value

    def validate_horario(self, value):
        qs_agenda = Agenda.objects.filter(id=self.initial_data['agenda_id'])
        if not qs_agenda.exists():
            raise serializers.ValidationError("Informe uma agenda válida")
        
        if not value:
            raise serializers.ValidationError("Informe o horário")

        agenda = qs_agenda.first()
        if agenda.dia == datetime.now().date():
            value_time = datetime.strptime(value, '%H:%M').time()
            if not value_time >= datetime.now().time():
                raise serializers.ValidationError(
                    "Não é possível marcar uma consulta para um horário passado.")
        
        if not agenda.horarios.filter(horario=value).exists():
            raise serializers.ValidationError(
                "Esse horário não está disponível.")
        
        return value
