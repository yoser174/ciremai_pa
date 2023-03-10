# Generated by Django 4.1.7 on 2023-02-18 16:37

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import pa.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Diangosis Name')),
                ('ext_code', models.CharField(max_length=30, verbose_name='External code')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Diagnosis',
                'verbose_name_plural': 'Diagnosis',
            },
        ),
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Doctor Name')),
                ('ext_code', models.CharField(max_length=30, verbose_name='External code')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
        ),
        migrations.CreateModel(
            name='Genders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Gender Name')),
                ('ext_code', models.CharField(max_length=30, verbose_name='External code')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Gender',
                'verbose_name_plural': 'Genders',
            },
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Insurence Name')),
                ('ext_code', models.CharField(max_length=30, verbose_name='External code')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Insurence',
                'verbose_name_plural': 'Insurences',
            },
        ),
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Group Name')),
                ('ext_code', models.CharField(max_length=30, verbose_name='External code')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Priority',
                'verbose_name_plural': 'Priorities',
            },
        ),
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(help_text='Medical record number', max_length=100, unique=True, verbose_name='Patient ID')),
                ('name', models.CharField(help_text='Patient Name', max_length=100, verbose_name='Name')),
                ('dob', models.DateField(verbose_name='Date of birth')),
                ('address', models.CharField(help_text='Patient Address', max_length=100, verbose_name='Address')),
                ('data0', models.CharField(blank=True, help_text='Additional data 0', max_length=100, null=True, verbose_name='Data 0')),
                ('data1', models.CharField(blank=True, help_text='Additional data 1', max_length=100, null=True, verbose_name='Data 1')),
                ('data2', models.CharField(blank=True, help_text='Additional data 3', max_length=100, null=True, verbose_name='Data 2')),
                ('dateofcreation', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pa.genders', verbose_name='Gender')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Patient',
                'verbose_name_plural': 'Patients',
                'ordering': ['patient_id', 'name'],
                'permissions': (('view_pa_patients', 'Can view test patients'),),
            },
        ),
        migrations.CreateModel(
            name='Parameters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('char_value', models.CharField(blank=True, max_length=100, null=True, verbose_name='Char value')),
                ('num_value', models.IntegerField(blank=True, null=True, verbose_name='Numeric value')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'Parameters',
            },
        ),
        migrations.CreateModel(
            name='Origins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Origin Name')),
                ('ext_code', models.CharField(max_length=30, verbose_name='External code')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
            options={
                'verbose_name': 'Origin',
                'verbose_name_plural': 'Origins',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(auto_now_add=True, verbose_name='Order date')),
                ('number', models.CharField(blank=True, default=pa.models.auto_order_no, max_length=100, null=True, unique=True, verbose_name='Number')),
                ('med_doctor', models.CharField(blank=True, choices=[('DIAH', 'DR.dr. Diah Rini Handjari, SpPA (K)'), ('TNTR', 'dr.  Tantri Hellyanti, SpPA (K)')], max_length=4, null=True, verbose_name='Medical val. doctor')),
                ('note', models.CharField(blank=True, max_length=100, null=True, verbose_name='Note/Comment')),
                ('sample_taken', models.DateField(null=True, verbose_name='Sample Taken')),
                ('sample_received', models.DateField(null=True, verbose_name='Sample Received')),
                ('validated_at', models.DateField(null=True, verbose_name='Validated at')),
                ('lab_number', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Lab number')),
                ('conclusion', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Conclusion')),
                ('dateofcreation', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('diagnosis', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pa.diagnosis', verbose_name='Diagnosis')),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pa.doctors', verbose_name='Sender doctor')),
                ('insurance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pa.insurance', verbose_name='Insurance')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
                ('origin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='pa.origins', verbose_name='Origin')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pa.patients', verbose_name='Patient')),
                ('priority', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pa.priority', verbose_name='Order priority')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ['number', 'origin'],
                'permissions': (('view_pa_orders', 'Can view orders'),),
            },
        ),
        migrations.CreateModel(
            name='OrderPathology',
            fields=[
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pa.orders')),
                ('lab_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Lab Number')),
                ('clinical_information', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Clinical information')),
                ('macroscopic', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Macroscopic')),
                ('microscopic', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Microscopic')),
                ('conclusion', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='conclusion')),
                ('result_pdf_url', models.CharField(max_length=500, null=True, verbose_name='Result PDF url')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
        ),
        migrations.CreateModel(
            name='OrderCythology',
            fields=[
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pa.orders')),
                ('lab_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Lab Number')),
                ('hp', models.CharField(blank=True, max_length=100, null=True, verbose_name='Hp')),
                ('specimen_adhesion', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Specimen adhesion')),
                ('general_category', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='General category')),
                ('explanation', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Explanation')),
                ('suggestions', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Suggestions')),
                ('result_pdf_url', models.CharField(max_length=500, null=True, verbose_name='Result PDF url')),
                ('lastmodification', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Last modified')),
                ('lastmodifiedby', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Last modified by')),
            ],
        ),
    ]
