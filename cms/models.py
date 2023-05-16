# Standard library
import sys

# Packages
from django.db import models
from django.core import serializers
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.core.validators import MaxLengthValidator


if sys.version_info[0] == 3:
    unicode = str


class PartnerModel(models.Model):
    "Partner metadata"
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(
        unique=True, help_text="Auto-generated, for use in URLs"
    )
    ordering = "name"

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(PartnerModel, self).save(*args, **kwargs)


class CategoryModel(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return self.name


class PartnerType(CategoryModel):
    class Meta:
        verbose_name_plural = "partner type"


class Technology(CategoryModel):
    class Meta:
        verbose_name_plural = "technology"


class Programme(CategoryModel):
    class Meta:
        verbose_name_plural = "programme"

    pass


class ServiceOffered(CategoryModel):
    class Meta:
        verbose_name_plural = "service offered"


class Partner(PartnerModel):

    published = models.BooleanField(
        help_text=(
            "Partners without this checked will never be seen by the public"
        )
    )
    logo = models.URLField(
        help_text=(
            "The URL to the logo (e.g. http://example.com/logo.svg).\n"
            "Please only upload .png and .svg files, "
            "no less than 200 pixels wide.\n"
        )
    )
    partner_website = models.URLField(
        help_text=(
            "The URL to the partner's site "
            "where the info about partnering with Canonical is."
        )
    )
    fallback_website = models.URLField(
        help_text=(
            "If our partner changes their site without us realising it, "
            "and the 'external page' errors, this will be` used instead."
        )
    )
    short_description = models.TextField(
        help_text=(
            "Used in search results, max 375 characters."
            "(<a href='http://daringfireball.net/projects/markdown/basics'>"
            "Markdown formatted"
            "</a>)"
        ),
        validators=[MaxLengthValidator(375)],
    )
    long_description = models.TextField(
        blank=True,
        null=True,
        help_text=(
            "Only displayed on the dedicated partner page "
            "(when 'generate page' is selected). "
            "(<a href='http://daringfireball.net/projects/markdown/basics'>"
            "Markdown formatted"
            "</a>)"
        ),
    )
    featured = models.BooleanField(help_text="Promote to the front page")
    always_featured = models.BooleanField(
        help_text="Always promote to the top of lists.", default=False
    )
    dedicated_partner_page = models.BooleanField(
        help_text="Does this partner have it's own dedicated page?"
    )
    technology = models.ManyToManyField(
        Technology, related_name="partners", blank=True
    )
    programme = models.ManyToManyField(
        Programme, related_name="partners", blank=True
    )
    service_offered = models.ManyToManyField(
        ServiceOffered, related_name="partners", blank=True
    )
    partner_type = models.ManyToManyField(
        PartnerType,
        related_name="partners",
        blank=True,
        help_text=("test"),
    )
    notes = models.TextField(
        blank=True, help_text="Private, for internal Canonical use"
    )

    def quotes(self):
        return serializers.serialize("python", self.quote_set.all())

    def links(self):
        return serializers.serialize("python", self.link_set.all())

    def insights_tags(self):
        return serializers.serialize("python", self.insightstag_set.all())

    tags_label = models.CharField(
        max_length=200,
        blank=True,
        help_text="The displayed name for the tags list",
    )

    def tags(self):
        return serializers.serialize("python", self.tag_set.all())

    def texts(self):
        return serializers.serialize("python", self.text_set.all())


class Quote(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    attribution = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.text)

    def __str__(self):
        return self.text


class Link(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    url = models.URLField()
    text = models.TextField()

    def __unicode__(self):
        return unicode(self.text)

    def __str__(self):
        return self.text


class InsightsTag(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    tag = models.CharField(
        max_length=200,
        help_text=(
            "Link to a tag on insights.ubuntu.com "
            "and pulls in the RSS feed to the partner page."
        ),
    )

    def __unicode__(self):
        return unicode(self.tag)

    def __str__(self):
        return self.tag


class Tag(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    tag = models.CharField(max_length=200, help_text=(""))

    def __unicode__(self):
        return unicode(self.tag)

    def __str__(self):
        return self.tag


class Text(models.Model):
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    header = models.TextField()
    body = models.TextField()
    html_class = models.CharField(
        max_length=200,
        blank=True,
        help_text="The class added to the generated HTML for this section",
    )
    image_url = models.URLField(
        help_text="A URL for an image to appear alongside the text",
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        help_text="A Youtube video URL.", blank=True, null=True
    )
    read_more_link = models.URLField(blank=True, null=True)
    read_more_link_text = models.CharField(
        max_length=200,
        blank=True,
        help_text=(
            "The content of the field's link. Leave blank for 'read more'"
        ),
    )
    read_more_cta = models.BooleanField(
        help_text=("Should the 'read more' link be a CTA button?"),
        default=False,
    )
    read_more_external = models.BooleanField(
        help_text=(
            "Does the 'read more' link to an external site (other canonical"
            " sites or subdomains count as external)?"
        ),
        default=False,
    )
    insights_tag = models.CharField(
        max_length=200,
        blank=True,
        help_text=(
            "Articles matching this insigts tag will be included in the"
            " block. Leave blank for no insights feed."
        ),
    )

    def __unicode__(self):
        return unicode(self.header)

    def __str__(self):
        return self.header


def make_user_admin(sender, instance, **kwargs):
    """
    Update all created users to become admin users
    by setting is_staff and is_superuser
    """

    if type(instance).__name__ == "User":
        user = instance

        user.is_staff = True
        user.is_superuser = True


pre_save.connect(make_user_admin)
