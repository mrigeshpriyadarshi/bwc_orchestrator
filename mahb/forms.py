# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory

from collections import OrderedDict as SortedDict
from bootstrap3.tests import TestForm
from mongodbforms import *

ICX_PORTS = (
    ('ports', '--- Select available ports ---'),
    ('22', '22'),
)


class ChoiceFieldNoValidation(forms.ChoiceField):
    def validate(self, value):
        pass

class LoginForm(forms.Form):
        email = forms.EmailField(label=(u''), max_length=64, strip=True, widget=forms.EmailInput(attrs={'autofocus': 'autofocus', 'required': 'required'}))
        password = forms.CharField(label=(u''), widget=forms.PasswordInput(render_value=False, attrs={'required': 'required'}), max_length=20)

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

class MahbCustFom(DocumentForm):
        cust_name = ChoiceFieldNoValidation(label=(u'Customer Name'))
 
class MAHBCustEditForm(forms.Form):
        vdx_host = forms.CharField(label=(u'VDX Host'))
        vlanid = forms.CharField(label=(u'VLan ID'), max_length=10)
        vlan_name = forms.CharField(label=(u'VLan Name'), max_length=10)
        icx_host = forms.CharField(label=(u'ICX Host'))
        icx_tagged_port = forms.CharField(label=(u'ICX Tagged Port'))
        icx_avail_ports = ChoiceFieldNoValidation(label=(u'ICX Avail Ports'))
        email = forms.CharField(label=(u'Email ID'))