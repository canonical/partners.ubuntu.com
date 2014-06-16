import json

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import (
    HttpResponseNotFound, HttpResponseServerError
)
from django.template import RequestContext, loader, Context
from django.core import serializers
from preserialize.serialize import serialize

from fenchurch import TemplateFinder
from cms.models import Partner

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
    url(r'^(?P<template>.*)$', PartnerView.as_view()),
)

# Error handlers
handler404 = custom_404
handler500 = custom_500
