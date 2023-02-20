# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponseRedirect,redirect,reverse,get_object_or_404
#from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from braces.views import PermissionRequiredMixin, LoginRequiredMixin
#from extra_views.advanced import UpdateWithInlinesView,NamedFormsetsMixin, CreateWithInlinesView,InlineFormSet,ModelFormMixin
from extra_views import UpdateWithInlinesView,NamedFormsetsMixin, CreateWithInlinesView,InlineFormSetView,ModelFormSetView
from django_tables2 import SingleTableView, RequestConfig
from .custom.mixins import UpdateWithInlinesAndModifiedByMixin,CreateWithInlinesAndModifiedByMixin
from django.conf import settings
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView


from avatar.forms import PrimaryAvatarForm,UploadAvatarForm 
from avatar.views import _get_avatars
from avatar.models import Avatar
from avatar.signals import avatar_updated
from avatar.utils import invalidate_cache

from datetime import datetime


from . import models,tables,filters,forms,report

from django.shortcuts import render


# ######################
# ##   Helper Views   ##
# ######################
def login_user(request):
    logout(request)
    next_url = request.GET.get('next','')
    
    
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        next_url = request.POST.get('next','')
        

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next_url!='':
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect(reverse_lazy('dashboard'), permanent=True)
        else:
            messages.error(request, _("Wrong username and/or password."))
            
            
    context = {'next':next_url}
    return render(request,'registration/login.html',context)

@login_required(login_url='login')
def show_dashboard(request):
    today = datetime.now().date()
    ordercount_today = models.Orders.objects.filter(order_date__gte=today).count()
    patientcount_today = models.Patients.objects.filter(dateofcreation__gte=today).count()
    context = {'ordercount_today': ordercount_today,'patientcount_today':patientcount_today}
    next_url = request.GET.get('next')
    if next_url:
        return HttpResponseRedirect(next_url)
    else:
        return render(request,'dashboard.html',context)


@login_required(login_url='login')
def home(request):
    template = 'index.html'
    context = {}
    return render(request,template,context) 

