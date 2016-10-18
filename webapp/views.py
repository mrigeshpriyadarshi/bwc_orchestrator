# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
import json
# from __future__ import unicode_literals

# from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms

from django.core.files.storage import default_storage
from django.template import RequestContext

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages

from .forms import ContactForm, FilesForm, ContactFormSet, LoginForm, MAHBForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.

class HomePageView(TemplateView):
    template_name = 'apps/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # messages.info(self.request, 'hello http://example.com')
        return context

class IcxPageView(FormView):
    template_name = 'apps/icx.html'
    form_class = ContactForm
    field_class = FilesForm

    # def get_context_data(self, **kwargs):
    #     context = super(IcxPageView, self).get_context_data(**kwargs)
    #     # messages.info(self.request, 'hello http://example.com')
    #     return context

class MahbPageView(FormView):
    template_name = 'apps/mahb1.html'
    form_class = MAHBForm

class ThanksView(TemplateView):
    template_name = 'apps/thanks.html'

    # def get_context_data(self, **kwargs):
    #     context = super(ThanksView, self).get_context_data(**kwargs)
    #     # messages.info(self.request, 'hello http://example.com')
    #     return context

class LoginPageView(TemplateView):
    template_name = 'apps/index.html'

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        # messages.info(self.request, 'hello http://example.com')
        return context

def LoginRequest(request):
    if request.user.is_authenticated():
        # return render_to_response('/webapp', {'form': form}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/webapp/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/webapp/home')
                # return render_to_response('/webapp/home', {'form': form}, context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect('/webapp/home')
                # return render_to_response('/webapp/home', {'form': form}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/webapp/home')
            # return render_to_response('/webapp/home', {'form': form}, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        return HttpResponseRedirect('/webapp/home')
        # return render_to_response('/webapp/home', {'form': form}, context_instance=RequestContext(request))

def MAHBRequest(request):
    print "mrigesh"
    if request.method == 'POST':
        form = MAHBForm(request.POST)
        if form.is_valid():
            pass
        vdx_host = form.cleaned_data['vdx_host']
        vdx_username = form.cleaned_data['vdx_username']
        vdx_password = form.cleaned_data['vdx_password']
        vlanid = form.cleaned_data['vlanid']
        vlan_name = form.cleaned_data['vlan_name']
        icx_host = form.cleaned_data['icx_host']
        icx_username = form.cleaned_data['icx_username']
        icx_password = form.cleaned_data['icx_password']
        email = form.cleaned_data['email']
        parameters = {
            "vdx_host": vdx_host,
            "vdx_username": vdx_username,
            "vdx_password": vdx_password,
            "vlanid": vlanid,
            "vlan_name": vlan_name,
            "icx_host": icx_host,
            "icx_username": icx_username,
            "icx_password": icx_password,
            "email": email,
            }
        payload = {"action": "demo.mahb_config", "user": "st2admin", "parameters": parameters}
        print json.dumps(payload)
        # response = requests.get(url, headers=request_headers, verify=False)
        url="https://10.88.88.140/api/v1/executions"
        api="ZWI1YmMyNGM0NWMyMDBkNDA3ZjVmOTJmNTM5ZjQxNGUyMmIyYTcxZjU0MjAxNDgzYzdmNWE1NWMzYjI2ZmM2NA"
        request_headers = {'Connection': 'keep-alive',  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Content-Type': 'Application/json', 'St2-Api-Key': api}
        response = requests.post(url, headers=request_headers, data=json.dumps(payload), verify=False)
        # print response.content
        print  json.dumps(json.loads(response.content), indent=4)
        return HttpResponseRedirect('/webapp/thanks')
    else:
        return HttpResponseRedirect('/webapp/home')
            