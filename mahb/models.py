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
        icx_tagged_port = StringField(max_length = 64)
        vlan_name = StringField(max_length = 64)
        vlanid = StringField(max_length = 64)
        vdx_host = StringField(max_length = 64)
        vdx_username = StringField(max_length = 64)
        vdx_password = StringField(max_length = 64)
        email = StringField(max_length = 64)

class Icx_servers(Document):  
        _id = StringField(max_length = 64)
        username = StringField(max_length = 64)
        password = StringField(max_length = 64)

class Vdx_servers(Document):  
        _id = StringField(max_length = 64)
        username = StringField(max_length = 64)
        password = StringField(max_length = 64)

class Emails(Document):  
        _id = EmailField(max_length = 64)

class Bwc_info(Document):
        host = StringField(max_length = 64)
        username = StringField(max_length = 64)
        password = StringField(max_length = 64)
        st2_api = StringField()

class Login_creds(Document):  
        email = EmailField(max_length = 64)
        password = StringField(max_length = 64)