from __future__ import unicode_literals

from django.db import models
from mongoengine import *

# Create your models here.
class Customers_vlan(Document):  
    _id = IntField(max_length = 64)
    cust_name = StringField(max_length = 64)

class Customers_config(Document):  
    _id = IntField(max_length = 64)
    icx_host = StringField(max_length = 64)
    icx_username = StringField(max_length = 64)
    icx_password = StringField(max_length = 64)
    icx_untagged_port = StringField(max_length = 64)
    vlan_name = StringField(max_length = 64)
    vlanid = StringField(max_length = 64)
    vdx_host = StringField(max_length = 64)
    vdx_username = StringField(max_length = 64)
    vdx_password = StringField(max_length = 64)
    email = StringField(max_length = 64)

class icx_servers(Document):  
    _id = StringField(max_length = 64)
    username = StringField(max_length = 64)
    password = StringField(max_length = 64)

class vdx_servers(Document):  
    _id = StringField(max_length = 64)
    username = StringField(max_length = 64)
    password = StringField(max_length = 64)

class emails(Document):  
    _id = EmailField(max_length = 64)
