# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

# from . import views
# from .views import HomePageView, FormHorizontalView, FormInlineView, PaginationView, FormWithFilesView, \
#     DefaultFormView, MiscView, DefaultFormsetView, DefaultFormByFieldView

from .views import HomePageView, LoginPageView, LoginRequest, IcxPageView, ICXTelemetricsRequest, MAHBCustAudit, \
    MAHBRequest, ThanksView, Test_form, MahbCustForm, MAHBCustAddReq, MAHBCustExecReq

urlpatterns = [
    url(r'^$', LoginPageView.as_view(), name='index'),
    url(r'^login$', LoginRequest, name='login'),
    url(r'^home$', HomePageView.as_view(), name='webhome'),
    url(r'^mahb$', MAHBCustAudit, name='mahb'),
    url(r'^mahbcustomer$', MahbCustForm.as_view(), name='mahbcustomer'),
    url(r'^addmahbcustomer$', MAHBCustAddReq, name='addmahbcustomer'),
    url(r'^confirmmahbcustomer$', MAHBCustExecReq, name='confirmmahbcustomer'),
    url(r'^mreq$', MAHBRequest, name='mreq'),
    url(r'^icx$', IcxPageView.as_view(), name='icxhome'),
    url(r'^icxreq$', ICXTelemetricsRequest, name='icxreq'),
    url(r'^thanks$', ThanksView.as_view(), name='thanks'),
    url(r'^test$', Test_form.as_view(), name='test')
]