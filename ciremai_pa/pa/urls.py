#from django.conf.urls import  url,include
from django.urls import include, re_path as url
from . import views


urlpatterns = [
    
    url("^$", views.home, name="home"),
    url(r'^dashboard/$', views.show_dashboard, name='dashboard'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.login_user, name='logout'),
    url(r'^avatarchange/$', views.AvatarChange, name='avatar_change'),
    url(r'^avataradd/$', views.AvatarAdd, name='avatar_add'),
    
    url(r'^profileupdate/(?P<pk>\d+)/$', views.UpdateUserProfile, name='profile_update'),
    
     # #############
    # Order urls
    # #############
    url(r'^orders/$', views.ListOrders.as_view(), name='orders_list'),
    url(r'^orders/edit/(?P<pk>\d+)/$', views.EditOrder.as_view(), name='order_edit'),
    url(r'^orders/patient/$', views.order_patient, name='order_patient'),
    url(r'^orders/delete/(?P<pk>\d+)/$', views.DeleteOrder.as_view(), name='order_delete'),
    url(r'^orders/add/patient/$', views.order_add_patient, name='order_add_patient'),
    url(r'^orders/patient/create/(?P<patient_pk>\d+)/$', views.create_order_from_patient, name='create_order_from_patient'),
    url(r'^orders/detail/(?P<pk>\d+)/$', views.ViewOrder.as_view(), name='order_detail'),
    url(r'^orders/detail/(?P<pk>\d+)/pathology/', views.OrderPathology, name='pathology_result'),
    url(r'^orders/detail/(?P<pk>\d+)/pathology_print/', views.OrderPathologyPrint, name='pathology_result_print'),
    url(r'^orders/detail/(?P<pk>\d+)/pathology_print_en/', views.OrderPathologyPrintEN, name='pathology_result_print_en'),
    url(r'^orders/detail/(?P<pk>\d+)/cythology/', views.OrderCythology, name='cythology_result'),
    url(r'^orders/detail/(?P<pk>\d+)/cythology_print/', views.OrderCythologyPrint, name='cythology_result_print'),
    url(r'^orders/detail/(?P<pk>\d+)/cythology_print_en/', views.OrderCythologyPrintEN, name='cythology_result_print_en'),
    
    # #############
    # Patient urls
    # #############
    url(r'^patients/$', views.ListPatients.as_view(), name='patients_list'),
    url(r'^patients/detail/(?P<pk>\d+)/$', views.ViewPatients.as_view(), name='patient_detail'),
    url(r'^patients/create/$', views.CreatePatient.as_view(), name='patient_create'),
    url(r'^patients/edit/(?P<pk>\d+)/$', views.EditPatient.as_view(), name='patient_edit'),
    url(r'^patients/delete/(?P<pk>\d+)/$', views.DeletePatient.as_view(), name='patient_delete'), 
    ]
