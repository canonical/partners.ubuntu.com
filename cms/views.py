import json
from collections import namedtuple

from preserialize.serialize import serialize
from fenchurch import TemplateFinder
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import FieldError 

from cms.models import (
    Partner, Technology, IndustrySector, Programme, ServiceOffered, Region
)

def add_default_values_to_context(context, request):
    """
    Untill Fenchurch is updated to export this functionality, had to paste it in here.
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

        context['partners'] = Partner.objects.filter(
            published=True,
        ).exclude(logo="").order_by('?')[:8]
        return super(PartnerView, self).render_to_response(
            context,
            **response_kwargs
        )


def partner_programmes(request, name):
    """
    /partner-programmes/<name>

    Renders the template, 'partner-programmes/<name>.html' with the partners defined in:
    https://basecamp.com/2179997/projects/4523250/messages/27494952#comment_171423781
    """
    base_partners = Partner.objects.filter(published=True).exclude(logo="")
    lookup_partners = {
        "public-cloud": base_partners.filter(
            programme__name="Certified Public Cloud",
            featured=True),

        "phone-carrier": base_partners.filter(
            Q(service_offered__name='Mobile network operator') |
            Q(service_offered__name='Hardware manufacturer'),
            technology__name="Phone"),

        "reseller": base_partners.filter(
            programme__name="Reseller"),

        "retail": base_partners.filter(
            programme__name="Retailer"),

        "hardware": base_partners.filter(
            (
                Q(programme__name="Technical Partner Programme") |
                Q(programme__name="OpenStack Interoperability Lab")
            ) & (
                Q(service_offered__name="Mobile network operator") |
                Q(service_offered__name="Hardware manufacturer") |
                Q(service_offered__name="Component manufacturer") |
                Q(service_offered__name="Silicon vendor"))
        ),

        "software": base_partners.filter(
            (
                Q(programme__name="Technical Partner Programme") |
                Q(programme__name="OpenStack interoperability Lab")
            ) & (
                Q(service_offered__name="Software publisher") |
                Q(service_offered__name="Bespoke software developer") |
                Q(service_offered__name="Cloud software provider") |
                Q(service_offered__name="Software reseller")
            )
        ),

        "openstack": base_partners.filter(
            programme__name="Openstack Interoperability Lab"),
    }
    partners = lookup_partners[name][:8].distinct()
    context = {'programme_partners': partners}

    if name == "phone-carrier":
        context['cag_partners'] = base_partners.filter(
            (
                Q(technology__name="phone") or Q(technology__name="tablet")
            ) & (
                Q(programme__name="Carrier Advisory Group")
            ),
            featured=True
        )

    context = add_default_values_to_context(context, request)
    return render_to_response(
        'partner-programmes/%s.html' % name,
        context
    )


def partner_view(request, slug):
    """
    /<slug>
    Gets the partner specified in <slug> and renders partner.html with that partner
    """
    partner = get_object_or_404(
        Partner,
        slug=slug,
        published=True,
        generate_page=True
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
    context = {'partners': Partner.objects.filter(published=True).order_by('name')}
    context = add_default_values_to_context(context, request)
    Filter = namedtuple('Filter', ['name', 'items'])
    context['filters'] = [
        Filter("Technology",      Technology.objects.all()),
        Filter("Industry Sector", IndustrySector.objects.all()),
        Filter("Programme",       Programme.objects.all()),
        Filter("Service Offered", ServiceOffered.objects.all()),
        Filter("Region",          Region.objects.all()),
    ]

    return render_to_response(
        'find-a-partner/index.html',
        context
    )


def partners_json_view(request):
    """
    Returns a JSON list of partners, depending on query strings.
    """
    partners = Partner.objects.filter(published=True).order_by('?')
    try:
        for attribute, value in request.GET.iteritems():
            if value.find(','):
                query_list = Q()
                for listed_value in value.split(','):
                    query_list = query_list | Q(**{attribute:listed_value})
                partners = partners.filter(query_list)
            else:
                partners = partners.filter(**{attribute:value})
        partners_json = json.dumps(
        serialize(
            partners,
            fields=[':all'],
            exclude=['created_on', 'updated_on', 'generate_page', 'id', 'created_by', 'updated_by']
        ),
        default=lambda obj: None
    )
    except FieldError as e:
        partners_json = json.dumps({"Error": e.message})

    return HttpResponse(partners_json, content_type="application.json")
