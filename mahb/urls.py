# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.views.generic.base import RedirectView
# from . import views
# from .views import HomePageView, FormHorizontalView, FormInlineView, PaginationView, FormWithFilesView, \
#     DefaultFormView, MiscView, DefaultFormsetView, DefaultFormByFieldView

from .views import LoginPageView, LoginRequest, LogOutRequest, MAHBCustAudit, \
    MAHBRequest, ThanksView, MahbCustForm, MAHBCustAddReq, MAHBCustExecReq, MAHBCustEditReq

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='login', permanent=False), name='index'),
    url(r'^login$', LoginPageView.as_view(), name='login'),
    url(r'^home$', LoginRequest, name='loginrequest'),
    # url(r'^home$', HomePageView.as_view(), name='home'),
    url(r'^selectcustomer$', MAHBCustAudit, name='selectcustomer'),
    url(r'^editcustomer$', MAHBCustEditReq, name='editcustomer'),
    url(r'^addcustomer$', MahbCustForm.as_view(), name='addcustomer'),
    url(r'^addmahbcustomer$', MAHBCustAddReq, name='addmahbcustomer'),
    url(r'^confirmmahbcustomer$', MAHBCustExecReq, name='confirmmahbcustomer'),
    url(r'^executerequest$', MAHBRequest, name='executerequest'),
    url(r'^thanks$', ThanksView.as_view(), name='thanks'),
    url(r'^logout$', LogOutRequest, name='logout'),
]