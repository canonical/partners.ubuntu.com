# Modules
from django.db import migrations

# Local
from cms.models import Partner
try:
    from urlparse import urlparse, urlunparse
except ImportError:
    from urllib.parse import urlparse


def update_logo_urls(apps, schema_editor):
    partners = Partner.objects.all()

    for partner in partners:
        (scheme, netloc, path, params, query, fragment) = urlparse(
            partner.logo
        )

        if scheme == 'http' and netloc == 'assets.ubuntu.com':
            new_url = urlunparse(
                ('https', netloc, path, params, query, fragment)
            )

            partner.logo = new_url
            partner.save()


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0004_auto_20160331_1555'),
    ]

    operations = [
        migrations.RunPython(update_logo_urls)
    ]
