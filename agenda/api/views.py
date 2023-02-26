from datetime import datetime

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from ..models import Consulta, Agenda, Horario
from .serializers import ConsultaSerializer, AgendaSerializer
from .filters import AgendaFilter


class ConsultaListCreate(generics.ListCreateAPIView):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['agenda__dia', 'horario']
    ordering = ['agenda__dia', 'horario']

    def get_queryset(self):
        return self.queryset.filter(agenda__dia__gte=datetime.now().date())


class ConsultaDestroy(generics.DestroyAPIView):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer


class AgendaList(generics.ListAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    filterset_class = AgendaFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['dia']
    ordering = ['dia']

    def get_queryset(self):
        return self.queryset.filter(
            Q(dia__gte=datetime.now().date()) &
            Q(horarios__isnull=False)
        ).distinct()
