# System
import json

# Modules
from django.db.models import Q
from django.http import HttpResponse

# Local
from cms.settings import TALISKER_REVISION_ID
from cms.models import Partner
from cms.serializers import serialize


def get_grouped_random_partners():
    """
    Group the partners by `always_featured` first, and then randomise
    within those two groups.
    "no customers if they have no [programme, service_offered, technology]"
    """

    return (
        Partner.objects.exclude(
            partner_type__name="Customer",
            programme__isnull=True,
            service_offered__isnull=True,
            technology__isnull=True,
        )
        .exclude(published=False)
        .order_by("-always_featured", "?")
    )


class AllowJSONPCallback(object):
    """
    This decorator function wraps a normal view function
    so that it can be read through a jsonp callback.
    Source: https://djangosnippets.org/snippets/2208/

    Usage:

    @AllowJSONPCallback
    def my_view_function(request):
        return HttpResponse('this should be viewable through jsonp')

    It looks for a GET parameter called "callback", and if one exists,
    wraps the payload in a javascript function named per the value of callback.

    If the input does not appear to be json, wrap the input in quotes
    so as not to throw a javascript error upon receipt of the response.
    """

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        request = args[0]
        callback = request.GET.get("callback")
        # if callback parameter is present,
        # this is going to be a jsonp callback.
        if callback:
            try:
                response = self.f(*args, **kwargs)
            except Exception:
                response = HttpResponse("error", status=500)
            if response.status_code / 100 != 2:
                response.content = "error"
            if response.content[0] not in ['"', "[", "{"] or response.content[
                -1
            ] not in ['"', "]", "}"]:
                response.content = '"%s"' % response.content
            response.content = "%s(%s)" % (callback, response.content)
            response["Content-Type"] = "application/javascript"
        else:
            response = self.f(*args, **kwargs)
        return response


def filter_partners(request, partners):
    """
    Returns a JSON list of partners, depending on request.GET query strings.
    """

    filter_whitelist = [
        "featured",
        "dedicated_partner_page",
        "name",
        "programme__name",
        "service_offered__name",
        "slug",
        "technology__name",
    ]

    try:
        query_list = Q()
        for query, value in dict(request.GET).items():
            if query in filter_whitelist:
                if len(value) > 1:
                    for listed_value in value:
                        if listed_value.lower() == "true":
                            listed_value = True
                        elif listed_value.lower() == "false":
                            listed_value = False
                        query_list = query_list | Q(**{query: listed_value})
                else:
                    listed_value = value[0]
                    if listed_value.lower() == "true":
                        listed_value = True
                    elif listed_value.lower() == "false":
                        listed_value = False
                    partners = partners.filter(Q(**{query: listed_value}))

        partners_json = json.dumps(
            serialize(
                partners.filter(query_list).order_by("-always_featured", "?")
            )
        )

    except Exception as e:
        raise e

    return partners_json


@AllowJSONPCallback
def partners_json_view(request):
    return HttpResponse(
        filter_partners(request, get_grouped_random_partners()),
        content_type="application.json",
    )


@AllowJSONPCallback
def customers_json_view(request):
    return HttpResponse(
        filter_partners(
            request,
            Partner.objects.order_by("-always_featured", "?").filter(
                published=True, partner_type__name="Customer"
            ),
        ),
        content_type="application.json",
    )


@AllowJSONPCallback
def status_view(request):
    return HttpResponse(TALISKER_REVISION_ID)
