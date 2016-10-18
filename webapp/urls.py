# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

# from . import views
# from .views import HomePageView, FormHorizontalView, FormInlineView, PaginationView, FormWithFilesView, \
#     DefaultFormView, MiscView, DefaultFormsetView, DefaultFormByFieldView

from .views import HomePageView, LoginPageView, LoginRequest, IcxPageView, MahbPageView, MAHBRequest, ThanksView

urlpatterns = [
    url(r'^$', LoginPageView.as_view(), name='index'),
    url(r'^home$', HomePageView.as_view(), name='webhome'),
    url(r'^icx$', IcxPageView.as_view(), name='icxhome'),
    url(r'^mahb$', MahbPageView.as_view(), name='mahb'),
    url(r'^login$', LoginRequest, name='login'),
    url(r'^mreq$', MAHBRequest, name='mreq'),
    url(r'^thanks$', ThanksView.as_view(), name='thanks')
]