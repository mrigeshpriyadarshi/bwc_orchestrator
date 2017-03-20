# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
import json, os, time, sys

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# from __future__ import unicode_literals

# from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.files.storage import default_storage
from django.template import RequestContext

from django import forms
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.utils.safestring import SafeString

from pymongo import MongoClient
from bson import json_util

from django.shortcuts import render
from models import Customers_vlan, Customers_config

from .forms import ContactForm, FilesForm, ContactFormSet, LoginForm, MahbCustAuditForm, ICXTelmetricForm, MAHBCustConfigForm, MAHBCustForm, \
    MAHBCustConfirmForm, MAHBCustEditForm


def mongodb_client():
        client = MongoClient("mongodb://127.0.0.1:27017")
        return client.webapp

def mongodb_insert(collection, data):
        try:
            result = mongodb_client()[collection].insert(data)
        except Exception as e:
            result = mongodb_client()[collection].update({"_id": data['_id']}, data)
        finally:
            return result

def get_mongo_id_list(collection):
        id_list = []
        cursor = mongodb_client()[collection].find( )
        for document in cursor:
            # id_list.append(document["_id"].encode('utf-8'))
            id_list.append(document["_id"])
            id_list.sort()
        return id_list

def populate_mongo_params(id, params):
    parameters = {
    "_id": int(id),
    }
    # new_dict = {i:d[i] for d in [params,parameters] for i in d}
    parameters.update(params)
    return parameters

def get_max_customers_vlan():
        vlan_list = get_mongo_id_list("customers_vlan")
        return int(vlan_list[-1])

def get_emails_tuple():
        email_list = get_mongo_id_list("emails")
        return tuple(tuple([x,x]) for x in email_list)

def get_vdx_server_tuple():
        vdx_list = get_mongo_id_list("vdx_servers")
        return tuple(tuple([x,x]) for x in vdx_list)

def get_icx_server_tuple():
        icx_list = get_mongo_id_list("icx_servers")
        return tuple(tuple([x,x]) for x in icx_list)

def get_cust_name_tuple():
        icx_list = get_mongo_id_list("customers_vlan")
        return tuple(tuple([x,x]) for x in icx_list)

def get_server_creds(collection, host):
            cursor = mongodb_client()[collection].find({"_id": host})           
            return cursor[0]["username"].encode('utf-8'), cursor[0]["password"].encode('utf-8')

