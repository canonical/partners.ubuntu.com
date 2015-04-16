import json
from collections import namedtuple

from preserialize.serialize import serialize
from fenchurch import TemplateFinder
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse

from cms.models import (
    Partner, Technology, Programme, ServiceOffered
)


def get_grouped_random_partners():
    """
    Group the partners by `always_featured` first, and then randomise
    within those two groups.
    """
    return Partner.objects.order_by('-always_featured', '?')


def add_default_values_to_context(context, request):
    """
    Until Fenchurch is updated to export this functionality,
    had to paste it in here.
    """

    path_list = [p for p in request.path.split('/') if p]
    for i, path, in enumerate(path_list):
        level = "level_%s" % str(i+1)
        context[level] = path
    context['STATIC_URL'] = settings.STATIC_URL
    return context


class PartnerView(TemplateFinder):
    """
    This view injects Partners into every template. You know, for prototyping.
    """

    def render_to_response(self, context, **response_kwargs):

        published_partners = get_grouped_random_partners().filter(
            published=True,
        ).exclude(logo="")

        context['partners'] = published_partners[:8]

        context['alliance_partners'] = published_partners.filter(
            dedicated_partner_page=True,
        )[:8]

        return super(PartnerView, self).render_to_response(
            context,
            **response_kwargs
        )


def partner_programmes(request, name):
    """
    /programmes/<name>

    Renders the template, 'programmes/<name>.html'
    with the partners defined in:
    https://basecamp.com/2179997/projects/4523250/messages/27494952#comment_171423781
    """

    max_num_of_partners = 8
    base_partners = get_grouped_random_partners().filter(published=True).exclude(logo="")
    lookup_partners = {
        "public-cloud": base_partners.filter(
            programme__name="Certified Public Cloud",
            featured=True
        ),

        "phone": base_partners.filter(
            (
                Q(technology__name="Personal computing/devices")
            ) & (
                Q(programme__name="Carrier Advisory Group")
            ),
            featured=True
        ),

        "reseller": base_partners.filter(
            programme__name="Reseller"
        ),

        "retail": base_partners.filter(
            programme__name="Retailer"
        ),

        "hardware": base_partners.filter(
            (
                Q(programme__name="Technical Partner Programme") |
                Q(programme__name="OpenStack")
            ) & (
                Q(service_offered__name="Network operator") |
                Q(service_offered__name="Hardware manufacturer"))
        ),

        "software": base_partners.filter(
            (
                Q(programme__name="Technical Partner Programme") |
                Q(programme__name="OpenStack")
            ) & (
                Q(service_offered__name="Software/content publisher")
            )
        ),

        "openstack": base_partners.filter(
            programme__name="OpenStack"
        ),

        "iot": base_partners.filter(
            programme__name="IoT"
        ),

        "charm": base_partners.filter(
            programme__name="Charm"
        ),
    }
    distinct_partners = list(set(lookup_partners[name]))
    partners = distinct_partners[:max_num_of_partners]
    context = {'programme_partners': partners}

    context = add_default_values_to_context(context, request)
    return render_to_response(
        'programmes/%s.html' % name,
        context
    )


def partner_view(request, slug):
    """
    /<slug>
    Gets the partner specified in <slug>
    and renders partner.html with that partner
    """

    partner = get_object_or_404(
        Partner,
        slug=slug,
        published=True,
        dedicated_partner_page=True
    )

    context = {'partner': partner}
    context = add_default_values_to_context(context, request)

    return render_to_response(
        'partner.html',
        context
    )


def find_a_partner(request):
    """
    /find-a-partner/
    List all partners to the page, for frontend searching.
    """

    context = {
        'partners': get_grouped_random_partners().filter(published=True).order_by('name')
    }
    context = add_default_values_to_context(context, request)
    Filter = namedtuple('Filter', ['name', 'items'])
    context['filters'] = [
        Filter("Technology",      Technology.objects.all()),
        Filter("Programme",       Programme.objects.all()),
        Filter("Service Offered", ServiceOffered.objects.all()),
    ]

    return render_to_response(
        'find-a-partner/index.html',
        context
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
        callback = request.GET.get('callback')
        # if callback parameter is present,
        # this is going to be a jsonp callback.
        if callback:
            try:
                response = self.f(*args, **kwargs)
            except:
                response = HttpResponse('error', status=500)
            if response.status_code / 100 != 2:
                response.content = 'error'
            if response.content[0] not in ['"', '[', '{'] \
                    or response.content[-1] not in ['"', ']', '}']:
                response.content = '"%s"' % response.content
            response.content = "%s(%s)" % (callback, response.content)
            response['Content-Type'] = 'application/javascript'
        else:
            response = self.f(*args, **kwargs)
        return response


def filter_partners(request, partners):
    """
    Returns a JSON list of partners, depending on request.GET query strings.
    """

    filter_whitelist = [
        'featured',
        'dedicated_partner_page',
        'name',
        'programme__name',
        'service_offered__name',
        'slug',
        'technology__name',
    ]

    try:
        query_list = Q()
        for query, value in request.GET.iterlists():
            if query in filter_whitelist:
                if len(value) > 1:
                    for listed_value in value:
                        query_list = query_list | Q(**{query: listed_value})
                else:
                    partners = partners.filter(Q(**{query: value[0]}))
        partners = list(partners.filter(query_list).distinct())
        partners_json = json.dumps(
            serialize(
                partners,
                fields=[':all'],
                exclude=[
                    'created_on', 'updated_on', 'dedicated_partner_page',
                    'id', 'created_by', 'updated_by'
                ]
            ),
            default=lambda obj: None
        )
    except Exception as e:
        raise e

    return partners_json


@AllowJSONPCallback
def partners_json_view(request):
    return HttpResponse(
        filter_partners(
            request,
            get_grouped_random_partners().filter(
                published=True
            ).exclude(
                partner_type__name="Customer"
            )
        ),
        content_type="application.json"
    )


@AllowJSONPCallback
def customers_json_view(request):
    return HttpResponse(
        filter_partners(
            request,
            get_grouped_random_partners().filter(
                published=True,
                partner_type__name="Customer"
            )
        ),
        content_type="application.json"
    )
