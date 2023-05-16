from django.urls import include, re_path
from django.contrib import admin
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.template import loader
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from cms.django_helpers import (
    create_redirect_views,
)

from cms.views import (
    partners_json_view,
    customers_json_view,
)

admin.autodiscover()


def handler404(request, exception):
    t = loader.get_template("404.html")
    return HttpResponseNotFound(t.render({"request_path": request.path}))


def handler500(request):
    t = loader.get_template("500.html")
    return HttpResponseServerError(t.render({}))


urlpatterns = create_redirect_views()

urlpatterns += [
    re_path(r"^openid/", include("django_openid_auth.urls")),
    re_path(
        r"^admin/help/$",
        TemplateView.as_view(template_name="admin/help.html"),
        name="admin_help",
    ),
    re_path(
        r"^admin/?$",
        RedirectView.as_view(url="/admincms/partner/", permanent=True),
    ),
    re_path(r"^admin/?", admin.site.urls),
    re_path(r"^partners.json$", partners_json_view),
    re_path(r"^customers.json$", customers_json_view),
]
