from django_filters import rest_framework as filters


from .models import Agenda


class AgendaFilter(filters.FilterSet):
    data_inicio = filters.DateFilter(field_name="dia", lookup_expr='gte')
    data_final = filters.DateFilter(field_name="dia", lookup_expr='lte')
    crm = filters.CharFilter(method='filter_crm')
    medico = filters.CharFilter(method='filter_medico')
    
    def filter_crm(self, queryset, name, value):
        value_filter = dict(self.data).get('crm')
        if value_filter:
            return queryset.filter(medico__crm__in=value_filter)
        else:
            return queryset

    def filter_medico(self, queryset, name, value):
        value_filter = dict(self.data).get('medico')
        if value_filter:
            return queryset.filter(medico_id__in=value_filter)
        else:
            return queryset

    class Meta:
        model = Agenda
        fields = ['medico', 'dia', 'horarios']
