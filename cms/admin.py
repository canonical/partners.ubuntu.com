from django.contrib import admin
from cms.models import (
    Partner, Category, IndustrySector, Programme, ServiceOffered, Region,
    Quote, Link, InsightsTag, Text
)


class PartnerAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'quote',
        'link',
        'insights_tag',
        'text'
    )
    list_display = (
        'name',
        'short_description',
        'featured',
        'generate_page',
    )
    list_filter = (
        'name',
        'featured',
        'generate_page',
    )
    search_fields = ['name']
    readonly_fields = (
        'created_by',
        'updated_by'
    )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'logo',
                'external_page',
                'external_fallback',
                'short_description',
                'long_description',
                'featured',
                'generate_page'
            )
        }),
        ('Categories', {
            'fields': (
                'category',
                'industry_sector',
                'programme',
                'service_offered',
                'region'
            )
        }),
        ("Metadata", {
            'fields': ('quote', 'link', 'insights_tag', 'text')
        }),
        ("Other", {
            'fields': ('notes', 'created_by', 'updated_by')
        }),
    )


class CategoryAdmin(admin.ModelAdmin):
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


class QuoteAdmin(MetadataAdmin):
    pass


class LinkAdmin(MetadataAdmin):
    pass


class InsightsTagAdmin(MetadataAdmin):
    pass


class TextAdmin(MetadataAdmin):
    pass


admin.site.register(Partner, PartnerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(IndustrySector, IndustrySectorAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(ServiceOffered, ServiceOfferedAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(InsightsTag, InsightsTagAdmin)
admin.site.register(Text, TextAdmin)
