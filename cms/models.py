from django.db import models


class PartnerModel(models.Model):
    "Partner metadata"

    name = models.CharField(max_length=200)
    notes = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_ip = models.IPAddressField(null=True)
    created_by = models.CharField(max_length=200)
    updated_on = models.DateTimeField(auto_now=True)
    updated_ip = models.IPAddressField(null=True)
    updated_by = models.CharField(max_length=200)

    class Meta:
        abstract = True


class CategoryModel(PartnerModel):
    class Meta:
        abstract = True


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
    category = models.ManyToManyField(Category, related_name='partners')
