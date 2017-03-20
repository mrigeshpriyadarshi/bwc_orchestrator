# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory

from collections import OrderedDict as SortedDict
from bootstrap3.tests import TestForm
from mongodbforms import *

RADIO_CHOICES = (
    ('1', 'Radio 1'),
    ('2', 'Radio 2'),
)

MEDIA_CHOICES = (
    ('Audio', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
    ),
    ('Video', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
    ),
    ('unknown', 'Unknown'),
)

VDX_HOST = (
    ('host3', '--- Select Hostname ---'),
    ('10.88.88.146', '10.88.88.146'),
)

ICX_HOST = (
    ('host', '--- Select Hostname ---'),
    ('192.168.10.65', '192.168.10.65'),
)

EMAIL_LIST = (
    ('mail3', '--- Select Email ID ---'),
    ('mpriyada@brocade.com', 'mpriyada@brocade.com'),
    ('pfong@brocade.com', 'pfong@brocade.com'),
)

ICX_PORTS = (
    ('ports', '--- Select available ports ---'),
    ('22', '22'),
)

class ContactForm(TestForm):
    pass


class ContactBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        raise forms.ValidationError("This error was added to show the non form errors styling")

ContactFormSet = formset_factory(TestForm, formset=ContactBaseFormSet,
                                 extra=2,
                                 max_num=4,
                                 validate_max=True)


class FilesForm(forms.Form):
    # pass
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file5 = forms.ImageField()
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class LoginForm(forms.Form):
        email = forms.CharField(label=(u''), max_length=18, strip=True)
        password = forms.CharField(label=(u''), widget=forms.PasswordInput(render_value=False), max_length=20)

class MAHBCustForm(forms.Form):
        cust_name = forms.CharField(label=(u'Customer Name'), max_length=10)

class MahbCustAuditForm(forms.Form):
        cust_name = ChoiceFieldNoValidation(label=(u'Customer Name'))

class MAHBCustConfigForm(forms.Form):
        vdx_host = ChoiceFieldNoValidation(label=(u'VDX Host'))
        vlanid = forms.CharField(label=(u'VLan ID'), max_length=10)
        vlan_name = forms.CharField(label=(u'VLan Name'), max_length=10)
        icx_host = ChoiceFieldNoValidation(label=(u'ICX Host'))
        email = ChoiceFieldNoValidation(label=(u'Email ID'))

class MAHBCustConfirmForm(forms.Form):
        vdx_host = forms.CharField(label=(u'VDX Host'))
        vlanid = forms.CharField(label=(u'VLan ID'), max_length=10)
        vlan_name = forms.CharField(label=(u'VLan Name'), max_length=10)
        icx_host = forms.CharField(label=(u'ICX Host'))
        icx_avail_ports = ChoiceFieldNoValidation(label=(u'ICX Avail Ports'))
        email = forms.CharField(label=(u'Email ID'))

class ICXTelmetricForm(forms.Form):
        hosts = forms.ChoiceField(choices=ICX_HOST, required=True, label=(u'Hosts'))
        username = forms.CharField(label=(u'Username'), max_length=10)
        password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False), max_length=10)
        email = forms.ChoiceField(choices=EMAIL_LIST, required=True, label=(u'Email'))

class MahbCustFom(DocumentForm):
        cust_name = ChoiceFieldNoValidation(label=(u'Customer Name'))
 
class MAHBCustEditForm(forms.Form):
        vdx_host = forms.CharField(label=(u'VDX Host'))
        vlanid = forms.CharField(label=(u'VLan ID'), max_length=10)
        vlan_name = forms.CharField(label=(u'VLan Name'), max_length=10)
        icx_host = forms.CharField(label=(u'ICX Host'))
        icx_untagged_port = forms.CharField(label=(u'ICX Tagged Port'))
        icx_avail_ports = ChoiceFieldNoValidation(label=(u'ICX Avail Ports'))
        email = forms.CharField(label=(u'Email ID'))