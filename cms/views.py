import json
from collections import namedtuple

from preserialize.serialize import serialize
from fenchurch import TemplateFinder
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.db.models import Q

from cms.models import (
    Partner, Technology, IndustrySector, Programme, ServiceOffered, Region
)


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
        context['partners'] = Partner.objects.filter(
            published=True,
        ).exclude(logo="")
        context['partners_json'] = partners_json
        return super(PartnerView, self).render_to_response(
            context,
            **response_kwargs
        )


def partner_programmes(request, name):
    base_partners = Partner.objects.filter(published=True).exclude(logo="")
    lookup_partners = {
        "public-cloud": base_partners.filter(
            programme__name="Certified Public Cloud",
            featured=True),

        "phone-carrier": base_partners.filter(
            Q(service_offered__name='Mobile network operator') or
            Q(service_offered__name='Hardware manufacturer'),
            technology__name="Phone"),

        "reseller": base_partners.filter(
            programme__name="Reseller"),

        "retail": base_partners.filter(
            programme__name="Retailer"),

        "hardware": base_partners.filter(
            (
                Q(programme__name="Technical Partner Programme") or
                Q(programme__name="OpenStack interoperability Lab")
            ) and (
                Q(service_offered__name="Mobile network operator") or
                Q(service_offered__name="hardware manufacturer") or
                Q(service_offered__name="component manufacturer") or
                Q(service_offered__name="silicon vendor"))
        ),

        "software": base_partners.filter(
            (
                Q(programme__name="Technical Partner Programme") or
                Q(programme__name="OpenStack interoperability Lab")
            ) and (
                Q(service_offered__name="Software publisher") or
                Q(service_offered__name="bespoke software developer") or
                Q(service_offered__name="cloud software provider") or
                Q(service_offered__name="software reseller")
            )
        ),

        "openstack": base_partners.filter(
            programme__name="software reseller"),
    }
    partners = lookup_partners[name][:15]
    context = {'programme_partners': partners}

    if name == "phone-carrier":
        context['cag_partners'] = base_partners.filter(
            (
                Q(technology__name="phone") or Q(technology__name="tablet")
            ) and (
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


def add_default_values_to_context(context, request):
    path_list = [p for p in request.path.split('/') if p]
    for i, path, in enumerate(path_list):
        level = "level_%s" % str(i+1)
        context[level] = path
    context['STATIC_URL'] = settings.STATIC_URL
    return context
