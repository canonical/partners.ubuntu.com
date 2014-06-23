from django.shortcuts import render_to_response
from django.conf import settings

from cms.models import Partner


def partner_programmes(request, name):
    partners = Partner.objects.filter(programme__name=name)
    context = {'programme_partners': partners}
    path_list = [p for p in request.path.split('/') if p]
    for i, path, in enumerate(path_list):
        level = "level_%s" % str(i+1)
        context[level] = path
    context['STATIC_URL'] = settings.STATIC_URL
    return render_to_response(
        'partner-programmes/%s.html' % name,
        context
    )
