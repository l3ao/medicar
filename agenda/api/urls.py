from django.urls import path

from .views import ConsultaListCreate, ConsultaDestroy, AgendaList


urlpatterns = [
    path('consultas/', ConsultaListCreate.as_view(), name='api_consulta_list'),
    path('consultas/<int:pk>', ConsultaDestroy.as_view(), name='api_consulta_destroy'),
    path('agendas/', AgendaList.as_view(), name='api_agenda_list'),
]
