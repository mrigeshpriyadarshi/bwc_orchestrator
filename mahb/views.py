# -*- coding: utf-8 -*-
import json, os, time, sys

import json
from bson import ObjectId

# from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages

from libs import bwc, mongoc
from models import Customers_vlan, Customers_config, Icx_servers, Vdx_servers, Emails, Login_creds

from .forms import LoginForm, MahbCustAuditForm, MAHBCustConfigForm, MAHBCustForm, \
    MAHBCustConfirmForm, MAHBCustEditForm

def get_ports(host):
            username, password = mongoc.get_device_creds(Icx_servers, host)
            parameters = {
                "host": host,
                "username": username,
                "password": password,
                }
            return bwc.get_icx_ports(parameters)


def index(request):
            return HttpResponse("Hello, world. You're at the polls index.")
            # Create your views here.

# class HomePageView(TemplateView):
#             template_name = 'html/home.html'

#             def get_context_data(self, request, **kwargs):
#                 if request.session.get('member_id'):
#                     context = super(HomePageView, self).get_context_data(request, **kwargs)
#                     # messages.info(self.request, 'hello http://example.com')
#                     return context
#                 else:
#                     return HttpResponseRedirect('/mahb')

class MahbCustForm(FormView):
    template_name = 'html/mahb_cust_form.html'
    form_class = MAHBCustForm

class MahbCusExecForm(FormView):
    template_name = 'html/mahb_cust_exec_form.html'
    form_class = MAHBCustConfirmForm

class ThanksView(TemplateView):
    template_name = 'html/thanks.html'

