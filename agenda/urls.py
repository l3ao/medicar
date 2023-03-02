from django.urls import path

import agenda.views.api as api


urlpatterns = [
    path('consultas/',
        api.ConsultaListCreate.as_view(),
        name='api_consulta_list'),

    path('consultas/<int:pk>',
        api.ConsultaDestroy.as_view(),
        name='api_consulta_destroy'),

    path('agendas/',
        api.AgendaList.as_view(),
        name='api_agenda_list'),
]