def bwc_request_header():
        api="ZWI1YmMyNGM0NWMyMDBkNDA3ZjVmOTJmNTM5ZjQxNGUyMmIyYTcxZjU0MjAxNDgzYzdmNWE1NWMzYjI2ZmM2NA"
        request_headers = {'Connection': 'keep-alive',  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Content-Type': 'Application/json', 'St2-Api-Key': api}
        return request_headers

def bwc_data_payload(action, parameters):
        payload = {"action": action, "user": "st2admin", "parameters": parameters}
        bwc_data_payload = json.dumps(payload)
        # print bwc_data_payload
        return bwc_data_payload

def bwc_api_url(uid = None):
    if uid == None:
        api_url="https://10.88.88.140/api/v1/executions"
    else:
        api_url="https://10.88.88.140/api/v1/executions/%s" % uid
    return api_url

def bwc_api_get(uid):
            response = requests.get(bwc_api_url(uid), headers=bwc_request_header(), verify=False)
            return json.loads(response.content.encode('utf-8'))

def bwc_api_get_result(uid):
            result = json.dumps(bwc_api_get(uid)["result"], indent=4)
            # print result
            return result

def bwc_api_get_status(uid):
            status = json.dumps(bwc_api_get(uid)["status"], indent=4)
            sys.stdout.write("Process %s..."  % status)
            return status

def bwc_api_post(action_name, parameters):
        response = requests.post(bwc_api_url(), headers=bwc_request_header(), data=bwc_data_payload(action_name, parameters), verify=False)
        return  json.dumps(json.loads(response.content), indent=4)

def bwc_wait(response):
            exec_id = json.loads(response)['id']
            print exec_id
            while bwc_api_get_status(exec_id).strip("\"") == "running":
                        print "sleeping for 15 secs.."
                        time.sleep(15)
            return exec_id, bwc_api_get_status(exec_id).strip("\"")

def bwc_api(action, parameters):
        payload = {"action": action, "user": "st2admin", "parameters": parameters}
        print json.dumps(payload)
        api_url="https://10.88.88.140/api/v1/executions"
        api="ZWI1YmMyNGM0NWMyMDBkNDA3ZjVmOTJmNTM5ZjQxNGUyMmIyYTcxZjU0MjAxNDgzYzdmNWE1NWMzYjI2ZmM2NA"
        request_headers = {'Connection': 'keep-alive',  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Content-Type': 'Application/json', 'St2-Api-Key': api}
        response = requests.post(api_url, headers=request_headers, data=json.dumps(payload), verify=False)
        return  json.dumps(json.loads(response.content), indent=4)
        # return  json.dumps(payload, indent=4)

def get_icx_ports(host):
            username, password = get_server_creds("icx_servers", host)
            parameters = {
                "host": host,
                "username": username,
                "password": password,
                }
            response = bwc_api_post("demo.get_icx_open_ports", parameters)
            exec_id, status = bwc_wait(response)
            if status == "succeeded":
                return bwc_api_get(exec_id)["result"]["tasks"][1]["result"]["result"]
            else:
                print "Connectivity to ICX is broken:", sys.exc_info()[0]
                raise RuntimeError


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
    template_name = 'apps/icx_tel_form.html'
    form_class = ICXTelmetricForm

class MahbCustForm(FormView):
    template_name = 'apps/mahb_cust_form.html'
    form_class = MAHBCustForm

class Test_form(FormView):
    template_name = 'apps/mahb_cust_config_form.html'
    form_class = MAHBCustForm

class MahbCusExecForm(FormView):
    template_name = 'apps/mahb_cust_exec_form.html'
    form_class = MAHBCustConfirmForm

class ThanksView(TemplateView):
    template_name = 'apps/thanks.html'

class LoginPageView(FormView):
    template_name = 'apps/login.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        # messages.info(self.request, 'hello http://example.com')
        return context

def LoginRequest(request):
    # print request.user.is_authenticated()
    if request.user.is_authenticated():
        # return render_to_response('/webapp', {'form': form}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/webapp/home')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print "mm", form.is_valid()
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            print "mrigesh", user
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

def MAHBCustAudit(request):
    # if request.method == 'GET':
            cust_id_list = []
            for cust in Customers_vlan.objects:
                cust_id_list.append(cust.cust_name.encode('utf-8'))
            for cust in Customers_config.objects(_id=13):
                print cust.vdx_host.encode('utf-8') 
            form_class = MahbCustAuditForm(auto_id=False)
            # form_class.fields['cust_name'].choices = tuple(tuple([x,x]) for x in [cust.cust_name.encode('utf-8')])
            form_class.fields['cust_name'].choices = tuple(tuple([x,x]) for x in cust_id_list)
            return render_to_response('apps/mahb_select_cust_edit_form.html', {'form': form_class}, context_instance=RequestContext(request))
    # else:
    #     return HttpResponseRedirect('/webapp/home')

def MAHBCustEditReq(request):
    if request.method == 'POST':
        form = MahbCustAuditForm(request.POST)
        if form.is_valid():
            cust_name = form.cleaned_data['cust_name'].encode('utf-8')
            icx_host = None
            for cust in Customers_config.objects(vlan_name=cust_name):
                icx_host = cust.icx_host
                initial = {
                    'vdx_host': cust.vdx_host,
                    'icx_host': icx_host,
                    'vlanid': cust.vlanid,
                    'vlan_name': cust_name,
                    'email': cust.email,
                    'icx_untagged_port': cust.icx_untagged_port
                }
            form_class = MAHBCustEditForm(initial=initial, auto_id=False)
            form_class.fields['vdx_host'].widget.attrs['readonly'] = True
            form_class.fields['icx_host'].widget.attrs['readonly'] = True
            form_class.fields['vlanid'].widget.attrs['readonly'] = True
            form_class.fields['vlan_name'].widget.attrs['readonly'] = True
            form_class.fields['email'].widget.attrs['readonly'] = True
            form_class.fields['icx_untagged_port'].widget.attrs['readonly'] = True
            form_class.fields['icx_avail_ports'].choices  = tuple(tuple([x,x]) for x in get_icx_ports(icx_host))
                # print form_class
            return render_to_response('apps/mahb_cust_edit_form.html', {'form': form_class}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/webapp/home')


def MAHBCustAddReq(request):
    if request.method == 'POST':
        form = MAHBCustForm(request.POST)
        if form.is_valid():
            new_vlan = get_max_customers_vlan() + 1
            cust_name = form.cleaned_data['cust_name'].encode('utf-8')
            form_class = MAHBCustConfigForm(initial={'vlanid': new_vlan, 'vlan_name': cust_name }, auto_id=False)
            form_class.fields['vlanid'].widget.attrs['readonly'] = True
            form_class.fields['vlan_name'].widget.attrs['readonly'] = True
            form_class.fields['vdx_host'].choices = get_vdx_server_tuple()
            form_class.fields['icx_host'].choices = get_icx_server_tuple()
            form_class.fields['email'].choices = get_emails_tuple()
            # print form_class
            return render_to_response('apps/mahb_cust_config_form.html', {'form': form_class}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/webapp/home')

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
            form_class.fields['vdx_host'].widget.attrs['readonly'] = True
            form_class.fields['icx_host'].widget.attrs['readonly'] = True
            form_class.fields['vlanid'].widget.attrs['readonly'] = True
            form_class.fields['vlan_name'].widget.attrs['readonly'] = True
            form_class.fields['email'].widget.attrs['readonly'] = True
            form_class.fields['icx_avail_ports'].choices  = tuple(tuple([x,x]) for x in get_icx_ports(icx_host))
            # print form_class
            return render_to_response('apps/mahb_cust_exec_form.html', {'form': form_class}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/webapp/home')

def MAHBRequest(request):
    if request.method == 'POST':
        form = MAHBCustConfirmForm(request.POST)
        # print form, form.is_valid()
        if form.is_valid():
            vdx_host = form.cleaned_data['vdx_host'].encode('utf-8')
            icx_host = form.cleaned_data['icx_host'].encode('utf-8')
            vdx_username, vdx_password = get_server_creds("vdx_servers", vdx_host)
            icx_username, icx_password = get_server_creds("icx_servers", icx_host)
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
                "icx_untagged_port": form.cleaned_data['icx_avail_ports'].encode('utf-8'),
                "email": form.cleaned_data['email'].encode('utf-8'),
                }
            print parameters
            response = bwc_api_post("demo.mahb_channel_allotment", parameters)
            exec_id, status = bwc_wait(response)
            mongo_parameters = {
                "_id": vlanid,
                "cust_name": vlan_name
                }
            cust_vlanid_mongo_params = populate_mongo_params(vlanid, {"cust_name": vlan_name})
            cust_config_mongo_params = populate_mongo_params(vlanid, parameters)
            mongodb_insert("customers_vlan", cust_vlanid_mongo_params)
            mongodb_insert("customers_config", cust_config_mongo_params)
            # response = mongodb_insert("customers_vlan", mongo_parameters)
            print cust_vlanid_mongo_params, cust_config_mongo_params
            return render_to_response('apps/thanks.html', {'exec_id': exec_id, 'status': status, 'output': bwc_api_get_result(exec_id)})
            return render_to_response('apps/thanks.html', {'exec_id': "exec_id", 'status': "status", 'output': ""})
            # return HttpResponseRedirect('/webapp/thanks')
    else:
        return HttpResponseRedirect('/webapp/home')
        
def ICXTelemetricsRequest(request):
    if request.method == 'POST':
        form = ICXTelmetricForm(request.POST)
        if form.is_valid():
            parameters = {
                "host": form.cleaned_data['hosts'],
                "username": form.cleaned_data['username'],
                "password": form.cleaned_data['password'],
                "email": form.cleaned_data['email'],
                }
            response = bwc_api_post("default.icx_telemetrics", parameters)
            exec_id, status = bwc_wait(response)
            return render_to_response('html/thanks.html', {'exec_id': exec_id, 'status': status, 'output': bwc_api_get_result(exec_id)})
            # return HttpResponseRedirect('/webapp/thanks')
    else:
        return HttpResponseRedirect('/webapp/home')

def ICXports(request):
    if request.method == 'GET':
        form = ICXTelmetricForm(request.GET)
        if form.is_valid():
            parameters = {
                "host": form.cleaned_data['hosts'],
                "username": form.cleaned_data['username'],
                "password": form.cleaned_data['password'],
                "email": form.cleaned_data['email'],
                }
            response = bwc_api_post("default.icx_telemetrics", parameters)
            exec_id, status = bwc_wait(response)
            return render_to_response('apps/thanks.html', {'exec_id': exec_id, 'status': status, 'output': bwc_api_get_result(exec_id)})
            # return render_to_response('apps/thanks.html', {'exec_id': "abc"})
            # return HttpResponseRedirect('/webapp/thanks')
    else:
        return HttpResponseRedirect('/webapp/home')  