from django.db import models
from django.core import serializers


class PartnerModel(models.Model):
    "Partner metadata"
    name = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(
        max_length=200,
        blank=True,
        default="TEST_USER"
    )
    updated_on = models.DateTimeField(
        auto_now=True,
        blank=True
    )
    updated_by = models.CharField(
        max_length=200,
        blank=True,
        default="TEST_USER"
    )

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
    published = models.BooleanField()
    logo = models.URLField(blank=True, null=True)
    external_page = models.CharField(max_length=200, blank=True, null=True)
    external_fallback = models.CharField(max_length=200, blank=True, null=True)
    short_description = models.CharField(max_length=200)
    long_description = models.TextField(blank=True, null=True)
    featured = models.BooleanField()
    generate_page = models.BooleanField()
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
    notes = models.TextField(blank=True)

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
    tag = models.CharField(max_length=200)


class Text(models.Model):
    partner = models.ForeignKey(Partner)
    image = models.URLField()
    header = models.TextField()
    body = models.TextField()
    url = models.URLField()
