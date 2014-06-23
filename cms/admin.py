from django.contrib import admin
from cms.models import (
    Partner, Technology, IndustrySector, Programme, ServiceOffered, Region,
    Quote, Link, InsightsTag, Text
)


class TextInline(admin.TabularInline):
    model = Text
    extra = 0


class QuoteInline(admin.TabularInline):
    model = Quote
    extra = 0


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0


class InsightsTagInline(admin.TabularInline):
    model = InsightsTag
    extra = 0


class PartnerAdmin(admin.ModelAdmin):

    def technology(obj):
        return ",".join([str(o) for o in obj.technology.all()])

    def industry_sector(obj):
        return ",".join([str(o) for o in obj.industry_sector.all()])

    def programme(obj):
        return ",".join([str(o) for o in obj.programme.all()])

    def service_offered(obj):
        return ",".join([str(o) for o in obj.service_offered.all()])

    def region(obj):
        return ",".join([str(o) for o in obj.region.all()])

    technology.short_description = 'Technology'
    industry_sector.short_description = 'Industry Sector'
    programme.short_description = 'Programme'
    service_offered.short_description = 'Service Offered'
    region.short_description = 'Region'

    list_display = (
        'name',
        'logo',
        'published',
        'short_description',
        'featured',
        'generate_page',
        technology,
        industry_sector,
        programme,
        service_offered,
        region,
    )
    list_filter = (
        'name',
        'published',
        'featured',
        'generate_page',
        'technology',
        'industry_sector',
        'programme',
        'service_offered',
        'region'
    )
    list_editable = (
        'published',
        'logo'
    )
    search_fields = ['name']
    readonly_fields = (
        'created_by',
        'updated_by'
    )
    fieldsets = (
        ('Required', {
            'fields': (
                'name',
                'short_description',
            )
        }),
        ('Further information', {
            'fields': (
                'published',
                'logo',
                'external_page',
                'external_fallback',
                'long_description',
                'featured',
                'generate_page'
            )
        }),
        ('Categories', {
            'fields': (
                'technology',
                'industry_sector',
                'programme',
                'service_offered',
                'region'
            )
        }),
        ("Other", {
            'fields': ('notes', 'created_by', 'updated_by')
        }),
    )
    inlines = [
        TextInline,
        QuoteInline,
        LinkInline,
        InsightsTagInline
    ]


class TechnologyAdmin(admin.ModelAdmin):
    pass


class IndustrySectorAdmin(admin.ModelAdmin):
    pass


class ProgrammeAdmin(admin.ModelAdmin):
    pass


class ServiceOfferedAdmin(admin.ModelAdmin):
    pass


class RegionAdmin(admin.ModelAdmin):
    pass


class MetadataAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_by',
        'updated_by'
    )


class QuoteAdmin(admin.ModelAdmin):
    pass


class LinkAdmin(admin.ModelAdmin):
    pass


class InsightsTagAdmin(admin.ModelAdmin):
    pass


class TextAdmin(admin.ModelAdmin):
    pass


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(IndustrySector, IndustrySectorAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(ServiceOffered, ServiceOfferedAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(InsightsTag, InsightsTagAdmin)
admin.site.register(Text, TextAdmin)
