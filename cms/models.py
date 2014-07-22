from django.db import models
from django.core import serializers
from django.db.models.signals import pre_save


class PartnerModel(models.Model):
    "Partner metadata"
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, help_text="Auto-generated, for use in URLs")
    ordering = "name"

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.name)


class CategoryModel(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.name)


class Technology(CategoryModel):
    class Meta:
        verbose_name_plural = 'technology'


class IndustrySector(CategoryModel):
    class Meta:
        verbose_name_plural = 'industry sector'
    pass


class Programme(CategoryModel):
    class Meta:
        verbose_name_plural = 'programme'
    pass


class ServiceOffered(CategoryModel):
    class Meta:
        verbose_name_plural = 'service offered'


class Region(CategoryModel):
    class Meta:
        verbose_name_plural = 'region'


class Partner(PartnerModel):
    published = models.BooleanField(help_text="Partners without this checked will never be seen by the public")
    logo = models.URLField(help_text="The URL to the logo. (must start with with http or https)")
    external_page = models.URLField(help_text="The URL to the partner's site where the info about partnering with Canonical is.")
    external_fallback = models.URLField(help_text="If our partner changes their site without us realising it, and the 'external page' errors, this will be used instead.")
    short_description = models.TextField(help_text="Used in search results, max 70 characters")
    long_description = models.TextField(blank=True, null=True, help_text="Only displayed on the dedicated partner page (when 'generate page' is selected)")
    featured = models.BooleanField(help_text="Promote to the front page")
    generate_page = models.BooleanField(help_text="Does this partner have it's own dedicated page?")
    technology = models.ManyToManyField(
        Technology,
        related_name='partners',
        blank=True,
        null=True
    )
    industry_sector = models.ManyToManyField(
        IndustrySector,
        related_name='partners',
        blank=True,
        null=True
    )
    programme = models.ManyToManyField(
        Programme,
        related_name='partners',
        blank=True,
        null=True
    )
    service_offered = models.ManyToManyField(
        ServiceOffered,
        related_name='partners',
        blank=True,
        null=True
    )
    region = models.ManyToManyField(
        Region,
        related_name='partners',
        blank=True,
        null=True
    )
    notes = models.TextField(blank=True, help_text="Private, for internal Canonical use")

    def quotes(self):
        return serializers.serialize('python', self.quote_set.all())

    def links(self):
        return serializers.serialize('python', self.link_set.all())

    def insights_tags(self):
        return serializers.serialize('python', self.insightstag_set.all())

    def texts(self):
        return serializers.serialize('python', self.text_set.all())


class Quote(models.Model):
    partner = models.ForeignKey(Partner)
    text = models.TextField(blank=True)
    attribution = models.CharField(max_length=200)


class Link(models.Model):
    partner = models.ForeignKey(Partner)
    url = models.URLField()
    text = models.TextField()


class InsightsTag(models.Model):
    partner = models.ForeignKey(Partner)
    tag = models.CharField(max_length=200, help_text="Link to a tag on insights.ubuntu.com and pulls in the RSS feed to the partner page.")


class Text(models.Model):
    partner = models.ForeignKey(Partner)
    image = models.URLField()
    header = models.TextField()
    body = models.TextField()
    url = models.URLField(blank=True, null=True)


def make_user_admin(sender, instance, **kwargs):
    """
    Update all created users to become admin users
    by setting is_staff and is_superuser
    """

    if type(instance).__name__ == 'User':
        user = instance

        user.is_staff = True
        user.is_superuser = True


pre_save.connect(make_user_admin)
