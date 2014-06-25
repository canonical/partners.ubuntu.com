from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import (
    HttpResponseNotFound, HttpResponseServerError
)
from django.template import RequestContext, loader, Context

from cms.views import partner_programmes, partner_view, PartnerView

admin.autodiscover()


def custom_404(request):
    t = loader.get_template('404.html')
    context = RequestContext(request, {'request_path': request.path})
    return HttpResponseNotFound(t.render(context))


def custom_500(request):
    t = loader.get_template('500.html')
    return HttpResponseServerError(t.render(Context({})))

urlpatterns = patterns(
    '',
    url(r'^admin', include(admin.site.urls)),
    url(r'^partner-programmes/?$', PartnerView.as_view()),
    url(r'^partner-programmes/(?P<name>[-\w]+)', partner_programmes),
    url(r'^$', PartnerView.as_view()),
    url(r'^contact-us$', PartnerView.as_view()),
    url(r'^thank-you$', PartnerView.as_view()),
    url(r'^find-a-partner$', PartnerView.as_view()),
    url(r'^ubuntu-and-canonical$', PartnerView.as_view()),
    url(r'^(?P<slug>[-\w]+)$', partner_view),
    #url(r'^(?P<template>.*)$', PartnerView.as_view()),
)

# Error handlers
handler404 = custom_404
handler500 = custom_500
