import json, os, time, sys
from mahb.models import Login_creds


def insert(collection, data):
	result = collection(**data).save()
	return result

def get_list(collection, field):
	obj_list = []
	for device in collection.objects():
		obj_list.append(device[field])
	return obj_list

def populate_params(id, params):
	parameters = {
		"_id": int(id),
	}
	parameters.update(params)
	return parameters

def get_max_id(collection):
	collection_list = get_list(collection, "_id")
	return int(collection_list[-1])

def get_model_tuple(collection, field):
	return get_tuple(get_list(collection, field))

def find(collection, **filter):
	return collection.objects.get(**filter)

def get_tuple(obj_list):
	return tuple(tuple([x,x]) for x in obj_list)

def get_device_creds(collection, host):
            username = password = None
            for device in collection.objects(_id=host):
                username = device.username.encode('utf-8')
                password = device.password.encode('utf-8')
            return username, password

def authenticate(email, password):
	for obj in Login_creds.objects():
		if obj['email'] == email and obj['password'] == password:
			return True
		else:
			return False
