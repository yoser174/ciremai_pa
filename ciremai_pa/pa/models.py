# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.conf import settings
from django.db import models

from datetime import date
import datetime

from ckeditor.fields import RichTextField

class Parameters(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Name"))
    char_value = models.CharField(max_length=100,verbose_name=_("Char value"),null=True,blank=True)
    num_value = models.IntegerField(verbose_name=_("Numeric value"),null=True,blank=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(        
        settings.AUTH_USER_MODEL, 
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True, verbose_name=_("Last modified by"), 
        null=True,
        )
    
    def get_absolute_url(self):
        return reverse('parameters_detail', args=[str(self.id)])
    
    def __str__(self):
        return "%s %s %s" % (self.name,self.char_value,self.num_value)

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")



class Priority(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Group Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True, 
        verbose_name=_("Last modified by"), 
        null=True)
    
    def get_absolute_url(self):
        return reverse('priority_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Priority")
        verbose_name_plural = _("Priorities")
        
class Insurance(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Insurence Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True, 
        verbose_name=_("Last modified by"), 
        null=True)
    
    def get_absolute_url(self):
        return reverse('insurence_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Insurence")
        verbose_name_plural = _("Insurences")
        
class Doctors(models.Model):
    name = models.CharField(max_length=200,verbose_name=_("Doctor Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True,
        verbose_name=_("Last modified by"),
        null=True)
    
    def get_absolute_url(self):
        return reverse('doctors_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
        
class Origins(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Origin Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True, 
        verbose_name=_("Last modified by"),
        null=True)
    
    def get_absolute_url(self):
        return reverse('origins_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Origin")
        verbose_name_plural = _("Origins")
        
class Diagnosis(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Diangosis Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True,
        verbose_name=_("Last modified by"),
        null=True)
    
    def get_absolute_url(self):
        return reverse('diagnosis_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Diagnosis")
        verbose_name_plural = _("Diagnosis")
        
class Genders(models.Model):
    name = models.CharField(max_length=100,verbose_name=_("Gender Name"))
    ext_code = models.CharField(max_length=30,verbose_name=_("External code"))
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True,
        verbose_name=_("Last modified by"),
        null=True)
    
    def get_absolute_url(self):
        return reverse('priority_detail', args=[str(self.id)])
    
    def __str__(self):
        return ('%s (%s)' % (self.name,self.ext_code))

    class Meta:
        verbose_name = _("Gender")
        verbose_name_plural = _("Genders")


class Patients(models.Model):
    patient_id = models.CharField(max_length=100,verbose_name=_("Patient ID"),help_text=_("Medical record number"),unique=True)
    name = models.CharField(max_length=100,verbose_name=_("Name"),help_text=_("Patient Name"))
    gender = models.ForeignKey(Genders,on_delete=models.PROTECT,verbose_name=_("Gender"))
    dob = models.DateField(verbose_name=_("Date of birth"))
    address = models.CharField(max_length=100,verbose_name=_("Address"),help_text=_("Patient Address"))
    data0 = models.CharField(max_length=100,verbose_name=_("Data 0"),help_text=_("Additional data 0"),blank=True,null=True)
    data1 = models.CharField(max_length=100,verbose_name=_("Data 1"),help_text=_("Additional data 1"),blank=True,null=True)
    data2 = models.CharField(max_length=100,verbose_name=_("Data 2"),help_text=_("Additional data 3"),blank=True,null=True)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"),null=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True,
        verbose_name=_("Last modified by"),
        null=True) 
    
    def get_absolute_url(self):
        return reverse('patient_detail', args=[str(self.id)])
    
    def calculate_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    def create_order(self):
        order = Orders(patient=self)
        #order.doctor_id = 1
        #order.origin_id = 1
        #order.insurence_id = 1
        #order.priority_id = 1
        #order.lastmodifiedby_id = 1
        order.save()
        return order
    
    def __str__(self):
        return '%s %s' % (self.patient_id,self.name)

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        permissions = (
            ('view_pa_patients', 'Can view test patients'),
        )
        ordering = ['patient_id','name']
        
def auto_order_no():
        dtf = datetime.datetime.today().strftime('%y%m%d')
        par = Parameters.objects.filter(name='ORDER_NO',char_value=dtf)
        if par.count()==0:
            Parameters.objects.filter(name='ORDER_NO').delete()
            par = Parameters(name='ORDER_NO',char_value=dtf,num_value=1)
            par.save()
        par = Parameters.objects.filter(name='ORDER_NO',char_value=dtf)
        id = par.values('id')[0]['id']
        num_value = int(par.values('num_value')[0]['num_value'])
        par_upd = Parameters.objects.get(pk=id)
        par_upd.num_value=num_value+1
        par_upd.save()
        return dtf + ("%04d" % (num_value,))
    
MED_DOC = (
    ('DIAH','DR.dr. Diah Rini Handjari, SpPA (K)'),
    ('TNTR','dr.  Tantri Hellyanti, SpPA (K)')
    )  
class Orders(models.Model):
    order_date = models.DateField(verbose_name=_("Order date"),auto_now_add=True)
    number = models.CharField(max_length=100,verbose_name=_("Number"),default=auto_order_no,blank=True,null=True,unique=True)
    origin = models.ForeignKey(Origins,on_delete=models.PROTECT,verbose_name=_("Origin"),null=True)
    doctor = models.ForeignKey(Doctors,on_delete=models.PROTECT,verbose_name=_("Sender doctor"),null=True,blank=True)
    med_doctor =  models.CharField(
        max_length=4,
        verbose_name=_("Medical val. doctor"),
        choices=MED_DOC,
        null=True,
        blank=True,
    )
    diagnosis = models.ForeignKey(Diagnosis,on_delete=models.PROTECT,verbose_name=_("Diagnosis"),null=True,blank=True)
    priority = models.ForeignKey(Priority,on_delete=models.PROTECT,verbose_name=_("Order priority"),null=True,blank=True)
    insurance = models.ForeignKey(Insurance,on_delete=models.PROTECT,verbose_name=_("Insurance"),null=True,blank=True)
    note = models.CharField(max_length=100,verbose_name=_("Note/Comment"),blank=True,null=True)
    patient = models.ForeignKey(Patients,on_delete=models.PROTECT,verbose_name=_("Patient"))
    sample_taken = models.DateField(verbose_name=_("Sample Taken"),null=True)
    sample_received =models.DateField(verbose_name=_("Sample Received"),null=True)
    validated_at =models.DateField(verbose_name=_("Validated at"),null=True)
    lab_number = models.CharField(max_length=100,verbose_name=_("Lab number"),blank=True,null=True,unique=True)
    conclusion = models.CharField(max_length=1000,verbose_name=_("Conclusion"),blank=True,null=True)
    dateofcreation = CreationDateTimeField(verbose_name=_("Created at"),auto_now_add=True)
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True, 
        verbose_name=_("Last modified by"), 
        null=True)
    
    def get_absolute_url(self):
        return reverse('orders_detail', args=[str(self.id)])
        
    def __str__(self):
        return '%s %s' % (self.number,self.patient)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        permissions = (
            ('view_pa_orders', 'Can view orders'),
        )
        ordering = ['number','origin']


class OrderPathology(models.Model):
    order = models.OneToOneField(Orders,on_delete=models.CASCADE,primary_key=True,)
    lab_number = models.CharField(max_length=100,verbose_name=_("Lab Number"),null=True,blank=True)
    clinical_information = RichTextField(verbose_name=_("Clinical information"),null=True,blank=True)
    macroscopic = RichTextField(verbose_name=_("Macroscopic"),null=True,blank=True)
    microscopic = RichTextField(verbose_name=_("Microscopic"),null=True,blank=True)
    conclusion = RichTextField(verbose_name=_("conclusion"),null=True,blank=True)
    
    result_pdf_url = models.CharField(max_length=500,verbose_name=_("Result PDF url"),null=True)
    
    
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True, 
        verbose_name=_("Last modified by"), 
        null=True)
    
    def __str__(self):
        return "%s %s" % (self.order,self.lab_number)

class OrderCythology(models.Model):
    order = models.OneToOneField(Orders,on_delete=models.CASCADE,primary_key=True,)
    lab_number = models.CharField(max_length=100,verbose_name=_("Lab Number"),null=True,blank=True)
    hp = models.CharField(max_length=100,verbose_name=_("Hp"),null=True,blank=True)
    specimen_adhesion = RichTextField(verbose_name=_("Specimen adhesion"),null=True,blank=True)
    general_category = RichTextField(verbose_name=_("General category"),null=True,blank=True)
    explanation = RichTextField(verbose_name=_("Explanation"),null=True,blank=True)
    suggestions = RichTextField(verbose_name=_("Suggestions"),null=True,blank=True)
    
    result_pdf_url = models.CharField(max_length=500,verbose_name=_("Result PDF url"),null=True)
    
    
    lastmodification = ModificationDateTimeField(verbose_name=_("Last modified"))
    lastmodifiedby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        limit_choices_to={'is_staff': True},
        blank=True,
        verbose_name=_("Last modified by"),
        null=True)
    
    def __str__(self):
        return "%s" % (self.order)
  
