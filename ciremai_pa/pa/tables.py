import django_tables2 as tables
from pprint import pprint
from .custom.custom_columns import ModelDetailLinkColumn, IncludeColumn, CssFieldColumn, LabelIconColumn,ButtonColumn
from django.contrib.humanize.templatetags.humanize import intcomma

from django.utils.translation import gettext_lazy as _

from .models import Orders,Patients

class ColumnWithThausandSeparator(tables.Column):
    def render(self,value):
        return intcomma(value)

        
class OrdersTable(tables.Table):
    edit_order = IncludeColumn(
        'includes/orders_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
        
    
    class Meta:
        model = Orders
        exclude = ('id',)
        #sequence = ('number')
        fields = ('order_date','number','origin.name','doctor.name','patient.patient_id','patient.name','med_doctor',)
        order_by = ('-number',)
        
        
class PatientsTable(tables.Table):
    edit_order = IncludeColumn(
        'includes/patient_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )
    
    class Meta:
        model = Patients
        fields = ('patient_id','name','gender','dob','address',)
        exclude = ('id',)
        
        
class SelectPatientsTable(tables.Table):
    use_product = ButtonColumn(gl_icon="external-link",
                            extra_class="btn-info",
                            condition = '1',
                            onclick = "location.href='{% url 'create_order_from_patient' record.pk %}'",
                            verbose_name=_(''),orderable=False)
    
    class Meta:
        model = Patients
        exclude = ('id',)
        