@login_required(login_url='login')
class UpdateUserProfile(LoginRequiredMixin,NamedFormsetsMixin,UpdateWithInlinesView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'auth/user_form.html'
    success_url = reverse_lazy('home')

@login_required(login_url='login')
def AvatarChange(request,extra_context=None,next_override=None,upload_form=UploadAvatarForm,primary_form=PrimaryAvatarForm,
                 *args,**kwargs):
    if extra_context is None:
        extra_context = {}
        
    avatar, avatars = _get_avatars(request.user)
    if avatar:
        kwargs = {'initial':{'choice':avatar.id}}
    else:
        kwargs = {}
    upload_avatar_form = upload_form(user=request.user, **kwargs)
    primary_avatar_form = primary_form(request.POST or None,
                                       user=request.user,
                                       avatars=avatars, **kwargs)
    
    if request.method == 'POST':
        updated = False
        if 'choice' in request.POST and primary_avatar_form.is_valid():
            avatar = Avatar.objects.get(id=primary_avatar_form.cleaned_data['choice'])
            avatar.primary = True
            avatar.save()
            updated = True
            invalidate_cache(request.user)
            messages.success(request, _("Successfully updated your avatar."))
        if updated:
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
        return render(request,'auth/avatar_change.html')
    
    context = {
        'avatar':avatar,
        'avatars':avatars,
        'upload_avatar_form':upload_avatar_form,
        'primary_avatar_form':primary_avatar_form,
        'next':next_override
        }
    context.update(extra_context)
    template_name = 'auth/avatar_change.html'
    return render(request, template_name, context)
    
@login_required(login_url='login')           
def AvatarAdd(request,extra_context=None,next_override=None,upload_form=UploadAvatarForm,*args,**kwargs):
    if extra_context is None:
        extra_context = {}
    avatar,avatars = _get_avatars(request.user)
    upload_avatar_form = upload_form(request.POST or None,
                                     request.FILES or None,
                                     user = request.user)
    if request.method == 'POST' and 'avatar' in request.FILES:
        if upload_avatar_form.is_valid():
            avatar = Avatar(user=request.user, primary=True)
            image_file = request.FILES['avatar']
            avatar.avatar.save(image_file.name,image_file)
            avatar.save()
            invalidate_cache(request.user)
            messages.success(request, _("Successfully uploaded a new avatar."))
            avatar_updated.send(sender=Avatar, user=request.user, avatar=avatar)
            return render(request,'auth/avatar_change.html')
    context = {
        'avatar': avatar,
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'next': next_override,
    }
    context.update(extra_context)
    template_name = 'auth/avatar_add.html'
    return render(request, template_name, context)   

@login_required(login_url='login')
def OrderPathology(request,pk):
    orders = models.Orders.objects.get(pk=pk)
    orderpathology,update = models.OrderPathology.objects.get_or_create(order=orders)
    if request.method == 'POST':
        form = forms.PathologyForm(request.POST,instance=orderpathology)
        if form.is_valid():
            form.order_id = pk
            form.save()
    context = {'form':forms.PathologyForm(instance=orderpathology),'orders':orders,'pk':pk}
    template = 'pa/order_pathology.html'
    return render(request, template, context)

@login_required(login_url='login')
def OrderPathologyPrint(request,pk):
    order = models.Orders.objects.get(pk=pk)

    pa = models.OrderPathology.objects.get(order=order)

    parameters ={'ORDER_ID': pk}
    output = settings.MEDIA_ROOT+'/report/PA_'+str(order.patient.patient_id)+'_'+str(order.number)+'.pdf'

    
    
    res_rep = report.JasperServer()
    
    b_ok,content = res_rep.get_report_pa(pk)
    
    if b_ok:        
        fd = open (output, 'wb')
        fd.write(content)
        fd.close()

        try:
            output_report_his = settings.REPORT_ROOT+'/'+str(order.origin.ext_code)+'/PA'+str(order.origin.ext_code)+'_'+str(order.patient.patient_id)+'_'+str(order.sample_taken).replace('-','')+'_'+str(order.number)+'.pdf'
            fd = open (output_report_his, 'wb')
            fd.write(content)
            fd.close()
        except:
            pass
        
        base_url =  request.build_absolute_uri('/')[:-1].strip("/")
        url_pdf = base_url+'/media/report/PA_'+str(order.patient.patient_id)+'_'+str(order.number)+'.pdf'
        
        template = 'pa/result_pdf_preview.html'
        context = {'order':order,'url_pdf' : url_pdf}
        return render(request,template,context)
    else:
        return JsonResponse(content) 

@login_required(login_url='login')
def OrderPathologyPrintEN(request,pk):
    order = models.Orders.objects.get(pk=pk)

    pa = models.OrderPathology.objects.get(order=order)

    parameters ={'ORDER_ID': pk}
    output = settings.MEDIA_ROOT+'/report/PA_'+str(order.patient.patient_id)+'_'+str(order.number)+'_EN.pdf'
    
    res_rep = report.JasperServer()
    
    b_ok,content = res_rep.get_report_pa_en(pk)
    
    if b_ok:        
        fd = open (output, 'wb')
        fd.write(content)
        fd.close()

        try:
            output_report_his = settings.REPORT_ROOT+'/'+str(order.origin.ext_code)+'/PA'+str(order.origin.ext_code)+'_'+str(order.patient.patient_id)+'_'+str(order.sample_taken).replace('-','')+'_'+str(order.number)+'.pdf'
            fd = open (output_report_his, 'wb')
            fd.write(content)
            fd.close()
        except:
            pass
        
        base_url =  request.build_absolute_uri('/')[:-1].strip("/")
        url_pdf = base_url+'/media/report/PA_'+str(order.patient.patient_id)+'_'+str(order.number)+'_EN.pdf'
        
        template = 'pa/result_pdf_preview.html'
        context = {'order':order,'url_pdf' : url_pdf}
        return render(request,template,context)
    else:
        return JsonResponse(content) 


@login_required(login_url='login')
def OrderCythology(request,pk):
    orders = models.Orders.objects.get(pk=pk)
    ordercythology,update = models.OrderCythology.objects.get_or_create(order=orders)
    if request.method == 'POST':
        form = forms.CythologyForm(request.POST,instance=ordercythology)
        if form.is_valid():
            form.order_id = pk
            form.save()
    context = {'form':forms.CythologyForm(instance=ordercythology),'orders':orders,'pk':pk}
    template = 'pa/order_cythology.html'
    return render(request, template, context)

@login_required(login_url='login')
def OrderCythologyPrint(request,pk):
    order = models.Orders.objects.get(pk=pk)

    ca = models.OrderCythology.objects.get(order=order)
    
    #ts = datetime.today().strftime('%Y%m%d%H%M%S')
    parameters ={'ORDER_ID': pk}
    output = settings.MEDIA_ROOT+'/report/CA_'+str(order.patient.patient_id)+'_'+str(order.number)+'.pdf'
    
    res_rep = report.JasperServer()
    
    b_ok,content = res_rep.get_report_ca(pk)
    
    if b_ok:        
        fd = open (output, 'wb')
        fd.write(content)
        fd.close()

        try:
            output_report_his = settings.REPORT_ROOT+'/'+str(order.origin.ext_code)+'/CA'+str(order.origin.ext_code)+'_'+str(order.patient.patient_id)+'_'+str(order.sample_taken).replace('-','')+'_'+str(order.number)+'.pdf'
            fd = open (output_report_his, 'wb')
            fd.write(content)
            fd.close()
        except:
            pass
        
        base_url =  request.build_absolute_uri('/')[:-1].strip("/")
        url_pdf = base_url+'/media/report/CA_'+str(order.patient.patient_id)+'_'+str(order.number)+'.pdf'
        
        template = 'pa/result_pdf_preview.html'
        context = {'order':order,'url_pdf' : url_pdf}
        return render(request,template,context)
    else:
        return JsonResponse(content)

@login_required(login_url='login')
def OrderCythologyPrintEN(request,pk):
    order = models.Orders.objects.get(pk=pk)

    ca = models.OrderCythology.objects.get(order=order)
    
    #ts = datetime.today().strftime('%Y%m%d%H%M%S')
    parameters ={'ORDER_ID': pk}
    output = settings.MEDIA_ROOT+'/report/CA_'+str(order.patient.patient_id)+'_'+str(order.number)+'_EN.pdf'
    
    res_rep = report.JasperServer()
    
    b_ok,content = res_rep.get_report_ca_en(pk)
    
    if b_ok:        
        fd = open (output, 'wb')
        fd.write(content)
        fd.close()

        try:
            output_report_his = settings.REPORT_ROOT+'/'+str(order.origin.ext_code)+'/CA'+str(order.origin.ext_code)+'_'+str(order.patient.patient_id)+'_'+str(order.sample_taken).replace('-','')+'_'+str(order.number)+'.pdf'
            fd = open (output_report_his, 'wb')
            fd.write(content)
            fd.close()
        except:
            pass
        
        base_url =  request.build_absolute_uri('/')[:-1].strip("/")
        url_pdf = base_url+'/media/report/CA_'+str(order.patient.patient_id)+'_'+str(order.number)+'_EN.pdf'
        
        template = 'pa/result_pdf_preview.html'
        context = {'order':order,'url_pdf' : url_pdf}
        return render(request,template,context)
    else:
        return JsonResponse(content) 
        
        
    
        

@login_required(login_url='login')
def order_patient(request):
    if request.method == 'POST':  
        patient_pk = request.POST.get('patient','')  
        return redirect('create_order_fromtient',patient_pk=patient_pk)
    else:
        template = 'pa/select_patient.html'
        patients = models.Patients.objects.all()
        data = models.Patients.objects.all()
        if request.GET.get('patient_id'):
            data = data.filter(patient_id__contains=request.GET.get('patient_id') )
        if request.GET.get('name'):
            data = data.filter(name__contains=request.GET.get('name') )
               
        filter = filters.PatientFilter(request.GET,queryset=patients)
        patienttable = tables.SelectPatientsTable(data)
        patienttable.paginate(page=request.GET.get('page', 1), per_page=10)
        
        context = {'patienttable':patienttable,'filter':filter}
        return render(request,template,context)  
    
@login_required(login_url='login')
def order_add_patient(request):
    if request.method == 'POST':
        form = forms.PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('create_order_from_patient',patient_pk=patient.pk)
        else:
            template = 'pa/add_patient.html'
            context = {'form':form}
            return render(request,template,context)
    else:
        template = 'pa/add_patient.html'
        context = {'form':forms.PatientForm}
        return render(request,template,context)
    
@login_required(login_url='login')   
def create_order_from_patient(request,patient_pk):
    patient = models.Patients.objects.get(pk=patient_pk)
    order = patient.create_order()
    return redirect('order_edit', pk=order.pk)


# ###################
# ##   Base Views  ##
# ###################
class PaginatedTableView(SingleTableView):
    filter_class = None

    def __init__(self, **kwargs):
        super(PaginatedTableView, self).__init__(**kwargs)
        self.object_list = self.model.objects.all()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        config = RequestConfig(request)
        table = self.table_class(self.object_list)
        config.configure(table)
        table.paginate(page=request.GET.get('page', 1), per_page=self.tablegination)
        context[self.context_table_name] = table
        return self.render_to_response(context)

class FilteredSingleTableView(SingleTableView):
    filter_class = None

    def get_table_data(self):
        data = super(FilteredSingleTableView, self).get_table_data()
        self.filter = self.filter_class(self.request.GET, queryset=data)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(FilteredSingleTableView, self).get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class ListOrders(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.Orders
    permission_required = 'pa.view_orders'
    login_url = settings.LOGIN_URL_BILLING
    table_class = tables.OrdersTable
    table_data = models.Orders.objects.filter()
    context_table_name = 'orderstable'
    filter_class = filters.OrderFilter
    tablegination = 10
    
    
class EditOrder(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin,UpdateWithInlinesAndModifiedByMixin):
    model = models.Orders
    template_name = 'pa/orders_form.html'
    permission_required = 'pa.change_orders'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('orders_list')
    form_class = forms.OrderForm2
    
    def post(self,request,*args,**kwargs):
        order = models.Orders.objects.get(number=request.POST['number'])
        form = forms.OrderForm2(request.POST,instance=order)
        if form.is_valid():
            form.save()
            #tes = OrderTests.objects.filter(order=order)
            #tes.delete()
            #for test in form.cleaned_data['test_selections']:
            #    order_item = OrderTests()
            #    order_item.order = order
            #    order_item.test = test
            #    order_item.save()
            return redirect('order_detail', pk=order.pk)
        
        return render(request,self.template_name,{'form':form})
    
class ViewOrder(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Orders
    permission_required = 'pa.view_orders'
    login_url = settings.LOGIN_URL_BILLING
    
    def get_context_data(self, **kwargs):
        context = super(ViewOrder, self).get_context_data(**kwargs)
        context['pathology'],created = models.OrderPathology.objects.get_or_create(order_id=self.kwargs['pk'])
        context['cythology'],created = models.OrderCythology.objects.get_or_create(order_id=self.kwargs['pk'])
        #context['samples'] = OrderSamples.objects.filter(order_id=self.kwargs['pk'])
        #context['labelprinters'] = LabelPrinters.objects.filter(active=True)
        #context['MENU_BTN_PRINT_RECEIPT'] = Parameters.objects.filter(name='MENU_BTN_PRINT_RECEIPT')[0]
        #context['MENU_BTN_PRINT_BILL'] = Parameters.objects.filter(name='MENU_BTN_PRINT_BILL')[0]
        #context['MENU_BTN_PRINT_BARCODE'] = Parameters.objects.filter(name='MENU_BTN_PRINT_BARCODE')[0]
        return context


class DeleteOrder(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Orders
    permission_required = 'pa.delete_order'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('orders_list')
    tablegination = 10
    

class ListPatients(LoginRequiredMixin, PermissionRequiredMixin, FilteredSingleTableView):    
    model = models.Patients
    permission_required = 'pa.viewtients'
    login_url = settings.LOGIN_URL_BILLING
    table_class = tables.PatientsTable
    table_data = models.Patients.objects.all()
    context_table_name = 'patientstable'
    filter_class = filters.PatientFilter
    tablegination = 10

class CreatePatient(LoginRequiredMixin,PermissionRequiredMixin,
                     NamedFormsetsMixin,CreateWithInlinesView):
    model = models.Patients
    permission_required = 'pa.addtients'
    login_url = settings.LOGIN_URL_BILLING
    fields = ['patient_id','name','gender','dob','address',]
    success_url = reverse_lazy('patients_list')
    
class ViewPatients(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Patients
    permission_required = 'pa.viewtients'
    login_url = settings.LOGIN_URL_BILLING
    
class EditPatient(LoginRequiredMixin, PermissionRequiredMixin, NamedFormsetsMixin,UpdateWithInlinesAndModifiedByMixin):
    model = models.Patients
    permission_required = 'pa.changetient'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('patients_list')
    form_class = forms.PatientForm


class DeletePatient(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Patients
    permission_required = 'pa.deletetient'
    login_url = settings.LOGIN_URL_BILLING
    success_url = reverse_lazy('patient_list')
    tablegination = 10


