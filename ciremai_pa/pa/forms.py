from datetimewidget.widgets import DateWidget,DateInput
from django import forms
from crispy_forms.helper import FormHelper
from .models import Patients,Orders,OrderCythology,OrderPathology,Doctors,Diagnosis,Priority


from django.contrib.admin import widgets
from ckeditor.widgets import CKEditorWidget


from itertools import groupby
from django.forms.models import (
    ModelChoiceIterator, ModelChoiceField, ModelMultipleChoiceField
)

from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)


class Grouped(object):
    def __init__(self, queryset, group_by_field,
                 group_label=None, *args, **kwargs):
        """ 
        ``group_by_field`` is the name of a field on the model to use as
                           an optgroup.
        ``group_label`` is a function to return a label for each optgroup.
        """
        super(Grouped, self).__init__(queryset, *args, **kwargs)
        self.group_by_field = group_by_field
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label
   
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)


class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset.all()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, choices in groupby(self.queryset.all(),
                    key=lambda row: getattr(row, self.field.group_by_field)):
            if self.field.group_label(group):
                yield (
                    self.field.group_label(group),
                    [self.choice(ch) for ch in choices]
                )


class GroupedModelChoiceField(Grouped, ModelChoiceField):
    choices = property(Grouped._get_choices, ModelChoiceField._set_choices)


class GroupedModelMultiChoiceField(Grouped, ModelMultipleChoiceField):
    choices = property(Grouped._get_choices, ModelMultipleChoiceField._set_choices)
    
    
class PatientForm(forms.ModelForm):
    dob = forms.DateField(input_formats=["%d/%m/%Y"],widget=DateInput(format='%d/%m/%Y', attrs={'class': "input", 'placeholder': "Ex.: dd/mm/aaaa", "OnKeyPress":"mask('##/##/####', this)"}))
    class Meta:
        model = Patients
        fields = ('patient_id','name','gender','dob','address',)
        
class OrderForm2(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctors.objects.all(), widget=Select2Widget,empty_label=None,required=False)
    sample_taken = forms.DateField(input_formats=["%d/%m/%Y"],widget=DateInput(format='%d/%m/%Y', attrs={'class': "input", 'placeholder': "Ex.: dd/mm/yyyy", "OnKeyPress":"mask('##/##/####', this)"}))
    sample_received = forms.DateField(input_formats=["%d/%m/%Y"],widget=DateInput(format='%d/%m/%Y', attrs={'class': "input", 'placeholder': "Ex.: dd/mm/yyyy", "OnKeyPress":"mask('##/##/####', this)"}))
    validated_at = forms.DateField(input_formats=["%d/%m/%Y"],widget=DateInput(format='%d/%m/%Y', attrs={'class': "input", 'placeholder': "Ex.: dd/mm/yyyy", "OnKeyPress":"mask('##/##/####', this)"}))
    
    def __init__(self, *args, **kwargs):
        super(OrderForm2, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['number'].widget.attrs['readonly'] = True
    def clean_number(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.number
        else:
            return self.cleaned_data['number']
    class Meta:
        model = Orders
        fields = ('id','number','origin','sample_taken','sample_received','doctor','med_doctor','validated_at')
        widgets = {'sample_taken': forms.DateInput(attrs={'id': 'dt_sample_taken'}),
                   'sample_received': forms.DateInput(attrs={'id': 'dt_sample_received'}),
                   'validated_at': forms.DateInput(attrs={'id': 'dt_validated_at'})}
        
        
class CythologyForm(forms.ModelForm):
    class Meta:
        fields = ('lab_number','hp','specimen_adhesion','general_category','explanation','suggestions',)
        model = OrderCythology
        
class PathologyForm(forms.ModelForm):
    clinical_information = forms.CharField(widget=CKEditorWidget())
    class Meta:
        fields = ('lab_number','clinical_information','macroscopic','microscopic','conclusion',)
        model = OrderPathology
