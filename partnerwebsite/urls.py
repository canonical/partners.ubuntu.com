import json
from collections import namedtuple

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import (
    HttpResponseNotFound, HttpResponseServerError
)
from django.template import RequestContext, loader, Context
from preserialize.serialize import serialize

from fenchurch import TemplateFinder
from cms.models import (
    Partner, Technology, IndustrySector, Programme, ServiceOffered, Region
)
from cms.views import partner_programmes, partner_view

admin.autodiscover()


class PartnerView(TemplateFinder):
    """
    This view injects Partners into every template. You know, for prototyping.
    """
    def render_to_response(self, context, **response_kwargs):

        partners_json = json.dumps(
            serialize(
                Partner.objects.filter(published=True),
                fields=[':all'],
                exclude=['created_on', 'updated_on']
            ),
            default=lambda obj: None
        )
        Filter = namedtuple('Filter', ['name', 'items'])
        context['filters'] = [
            Filter("Technology",        Technology.objects.all()),
            Filter("Industry Sector", IndustrySector.objects.all()),
            Filter("Programme",       Programme.objects.all()),
            Filter("Service Offered", ServiceOffered.objects.all()),
            Filter("Region",          Region.objects.all()),
        ]
        context['partners'] = Partner.objects.filter(published=True)
        context['partners_json'] = partners_json
        return super(PartnerView, self).render_to_response(
            context,
            **response_kwargs
        )


def custom_404(request):
    t = loader.get_template('templates/404.html')
    context = RequestContext(request, {'request_path': request.path})
    return HttpResponseNotFound(t.render(context))


def custom_500(request):
    t = loader.get_template('templates/500.html')
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
    url(r'^(?P<partner>[-\w]+)$', partner_view),
    #url(r'^(?P<partner>.*)$', PartnerView.as_view())
    #url(r'^(?P<template>.*)$', PartnerView.as_view()),
)

# Error handlers
handler404 = custom_404
handler500 = custom_500
