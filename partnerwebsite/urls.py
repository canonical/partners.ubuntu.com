from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from fenchurch import TemplateFinder

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<template>.*)$', TemplateFinder.as_view()),
)
