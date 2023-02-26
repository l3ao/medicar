from django_filters import rest_framework as filters


from ..models import Agenda


class AgendaFilter(filters.FilterSet):
    data_inicio = filters.DateFilter(field_name="dia", lookup_expr='gte')
    data_final = filters.DateFilter(field_name="dia", lookup_expr='lte')
    crm = filters.CharFilter(method='filter_crm')
    medico = filters.CharFilter(method='filter_medico')
    
    def filter_crm(self, queryset, name, value):
        value_filter = dict(self.data).get('crm')
        return queryset.filter(medico__crm__in=value_filter) if value_filter else queryset

    def filter_medico(self, queryset, name, value):
        value_filter = dict(self.data).get('medico')
        return queryset.filter(medico_id__in=value_filter) if value_filter else queryset

    class Meta:
        model = Agenda
        fields = ['medico', 'dia', 'horarios']
