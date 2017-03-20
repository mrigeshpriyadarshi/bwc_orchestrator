# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPBasicAuth
import json, os, time, sys
import mongoc
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from mahb.models import Bwc_info


def common_headers():
	common_headers = {'Connection': 'keep-alive',  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Content-Type': 'Application/json'}
	return common_headers

def get_token(host, username, password):
	response = requests.post("https://%s/auth/v1/tokens" % host, headers=common_headers(), auth= HTTPBasicAuth(username, password), verify=False)
	return json.loads(response.content.encode('utf-8'))['token']

def request_header(host, username, password, st2_api):
	# api="ZWI1YmMyNGM0NWMyMDBkNDA3ZjVmOTJmNTM5ZjQxNGUyMmIyYTcxZjU0MjAxNDgzYzdmNWE1NWMzYjI2ZmM2NA"
	# request_headers = {'Connection': 'keep-alive',  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Content-Type': 'Application/json', 'St2-Api-Key': api}
	# return request_headers
	request_headers = common_headers()
	if st2_api == None:
		request_headers.update({'X-Auth-Token': get_token(host, username, password)})
	else:
		request_headers.update({'St2-Api-Key': st2_api})
	return request_headers


def data_payload(action, user, parameters):
	payload = {"action": action, "user": user, "parameters": parameters}
	data_payload = json.dumps(payload)
	return data_payload

def init_param():
	try:
		obj = mongoc.find(Bwc_info)
		host = obj['host']
		username = obj['username']
		password = obj['password']
		st2_api = obj['st2_api']
	except Exception as e:
		print e
		raise e
	else:
		return host, username, password, st2_api


def api_url(host, uid = None):
	if uid == None:
		api_url="https://%s/api/v1/executions" % host
	else:
		api_url="https://%s/api/v1/executions/%s" % (host, uid)
	return api_url

def get(uid, request_headers=None):
	host, user, password, st2_api = init_param()
	if request_headers == None:
		request_headers = request_header(host, user, password, st2_api)	
	response = requests.get(api_url(host, uid), headers=request_headers, verify=False)
	return json.loads(response.content.encode('utf-8'))

def get_result(uid, request_headers=None):
	return get(uid, request_headers)["result"]

def get_status(uid, request_headers=None):
	status = json.dumps(get(uid, request_headers)["status"], indent=4)
	sys.stdout.write("Process %s..."  % status)
	return status

def post_call(action_name, parameters, request_headers=None):
	host, user, password, st2_api = init_param()
	if request_headers == None:
		request_headers = request_header(host, user, password, st2_api)
	response = requests.post(api_url(host), headers=request_headers, data=data_payload(action_name, user, parameters), verify=False)
	return  json.dumps(json.loads(response.content), indent=4)

def wait(response, request_headers):
	exec_id = json.loads(response)['id']
	print exec_id
	status = "running"
	while status == "running":
		print "sleeping for 15 secs.."
		time.sleep(15)
		status = get_status(exec_id, request_headers).strip("\"")
	return exec_id, status

def post(action_name, parameters):
	host, user, password, st2_api = init_param()
	request_headers = request_header(host, user, password, st2_api)
	response = post_call(action_name, parameters, request_headers)
	exec_id, status = wait(response, request_headers)
	return exec_id, status, request_headers

def get_icx_ports(parameters):
	exec_id, status, request_headers = post("demo.get_icx_open_ports", parameters)
	if status == "succeeded":
		return get_result(exec_id, request_headers)["tasks"][1]["result"]["result"]
	else:
		print "Connectivity to ICX is broken:", sys.exc_info()[0]
		raise RuntimeError

def execute_mahb_workflow(parameters):
	exec_id, status, request_headers= post("demo.mahb_channel_allotment", parameters)
	return exec_id, status, get_result(exec_id, request_headers)

# def api_call(action, parameters):
#         payload = {"action": action, "user": "st2admin", "parameters": parameters}
#         print json.dumps(payload)
#         api_url="https://10.88.88.140/api/v1/executions"
#         api="ZWI1YmMyNGM0NWMyMDBkNDA3ZjVmOTJmNTM5ZjQxNGUyMmIyYTcxZjU0MjAxNDgzYzdmNWE1NWMzYjI2ZmM2NA"
#         request_headers = {'Connection': 'keep-alive',  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Content-Type': 'Application/json', 'St2-Api-Key': api}
#         response = requests.post(api_url, headers=request_headers, data=json.dumps(payload), verify=False)
#         return  json.dumps(json.loads(response.content), indent=4)
        # return  json.dumps(payload, indent=4)