class LoginPageView(FormView):
    template_name = 'html/login_form.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        # messages.info(self.request, 'hello http://example.com')
        return context

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def LoginRequest(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        # print "mm", form.is_valid(), form.is_bound, form.errors
        # print form.cleaned_data['email'], form.cleaned_data['password']
        if form.is_valid():
            auth = mongoc.find(Login_creds, email=form.cleaned_data['email'])
            if auth.password == request.POST['password']:
                request.session['id'] = JSONEncoder().encode(auth.id)
                return render(request, 'html/home.html')
            else:
                return HttpResponse("Your username and password didn't match.")
        else:
            return HttpResponseRedirect('/mahb')
    elif request.method == 'GET':
        if request.session.keys():
            print request.session["id"], "jjj"
            return render(request, 'html/home.html')
        else:
            return HttpResponseRedirect('/mahb')
    else:
        return HttpResponseRedirect('/mahb')


def LogOutRequest(request):
    try:
        del request.session['id']
    except KeyError:
        pass
    return HttpResponseRedirect('/mahb')


def MAHBCustAudit(request):
            form_class = MahbCustAuditForm(auto_id=False)
            form_class.fields['cust_name'].choices = mongoc.get_model_tuple(Customers_vlan, "cust_name")
            return render(request, 'html/select_cust_form.html', {'form': form_class})

def MAHBCustEditReq(request):
    if request.method == 'POST':
        form = MahbCustAuditForm(request.POST)
        if form.is_valid():
            cust_name = form.cleaned_data['cust_name'].encode('utf-8')
            cust = mongoc.find(Customers_config, vlan_name=cust_name)
            initial = {
                'vdx_host': cust.vdx_host,
                'icx_host': cust.icx_host,
                'vlanid': cust.vlanid,
                'vlan_name': cust_name,
                'email': cust.email,
                'icx_tagged_port': cust.icx_tagged_port
            }
            form_class = MAHBCustEditForm(initial=initial, auto_id=False)
            for x in ['vdx_host', 'icx_host', 'vlanid', 'vlan_name', 'email', 'icx_tagged_port']:
                form_class.fields[x].widget.attrs['readonly'] = True
            form_class.fields['icx_avail_ports'].choices  = mongoc.get_tuple(get_ports(cust.icx_host))
            # return render_to_response('html/cust_edit_form.html', {'form': form_class}, context_instance=RequestContext(request))
            return render(request, 'html/cust_edit_form.html', {'form': form_class})
    else:
        return render(request, 'html/home.html')


def MAHBCustAddReq(request):
    if request.method == 'POST':
        form = MAHBCustForm(request.POST)
        if form.is_valid():
            initial = {
                'vlanid': mongoc.get_max_id(Customers_vlan) + 1,
                'vlan_name': form.cleaned_data['cust_name'].encode('utf-8')
            }
            cust_name = form.cleaned_data['cust_name'].encode('utf-8')
            form_class = MAHBCustConfigForm(initial=initial, auto_id=False)
            for x in ['vlanid', 'vlan_name']:
                form_class.fields[x].widget.attrs['readonly'] = True
            form_class.fields['vdx_host'].choices = mongoc.get_model_tuple(Vdx_servers, "_id")
            form_class.fields['icx_host'].choices = mongoc.get_model_tuple(Icx_servers, "_id")
            form_class.fields['email'].choices = mongoc.get_model_tuple(Emails, "_id")
            # return render_to_response('html/mahb_cust_config_form.html', {'form': form_class}, context_instance=RequestContext(request))
            return render(request, 'html/mahb_cust_config_form.html', {'form': form_class})
    else:
        return render(request, 'html/home.html')

def MAHBCustExecReq(request):
    if request.method == 'POST':
        form = MAHBCustConfigForm(request.POST)
        if form.is_valid():
            icx_host = form.cleaned_data['icx_host'].encode('utf-8')
            initial = {
                'vdx_host': form.cleaned_data['vdx_host'].encode('utf-8'),
                'icx_host': icx_host,
                'vlanid': form.cleaned_data['vlanid'].encode('utf-8'),
                'vlan_name': form.cleaned_data['vlan_name'].encode('utf-8'),
                'email': form.cleaned_data['email'].encode('utf-8')
            }
            form_class = MAHBCustConfirmForm(initial=initial, auto_id=False)
            for x in ['vdx_host', 'icx_host', 'vlanid', 'vlan_name', 'email']:
                form_class.fields[x].widget.attrs['readonly'] = True     
            form_class.fields['icx_avail_ports'].choices  = mongoc.get_tuple(get_ports(icx_host))
            # return render_to_response('html/mahb_cust_exec_form.html', {'form': form_class}, context_instance=RequestContext(request))
            return render(request, 'html/mahb_cust_exec_form.html', {'form': form_class})
    else:
        return render(request, 'html/home.html')

def MAHBRequest(request):
    if request.method == 'POST':
        form = MAHBCustConfirmForm(request.POST)
        if form.is_valid():
            vdx_host = form.cleaned_data['vdx_host'].encode('utf-8')
            icx_host = form.cleaned_data['icx_host'].encode('utf-8')
            vdx_username, vdx_password = mongoc.get_device_creds(Vdx_servers, vdx_host)
            icx_username, icx_password = mongoc.get_device_creds(Icx_servers, icx_host)
            vlanid = form.cleaned_data['vlanid'].encode('utf-8')
            vlan_name = form.cleaned_data['vlan_name'].encode('utf-8')
            parameters = {
                "vdx_host": vdx_host,
                "vdx_username": vdx_username,
                "vdx_password": vdx_password,
                "vlanid": vlanid,
                "vlan_name": vlan_name,
                "icx_host": icx_host,
                "icx_username": icx_username,
                "icx_password": icx_password,
                "icx_tagged_port": form.cleaned_data['icx_avail_ports'].encode('utf-8'),
                "email": form.cleaned_data['email'].encode('utf-8'),
                }
            exec_id, status, output = bwc.execute_mahb_workflow(parameters)
            mongoc.insert(Customers_vlan, mongoc.populate_params(vlanid, {"cust_name": vlan_name}))
            mongoc.insert(Customers_config, mongoc.populate_params(vlanid, parameters))
            return render(request, 'html/thanks.html', {'exec_id': exec_id, 'status': status, 'output':  json.dumps(output)})
            # return render(request, 'html/thanks.html', {'exec_id': "exec_id", 'status': "status", 'output': json.dumps({'hi': 'mrigesh'})})
    else:
        return render(request, 'html/home.html')
        
