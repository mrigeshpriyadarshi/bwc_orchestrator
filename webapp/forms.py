# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory


from bootstrap3.tests import TestForm

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
    ('10.88.88.146', '10.88.88.146'),
    ('host3', '--- Select Hostname ---')
)

ICX_HOST = (
    ('192.168.10.65', '192.168.10.65'),
    ('host3', '--- Select Hostname ---')
)

EMAIL_LIST = (
    ('mpriyada@brocade.com', 'mpriyada@brocade.com'),
    ('pfong@brocade.com', 'pfong@brocade.com'),
    ('mail3', '--- Select Email ID ---')
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

class LoginForm(forms.Form):
        email = forms.CharField(label=(u'Email'), max_length=18)
        password = forms.CharField(label=(u'Pass'), widget=forms.PasswordInput(render_value=False), max_length=20)

class MAHBForm(forms.Form):
        vdx_host = forms.ChoiceField(choices=VDX_HOST, required=True, label=(u'vdx_host'))
        vdx_username = forms.CharField(label=(u'vdx_username'), max_length=10)
        vdx_password = forms.CharField(label=(u'vdx_password'), widget=forms.PasswordInput(render_value=False), max_length=10)
        vlanid = forms.CharField(label=(u'vlanid'), max_length=10)
        vlan_name = forms.CharField(label=(u'vlan_name'), max_length=10)
        icx_host = forms.ChoiceField(choices=ICX_HOST, required=True, label=(u'icx_host'))
        icx_username = forms.CharField(label=(u'icx_username'), max_length=10)
        icx_password = forms.CharField(label=(u'icx_password'), widget=forms.PasswordInput(render_value=False), max_length=10)
        email = forms.ChoiceField(choices=EMAIL_LIST, required=True, label=(u'Email'))
