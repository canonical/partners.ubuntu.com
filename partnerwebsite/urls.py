from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import (
    HttpResponseNotFound, HttpResponseServerError
)
from django.template import RequestContext, loader, Context
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from django_yaml_redirects import load_redirects

from cms.views import (
    partner_programmes, partner_view, PartnerView,
    find_a_partner, partners_json_view, customers_json_view
)

admin.autodiscover()


def handler404(request):
    t = loader.get_template('404.html')
    context = RequestContext(request, {'request_path': request.path})
    return HttpResponseNotFound(t.render(context))


def handler500(request):
    t = loader.get_template('500.html')
    return HttpResponseServerError(t.render(Context({})))

urlpatterns = load_redirects()

urlpatterns += patterns(
    '',
    url(r'^openid/', include('django_openid_auth.urls')),
    url(
        r'^admin/help/$',
        TemplateView.as_view(template_name='admin/help.html'),
        name='admin_help'
    ),
    url(
        r'^admin/?$',
        RedirectView.as_view(url='/admincms/partner/', permanent=True)
    ),
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^partners.json$', partners_json_view),
    url(r'^customers.json$', customers_json_view),
    url(r'^programmes/?$', PartnerView.as_view()),
    url(
        r'^programmes/phone-carrier$',
        RedirectView.as_view(url='/programmes/phone', permanent=True)
    ),
    url(
        r'^partner-programmes/?$',
        RedirectView.as_view(url='/programmes/', permanent=True)
    ),
    url(
        r'^partner-programmes/(?P<name>[-\w]+)',
        lambda request, name: RedirectView.as_view(
            url='/programmes/' + name, permanent=True
        )(request)
    ),
    url(r'^programmes/(?P<name>[-\w]+)', partner_programmes),
    url(r'^$', PartnerView.as_view()),
    url(r'^contact-us$', PartnerView.as_view()),
    url(r'^thank-you$', PartnerView.as_view()),
    url(r'^find-a-partner$', find_a_partner),
    url(r'^partnering-with-us$', PartnerView.as_view()),
    url(r'^(?P<slug>[-\w]+)$', partner_view),
)
