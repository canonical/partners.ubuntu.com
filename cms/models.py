from django.db import models


class PartnerModel(models.Model):
    "Partner metadata"

    name = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.CharField(max_length=200, blank=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return str(self.name)


class Quote(PartnerModel):
    text = models.TextField(blank=True)
    attribution = models.CharField(max_length=200)


class Link(PartnerModel):
    url = models.URLField()
    text = models.TextField()


class InsightsTag(PartnerModel):
    tag = models.TextField()


class Text(PartnerModel):
    image = models.URLField()
    header = models.TextField()
    body = models.TextField()
    url = models.URLField()


class CategoryModel(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __unicode__(self):
        return str(self.name)


class Category(CategoryModel):
    pass


class IndustrySector(CategoryModel):
    pass


class Programme(CategoryModel):
    pass


class ServiceOffered(CategoryModel):
    pass


class Region(CategoryModel):
    pass


class Partner(PartnerModel):
    logo = models.URLField()
    external_page = models.CharField(max_length=200)
    external_fallback = models.CharField(max_length=200)
    short_description = models.CharField(max_length=200)
    long_description = models.TextField()
    featured = models.BooleanField()
    category = models.ManyToManyField(
        Category,
        related_name='partners'
    )
    industry_sector = models.ManyToManyField(
        IndustrySector,
        related_name='partners'
    )
    programme = models.ManyToManyField(
        Programme,
        related_name='partners'
    )
    service_offered = models.ManyToManyField(
        ServiceOffered,
        related_name='partners'
    )
    region = models.ManyToManyField(
        Region,
        related_name='partners'
    )
    quote = models.ManyToManyField(
        Quote,
        related_name='partners'
    )
    link = models.ManyToManyField(
        Link,
        related_name='partners'
    )
    insights_tag = models.ManyToManyField(
        InsightsTag,
        related_name='partners'
    )
    text = models.ManyToManyField(
        Text,
        related_name='partners'
    )
