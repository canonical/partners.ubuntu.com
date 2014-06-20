from django.shortcuts import get_object_or_404, render_to_response

from cms.models import Programme, Partner


def partner_programmes(request, name):
    partners = Partner.objects.filter(programme__name=name)
    return render_to_response(
        'partner-programmes/%s.html' % name,
        {'programme_partners': partners}
    )
