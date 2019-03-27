# System
import json
from collections import namedtuple

# Modules
from preserialize.serialize import serialize
from django_template_finder_view import TemplateFinder
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponse

# Local
from cms.models import Partner, Technology, Programme, ServiceOffered


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


def add_default_values_to_context(context, request):
    """
    Until Fenchurch is updated to export this functionality,
    had to paste it in here.
    """

    path_list = [p for p in request.path.split("/") if p]
    for i, path in enumerate(path_list):
        level = "level_%s" % str(i + 1)
        context[level] = path.lower()
    context["STATIC_URL"] = settings.STATIC_URL
    context["ASSET_SERVER_URL"] = settings.ASSET_SERVER_URL
    return context


class PartnerView(TemplateFinder):
    """
    This view injects Partners into every template. You know, for prototyping.
    """

    def render_to_response(self, context, **response_kwargs):

        published_partners = (
            get_grouped_random_partners()
            .filter(published=True)
            .exclude(logo="")
        )

        context["partners"] = published_partners[:8]

        context["alliance_partners"] = published_partners.filter(
            dedicated_partner_page=True
        )[:8]

        # Add contact query
        context["aliId"] = self.request.GET.get("aliId", "")

        # Add level_* context variables
        clean_path = self.request.path.strip("/")
        for index, path in enumerate(clean_path.split("/")):
            context["level_" + str(index + 1)] = path

        return super(PartnerView, self).render_to_response(
            context, **response_kwargs
        )


def partner_programmes(request, name):
    """
    /programmes/<name>

    Renders the template, 'programmes/<name>.html'
    with the partners defined in:
    basecamp.com/2179997/projects/4523250/messages/27494952#comment_171423781
    """

    max_num_of_partners = 8
    base_partners = (
        get_grouped_random_partners().filter(published=True).exclude(logo="")
    )
    lookup_partners = {
        "public-cloud": base_partners.filter(
            programme__name="Certified Public Cloud", featured=True
        ),
        "phone": base_partners.filter(
            (Q(technology__name="Personal computing/devices"))
            & (Q(programme__name="Carrier Advisory Group")),
            featured=True,
        ),
        "channel": base_partners.filter(programme__name="channel"),
        "retail": base_partners.filter(programme__name="Retailer"),
        "hardware": base_partners.filter(
            (
                Q(programme__name="Technical Partner Programme")
                | Q(programme__name="OpenStack")
            )
            & (
                Q(service_offered__name="Network operator")
                | Q(service_offered__name="Hardware manufacturer")
            )
        ),
        "software": base_partners.filter(
            (
                Q(programme__name="Technical Partner Programme")
                | Q(programme__name="OpenStack")
            )
            & (Q(service_offered__name="Software/content publisher"))
        ),
        "openstack": base_partners.filter(programme__name="OpenStack"),
        "iot": base_partners.filter(programme__name="Internet of Things"),
        "charm": base_partners.filter(
            programme__name="Charm partner programme"
        ),
    }
    distinct_partners = list(lookup_partners[name])
    partners = distinct_partners[:max_num_of_partners]
    context = {"programme_partners": partners}

    context = add_default_values_to_context(context, request)
    return render_to_response("programmes/%s.html" % name, context)


def partner_view(request, slug):
    """
    /<slug>
    Gets the partner specified in <slug>
    and renders partner.html with that partner
    """

    partner = get_object_or_404(
        Partner, slug=slug.lower(), published=True, dedicated_partner_page=True
    )

    context = {"partner": partner}
    context = add_default_values_to_context(context, request)

    return render_to_response("partner.html", context)


def find_a_partner(request):
    """
    /find-a-partner/
    List all partners to the page, for frontend searching.
    """

    context = {
        "partners": get_grouped_random_partners()
        .filter(published=True)
        .order_by(Lower("name"))
    }
    context = add_default_values_to_context(context, request)
    Filter = namedtuple("Filter", ["name", "items"])
    context["filters"] = [
        Filter("Technology", Technology.objects.all()),
        Filter("Programme", Programme.objects.all()),
        Filter("Service Offered", ServiceOffered.objects.all()),
    ]

    return render_to_response("find-a-partner/index.html", context)


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

        distinct_partners = list(
            partners.filter(query_list).order_by("-always_featured", "?")
        )
        partners_json = json.dumps(
            serialize(
                distinct_partners,
                fields=[":all"],
                exclude=[
                    "created_on",
                    "updated_on",
                    "dedicated_partner_page",
                    "id",
                    "created_by",
                    "updated_by",
                ],
            ),
            default=lambda obj: None,
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
