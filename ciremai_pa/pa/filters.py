import django_filters
import datetime
from .models import Orders,Patients


class OrderFilter(django_filters.FilterSet):
    order_date = django_filters.DateRangeFilter()
    number = django_filters.CharFilter(lookup_expr='icontains')
    patient__patient_id = django_filters.CharFilter(lookup_expr='icontains')
    patient__name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Orders
        fields = ['order_date','number','patient__patient_id','patient__name']
        
class PatientFilter(django_filters.FilterSet):
    patient_id = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    address = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Patients
        fields = ['patient_id','name','address']